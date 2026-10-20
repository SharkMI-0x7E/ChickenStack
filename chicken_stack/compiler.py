"""
ChickenStack 字节码编译器

把栈式源程序翻译成等价的 Python 源码，交给内置的 compile() 生成 code object。
运行时不再逐条 token 分派，栈操作直接编译成 list 的原地操作。

核心观察：解释器执行一条二元运算要做这些事

    op_map[token.type]()      # 字典查找 + 方法调用
    _require_stack(2)         # 长度检查
    b = self.pop()            # 方法调用 + 边界检查
    a = self.pop()            # 再来一次
    self.push(a + b)          # 类型检查 + 容量检查 + append

而编译后只剩两条字节码：

    b = s.pop()
    s[-1] += b

栈顶就是左操作数，弹出右操作数后直接原地更新，省掉一次 pop 和一次 push。

控制流按静态跳转表展开成 Python 的 while / if，不再有跳转索引的查表与边界校验。
"""

import io

from .parser import Parser, TokenType

DEFAULT_MAX_ITERATIONS = 1_000_000

# 二元运算：弹出右操作数，原地更新新的栈顶（即左操作数）
_BINARY_OPS = {
    TokenType.PLUS: "+=",
    TokenType.MINUS: "-=",
    TokenType.MULTIPLY: "*=",
    TokenType.DIVIDE: "//=",
    TokenType.MODULO: "%=",
}

# 每条指令对栈深的影响，用于栈槽分析
_STACK_DELTA = {
    TokenType.INTEGER: 1,
    TokenType.STRING: 0,
    TokenType.REG_GET: 1,
    TokenType.REG_SET: -1,
    TokenType.PLUS: -1,
    TokenType.MINUS: -1,
    TokenType.MULTIPLY: -1,
    TokenType.DIVIDE: -1,
    TokenType.MODULO: -1,
    TokenType.NEG: 0,
    TokenType.DUP: 1,
    TokenType.SWAP: 0,
    TokenType.DROP: -1,
    TokenType.ROT: 0,
    TokenType.OVER: 1,
    TokenType.PICK: 0,
    TokenType.EQ: -1,
    TokenType.GT: -1,
    TokenType.PRINT_NUM: -1,
    TokenType.PRINT_CHAR: -1,
    TokenType.INPUT_NUM: 1,
    TokenType.INPUT_CHAR: 1,
}

# 栈槽变量化的深度上限。超过就退回 list 模式，避免生成上千个局部变量。
SLOT_LIMIT = 64


def analyze_depths(tokens):
    """
    算出每条指令执行时的栈深。

    依赖 ChickenStack 的结构化控制流：没有 goto，所有跳转目标静态已知，
    所以单遍线性扫描就能确定每个位置的栈深。

    返回 (depth_at, max_depth)；无法静态确定时返回 (None, 原因)。
    """
    if not tokens:
        return [0], 0

    kinds = {token.type for token in tokens}
    if TokenType.PICK in kinds:
        return None, "含 ! 指令，索引在运行时才确定"

    depth_at = [0] * len(tokens)
    depth = 0
    max_depth = 0
    frames = []

    for index, token in enumerate(tokens):
        kind = token.type
        depth_at[index] = depth

        if kind == TokenType.LOOP_START:
            frames.append([kind, depth, None])
            continue

        if kind == TokenType.LOOP_END:
            if not frames or frames[-1][0] != TokenType.LOOP_START:
                return None, "循环符号不匹配"
            entry = frames.pop()[1]
            if depth != entry:
                return None, f"循环体净栈变化 {depth - entry:+d}，不是 0"
            continue

        if kind == TokenType.IF_START:
            if depth < 1:
                return None, "条件块前栈为空"
            frames.append([kind, depth, None])
            depth -= 1
            continue

        if kind == TokenType.ELSE:
            if not frames or frames[-1][0] != TokenType.IF_START:
                return None, "| 没有对应的 {"
            frame = frames[-1]
            entry = frame[1] - 1
            frame[2] = depth - entry
            depth = entry
            continue

        if kind == TokenType.IF_END:
            if not frames or frames[-1][0] != TokenType.IF_START:
                return None, "} 没有对应的 {"
            frame = frames.pop()
            entry = frame[1] - 1
            if frame[2] is None:
                if depth != entry:
                    return None, f"无 else 的条件块改变了栈深 {depth - entry:+d}"
            elif depth - entry != frame[2]:
                return None, "then 与 else 分支结束时栈深不一致"
            continue

        delta = _STACK_DELTA.get(kind)
        if delta is None:
            return None, f"未知指令 {kind.name}"
        depth += delta
        if depth < 0:
            return None, f"第 {index} 条指令处栈深为负"
        if depth > max_depth:
            max_depth = depth

    if frames:
        return None, "有未闭合的块"
    if max_depth > SLOT_LIMIT:
        return None, f"最大栈深 {max_depth} 超过上限 {SLOT_LIMIT}"
    return depth_at, max_depth


class _Output:
    """把 Ch 的输出原语转成对缓冲区的写入，避免每条输出都 flush 一次终端。"""

    __slots__ = ("buffer",)

    def __init__(self, buffer):
        self.buffer = buffer

    def num(self, value):
        if isinstance(value, float):
            self.buffer.write(f"{value:.10g} ")
        else:
            self.buffer.write(f"{value} ")

    def char(self, value):
        if isinstance(value, float):
            value = int(value)
        self.buffer.write(chr(value))

    def text(self, value):
        self.buffer.write(value)


def _read_char(io_handler):
    data = io_handler.get_char()
    return ord(data.decode("utf-8")[0])


class CompileError(Exception):
    """源码无法翻译成 Python 时抛出。"""


class Compiler:
    """把 token 序列展开成 Python 源码行。

    value_limit 大于 0 时，每轮循环会检查栈顶绝对值是否超过该上限，
    用于校验可能写错的循环（数值失控比死循环更麻烦：它会让 Python
    卡在大整数乘法上，而不是被迭代计数器拦住）。
    """

    def __init__(self, source, value_limit=0, use_slots=True):
        self.parser = Parser()
        self.tokens = self.parser.parse(source)
        self.loops = self.parser.get_loop_table()
        self.braces = self.parser.get_brace_table()
        self.value_limit = value_limit
        self.use_slots = use_slots
        self.lines = []
        self.depth = 1

    def _add(self, statement):
        self.lines.append("    " * self.depth + statement)

    def _open(self, statement):
        """开始一个缩进块，先放一条 pass 占位，空块也合法。"""
        self._add(statement)
        self.depth += 1
        self._add("pass")

    def _close(self):
        self.depth -= 1

    def _walk(self):
        for token in self.tokens:
            kind = token.type

            if kind == TokenType.INTEGER:
                self._add(f"s.append({token.value!r})")

            elif kind == TokenType.STRING:
                self._add(f"out.text({token.value!r})")

            elif kind == TokenType.REG_GET:
                self._add(f"s.append(r[{token.value}])")

            elif kind == TokenType.REG_SET:
                self._add(f"r[{token.value}] = s.pop()")

            elif kind in _BINARY_OPS:
                self._add("b = s.pop()")
                self._add(f"s[-1] {_BINARY_OPS[kind]} b")

            elif kind == TokenType.NEG:
                self._add("s[-1] = -s[-1]")

            elif kind == TokenType.DUP:
                self._add("s.append(s[-1])")

            elif kind == TokenType.SWAP:
                self._add("s[-1], s[-2] = s[-2], s[-1]")

            elif kind == TokenType.DROP:
                self._add("s.pop()")

            elif kind == TokenType.ROT:
                self._add("s[-3], s[-2], s[-1] = s[-2], s[-1], s[-3]")

            elif kind == TokenType.OVER:
                self._add("s.append(s[-2])")

            elif kind == TokenType.PICK:
                self._add("n = s.pop()")
                self._add("if isinstance(n, float):")
                self._add("    n = int(n)")
                self._add("if n < 0 or n >= len(s):")
                self._add("    raise ValueError(f'pick 索引越界: {n} (栈深度 {len(s)})')")
                self._add("s.append(s[-1 - n])")

            elif kind == TokenType.EQ:
                self._add("b = s.pop()")
                self._add("s[-1] = 1 if s[-1] == b else 0")

            elif kind == TokenType.GT:
                self._add("b = s.pop()")
                self._add("s[-1] = 1 if s[-1] > b else 0")

            elif kind == TokenType.PRINT_NUM:
                self._add("out.num(s.pop())")

            elif kind == TokenType.PRINT_CHAR:
                self._add("out.char(s.pop())")

            elif kind == TokenType.INPUT_NUM:
                self._add("s.append(io.get_num())")

            elif kind == TokenType.INPUT_CHAR:
                self._add("s.append(_read_char(io))")

            elif kind == TokenType.LOOP_START:
                self._open("while True:")
                self._add("tick += 1")
                self._add("if tick > limit:")
                self._add("    raise RuntimeError("
                          "f'执行超时：超过最大迭代次数 {limit}，可能存在无限循环')")
                if self.value_limit:
                    self._add(f"if s and abs(s[-1]) > {self.value_limit}:")
                    self._add("    raise RuntimeError("
                              "'数值增长失控，已中止（循环条件可能写错了）')")
                self._add("if not s or s[-1] == 0:")
                self._add("    break")

            elif kind == TokenType.LOOP_END:
                self._close()

            elif kind == TokenType.IF_START:
                self._open("if s.pop() != 0:")

            elif kind == TokenType.ELSE:
                self._close()
                self._open("else:")

            elif kind == TokenType.IF_END:
                self._close()

            else:
                raise CompileError(f"不支持的指令: {kind.name}")

    def _slot(self, depth, offset=0):
        """depth 是进入指令时的栈深。

        offset=0   取压入位置（第 depth+1 个值）
        offset=-1  取栈顶
        offset=-2  取次栈顶
        """
        index = depth + offset
        if index < 0:
            raise CompileError("栈槽分析出错：访问了不存在的栈槽")
        return f"v{index}"

    def _walk_slots(self, depth_at):
        """
        栈槽变量化：把 s[i] 换成 Python 局部变量 v{i}。

        栈深在编译期已知，所以每个位置该读写哪个变量都是常数，
        不再需要 list 的 append / pop。
        """
        for index, token in enumerate(self.tokens):
            kind = token.type
            depth = depth_at[index]
            # 栈深为 0 时还没压过值，此时只有压栈类指令会走，不会用到 top
            top = self._slot(depth, -1) if depth else "v0"

            if kind == TokenType.INTEGER:
                self._add(f"{self._slot(depth)} = {token.value!r}")

            elif kind == TokenType.STRING:
                self._add(f"out.text({token.value!r})")

            elif kind == TokenType.REG_GET:
                self._add(f"{self._slot(depth)} = r[{token.value}]")

            elif kind == TokenType.REG_SET:
                self._add(f"r[{token.value}] = {top}")

            elif kind in _BINARY_OPS:
                target = self._slot(depth, -2)
                self._add(f"{target} {_BINARY_OPS[kind]} {top}")

            elif kind == TokenType.NEG:
                self._add(f"{top} = -{top}")

            elif kind == TokenType.DUP:
                self._add(f"{self._slot(depth)} = {top}")

            elif kind == TokenType.SWAP:
                low, high = self._slot(depth, -2), top
                self._add(f"{low}, {high} = {high}, {low}")

            elif kind == TokenType.DROP:
                self._add("pass")

            elif kind == TokenType.ROT:
                low = self._slot(depth, -3)
                mid = self._slot(depth, -2)
                self._add(f"{low}, {mid}, {top} = {mid}, {top}, {low}")

            elif kind == TokenType.OVER:
                self._add(f"{self._slot(depth)} = {self._slot(depth, -2)}")

            elif kind == TokenType.EQ:
                target = self._slot(depth, -2)
                self._add(f"{target} = 1 if {target} == {top} else 0")

            elif kind == TokenType.GT:
                target = self._slot(depth, -2)
                self._add(f"{target} = 1 if {target} > {top} else 0")

            elif kind == TokenType.PRINT_NUM:
                self._add(f"out.num({top})")

            elif kind == TokenType.PRINT_CHAR:
                self._add(f"out.char({top})")

            elif kind == TokenType.INPUT_NUM:
                self._add(f"{self._slot(depth)} = io.get_num()")

            elif kind == TokenType.INPUT_CHAR:
                self._add(f"{self._slot(depth)} = _read_char(io)")

            elif kind == TokenType.LOOP_START:
                self._open("while True:")
                self._add("tick += 1")
                self._add("if tick > limit:")
                self._add("    raise RuntimeError("
                          "f'执行超时：超过最大迭代次数 {limit}，可能存在无限循环')")
                if self.value_limit:
                    self._add(f"if abs({top}) > {self.value_limit}:")
                    self._add("    raise RuntimeError("
                              "'数值增长失控，已中止（循环条件可能写错了）')")
                self._add(f"if {top} == 0:")
                self._add("    break")

            elif kind == TokenType.LOOP_END:
                self._close()

            elif kind == TokenType.IF_START:
                self._open(f"if {top} != 0:")

            elif kind == TokenType.ELSE:
                self._close()
                self._open("else:")

            elif kind == TokenType.IF_END:
                self._close()

            else:
                raise CompileError(f"不支持的指令: {kind.name}")

    def finish(self):
        """返回 (run_function, token 数, 生成的 Python 源码)。"""
        depth_at, max_depth = (
            analyze_depths(self.tokens) if self.use_slots else (None, 0)
        )

        if depth_at is None:
            self._walk()
            prologue = "    pass\n"
        else:
            self._walk_slots(depth_at)
            if max_depth:
                names = " = ".join(f"v{index}" for index in range(max_depth))
                prologue = f"    {names} = 0\n"
            else:
                prologue = "    pass\n"

        body = "\n".join(self.lines)
        source = (
            "def __run(s, r, io, out, tick, limit):\n"
            f"{prologue}"
            f"{body}\n"
            "    return tick\n"
        )
        try:
            code = compile(source, "<chickenstack>", "exec")
        except SyntaxError as exc:
            raise CompileError(f"生成的 Python 代码有语法错误: {exc}") from exc

        namespace = {"_read_char": _read_char}
        exec(code, namespace)
        return namespace["__run"], len(self.tokens), source


class CompiledProgram:
    """一次编译、多次执行。"""

    __slots__ = ("_run", "token_count", "source")

    def __init__(self, run, token_count, source):
        self._run = run
        self.token_count = token_count
        self.source = source

    def run(self, io_handler=None, max_iterations=DEFAULT_MAX_ITERATIONS):
        """执行程序，返回程序打印到标准输出的全部文本。"""
        buffer = io.StringIO()
        out = _Output(buffer)
        self._run([], [0] * 26, io_handler, out, 0, max_iterations)
        return buffer.getvalue()


def compile_source(source, value_limit=0, use_slots=True):
    """把 ChickenStack 源码编译成 CompiledProgram。

    Args:
        source: 源码字符串
        value_limit: 大于 0 时在每轮循环检查栈顶绝对值上限，用于校验
            会数值失控的程序；正常运行不要开启，会有额外开销。
        use_slots: 是否启用栈槽变量化。程序能被静态分析时，栈槽会直接映射
            成 Python 局部变量；不能分析（例如含 `!`）时自动退回 list 模式。
    """
    run, count, generated = Compiler(source, value_limit, use_slots).finish()
    return CompiledProgram(run, count, generated)

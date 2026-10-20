"""
ChickenStack 解释器

把 Parser、VM、IOHandler 三个组件组装成可直接运行源码的解释器。
从 main.py 中拆出，以便通过包直接导入。
"""

import time
from typing import Callable, Dict, List, Optional

from .io_handler import IOHandler
from .parser import Parser, Token, TokenType
from .vm import ChickenStackVM


class ChickenStackInterpreter:
    """
    ChickenStack 解释器

    整合 Parser、VM 和 IOHandler 三个核心组件，提供完整的代码执行功能。
    采用依赖注入模式，将 IOHandler 注入到 VM 中。

    Attributes:
        vm (ChickenStackVM): 虚拟机实例，负责执行指令
        parser (Parser): 解析器实例，负责将源代码转换为 Token 列表
        io_handler (IOHandler): 输入输出处理器，处理 I/O 操作
        op_map (Dict[TokenType, Callable]): Token 到操作函数的映射字典

    Example:
        >>> interpreter = ChickenStackInterpreter()
        >>> interpreter.run("10 20 + .")
        ChickenStack 运行中... (指令数: 4)
        30
        运行结束 | 栈: [] | 耗时: 0.000s | 迭代: 4
    """

    # 使用 __slots__ 减少内存占用
    __slots__ = ('vm', 'parser', 'io_handler', 'op_map')

    def __init__(self, max_iterations: Optional[int] = None) -> None:
        """
        初始化 ChickenStack 解释器

        创建虚拟机、解析器和 IOHandler 的实例。
        同时初始化指令映射字典，提高执行效率。

        Args:
            max_iterations: 最大迭代次数，防止无限循环
        """
        self.vm = ChickenStackVM(max_iterations=max_iterations)
        self.parser = Parser()
        self.io_handler = IOHandler()

        # Token 到操作函数的映射字典（使用 TokenType 枚举）
        self.op_map: Dict[TokenType, Callable[[], None]] = {
            TokenType.PLUS: self.vm.op_add,
            TokenType.MINUS: self.vm.op_sub,
            TokenType.MULTIPLY: self.vm.op_mul,
            TokenType.DIVIDE: self.vm.op_div,
            TokenType.MODULO: self.vm.op_mod,
            TokenType.DUP: self.vm.op_dup,
            TokenType.SWAP: self.vm.op_swap,
            TokenType.DROP: self.vm.op_drop,
            TokenType.ROT: self.vm.op_rot,
            TokenType.OVER: self.vm.op_over,
            TokenType.PICK: self.vm.op_pick,
            TokenType.NEG: self.vm.op_neg,
            TokenType.EQ: self.vm.op_eq,
            TokenType.GT: self.vm.op_gt,
            TokenType.PRINT_NUM: self.vm.op_print_num,
            TokenType.PRINT_CHAR: self.vm.op_print_char,
            TokenType.INPUT_NUM: self.vm.op_input_num,
            TokenType.INPUT_CHAR: self.vm.op_input_char,
        }

    def run(self, source_code: str, verbose: bool = True, trace: bool = False) -> None:
        """
        运行 ChickenStack 代码

        这是解释器的核心方法，执行完整的代码运行流程：
        1. 解析源代码为 Token 列表
        2. 构建循环跳转表
        3. 设置 IO Handler
        4. 逐条执行指令
        5. 添加迭代计数和跳转验证

        Args:
            source_code: 源代码字符串
            verbose: 是否打印运行状态（REPL 传 False）
            trace: 是否逐步打印 token 与栈状态

        Returns:
            None

        Raises:
            Exception: 捕获所有运行时错误并打印错误信息

        Example:
            >>> interpreter = ChickenStackInterpreter()
            >>> interpreter.run("5 3 + .")
            ChickenStack 运行中... (指令数: 4)
            8
            运行结束 | 栈: [] | 耗时: 0.000s | 迭代: 4

        Note:
            - 错误会被捕获并打印，不会导致程序崩溃
            - 循环跳转表由 Parser 构建并传递给 VM
            - 添加了迭代计数器，防止无限循环
            - 添加了跳转验证，防止索引越界
        """
        start_time = time.time()
        idx = 0
        token: Optional[Token] = None

        try:
            # 第一步：解析代码
            tokens: List[Token] = self.parser.parse(source_code)
            self.vm.loops = self.parser.get_loop_table()
            self.vm.braces = self.parser.get_brace_table()
            self.vm.io_handler = self.io_handler
            self.vm.reset_iteration_count()

            # 第二步：执行代码
            if verbose:
                print(f"ChickenStack 运行中... (指令数: {len(tokens)})")

            limit = len(tokens)

            while idx < limit:
                token = tokens[idx]
                self.vm.increment_iteration()

                if token.is_integer():
                    self.vm.push(token.value)
                elif token.type == TokenType.STRING:
                    print(token.value, end='', flush=True)
                elif token.type == TokenType.REG_GET:
                    self.vm.push(self.vm.registers[token.value])
                elif token.type == TokenType.REG_SET:
                    self.vm.registers[token.value] = self.vm.pop()
                elif token.type in self.op_map:
                    self.op_map[token.type]()
                elif token.type == TokenType.IF_START:
                    if not self.vm.stack:
                        raise ValueError("if 需要栈顶条件")
                    if self.vm.pop() == 0:
                        target_idx = self.vm.braces[idx]
                        self.vm.validate_jump(target_idx, limit - 1)
                        idx = target_idx
                elif token.type == TokenType.ELSE:
                    target_idx = self.vm.braces[idx]
                    self.vm.validate_jump(target_idx, limit - 1)
                    idx = target_idx
                elif token.type == TokenType.IF_END:
                    pass
                elif token.type == TokenType.LOOP_START:
                    if not self.vm.stack or self.vm.peek() == 0:
                        target_idx = self.vm.loops[idx]
                        self.vm.validate_jump(target_idx, limit - 1)
                        idx = target_idx
                elif token.type == TokenType.LOOP_END:
                    target_idx = self.vm.loops[idx] - 1
                    self.vm.validate_jump(target_idx, limit - 1)
                    idx = target_idx

                idx += 1
                if trace:
                    print(f"[{idx - 1}] {token} -> 栈 {self.vm.get_stack_state()}")

            # 第三步：输出执行结果
            elapsed = time.time() - start_time
            if verbose:
                print(f"\n运行结束 | 栈: {self.vm.get_stack_state()} | 耗时: {elapsed:.3f}s | 迭代: {self.vm.iteration_count}")

        except Exception as e:
            elapsed = time.time() - start_time
            print(f"\n运行错误: {e}")
            if token:
                print(f"位置: Token #{idx} ({token}) - 行 {token.line}, 列 {token.column}")
            print(f"栈: {self.vm.get_stack_state()} | 迭代: {self.vm.iteration_count} | 耗时: {elapsed:.3f}s")
            if "迭代次数" in str(e):
                print("提示: 用 --max-iter <次数> 提高上限，或改用 --compile 执行")

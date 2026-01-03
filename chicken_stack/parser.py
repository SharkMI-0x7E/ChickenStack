"""
🐔 ChickenStack 解析器模块
====================================

本模块负责将 ChickenStack 源代码解析为 Token 列表，并构建循环跳转表。
是解释器的前端处理部分，负责词法分析和语法预处理。

## 核心功能

1. **词法分析 (Lexical Analysis)**
   - 将源代码字符串转换为 Token 列表
   - 识别数字和符号
   - 处理多位数字（如 "10" 识别为整数 10）

2. **循环跳转表构建**
   - 预处理循环符号 `[` 和 `]`
   - 构建循环开始和结束位置的映射关系
   - 验证循环符号的匹配性

3. **语法检查**
   - 检测循环符号是否匹配
   - 提供清晰的错误信息

## Token 结构

解析后的 Token 列表使用优化的 Token 类：

1. **INTEGER**: 表示数字字面量
   - 例如: 10, 20, 5
   - 使用 __slots__ 优化内存占用

2. **操作符**: 表示各种操作
   - 数学运算: PLUS, MINUS, MULTIPLY, DIVIDE, MODULO
   - 栈操作: DUP, SWAP, DROP
   - 逻辑运算: EQ, GT
   - 输入输出: PRINT_NUM, PRINT_CHAR, INPUT_NUM, INPUT_CHAR
   - 循环控制: LOOP_START, LOOP_END

每个 Token 包含位置信息（行号、列号）用于错误定位。

## 循环跳转表

循环跳转表是一个字典，记录循环开始和结束位置的对应关系：

```python
{
    start_index: end_index,  # 循环开始位置 -> 循环结束位置
    end_index: start_index   # 循环结束位置 -> 循环开始位置
}
```

例如，对于代码 "5 [ : . 1 - ]"：
- Token 列表: [Token(INTEGER, 5), Token(LOOP_START), Token(DUP), Token(PRINT_NUM), Token(INTEGER, 1), Token(MINUS), Token(LOOP_END)]
- 跳转表: {1: 6, 6: 1}  # [ 在位置 1，] 在位置 6

## 使用示例

```python
from chicken_stack import Parser

parser = Parser()

# 解析代码
code = "10 20 + 2 * ."
tokens = parser.parse(code)
print(tokens)  # [Token(INTEGER, 10), Token(INTEGER, 20), Token(PLUS), Token(INTEGER, 2), Token(MULTIPLY), Token(PRINT_NUM)]

# 获取循环跳转表
code = "5 [ : . 1 - ]"
tokens = parser.parse(code)
loop_table = parser.get_loop_table()
print(loop_table)  # {1: 6, 6: 1}

# 重置解析器状态
parser.reset()
```

## 解析流程

1. **Token 化 (Tokenization)**
   - 遍历源代码的每个字符
   - 连续的数字字符组成多位数字（使用列表收集，避免字符串拼接）
   - 非数字字符作为独立的符号
   - 记录每个 Token 的位置信息

2. **循环表构建**
   - 使用栈结构匹配 `[` 和 `]`
   - 遇到 `[` 时将位置入栈
   - 遇到 `]` 时弹出栈顶位置，建立映射

3. **错误检测**
   - 检测多余的 `]`（栈为空时遇到 `]`）
   - 检测未闭合的 `[`（解析结束后栈不为空）
"""

from enum import Enum
from typing import Optional


class TokenType(Enum):
    """Token 类型枚举"""
    INTEGER = "INTEGER"      # 整数
    PLUS = "PLUS"            # 加号 +
    MINUS = "MINUS"          # 减号 -
    MULTIPLY = "MULTIPLY"    # 乘号 *
    DIVIDE = "DIVIDE"        # 除号 /
    MODULO = "MODULO"        # 取余 %
    DUP = "DUP"              # 复制 :
    SWAP = "SWAP"            # 交换 \
    DROP = "DROP"            # 丢弃 $
    EQ = "EQ"                # 相等 =
    GT = "GT"                # 大于 >
    PRINT_NUM = "PRINT_NUM"  # 打印数字 .
    PRINT_CHAR = "PRINT_CHAR"  # 打印字符 "
    INPUT_NUM = "INPUT_NUM"  # 输入数字 ,
    INPUT_CHAR = "INPUT_CHAR"  # 输入字符 ?
    LOOP_START = "LOOP_START"  # 循环开始 [
    LOOP_END = "LOOP_END"      # 循环结束 ]


class Token:
    """
    优化的 Token 类，使用 __slots__ 减少内存占用

    Attributes:
        type: Token 类型
        value: Token 值（整数或 None）
        line: 行号（用于错误定位）
        column: 列号（用于错误定位）
    """
    # 强制使用 __slots__ 减少内存占用，避免 __dict__ 开销
    __slots__ = ('type', 'value', 'line', 'column')
    
    # 类级别的常量集合（使用 frozenset 避免被修改）
    _OPERATOR_TYPES = frozenset({
        TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY,
        TokenType.DIVIDE, TokenType.MODULO
    })
    
    _STACK_OP_TYPES = frozenset({TokenType.DUP, TokenType.SWAP, TokenType.DROP})
    
    _LOGIC_OP_TYPES = frozenset({TokenType.EQ, TokenType.GT})
    
    _IO_OP_TYPES = frozenset({
        TokenType.PRINT_NUM, TokenType.PRINT_CHAR,
        TokenType.INPUT_NUM, TokenType.INPUT_CHAR
    })
    
    _LOOP_TYPES = frozenset({TokenType.LOOP_START, TokenType.LOOP_END})

    def __init__(self, type: TokenType, value: Optional[int] = None, line: int = 0, column: int = 0) -> None:
        """
        初始化 Token

        Args:
            type: Token 类型
            value: Token 值（仅 INTEGER 类型有值）
            line: 行号
            column: 列号
        """
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self) -> str:
        """Token 的字符串表示"""
        if self.type == TokenType.INTEGER:
            return f"Token(INTEGER, {self.value}, line={self.line}, col={self.column})"
        return f"Token({self.type.name}, line={self.line}, col={self.column})"

    def is_integer(self) -> bool:
        """判断是否为整数 Token"""
        return self.type == TokenType.INTEGER

    def is_operator(self) -> bool:
        """判断是否为操作符 Token"""
        return self.type in self._OPERATOR_TYPES

    def is_stack_op(self) -> bool:
        """判断是否为栈操作 Token"""
        return self.type in self._STACK_OP_TYPES

    def is_logic_op(self) -> bool:
        """判断是否为逻辑操作 Token"""
        return self.type in self._LOGIC_OP_TYPES

    def is_io_op(self) -> bool:
        """判断是否为 I/O 操作 Token"""
        return self.type in self._IO_OP_TYPES

    def is_loop(self) -> bool:
        """判断是否为循环控制 Token"""
        return self.type in self._LOOP_TYPES

class Parser:
    """
    ChickenStack 代码解析器

    负责将源代码字符串解析为 Token 列表，并构建循环跳转表。
    采用两阶段解析：先进行词法分析，再构建循环跳转表。

    Attributes:
        loops (dict): 循环跳转表，记录循环开始和结束位置的映射关系

    Example:
        >>> parser = Parser()
        >>> tokens = parser.parse("10 20 + .")
        >>> print(tokens)
        [10, 20, '+', '.']
        >>> print(parser.get_loop_table())
        {}
    """

    # 使用 __slots__ 减少内存占用
    __slots__ = ('loops',)

    # 最大循环嵌套深度，防止栈溢出
    MAX_LOOP_DEPTH = 100
    
    # 类级别的常量
    _WHITESPACE = frozenset({' ', '\t', '\r'})
    
    _CHAR_TO_TOKEN = {
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.MULTIPLY,
        '/': TokenType.DIVIDE,
        '%': TokenType.MODULO,
        ':': TokenType.DUP,
        '\\': TokenType.SWAP,
        '$': TokenType.DROP,
        '=': TokenType.EQ,
        '>': TokenType.GT,
        '.': TokenType.PRINT_NUM,
        '"': TokenType.PRINT_CHAR,
        ',': TokenType.INPUT_NUM,
        '?': TokenType.INPUT_CHAR,
        '[': TokenType.LOOP_START,
        ']': TokenType.LOOP_END,
    }

    def __init__(self) -> None:
        """
        初始化 Parser

        创建空的循环跳转表，准备进行代码解析。
        """
        self.loops: dict[int, int] = {}  # 循环跳转表，格式: {start_index: end_index, end_index: start_index}

    def parse(self, source_code: str) -> list[Token]:
        """
        解析代码，处理循环跳转，把代码变成 Token 列表

        这是 Parser 的核心方法，执行完整的解析流程：
        1. 词法分析：将源代码字符串转换为 Token 列表
        2. 循环表构建：构建循环符号的跳转映射关系

        Args:
            source_code: 源代码字符串，包含数字和操作符

        Returns:
            Token 列表，使用优化的 Token 类

        Raises:
            SyntaxError: 当循环符号不匹配时（如多余的 ] 或未闭合的 [）

        Example:
            >>> parser = Parser()
            >>> tokens = parser.parse("10 20 + .")
            >>> print(tokens)
            [Token(INTEGER, 10, line=1, col=1), Token(INTEGER, 20, line=1, col=4), Token(PLUS, line=1, col=7), Token(PRINT_NUM, line=1, col=9)]

            >>> tokens = parser.parse("5 [ : . 1 - ]")
            >>> print(parser.get_loop_table())
            {1: 6, 6: 1}

        Note:
            - 空格作为分隔符，不生成 Token
            - 多位数字会被识别为单个整数（如 "10" 识别为 10）
            - 循环符号必须成对出现，否则会抛出 SyntaxError
            - 支持行注释：从 # 开始到行尾的所有内容都会被忽略
            - 示例: "5 3 + . # 这是一个注释" 会被解析为 [5, 3, '+', '.']
            - 使用列表收集字符，避免字符串拼接，提升性能
        """
        tokens = []
        num_str = ''  # 使用字符串直接拼接，对小数字性能更好
        in_comment = False  # 标记是否在注释中
        line = 1  # 当前行号
        column = 0  # 当前列号

        # ========================================
        # 第一阶段：词法分析 (Tokenization)
        # ========================================

        # 缓存方法引用到局部变量，减少属性查找开销
        tokens_append = tokens.append
        token_integer = Token
        token_integer = Token

        # 遍历源代码的每个字符
        for char in source_code:
            column += 1

            # 处理换行
            if char == '\n':
                line += 1
                column = 0
                if in_comment:
                    in_comment = False
                continue

            # 处理注释：遇到 # 时进入注释模式，直到换行
            if char == '#':
                in_comment = True
                continue  # 跳过 # 字符本身

            # 如果在注释中，跳过所有字符
            if in_comment:
                continue

            # 处理数字字符
            if char.isdigit():
                # 收集数字字符到字符串
                num_str += char
            else:
                # 非数字字符，处理累积的数字
                if num_str:
                    value = int(num_str)
                    start_column = column - len(num_str)
                    tokens_append(token_integer(TokenType.INTEGER, value, line, start_column))
                    num_str = ''  # 清空字符串

                if char not in self._WHITESPACE:
                    # 如果字符不是空白字符，创建对应的 Token
                    token_type = self._CHAR_TO_TOKEN.get(char)
                    if token_type:
                        tokens_append(token_integer(token_type, line=line, column=column))

        # 处理源代码末尾的数字（如果有的话）
        if num_str:
            start_column = column - len(num_str) + 1
            tokens.append(Token(TokenType.INTEGER, int(num_str), line, start_column))

        # ========================================
        # 第二阶段：构建循环跳转表
        # ========================================

        self._build_loop_table(tokens)

        return tokens

    def _build_loop_table(self, tokens: list[Token]) -> None:
        """
        构建循环跳转表

        使用栈结构匹配循环符号 `[` 和 `]`，建立它们之间的跳转关系。
        这个表在执行循环时用于快速跳转到对应的位置。

        Args:
            tokens: Token 列表（使用优化的 Token 类）

        Raises:
            SyntaxError: 当循环符号不匹配时或循环嵌套过深时

        Example:
            >>> parser = Parser()
            >>> tokens = [Token(TokenType.INTEGER, 5), Token(TokenType.LOOP_START), Token(TokenType.DUP), Token(TokenType.PRINT_NUM), Token(TokenType.INTEGER, 1), Token(TokenType.MINUS), Token(TokenType.LOOP_END)]
            >>> parser._build_loop_table(tokens)
            >>> print(parser.loops)
            {1: 6, 6: 1}

        Note:
            - 使用栈结构确保循环符号的正确嵌套
            - 每对匹配的 `[` 和 `]` 会建立双向映射
            - 循环符号必须成对出现，否则会抛出 SyntaxError
            - 循环嵌套深度不能超过 MAX_LOOP_DEPTH（默认 100）
        """
        # 类型验证
        if not isinstance(tokens, list):
            raise TypeError(f"tokens 必须是列表: {type(tokens)}")

        stack = []  # 用于匹配循环符号的栈
        loops = self.loops  # 缓存属性引用
        max_loop_depth = self.MAX_LOOP_DEPTH  # 缓存常量
        loop_start = TokenType.LOOP_START  # 缓存枚举值
        loop_end = TokenType.LOOP_END  # 缓存枚举值

        # 遍历所有 Token，查找循环符号
        for i, token in enumerate(tokens):
            token_type = token.type  # 缓存属性访问
            if token_type == loop_start:
                # 遇到循环开始符号：将位置索引入栈
                # 检查循环嵌套深度
                if len(stack) >= max_loop_depth:
                    raise SyntaxError(
                        f"循环嵌套过深（行 {token.line}, 列 {token.column}），"
                        f"最大深度为 {max_loop_depth}"
                    )
                stack.append(i)
            elif token_type == loop_end:
                # 遇到循环结束符号
                if not stack:
                    # 栈为空，说明没有匹配的 [
                    # 这是一个多余的 ]，抛出语法错误
                    raise SyntaxError(
                        f"循环符号 ] 多余了 (行 {token.line}, 列 {token.column})"
                    )

                # 弹出栈顶位置（最近的 [ 的位置）
                start = stack.pop()

                # 建立双向映射关系
                # start -> end: 从 [ 跳转到 ]
                # end -> start: 从 ] 跳回 [
                loops[start] = i
                loops[i] = start

        # 检查是否有未闭合的 [
        if stack:
            # 栈不为空，说明有 [ 没有匹配的 ]
            # 抛出语法错误，列出所有未闭合的位置
            unclosed_positions = [tokens[pos].line for pos in stack]
            raise SyntaxError(
                f"循环符号 [ 没有闭合（位置: {stack}, 行号: {unclosed_positions}）"
            )

    def get_loop_table(self) -> dict[int, int]:
        """
        获取循环跳转表

        返回循环符号的跳转映射关系，供虚拟机在执行循环时使用。

        Returns:
            循环跳转表的副本，格式: {start_index: end_index, end_index: start_index}

        Example:
            >>> parser = Parser()
            >>> parser.parse("5 [ : . 1 - ]")
            >>> print(parser.get_loop_table())
            {1: 6, 6: 1}

        Note:
            - 返回的是副本，防止外部修改内部状态
            - 如果代码中没有循环，返回空字典
        """
        return self.loops.copy()

    def reset(self) -> None:
        """
        重置解析器状态

        清空循环跳转表，使解析器可以重新解析新的代码。
        主要用于需要多次解析的场景。

        Returns:
            None

        Example:
            >>> parser = Parser()
            >>> parser.parse("5 [ : . 1 - ]")
            >>> parser.reset()
            >>> print(parser.get_loop_table())
            {}
            >>> parser.parse("10 20 + .")
            >>> print(parser.get_loop_table())
            {}

        Note:
            - 不需要重新创建 Parser 对象即可复用
            - 主要在需要多次解析不同代码时使用
        """
        self.loops.clear()
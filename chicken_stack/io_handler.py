"""
ChickenStack 输入输出处理模块

本模块负责处理 ChickenStack 语言的输入操作（输出由 VM 负责）。
支持无缓冲的键盘输入，提供流畅的交互体验。

## 设计目标

1. **无缓冲输入**: 实现类似 C 语言 getch() 的功能，无需按回车即可读取字符
2. **跨平台兼容**: 同时支持 Windows 和非 Windows 系统
3. **用户友好**: 提供清晰的输入提示，实时显示输入内容
4. **错误处理**: 优雅处理输入错误，避免程序崩溃

## 平台差异

### Windows 平台
- 使用 `msvcrt` 模块实现无缓冲输入
- `msvcrt.kbhit()`: 检查键盘是否有按键
- `msvcrt.getch()`: 读取一个字符（不需要按回车）

### 非 Windows 平台 (Linux/macOS)
- 使用标准 `input()` 函数作为回退方案
- 需要按回车确认输入
- 功能受限但保证跨平台兼容

## 使用场景

1. **字符输入 (? 指令)**: 读取单个字符并转换为 ASCII 码
2. **数字输入 (, 指令)**: 读取多位数字并转换为整数

> 数字/字符的输出由 VM（op_print_num / op_print_char）负责，不在本模块内。

## 示例

```python
from chicken_stack import IOHandler

io = IOHandler()

# 读取字符
char_bytes = io.get_char()  # 返回字节串，如 b'A'
ascii_code = ord(char_bytes)  # 转换为 ASCII 码，如 65

# 读取数字
number = io.get_num()  # 返回整数，如 42

```
"""

import sys
try:
    import msvcrt  # Windows 键盘神器，提供无缓冲输入功能
except ImportError:
    msvcrt = None  # 非Windows系统


class IOHandler:
    """
    输入输出处理器

    负责处理 ChickenStack 语言的输入操作（输出由 VM 负责）。
    采用策略模式，根据操作系统平台选择不同的实现方式。

    Attributes:
        is_windows (bool): 标识当前是否为 Windows 系统

    Example:
        >>> io = IOHandler()
        >>> num = io.get_num()
         [等待输入数字] 100
        >>> num
        100
    """

    # 使用 __slots__ 减少内存占用
    __slots__ = ('is_windows',)

    def __init__(self) -> None:
        """
        初始化 IOHandler

        检测当前操作系统平台，设置相应的输入处理策略。
        """
        self.is_windows: bool = sys.platform == 'win32'

    def get_char(self) -> bytes:
        """
        无缓冲读取一个字符

        在 Windows 上使用 msvcrt.getch() 实现真正的无缓冲输入，
        用户按任意键即可读取，无需按回车。

        在非 Windows 系统上尝试使用 termios 实现无缓冲输入，
        如果不可用则回退到标准 input()。

        Returns:
            bytes: 字符的字节串表示（便于后续转换为 ASCII 码）

        Raises:
            无显式异常，但可能因编码问题产生警告

        Example:
            >>> io = IOHandler()
            >>> ch = io.get_char()
             [等待输入字符] A
            >>> ch
            b'A'
            >>> ord(ch)
            65

        Note:
            - 返回的是字节串而非字符串，便于直接获取 ASCII 码
            - 使用 ord() 函数可以将字节串转换为 ASCII 码
            - 在 ChickenStack 中，? 指令使用此方法读取字符
        """
        print("[等待输入字符] ", end='', flush=True)

        if self.is_windows and msvcrt:
            # Windows 平台：使用 msvcrt 实现无缓冲输入
            import time
            while True:
                if msvcrt.kbhit():  # 检查是否有按键
                    ch = msvcrt.getch()  # 读取一个字符
                    print(ch.decode(errors='ignore'), end='\n', flush=True)
                    return ch
                time.sleep(0.001)  # 短暂休眠，减少 CPU 使用率
        else:
            # 非 Windows 平台：尝试使用 termios 实现无缓冲输入
            try:
                import termios
                import tty

                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)

                try:
                    tty.setraw(sys.stdin.fileno())
                    ch = sys.stdin.read(1)
                    print(ch, end='\n', flush=True)
                    return ch.encode('utf-8')
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

            except (ImportError, AttributeError, OSError):
                # 回退到标准 input()（需要按回车）
                ch = input()
                return ch.encode('utf-8')

    def get_num(self) -> int:
        """
        读取一个数字

        支持读取多位数字，用户可以连续输入数字字符。
        按回车、空格或输入非数字字符时结束输入。

        在 Windows 上实现逐字符读取，实时显示输入内容。
        在非 Windows 系统上使用 input() 读取整行。

        Returns:
            int: 用户输入的数字，如果未输入则返回 0

        Example:
            >>> io = IOHandler()
            >>> num = io.get_num()
             [等待输入数字] 123
            >>> num
            123

        Note:
            - 支持负数吗？当前版本不支持，仅支持正整数
            - 输入空或直接按回车返回 0
            - 在 ChickenStack 中，, 指令使用此方法读取数字
        """
        print("[等待输入数字] ", end='', flush=True)
        num_str = ""

        if self.is_windows and msvcrt:
            # Windows 平台：逐字符读取，实时显示
            while True:
                if msvcrt.kbhit():  # 检查是否有按键
                    ch = msvcrt.getch().decode(errors='ignore')

                    if ch in '0123456789':
                        # 数字字符：添加到数字字符串并显示
                        print(ch, end='', flush=True)
                        num_str += ch
                    elif ch == '-' and not num_str:
                        # 负号：只能在开头出现
                        print(ch, end='', flush=True)
                        num_str += ch
                    elif ch == '\b' and num_str:
                        # 退格键：删除最后一个字符
                        print('\b \b', end='', flush=True)
                        num_str = num_str[:-1]
                    elif ch in ['\r', '\n', ' ']:
                        # 回车、换行或空格：结束输入
                        print("")
                        return int(num_str) if num_str else 0
                    # 其他按键被忽略

            # 安全返回（理论上不会执行到这里）
            return int(num_str) if num_str else 0
        else:
            # 非 Windows 平台：读取整行
            num_str = input()
            try:
                return int(num_str) if num_str else 0
            except ValueError:
                print("请输入有效的数字！")
                return 0

    def print_line(self, text: str = "") -> None:
        """
        打印一行文本

        打印文本并自动换行，用于输出提示信息或分隔线。

        Args:
            text (str, optional): 要打印的文本，默认为空字符串

        Returns:
            None

        Example:
            >>> io = IOHandler()
            >>> io.print_line("Hello, World!")
            Hello, World!
            >>> io.print_line()  # 打印空行

        Note:
            - 主要用于调试和输出格式化信息
            - 不是 ChickenStack 语言的指令，仅供内部使用
        """
        print(text, flush=True)
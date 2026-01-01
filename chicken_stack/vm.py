"""
🐔 ChickenStack 虚拟机核心模块
====================================

本模块是 ChickenStack 语言的虚拟机核心，负责执行所有指令操作。
采用基于栈的计算模型，实现了数学运算、栈操作、逻辑判断和输入输出功能。

## 核心设计

1. **基于栈的计算模型**
   - 所有数据操作都在栈上进行
   - 栈顶元素是最新的数据
   - 采用后缀表达式（逆波兰表达式）的计算方式

2. **栈操作原则**
   - push(): 将值推入栈顶
   - pop(): 弹出栈顶值
   - peek(): 查看栈顶值（不弹出）
   - 栈顶元素是操作的优先对象

3. **运算顺序**
   - 双目运算符（+, -, *, /, %, =, >）需要两个操作数
   - 先弹出的是第二个操作数（右操作数）
   - 后弹出的是第一个操作数（左操作数）
   - 计算结果推入栈顶

## 栈结构示意

```
栈顶 (Top)    ↓
              +---+
              | 5 |  ← 栈顶元素，最新推入
              +---+
              | 3 |
              +---+
              | 1 |  ← 栈底元素，最早推入
              +---+
```

## 运算示例

### 加法运算
```
初始栈: [1, 2, 3]
执行 +:
  1. pop() → 3 (右操作数)
  2. pop() → 2 (左操作数)
  3. 计算: 2 + 3 = 5
  4. push(5)
结果栈: [1, 5]
```

### 复制运算
```
初始栈: [1, 2, 3]
执行 ::
  1. peek() → 3 (不弹出)
  2. push(3)
结果栈: [1, 2, 3, 3]
```

### 交换运算
```
初始栈: [1, 2, 3]
执行 \\:
  1. pop() → 3
  2. pop() → 2
  3. push(3)
  4. push(2)
结果栈: [1, 3, 2]
```

## 指令映射

| 操作符 | 方法名 | 说明 | 栈变化 |
|--------|--------|------|--------|
| + | op_add() | 加法 | a b → a+b |
| - | op_sub() | 减法 | a b → a-b |
| * | op_mul() | 乘法 | a b → a*b |
| / | op_div() | 除法 | a b → a//b |
| % | op_mod() | 取余 | a b → a%b |
| : | op_dup() | 复制 | a → a a |
| \\ | op_swap() | 交换 | a b → b a |
| $ | op_drop() | 丢弃 | a b → a |
| = | op_eq() | 相等 | a b → (a==b) |
| > | op_gt() | 大于 | a b → (a>b) |
| . | op_print_num() | 打印数字 | a → (输出 a) |
| " | op_print_char() | 打印字符 | a → (输出 chr(a)) |
| , | op_input_num() | 输入数字 | → (输入的数字) |
| ? | op_input_char() | 输入字符 | → (输入字符的 ASCII) |

## 使用示例

```python
from chicken_stack import ChickenStackVM, IOHandler

# 创建虚拟机并设置 IO 处理器
vm = ChickenStackVM(io_handler=IOHandler())

# 计算表达式: 10 + 20 * 2
vm.push(10)
vm.push(20)
vm.push(2)
vm.op_mul()   # 20 * 2 = 40, 栈: [10, 40]
vm.op_add()   # 10 + 40 = 50, 栈: [50]
vm.op_print_num()  # 输出: 50

# 循环示例: 从 5 倒数到 1
vm.push(5)
# 循环逻辑由解释器控制，虚拟机提供操作方法
```
"""

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .io_handler import IOHandler


class ChickenStackVM:
    """
    ChickenStack 虚拟机

    负责执行所有 ChickenStack 指令，维护数据栈和循环跳转表。
    采用基于栈的计算模型，所有操作都在栈上进行。

    Attributes:
        stack (list): 数据栈，存储所有操作数和中间结果
        loops (dict): 循环跳转表，由 Parser 填充
        io_handler (IOHandler): 输入输出处理器，处理 I/O 操作
        max_iterations (int): 最大迭代次数，防止无限循环
        iteration_count (int): 当前迭代计数器

    Example:
        >>> from chicken_stack import ChickenStackVM, IOHandler
        >>> vm = ChickenStackVM(io_handler=IOHandler())
        >>> vm.push(10)
        >>> vm.push(20)
        >>> vm.op_add()
        >>> vm.get_stack_state()
        [30]
        >>> vm.op_print_num()
        30
    """

    # 使用 __slots__ 减少内存占用
    __slots__ = ('stack', 'loops', 'io_handler', 'max_iterations', 'iteration_count')

    # 默认最大迭代次数（防止无限循环）
    DEFAULT_MAX_ITERATIONS = 1000000
    # 栈大小限制，防止内存溢出
    MAX_STACK_SIZE = 10000

    def __init__(self, io_handler: Optional['IOHandler'] = None, max_iterations: Optional[int] = None) -> None:
        """
        初始化 ChickenStack 虚拟机

        Args:
            io_handler: 输入输出处理器。如果为 None，则无法执行输入输出操作。
            max_iterations: 最大迭代次数，防止无限循环。如果为 None，使用默认值。

        Note:
            - 栈初始为空列表 []
            - 循环跳转表初始为空字典 {}
            - io_handler 需要在执行 I/O 操作前设置
            - max_iterations 用于防止无限循环和 DOS 攻击
        """
        self.stack: list[int] = []           # 数据栈，存储所有操作数
        self.loops: dict[int, int] = {}           # 循环跳转表，由 Parser 填充
        self.io_handler = io_handler  # 输入输出处理器
        self.max_iterations = max_iterations or self.DEFAULT_MAX_ITERATIONS  # 最大迭代次数
        self.iteration_count = 0  # 当前迭代计数器

    # ========================================
    # 基础栈操作方法
    # ========================================

    def _require_stack(self, min_size: int = 1) -> None:
        """
        检查栈是否有足够的元素

        在执行需要多个操作数的运算前，检查栈的大小是否满足要求。
        如果不满足，抛出 ValueError 异常。

        Args:
            min_size (int): 需要的最小栈大小，默认为 1

        Raises:
            ValueError: 当栈的大小小于 min_size 时

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.push(1)
            >>> vm._require_stack(1)  # 通过
            >>> vm._require_stack(2)  # 抛出 ValueError
        """
        if len(self.stack) < min_size:
            raise ValueError(
                f"栈大小不足：当前 {len(self.stack)} 个元素，"
                f"需要至少 {min_size} 个元素"
            )

    def push(self, value: int) -> None:
        """
        推入值到栈顶

        将指定的值添加到栈的顶部，成为新的栈顶元素。

        Args:
            value (int): 要推入栈的值

        Returns:
            None

        Raises:
            TypeError: 当 value 不是整数时
            MemoryError: 当栈大小超过最大限制时

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.push(10)
            >>> vm.push(20)
            >>> vm.get_stack_state()
            [10, 20]
        """
        # 类型验证
        if not isinstance(value, int):
            raise TypeError(
                f"只能推入整数，收到类型: {type(value).__name__}"
            )

        # 栈大小检查
        if len(self.stack) >= self.MAX_STACK_SIZE:
            raise MemoryError(f"栈溢出: 超过最大栈大小 {self.MAX_STACK_SIZE}")

        self.stack.append(value)

    def pop(self) -> int:
        """
        弹出栈顶值

        移除并返回栈顶的值。如果栈为空，抛出 ValueError 异常。

        Returns:
            int: 栈顶的值

        Raises:
            ValueError: 当栈为空时

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.push(10)
            >>> vm.push(20)
            >>> vm.pop()
            20
            >>> vm.get_stack_state()
            [10]
        """
        if not self.stack:
            raise ValueError("栈空了，无法弹出")
        return self.stack.pop()

    def peek(self) -> int:
        """
        查看栈顶值（不弹出）

        返回栈顶的值，但不将其从栈中移除。如果栈为空，抛出 ValueError 异常。

        Returns:
            int: 栈顶的值

        Raises:
            ValueError: 当栈为空时

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.push(10)
            >>> vm.push(20)
            >>> vm.peek()
            20
            >>> vm.get_stack_state()
            [10, 20]  # 栈顶元素未被移除
        """
        if not self.stack:
            raise ValueError("栈空了，无法查看")
        return self.stack[-1]

    # ========================================
    # 迭代控制和跳转验证方法
    # ========================================

    def set_max_iterations(self, max_iterations: int) -> None:
        """
        设置最大迭代次数

        Args:
            max_iterations: 最大迭代次数

        Raises:
            TypeError: 当 max_iterations 不是整数时
            ValueError: 当 max_iterations 小于等于 0 时

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.set_max_iterations(1000000)
        """
        if not isinstance(max_iterations, int):
            raise TypeError("max_iterations 必须是整数")

        if max_iterations <= 0:
            raise ValueError("max_iterations 必须大于 0")

        self.max_iterations = max_iterations

    def increment_iteration(self) -> None:
        """
        增加迭代计数器

        Raises:
            RuntimeError: 当超过最大迭代次数时

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.increment_iteration()
        """
        self.iteration_count += 1
        if self.iteration_count > self.max_iterations:
            raise RuntimeError(
                f"执行超时：超过最大迭代次数 {self.max_iterations}，"
                f"可能存在无限循环"
            )

    def reset_iteration_count(self) -> None:
        """
        重置迭代计数器

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.reset_iteration_count()
        """
        self.iteration_count = 0

    def validate_jump(self, target_idx: int, max_idx: int) -> None:
        """
        验证跳转目标是否有效

        Args:
            target_idx: 跳转目标索引
            max_idx: 最大有效索引

        Raises:
            TypeError: 当参数类型不正确时
            IndexError: 当跳转目标超出范围时

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.validate_jump(5, 10)  # 有效
            >>> vm.validate_jump(15, 10)  # 抛出 IndexError
        """
        # 类型验证
        if not isinstance(target_idx, int):
            raise TypeError(f"跳转目标必须是整数: {type(target_idx)}")
        if not isinstance(max_idx, int):
            raise TypeError(f"最大索引必须是整数: {type(max_idx)}")

        # 范围验证
        if target_idx < 0 or target_idx > max_idx:
            raise IndexError(
                f"无效的跳转目标: {target_idx} (有效范围: 0-{max_idx})"
            )

    # ========================================
    # 数学运算方法
    # ========================================

    def op_add(self) -> None:
        """
        加法运算

        取栈顶两个数相加，将结果推入栈顶。
        操作顺序：第一个弹出的数是右操作数，第二个是左操作数。

        栈变化: [a, b] → [a + b]

        Raises:
            ValueError: 当栈中元素少于 2 个时

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.push(10)
            >>> vm.push(20)
            >>> vm.op_add()
            >>> vm.get_stack_state()
            [30]  # 10 + 20 = 30
        """
        self._require_stack(2)
        b = self.pop()  # 右操作数
        a = self.pop()  # 左操作数
        self.push(a + b)  # 结果推入栈顶

    def op_sub(self) -> None:
        """
        减法运算

        取栈顶两个数相减，将结果推入栈顶。
        操作顺序：第一个弹出的数是右操作数，第二个是左操作数。

        栈变化: [a, b] → [a - b]

        Raises:
            ValueError: 当栈中元素少于 2 个时

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.push(20)
            >>> vm.push(8)
            >>> vm.op_sub()
            >>> vm.get_stack_state()
            [12]  # 20 - 8 = 12
        """
        self._require_stack(2)
        b = self.pop()  # 右操作数
        a = self.pop()  # 左操作数
        self.push(a - b)  # 结果推入栈顶

    def op_mul(self) -> None:
        """
        乘法运算

        取栈顶两个数相乘，将结果推入栈顶。

        栈变化: [a, b] → [a * b]

        Raises:
            ValueError: 当栈中元素少于 2 个时

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.push(6)
            >>> vm.push(7)
            >>> vm.op_mul()
            >>> vm.get_stack_state()
            [42]  # 6 * 7 = 42
        """
        self._require_stack(2)
        b = self.pop()
        a = self.pop()
        self.push(a * b)

    def op_div(self) -> None:
        """
        除法运算

        取栈顶两个数相除，将结果推入栈顶。
        使用整数除法（向下取整）。

        栈变化: [a, b] → [a // b]

        Raises:
            ValueError: 当栈中元素少于 2 个时
            ZeroDivisionError: 当除数为零时

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.push(20)
            >>> vm.push(4)
            >>> vm.op_div()
            >>> vm.get_stack_state()
            [5]  # 20 // 4 = 5
        """
        self._require_stack(2)
        b = self.pop()
        a = self.pop()

        if b == 0:
            # 除零错误应该立即抛出异常
            raise ZeroDivisionError("除数为零，无法执行除法运算")

        self.push(a // b)

    def op_mod(self) -> None:
        """
        取余数运算

        取栈顶两个数相除的余数，将结果推入栈顶。

        栈变化: [a, b] → [a % b]

        Raises:
            ValueError: 当栈中元素少于 2 个时
            ZeroDivisionError: 当模数为零时

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.push(17)
            >>> vm.push(5)
            >>> vm.op_mod()
            >>> vm.get_stack_state()
            [2]  # 17 % 5 = 2
        """
        self._require_stack(2)
        b = self.pop()
        a = self.pop()

        if b == 0:
            # 模零错误应该立即抛出异常
            raise ZeroDivisionError("模数为零，无法执行取余运算")

        self.push(a % b)

    # ========================================
    # 栈操作方法
    # ========================================

    def op_dup(self) -> None:
        """
        复制栈顶 (Duplicate)

        复制栈顶元素，将副本推入栈顶。
        原栈顶元素保留在栈中。

        栈变化: [a] → [a, a]

        Raises:
            ValueError: 当栈为空时
            MemoryError: 当复制后栈溢出时

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.push(5)
            >>> vm.op_dup()
            >>> vm.get_stack_state()
            [5, 5]  # 栈顶元素被复制

        Note:
            - 对应 ChickenStack 指令: :
        """
        self._require_stack(1)

        # 检查复制后是否会溢出
        if len(self.stack) >= self.MAX_STACK_SIZE:
            raise MemoryError("无法复制: 栈已满")

        self.push(self.peek())

    def op_swap(self) -> None:
        """
        交换栈顶 (Swap)

        交换栈顶两个元素的位置。

        栈变化: [a, b] → [b, a]

        Raises:
            ValueError: 当栈中元素少于 2 个时

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.push(1)
            >>> vm.push(2)
            >>> vm.op_swap()
            >>> vm.get_stack_state()
            [2, 1]  # 两个元素交换位置

        Note:
            - 对应 ChickenStack 指令: \
            - 先弹出 b，再弹出 a，然后按 b、a 顺序推入
        """
        self._require_stack(2)
        b = self.pop()
        a = self.pop()
        self.push(b)  # 先推入 b
        self.push(a)  # 再推入 a

    def op_drop(self) -> None:
        """
        丢弃栈顶 (Drop)

        移除栈顶元素，不返回任何值。

        栈变化: [a, b] → [a]

        Raises:
            ValueError: 当栈为空时

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.push(10)
            >>> vm.push(20)
            >>> vm.op_drop()
            >>> vm.get_stack_state()
            [10]  # 栈顶元素 20 被丢弃

        Note:
            - 对应 ChickenStack 指令: $
        """
        self._require_stack(1)
        self.pop()  # 显式弹出栈顶元素

    # ========================================
    # 逻辑运算方法
    # ========================================

    def op_eq(self) -> None:
        """
        判断相等 (Equal)

        比较栈顶两个元素是否相等。
        如果相等，推入 1；否则推入 0。

        栈变化: [a, b] → [1] (如果 a == b)
        栈变化: [a, b] → [0] (如果 a != b)

        Raises:
            ValueError: 当栈中元素少于 2 个时

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.push(5)
            >>> vm.push(5)
            >>> vm.op_eq()
            >>> vm.get_stack_state()
            [1]  # 5 == 5，推入 1

            >>> vm.clear_stack()
            >>> vm.push(5)
            >>> vm.push(3)
            >>> vm.op_eq()
            >>> vm.get_stack_state()
            [0]  # 5 != 3，推入 0

        Note:
            - 对应 ChickenStack 指令: =
            - 返回值是布尔值的整数表示（1 表示真，0 表示假）
        """
        self._require_stack(2)
        b = self.pop()
        a = self.pop()
        self.push(1 if a == b else 0)

    def op_gt(self) -> None:
        """
        判断大于 (Greater Than)

        比较栈顶两个元素，判断第一个是否大于第二个。
        如果大于，推入 1；否则推入 0。

        栈变化: [a, b] → [1] (如果 a > b)
        栈变化: [a, b] → [0] (如果 a <= b)

        Raises:
            ValueError: 当栈中元素少于 2 个时

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.push(10)
            >>> vm.push(5)
            >>> vm.op_gt()
            >>> vm.get_stack_state()
            [1]  # 10 > 5，推入 1

            >>> vm.clear_stack()
            >>> vm.push(5)
            >>> vm.push(10)
            >>> vm.op_gt()
            >>> vm.get_stack_state()
            [0]  # 5 <= 10，推入 0

        Note:
            - 对应 ChickenStack 指令: >
            - 返回值是布尔值的整数表示（1 表示真，0 表示假）
        """
        self._require_stack(2)
        b = self.pop()
        a = self.pop()
        self.push(1 if a > b else 0)

    # ========================================
    # 输入输出方法
    # ========================================

    def op_print_num(self) -> None:
        """
        打印数字

        弹出栈顶元素并打印到标准输出。
        数字后自动添加一个空格。

        栈变化: [a] → [] (弹出并打印 a)

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.push(42)
            >>> vm.op_print_num()
            42  # 输出: 42
            >>> vm.get_stack_state()
            []  # 栈为空

        Note:
            - 对应 ChickenStack 指令: .
            - 如果栈为空，不执行任何操作
            - 使用 flush=True 确保立即输出
        """
        if self.stack:
            print(f"{self.pop()}", end=' ', flush=True)

    def op_print_char(self) -> None:
        """
        打印字符 (ASCII)

        弹出栈顶元素，将其作为 ASCII 码转换为字符并打印。
        不添加空格，适合连续打印字符串。

        栈变化: [a] → [] (弹出并打印 chr(a))

        Raises:
            ValueError: 当栈为空或字符码无效时

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.push(65)
            >>> vm.op_print_char()
            A  # 输出: A (ASCII 码 65)
            >>> vm.get_stack_state()
            []  # 栈为空

        Note:
            - 对应 ChickenStack 指令: "
            - 支持 Unicode 字符（0-1114111）
            - 使用 chr() 函数将 ASCII 码转换为字符
        """
        self._require_stack(1)
        value = self.pop()

        # 验证 Unicode 范围
        if value < 0 or value > 1114111:
            raise ValueError(
                f"无效的字符码: {value} (有效范围: 0-1114111)"
            )

        try:
            print(chr(value), end='', flush=True)
        except ValueError as e:
            raise ValueError(f"无法转换为字符: {value}") from e

    def op_input_num(self) -> None:
        """
        输入数字

        从用户输入读取一个数字，并将其推入栈顶。

        栈变化: [] → [n] (n 是用户输入的数字)

        Raises:
            RuntimeError: 当 io_handler 未设置时
            ValueError: 当输入为空或无效时

        Example:
            >>> from chicken_stack import IOHandler
            >>> vm = ChickenStackVM(io_handler=IOHandler())
            >>> vm.op_input_num()
            👉 [等待输入数字] 42
            >>> vm.get_stack_state()
            [42]

        Note:
            - 对应 ChickenStack 指令: ,
            - 必须先设置 io_handler 才能使用
            - 输入由 IOHandler.get_num() 方法处理
        """
        if self.io_handler is None:
            raise RuntimeError("IO Handler 未设置，无法输入数字")

        try:
            num = self.io_handler.get_num()
            if num is None:
                raise ValueError("输入为空或无效")
            self.push(num)
        except Exception as e:
            raise RuntimeError(f"输入数字失败: {e}") from e

    def op_input_char(self) -> None:
        """
        输入字符

        从用户输入读取一个字符，将其转换为 ASCII 码并推入栈顶。

        栈变化: [] → [n] (n 是输入字符的 ASCII 码)

        Raises:
            RuntimeError: 当 io_handler 未设置时
            ValueError: 当输入为空或解码失败时

        Example:
            >>> from chicken_stack import IOHandler
            >>> vm = ChickenStackVM(io_handler=IOHandler())
            >>> vm.op_input_char()
            👉 [等待输入字符] A
            >>> vm.get_stack_state()
            [65]  # 'A' 的 ASCII 码是 65

        Note:
            - 对应 ChickenStack 指令: ?
            - 必须先设置 io_handler 才能使用
            - 输入由 IOHandler.get_char() 方法处理
        """
        if self.io_handler is None:
            raise RuntimeError("IO Handler 未设置，无法输入字符")

        char_bytes = self.io_handler.get_char()

        if char_bytes is None:
            raise ValueError("输入为空")

        try:
            char = char_bytes.decode('utf-8')
            if not char:
                raise ValueError("输入字符为空")
            self.push(ord(char[0]))
        except UnicodeDecodeError as e:
            raise ValueError(f"字符解码失败: {e}") from e
        except (AttributeError, TypeError) as e:
            raise TypeError(f"无效的输入类型: {type(char_bytes)}") from e

    # ========================================
    # 栈状态管理方法
    # ========================================

    def get_stack_state(self) -> list[int]:
        """
        获取当前栈状态

        返回栈的副本，用于调试和状态检查。

        Returns:
            list: 栈的副本，包含所有元素

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.push(1)
            >>> vm.push(2)
            >>> vm.push(3)
            >>> vm.get_stack_state()
            [1, 2, 3]

        Note:
            - 返回的是副本，防止外部修改内部状态
            - 主要用于调试和测试
        """
        return self.stack.copy()

    def clear_stack(self) -> None:
        """
        清空栈

        移除栈中的所有元素，使栈变为空。

        Returns:
            None

        Example:
            >>> vm = ChickenStackVM()
            >>> vm.push(1)
            >>> vm.push(2)
            >>> vm.clear_stack()
            >>> vm.get_stack_state()
            []

        Note:
            - 主要用于调试和重置虚拟机状态
            - 不影响 loops 和 io_handler
        """
        self.stack.clear()
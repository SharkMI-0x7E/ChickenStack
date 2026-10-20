r"""
ChickenStack - 基于栈的 RPN 编程语言

ChickenStack 是一种受 Brainfuck 启发、但更人类友好的栈式编程语言。
它基于 "栈 (Stack)" 和 "逆波兰表达式 (RPN)" 设计，避免了 Brainfuck 中痛苦的指针移动。

## 核心设计原理

1. **基于栈的计算模型**
   - 所有数据操作都在栈上进行
   - 采用后缀表达式 (Reverse Polish Notation)
   - 例如：计算 5 + 3 写作 "5 3 +"（先入栈5，再入栈3，最后执行加法）

2. **指令覆盖**
   - 支持基本的数学运算 (+, -, *, /, %)
   - 支持栈操作 (复制、交换、丢弃、旋转、复制第二个、按深度复制)
   - 支持条件分支 ({ then | else })
   - 支持字符串 '...'、负数字面量 ~5、26 个寄存器 (a-z / A-Z)
   - 支持整数与小数（3.14），混算按 Python 规则提升
   - 支持逻辑判断 (=, >)
   - 支持循环控制 ([, ])
   - 支持输入输出 (., ", ,, ?)

   > 注：语言在理论上具备图灵完备的潜力，但本项目未给出严格论证；且实现层面有栈大小（10000）和迭代次数（1000000）上限，因此并非严格图灵完备。

3. **人类可读性**
   - 使用直观的符号而非晦涩的操作符
   - 数字直接表示（如 "10" 而非 "++++++++++"）
   - 逻辑清晰，易于理解和调试

## 语言特性对比

### Brainfuck vs ChickenStack

计算 5 + 3:
- Brainfuck: +++++>+++[<+>-]<. (需要数 + 号，移动指针)
- ChickenStack: 5 3 + . (直接、直观)

打印 "HELLO":
- Brainfuck: 需要大量 + 和 > 操作符，难以阅读
- ChickenStack: 72 " 69 " 76 " 76 " 79 " (直接使用 ASCII 码)

## 指令集

### 数据 (Data)
- 123: 整数字面量，任意位数
- 3.14: 小数字面量（IEEE 754 double），小数点前必须有数字，`.5` 非法
- ~5: 负数字面量（等价于 5 ~），同样支持小数 ~0.5
- '...': 字符串字面量，执行时原样打印，不压栈
- a-z: 读取寄存器（a=0 … z=25）
- A-Z: 写入寄存器（弹出栈顶）

### 数学运算 (Math)
- +: 加法（取栈顶两个数相加）
- -: 减法
- *: 乘法
- /: 除法
- %: 取余数
- ~: 取负（5 ~ 得到 -5）

### 栈操作 (Stack Ops)
- :: 复制栈顶 (Duplicate) -> 5 : 变成 5 5
- \: 交换栈顶 (Swap) -> 1 2 \ 变成 2 1
- $: 丢弃栈顶 (Pop)
- @: 旋转栈顶三个 (Rot) -> a b c 变成 b c a
- &: 复制第二个 (Over) -> a b 变成 a b a
- !: 按深度复制 (Pick) -> 弹出 n，复制往下第 n 个

### 输入输出 (I/O)
- .: 打印数字（如 65 . 输出 65）
- ": 打印字符（如 65 " 输出 A）
- ,: 输入数字
- ?: 输入字符

### 逻辑控制 (Logic)
- [: 循环开始（如果栈顶是 0，跳到 ]）
- ]: 循环结束（跳回 [）
- =: 判断相等（相等推入 1，不等推入 0）
- >: 判断大于
- { then | else }: 条件分支（`{` 弹出条件，0 执行 else；`| else` 可省略）

## 模块结构

本模块导出三个核心类：

1. **ChickenStackVM** (vm.py)
   - 虚拟机核心，负责执行所有指令
   - 维护数据栈和循环跳转表
   - 实现所有操作方法（数学、栈操作、逻辑、I/O）

2. **Parser** (parser.py)
   - 代码解析器，负责将源代码转换为 Token 列表
   - 构建循环符号的跳转表
   - 处理循环符号匹配错误

3. **IOHandler** (io_handler.py)
   - 输入输出处理器
   - 支持无缓冲的键盘输入
   - 跨平台兼容（Windows 和非 Windows 系统）

## 使用示例

### 基本数学运算

```python
from chicken_stack import ChickenStackVM, Parser, IOHandler

# 创建解释器组件
vm = ChickenStackVM()
parser = Parser()
io_handler = IOHandler()

# 解析代码
tokens = parser.parse("10 20 + 2 * .")
vm.loops = parser.get_loop_table()
vm.io_handler = io_handler

# 执行代码
for token in tokens:
    if isinstance(token, int):
        vm.push(token)
    elif token == '+':
        vm.op_add()
    elif token == '*':
        vm.op_mul()
    elif token == '.':
        vm.op_print_num()

# 输出: 60
```

### 循环示例

```python
# 从 5 倒数到 1
code = "5 [ : . 1 - ]"
# 执行过程：
# 1. 入栈 5
# 2. [ 检查栈顶 5 != 0，进入循环
# 3. : 复制栈顶 -> 栈: 5 5
# 4. . 打印栈顶 5
# 5. 1 入栈 -> 栈: 5 1
# 6. - 5-1=4 -> 栈: 4
# 7. ] 跳回 [
# 重复...直到栈顶为 0
```

## 版本历史

- v1.0.0: 初始版本，实现所有核心功能

## 参考资源

- Brainfuck: https://en.wikipedia.org/wiki/Brainfuck
- 逆波兰表达式: https://en.wikipedia.org/wiki/Reverse_Polish_notation
- 栈数据结构: https://en.wikipedia.org/wiki/Stack_(abstract_data_type)
"""

from .vm import ChickenStackVM
from .parser import Parser, Token, TokenType
from .io_handler import IOHandler
from .interpreter import ChickenStackInterpreter
from .compiler import CompiledProgram, compile_source

__version__ = "1.1.0"
__all__ = [
    "ChickenStackVM",
    "ChickenStackInterpreter",
    "Parser",
    "IOHandler",
    "Token",
    "TokenType",
    "CompiledProgram",
    "compile_source",
]
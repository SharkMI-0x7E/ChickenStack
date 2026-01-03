# Python API 基本使用

ChickenStack 提供了完整的 Python API，允许您在 Python 程序中直接使用 ChickenStack 解释器和虚拟机。

## 概述

ChickenStack 的 Python API 包含以下主要组件：

- **ChickenStackInterpreter**: 高级解释器，整合所有功能
- **ChickenStackVM**: 虚拟机核心，执行所有操作
- **Parser**: 解析器，将代码转换为 Token 列表
- **IOHandler**: 输入输出处理器

## 基本使用

### 导入模块

```python
# 方式一: 从 chicken_stack 导入解释器（推荐）
from chicken_stack import ChickenStackInterpreter

# 方式二: 从 chicken_stack 导入各个组件
from chicken_stack import ChickenStackVM, Parser, IOHandler, Token, TokenType

# 方式三: 从 main 导入解释器（仅用于直接运行脚本）
from main import ChickenStackInterpreter
```

### 创建解释器

```python
from chicken_stack import ChickenStackInterpreter

# 创建解释器实例
interpreter = ChickenStackInterpreter()

# 运行代码
interpreter.run("5 3 + .")  # 输出: 8
```

### 运行简单代码

```python
from chicken_stack import ChickenStackInterpreter

interpreter = ChickenStackInterpreter()

# 运行单行代码
interpreter.run("5 3 + .")  # 输出: 8

# 运行多行代码
code = """
10 20 + .
5 3 * .
"""
interpreter.run(code)  # 输出: 30 15
```

## ChickenStackInterpreter

### 创建解释器

```python
from main import ChickenStackInterpreter

# 创建默认解释器
interpreter = ChickenStackInterpreter()

# 创建自定义解释器
from chicken_stack import IOHandler
io = IOHandler()
interpreter = ChickenStackInterpreter(io_handler=io)
```

### run() 方法

运行 ChickenStack 代码：

```python
from main import ChickenStackInterpreter

interpreter = ChickenStackInterpreter()

# 运行代码字符串
interpreter.run("5 3 + .")

# 运行多行代码
code = """
5 3 + .
10 20 + .
"""
interpreter.run(code)
```

### 访问内部组件

```python
from main import ChickenStackInterpreter

interpreter = ChickenStackInterpreter()

# 访问虚拟机
vm = interpreter.vm
print(vm.get_stack_state())

# 访问解析器
parser = interpreter.parser

# 访问 IO 处理器
io = interpreter.io_handler
```

## ChickenStackVM

### 创建虚拟机

```python
from chicken_stack import ChickenStackVM

# 创建默认虚拟机
vm = ChickenStackVM()

# 创建带 IO 的虚拟机
from chicken_stack import IOHandler
io = IOHandler()
vm = ChickenStackVM(io_handler=io)
```

### 基本操作

```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()

# 推入数据
vm.push(10)
vm.push(20)
print(vm.get_stack_state())  # [10, 20]

# 查看栈顶
print(vm.peek())  # 20

# 弹出元素
value = vm.pop()
print(value)  # 20
print(vm.get_stack_state())  # [10]
```

### 数学运算

```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()

# 加法
vm.push(5)
vm.push(3)
vm.op_add()
print(vm.get_stack_state())  # [8]

# 减法
vm.push(10)
vm.push(4)
vm.op_sub()
print(vm.get_stack_state())  # [8, 6]

# 乘法
vm.push(6)
vm.push(7)
vm.op_mul()
print(vm.get_stack_state())  # [8, 6, 42]

# 除法
vm.push(20)
vm.push(4)
vm.op_div()
print(vm.get_stack_state())  # [8, 6, 42, 5]

# 取余
vm.push(17)
vm.push(5)
vm.op_mod()
print(vm.get_stack_state())  # [8, 6, 42, 5, 2]
```

### 栈操作

```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()

# 复制
vm.push(5)
vm.op_dup()
print(vm.get_stack_state())  # [5, 5]

# 交换
vm.push(1)
vm.push(2)
vm.op_swap()
print(vm.get_stack_state())  # [5, 5, 2, 1]

# 丢弃
vm.push(10)
vm.push(20)
vm.op_drop()
print(vm.get_stack_state())  # [5, 5, 2, 1, 10]
```

### 逻辑运算

```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()

# 相等
vm.push(5)
vm.push(5)
vm.op_eq()
print(vm.get_stack_state())  # [1]

# 大于
vm.push(10)
vm.push(5)
vm.op_gt()
print(vm.get_stack_state())  # [1, 1]
```

### 输入输出

```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()

# 输出数字
vm.push(42)
vm.op_print_num()  # 输出: 42

# 输出字符
vm.push(65)
vm.op_print_char()  # 输出: A

# 输入数字
vm.op_input_num()  # 从用户输入读取数字

# 输入字符
vm.op_input_char()  # 从用户输入读取字符
```

### 循环控制

```python
from chicken_stack import ChickenStackVM, Parser, TokenType

vm = ChickenStackVM()
parser = Parser()

# 解析循环代码
code = "5 [ : . 1 - ]"
tokens = parser.parse(code)
vm.loops = parser.get_loop_table()

# 执行循环（使用新的 Token 类型）
for i, token in enumerate(tokens):
    if token.is_integer():
        vm.push(token.value)
    elif token.type == TokenType.LOOP_START:
        if not vm.stack or vm.peek() == 0:
            i = vm.loops[i]
    elif token.type == TokenType.LOOP_END:
        i = vm.loops[i] - 1
    elif token.type == TokenType.DUP:
        vm.op_dup()
    elif token.type == TokenType.PRINT_NUM:
        vm.op_print_num()
    elif token.is_integer() and token.value == 1:
        vm.push(1)
    elif token.type == TokenType.MINUS:
        vm.op_sub()
```

### 查看栈状态

```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()

# 推入一些数据
vm.push(10)
vm.push(20)
vm.push(30)

# 获取栈状态
stack = vm.get_stack_state()
print(stack)  # [10, 20, 30]

# 查看栈顶
top = vm.peek()
print(top)  # 30

# 检查栈是否为空
is_empty = len(vm.stack) == 0
print(is_empty)  # False
```

## Parser

### 创建解析器

```python
from chicken_stack import Parser

parser = Parser()
```

### 解析代码

```python
from chicken_stack import Parser

parser = Parser()

# 解析简单代码
code = "10 20 + ."
tokens = parser.parse(code)
print(tokens)  # [10, 20, '+', '.']

# 解析复杂代码
code = "5 [ : . 1 - ]"
tokens = parser.parse(code)
print(tokens)  # [5, '[', ':', '.', 1, '-', ']']
```

### 获取循环跳转表

```python
from chicken_stack import Parser

parser = Parser()

# 解析包含循环的代码
code = "5 [ : . 1 - ]"
tokens = parser.parse(code)

# 获取循环跳转表
loop_table = parser.get_loop_table()
print(loop_table)  # {1: 6, 6: 1}
```

### 自定义解析器

```python
from chicken_stack import Parser

class CustomParser(Parser):
    def parse(self, source_code):
        tokens = super().parse(source_code)
        print(f"解析到 {len(tokens)} 个 token")
        print(f"Token 列表: {tokens}")
        return tokens

# 使用自定义解析器
parser = CustomParser()
tokens = parser.parse("5 3 + .")
```

## IOHandler

### 创建 IO Handler

```python
from chicken_stack import IOHandler

io = IOHandler()
```

### 基本输入输出

```python
from chicken_stack import IOHandler

io = IOHandler()

# 输出数字
io.print_num(42)  # 输出: 42

# 输出字符
io.print_char(65)  # 输出: A

# 输入数字
num = io.get_num()  # 从用户输入读取数字

# 输入字符
char = io.get_char()  # 从用户输入读取字符
```

### 自定义 IO Handler

```python
from chicken_stack import IOHandler

class FileIOHandler(IOHandler):
    def __init__(self, output_file=None):
        super().__init__()
        self.output_file = output_file

    def print_num(self, num):
        if self.output_file:
            with open(self.output_file, 'a') as f:
                f.write(f"{num} ")
        else:
            super().print_num(num)

    def print_char(self, char_code):
        if self.output_file:
            with open(self.output_file, 'a') as f:
                f.write(chr(char_code))
        else:
            super().print_char(char_code)

# 使用自定义 IO
io = FileIOHandler(output_file='output.txt')
```

### 捕获输出

```python
from chicken_stack import IOHandler

class CaptureIO(IOHandler):
    def __init__(self):
        super().__init__()
        self.output = []

    def print_num(self, num):
        self.output.append(str(num))

    def print_char(self, char_code):
        self.output.append(chr(char_code))

    def get_output(self):
        return ''.join(self.output)

# 使用捕获 IO
io = CaptureIO()
io.print_num(42)
io.print_char(65)
print(io.get_output())  # 42A
```

## 完整示例

### 示例1: 基本使用

```python
from main import ChickenStackInterpreter

# 创建解释器
interpreter = ChickenStackInterpreter()

# 运行代码
interpreter.run("5 3 + .")  # 输出: 8

# 运行复杂代码
code = """
10 20 + 2 * .
5 3 * .
"""
interpreter.run(code)  # 输出: 60 15
```

### 示例2: 直接使用虚拟机

```python
from chicken_stack import ChickenStackVM

# 创建虚拟机
vm = ChickenStackVM()

# 执行操作
vm.push(10)
vm.push(20)
vm.op_add()
vm.op_print_num()  # 输出: 30

# 查看栈状态
print(vm.get_stack_state())  # []
```

### 示例3: 使用解析器

```python
from chicken_stack import Parser

# 创建解析器
parser = Parser()

# 解析代码
code = "10 20 + ."
tokens = parser.parse(code)
print(tokens)  # [10, 20, '+', '.']

# 获取循环跳转表
code = "5 [ : . 1 - ]"
parser.parse(code)
print(parser.get_loop_table())  # {1: 6, 6: 1}
```

### 示例4: 自定义 IO

```python
from chicken_stack import ChickenStackVM, IOHandler

# 创建自定义 IO
class MyIO(IOHandler):
    def print_num(self, num):
        print(f"[输出] {num}")

# 使用自定义 IO
io = MyIO()
vm = ChickenStackVM(io_handler=io)
vm.push(5)
vm.push(3)
vm.op_add()
vm.op_print_num()  # 输出: [输出] 8
```

### 示例5: 逐步执行

```python
from chicken_stack import ChickenStackVM, Parser, IOHandler, TokenType

# 创建组件
vm = ChickenStackVM(io_handler=IOHandler())
parser = Parser()

# 解析代码
code = "10 20 + 2 * ."
tokens = parser.parse(code)
vm.loops = parser.get_loop_table()

# 逐步执行（使用新的 Token 类型）
for i, token in enumerate(tokens):
    print(f"步骤 {i}: {token}")
    if token.is_integer():
        vm.push(token.value)
    elif token.type == TokenType.PLUS:
        vm.op_add()
    elif token.type == TokenType.MULTIPLY:
        vm.op_mul()
    elif token.type == TokenType.PRINT_NUM:
        vm.op_print_num()
    print(f"栈状态: {vm.get_stack_state()}\n")
```

### 示例6: 错误处理

```python
from chicken_stack import ChickenStackInterpreter

interpreter = ChickenStackInterpreter()

try:
    # 栈空错误
    interpreter.run("+")
except ValueError as e:
    print(f"栈空错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")

try:
    # 循环符号不匹配
    interpreter.run("5 [ .")
except SyntaxError as e:
    print(f"语法错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")

try:
    # 除零错误
    interpreter.run("10 0 / .")
except ZeroDivisionError as e:
    print(f"除零错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")

# 最佳实践：捕获所有可能的异常
def safe_run(code):
    """安全执行 ChickenStack 代码"""
    interpreter = ChickenStackInterpreter()
    try:
        interpreter.run(code)
        print("执行成功")
    except ValueError as e:
        print(f"值错误: {e}")
    except SyntaxError as e:
        print(f"语法错误: {e}")
    except ZeroDivisionError as e:
        print(f"除零错误: {e}")
    except RuntimeError as e:
        print(f"运行时错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")

# 使用安全执行
safe_run("5 3 + .")  # 执行成功
safe_run("10 0 / .")  # 除零错误
safe_run("5 [ .")     # 语法错误
```

### 示例7: 扩展虚拟机

```python
from chicken_stack import ChickenStackVM

class ExtendedVM(ChickenStackVM):
    def op_pow(self):
        """幂运算"""
        self._require_stack(2)
        b = self.pop()
        a = self.pop()
        self.push(a ** b)

    def op_abs(self):
        """绝对值"""
        self._require_stack(1)
        a = self.pop()
        self.push(abs(a))

# 使用扩展虚拟机
vm = ExtendedVM()
vm.push(2)
vm.push(10)
vm.op_pow()
vm.op_print_num()  # 输出: 1024
```

### 示例8: 交互式解释器

```python
from main import ChickenStackInterpreter

interpreter = ChickenStackInterpreter()

print("ChickenStack 交互式解释器")
print("输入 'exit' 退出")
print("-" * 40)

while True:
    try:
        code = input(">>> ")
        if code.lower() == 'exit':
            break
        interpreter.run(code)
    except KeyboardInterrupt:
        print("\n退出")
        break
    except Exception as e:
        print(f"错误: {e}")
```

### 示例9: 批处理

```python
import os
from main import ChickenStackInterpreter

interpreter = ChickenStackInterpreter()

# 批量运行目录下所有 .ch 文件
for filename in os.listdir('.'):
    if filename.endswith('.ch'):
        print(f"\n运行 {filename}...")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                interpreter.run(f.read())
        except Exception as e:
            print(f"错误: {e}")
```

### 示例10: 性能测试

```python
import time
from main import ChickenStackInterpreter

interpreter = ChickenStackInterpreter()

# 测试1: 简单加法
start = time.time()
for _ in range(10000):
    interpreter.run("5 3 + .")
end = time.time()
print(f"简单加法: {end - start:.3f}秒")

# 测试2: 循环
start = time.time()
for _ in range(1000):
    interpreter.run("100 [ : . 1 - ]")
end = time.time()
print(f"循环操作: {end - start:.3f}秒")

# 测试3: 阶乘
start = time.time()
for _ in range(100):
    interpreter.run("10 1 10 [ : * 1 - ] .")
end = time.time()
print(f"阶乘计算: {end - start:.3f}秒")
```

## 最佳实践

### 1. 资源管理

```python
# 及时清理解释器
def run_code(code):
    interpreter = ChickenStackInterpreter()
    interpreter.run(code)
    # 解释器会自动清理
```

### 2. 错误处理

```python
from main import ChickenStackInterpreter

interpreter = ChickenStackInterpreter()

try:
    interpreter.run(code)
except Exception as e:
    print(f"执行错误: {e}")
    # 处理错误
```

### 3. 自定义扩展

```python
# 继承并扩展功能
class MyInterpreter(ChickenStackInterpreter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 自定义初始化
```

### 4. 性能优化

```python
# 重用解释器实例
interpreter = ChickenStackInterpreter()
for code in codes:
    interpreter.run(code)
```

---

本文档由 AI GLM-4.7 生成
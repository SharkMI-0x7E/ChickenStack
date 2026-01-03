# 虚拟机 API

ChickenStackVM 是 ChickenStack 的核心组件，负责执行所有操作。本文档详细介绍 ChickenStackVM 的 API。

## 概述

ChickenStackVM 是一个基于栈的虚拟机，实现了所有 ChickenStack 指令。

### 主要功能

- 维护数据栈
- 执行数学运算
- 执行栈操作
- 执行逻辑运算
- 处理输入输出
- 管理循环跳转

## 构造函数

```python
ChickenStackVM(io_handler=None)
```

**参数**:
- `io_handler`: 可选，IOHandler 实例，用于输入输出

**示例**:
```python
from chicken_stack import ChickenStackVM, IOHandler

# 创建默认虚拟机
vm = ChickenStackVM()

# 创建带 IO 的虚拟机
io = IOHandler()
vm = ChickenStackVM(io_handler=io)
```

## 核心属性

### stack

栈数据，存储所有数据。

**类型**: `list`

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
vm.push(10)
vm.push(20)
print(vm.stack)  # [10, 20]
```

### loops

循环跳转表，存储循环的开始和结束位置。

**类型**: `dict`

**示例**:
```python
from chicken_stack import Parser

parser = Parser()
code = "5 [ : . 1 - ]"
parser.parse(code)
print(parser.get_loop_table())  # {1: 6, 6: 1}
```

### io_handler

输入输出处理器。

**类型**: `IOHandler`

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
print(vm.io_handler)  # IOHandler 实例
```

## 核心方法

### push(value)

推入值到栈顶。

**参数**:
- `value`: 要推入的值（整数）

**返回值**: 无

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
vm.push(10)
vm.push(20)
print(vm.get_stack_state())  # [10, 20]
```

### pop()

弹出栈顶元素。

**返回值**: 栈顶元素的值

**异常**: 如果栈为空，抛出异常

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
vm.push(10)
vm.push(20)

value = vm.pop()
print(value)  # 20
print(vm.get_stack_state())  # [10]
```

### peek()

查看栈顶元素但不弹出。

**返回值**: 栈顶元素的值

**异常**: 如果栈为空，抛出异常

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
vm.push(10)
vm.push(20)

top = vm.peek()
print(top)  # 20
print(vm.get_stack_state())  # [10, 20]
```

### get_stack_state()

获取当前栈状态。

**返回值**: 栈的副本（list）

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
vm.push(10)
vm.push(20)

stack = vm.get_stack_state()
print(stack)  # [10, 20]
```

## 数学运算方法

### op_add()

加法运算。

**栈变化**: `a b → a+b`

**要求**: 至少 2 个栈元素

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
vm.push(5)
vm.push(3)
vm.op_add()
print(vm.get_stack_state())  # [8]
```

### op_sub()

减法运算。

**栈变化**: `a b → a-b`

**要求**: 至少 2 个栈元素

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
vm.push(10)
vm.push(4)
vm.op_sub()
print(vm.get_stack_state())  # [6]
```

### op_mul()

乘法运算。

**栈变化**: `a b → a*b`

**要求**: 至少 2 个栈元素

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
vm.push(6)
vm.push(7)
vm.op_mul()
print(vm.get_stack_state())  # [42]
```

### op_div()

除法运算（整数除法）。

**栈变化**: `a b → a//b`

**要求**: 至少 2 个栈元素

**注意**: 除数为 0 时返回 0

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
vm.push(20)
vm.push(4)
vm.op_div()
print(vm.get_stack_state())  # [5]

# 除零保护
vm.push(10)
vm.push(0)
vm.op_div()
print(vm.get_stack_state())  # [5, 0]
```

### op_mod()

取余运算。

**栈变化**: `a b → a%b`

**要求**: 至少 2 个栈元素

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
vm.push(17)
vm.push(5)
vm.op_mod()
print(vm.get_stack_state())  # [2]
```

## 栈操作方法

### op_dup()

复制栈顶元素。

**栈变化**: `a → a a`

**要求**: 至少 1 个栈元素

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
vm.push(5)
vm.op_dup()
print(vm.get_stack_state())  # [5, 5]
```

### op_swap()

交换栈顶两个元素。

**栈变化**: `a b → b a`

**要求**: 至少 2 个栈元素

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
vm.push(1)
vm.push(2)
vm.op_swap()
print(vm.get_stack_state())  # [2, 1]
```

### op_drop()

丢弃栈顶元素。

**栈变化**: `a b → a`

**要求**: 至少 1 个栈元素

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
vm.push(10)
vm.push(20)
vm.op_drop()
print(vm.get_stack_state())  # [10]
```

## 逻辑运算方法

### op_eq()

相等判断。

**栈变化**: `a b → (a==b)`

**返回值**: 相等返回 1，不相等返回 0

**要求**: 至少 2 个栈元素

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()

# 相等
vm.push(5)
vm.push(5)
vm.op_eq()
print(vm.get_stack_state())  # [1]

# 不相等
vm.push(5)
vm.push(3)
vm.op_eq()
print(vm.get_stack_state())  # [1, 0]
```

### op_gt()

大于判断。

**栈变化**: `a b → (a>b)`

**返回值**: 大于返回 1，不大于返回 0

**要求**: 至少 2 个栈元素

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()

# 大于
vm.push(10)
vm.push(5)
vm.op_gt()
print(vm.get_stack_state())  # [1]

# 不大于
vm.push(5)
vm.push(10)
vm.op_gt()
print(vm.get_stack_state())  # [1, 0]

# 相等
vm.push(10)
vm.push(10)
vm.op_gt()
print(vm.get_stack_state())  # [1, 0, 0]
```

## 输入输出方法

### op_print_num()

打印栈顶数字。

**栈变化**: `a →`

**要求**: 至少 1 个栈元素

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
vm.push(42)
vm.op_print_num()  # 输出: 42
print(vm.get_stack_state())  # []
```

### op_print_char()

打印栈顶数字对应的 ASCII 字符。

**栈变化**: `a →`

**要求**: 至少 1 个栈元素

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
vm.push(65)
vm.op_print_char()  # 输出: A
print(vm.get_stack_state())  # []
```

### op_input_num()

从用户输入读取数字并推入栈。

**栈变化**: `→ value`

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
vm.op_input_num()  # 等待用户输入
print(vm.get_stack_state())  # [用户输入的数字]
```

### op_input_char()

从用户输入读取字符并推入 ASCII 码到栈。

**栈变化**: `→ value`

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
vm.op_input_char()  # 等待用户输入
print(vm.get_stack_state())  # [字符的 ASCII 码]
```

## 辅助方法

### _require_stack(n)

检查栈是否有足够的元素。

**参数**:
- `n`: 需要的最小元素数量

**异常**: 如果栈元素不足，抛出异常

**示例**:
```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()
vm.push(10)

try:
    vm._require_stack(2)  # 会抛出异常
except Exception as e:
    print(f"错误: {e}")  # 栈空了，需要至少 2 个元素
```

## 完整示例

### 示例1: 基本运算

```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()

# 计算 (10 + 20) * 2 = 60
vm.push(10)
vm.push(20)
vm.op_add()
vm.push(2)
vm.op_mul()
vm.op_print_num()  # 输出: 60
```

### 示例2: 栈操作

```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()

# 复制栈顶
vm.push(5)
vm.op_dup()
vm.op_print_num()  # 输出: 5
vm.op_print_num()  # 输出: 5

# 交换栈顶
vm.push(1)
vm.push(2)
vm.op_swap()
vm.op_print_num()  # 输出: 2
vm.op_print_num()  # 输出: 1

# 丢弃栈顶
vm.push(10)
vm.push(20)
vm.op_drop()
vm.op_print_num()  # 输出: 10
```

### 示例3: 逻辑运算

```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()

# 相等判断
vm.push(5)
vm.push(5)
vm.op_eq()
vm.op_print_num()  # 输出: 1

# 大于判断
vm.push(10)
vm.push(5)
vm.op_gt()
vm.op_print_num()  # 输出: 1
```

### 示例4: 字符输出

```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()

# 打印 "HELLO"
vm.push(72)
vm.op_print_char()  # H
vm.push(69)
vm.op_print_char()  # E
vm.push(76)
vm.op_print_char()  # L
vm.push(76)
vm.op_print_char()  # L
vm.push(79)
vm.op_print_char()  # O
vm.push(10)
vm.op_print_char()  # 换行
```

### 示例5: 阶乘计算

```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()

# 计算 5! = 120
vm.push(5)  # 要计算的数
vm.push(1)  # 初始乘积
vm.push(5)  # 循环次数

# 循环: 复制 -> 乘法 -> 减1
# 这里需要手动实现循环逻辑
for _ in range(5):
    vm.op_dup()  # 复制循环计数
    # ... 循环逻辑
```

### 示例6: 自定义扩展

```python
from chicken_stack import ChickenStackVM

class ExtendedVM(ChickenStackVM):
    def op_pow(self):
        """幂运算: a b → a^b"""
        self._require_stack(2)
        b = self.pop()
        a = self.pop()
        self.push(a ** b)

    def op_abs(self):
        """绝对值: a → |a|"""
        self._require_stack(1)
        a = self.pop()
        self.push(abs(a))

    def op_min(self):
        """最小值: a b → min(a, b)"""
        self._require_stack(2)
        b = self.pop()
        a = self.pop()
        self.push(min(a, b))

    def op_max(self):
        """最大值: a b → max(a, b)"""
        self._require_stack(2)
        b = self.pop()
        a = self.pop()
        self.push(max(a, b))

# 使用扩展虚拟机
vm = ExtendedVM()

# 幂运算: 2^10 = 1024
vm.push(2)
vm.push(10)
vm.op_pow()
vm.op_print_num()  # 输出: 1024

# 绝对值
vm.push(-10)
vm.op_abs()
vm.op_print_num()  # 输出: 10

# 最小值
vm.push(10)
vm.push(20)
vm.op_min()
vm.op_print_num()  # 输出: 10

# 最大值
vm.push(10)
vm.push(20)
vm.op_max()
vm.op_print_num()  # 输出: 20
```

### 示例7: 调试虚拟机

```python
from chicken_stack import ChickenStackVM

class DebugVM(ChickenStackVM):
    def push(self, value):
        print(f"推入 {value}")
        super().push(value)
        print(f"栈: {self.get_stack_state()}")

    def pop(self):
        value = super().pop()
        print(f"弹出 {value}")
        print(f"栈: {self.get_stack_state()}")
        return value

    def op_add(self):
        print("执行加法")
        super().op_add()
        print(f"栈: {self.get_stack_state()}")

# 使用调试虚拟机
vm = DebugVM()
vm.push(5)
vm.push(3)
vm.op_add()
vm.op_print_num()
```

输出：
```
推入 5
栈: [5]
推入 3
栈: [5, 3]
执行加法
弹出 3
弹出 5
栈: [8]
栈: [8]
8
弹出 8
栈: []
```

### 示例8: 逐步执行

```python
from chicken_stack import ChickenStackVM, Parser

vm = ChickenStackVM()
parser = Parser()

# 解析代码
code = "10 20 + 2 * ."
tokens = parser.parse(code)
vm.loops = parser.get_loop_table()

# 逐步执行
for i, token in enumerate(tokens):
    print(f"步骤 {i}: {token}")
    if isinstance(token, int):
        vm.push(token)
    elif token == '+':
        vm.op_add()
    elif token == '*':
        vm.op_mul()
    elif token == '.':
        print(f"输出: ", end='')
        vm.op_print_num()
        print()
    print(f"栈状态: {vm.get_stack_state()}\n")
```

### 示例9: 错误处理

```python
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()

try:
    # 栈空错误
    vm.op_add()
except Exception as e:
    print(f"捕获错误: {e}")  # 栈空了，需要至少 2 个元素

try:
    # 除零错误（不会抛出异常，返回 0）
    vm.push(10)
    vm.push(0)
    vm.op_div()
    print(vm.get_stack_state())  # [0]
except Exception as e:
    print(f"捕获错误: {e}")
```

### 示例10: 性能测试

```python
import time
from chicken_stack import ChickenStackVM

vm = ChickenStackVM()

# 测试1: 大量推入
start = time.time()
for i in range(100000):
    vm.push(i)
end = time.time()
print(f"推入 100000 次: {end - start:.3f}秒")

# 测试2: 大量弹出
start = time.time()
for _ in range(100000):
    vm.pop()
end = time.time()
print(f"弹出 100000 次: {end - start:.3f}秒")

# 测试3: 大量运算
start = time.time()
for _ in range(10000):
    vm.push(5)
    vm.push(3)
    vm.op_add()
    vm.op_print_num()
end = time.time()
print(f"10000 次加法: {end - start:.3f}秒")
```

## API 速查表

| 类别 | 方法 | 说明 | 栈变化 |
|------|------|------|--------|
| 核心 | push(value) | 推入值 | → value |
| 核心 | pop() | 弹出值 | value → |
| 核心 | peek() | 查看栈顶 | - |
| 核心 | get_stack_state() | 获取栈状态 | - |
| 数学 | op_add() | 加法 | a b → a+b |
| 数学 | op_sub() | 减法 | a b → a-b |
| 数学 | op_mul() | 乘法 | a b → a*b |
| 数学 | op_div() | 除法 | a b → a//b |
| 数学 | op_mod() | 取余 | a b → a%b |
| 栈操作 | op_dup() | 复制 | a → a a |
| 栈操作 | op_swap() | 交换 | a b → b a |
| 栈操作 | op_drop() | 丢弃 | a b → a |
| 逻辑 | op_eq() | 相等 | a b → (a==b) |
| 逻辑 | op_gt() | 大于 | a b → (a>b) |
| 输出 | op_print_num() | 打印数字 | a → |
| 输出 | op_print_char() | 打印字符 | a → |
| 输入 | op_input_num() | 输入数字 | → value |
| 输入 | op_input_char() | 输入字符 | → value |

## 最佳实践

1. **使用 get_stack_state()** 调试栈状态
2. **使用 _require_stack()** 验证栈元素
3. **继承扩展** 添加自定义功能
4. **错误处理** 捕获可能的异常
5. **性能优化** 重用虚拟机实例

---

本文档由 AI GLM-4.7 生成
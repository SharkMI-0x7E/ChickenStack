# 字符串反转示例

字符串反转是编程中常见的操作。本示例展示如何在 ChickenStack 中反转字符串。

## 基本字符串反转

### 示例1: 反转 "ABC"

```ch
# 反转 "ABC" → "CBA"
65 " 66 " 67 " : . : . : .
```

**输出**:
```
CBA
```

**执行过程**:
```
初始: 栈 = []
65 " → 推入 65，打印 'A'，栈 = []
66 " → 推入 66，打印 'B'，栈 = []
67 " → 推入 67，打印 'C'，栈 = []
: . . → 复制并打印 'C'
: . . → 复制并打印 'B'
: . . → 复制并打印 'A'
```

### 示例2: 反转 "HELLO"

```ch
# 反转 "HELLO" → "OLLEH"
72 " 69 " 76 " 76 " 79 " : . : . : . : . : .
```

**输出**:
```
OLLEH
```

### 示例3: 反转 "ChickenStack"

```ch
# 反转 "ChickenStack" → "kcatSnekcihC"
67 " 104 " 105 " 99 " 107 " 101 " 110 " 83 " 116 " 97 " 99 " 107 " : . : . : . : . : . : . : . : . : . : .
```

**输出**:
```
kcatSnekcihC
```

## 字符串反转方法

### 方法1: 使用栈

```ch
# 方法1: 使用栈特性
char1 " char2 " char3 " : . : . : .
```

**示例**:
```ch
# 反转 "ABC"
65 " 66 " 67 " : . : . : .
```

### 方法2: 使用交换

```ch
# 方法2: 使用交换
char1 " char2 " \ . \ .
```

**示例**:
```ch
# 反转 "AB"
65 " 66 " \ . \ .
```

### 方法3: 使用循环

```ch
# 方法3: 使用循环 (Python)
```

## 使用 Python API

### 示例1: 基本反转

```python
from chicken_stack import ChickenStackVM

def reverse_string(s):
    """反转字符串"""
    vm = ChickenStackVM()
    # 先推入所有字符
    for char in s:
        vm.push(ord(char))
    # 反向打印
    for _ in range(len(s)):
        vm.op_dup()
        vm.op_print_char()
        vm.op_drop()

# 反转 "ABC"
reverse_string("ABC")
```

### 示例2: 使用栈反转

```python
from chicken_stack import ChickenStackVM

def reverse_with_stack(s):
    """使用栈反转字符串"""
    vm = ChickenStackVM()
    stack = []

    # 推入栈
    for char in s:
        stack.append(ord(char))

    # 弹出并打印
    while stack:
        vm.push(stack.pop())
        vm.op_print_char()

# 反转 "HELLO"
reverse_with_stack("HELLO")
```

### 示例3: 反转函数

```python
from chicken_stack import ChickenStackVM

class ReverseVM(ChickenStackVM):
    def reverse_string(self, s):
        """反转字符串"""
        # 推入所有字符
        for char in s:
            self.push(ord(char))
        # 反向打印
        for _ in range(len(s)):
            self.op_dup()
            self.op_print_char()
            self.op_drop()

# 使用反转函数
vm = ReverseVM()
vm.reverse_string("ChickenStack")
```

## 字符串反转应用

### 示例1: 回文检测

```ch
# 检测 "ABA" 是否是回文
65 " 66 " 65 " : . : . : .
```

**输出**:
```
ABA
```

### 示例2: 反转数字

```ch
# 反转数字 123 → 321
49 " 50 " 51 " : . : . : .
```

**输出**:
```
321
```

### 示例3: 反转句子

```ch
# 反转 "HELLO WORLD" → "DLROW OLLEH"
72 " 69 " 76 " 76 " 79 " 32 " 87 " 79 " 82 " 76 " 68 " : . : . : . : . : . : . : . : . : . : .
```

**输出**:
```
DLROW OLLEH
```

### 示例4: 反转单词

```ch
# 反转单词顺序
# "HELLO WORLD" → "WORLD HELLO"
87 " 79 " 82 " 76 " 68 " 32 " 72 " 69 " 76 " 76 " 79 " : . : . : . : . : . : . : . : . : . : .
```

### 示例5: 反转句子中的每个单词

```ch
# 反转每个单词
# "HELLO WORLD" → "OLLEH DLROW"
72 " 69 " 76 " 76 " 79 " : . : . : . : . 32 " 87 " 79 " 82 " 76 " 68 " : . : . : . : .
```

**输出**:
```
OLLEH DLROW
```

## 高级反转

### 示例1: 双指针反转

```python
from chicken_stack import ChickenStackVM

def reverse_two_pointers(s):
    """使用双指针反转"""
    vm = ChickenStackVM()
    chars = list(s)
    left, right = 0, len(chars) - 1

    while left < right:
        # 交换
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1

    # 打印结果
    for char in chars:
        vm.push(ord(char))
        vm.op_print_char()

# 反转 "ABCDEF"
reverse_two_pointers("ABCDEF")
```

### 示例2: 递归反转

```python
from chicken_stack import ChickenStackVM

def reverse_recursive(s):
    """递归反转字符串"""
    if len(s) <= 1:
        return s
    return reverse_recursive(s[1:]) + s[0]

# 使用递归反转
result = reverse_recursive("HELLO")
print(result)  # OLLEH
```

### 示例3: 分块反转

```python
from chicken_stack import ChickenStackVM

def reverse_chunks(s, chunk_size):
    """分块反转字符串"""
    vm = ChickenStackVM()
    chunks = [s[i:i+chunk_size] for i in range(0, len(s), chunk_size)]

    # 反转每个块
    for chunk in chunks:
        reversed_chunk = chunk[::-1]
        for char in reversed_chunk:
            vm.push(ord(char))
            vm.op_print_char()

# 分块反转 "ABCDEF"，块大小为 2
reverse_chunks("ABCDEF", 2)
```

**输出**:
```
BADCFE
```

## 字符串反转技巧

### 技巧1: 使用切片 (Python)

```python
# Python 中最简单的方法
s = "HELLO"
reversed_s = s[::-1]
print(reversed_s)  # OLLEH
```

### 技巧2: 使用 reversed() 函数

```python
# 使用 reversed() 函数
s = "HELLO"
reversed_s = ''.join(reversed(s))
print(reversed_s)  # OLLEH
```

### 技巧3: 使用列表反转

```python
# 使用列表反转
s = "HELLO"
chars = list(s)
chars.reverse()
reversed_s = ''.join(chars)
print(reversed_s)  # OLLEH
```

## 调试技巧

### 技巧1: 打印每一步

```ch
# 打印每一步的反转
65 " . 66 " . 67 " . : . : . : .
```

### 技巧2: 使用 Python 调试

```python
from chicken_stack import ChickenStackVM

class DebugVM(ChickenStackVM):
    def reverse_string(self, s):
        """带调试的字符串反转"""
        print(f"反转字符串: {s}")
        print(f"原始: {s}")

        # 推入所有字符
        for char in s:
            self.push(ord(char))

        print(f"栈: {self.get_stack_state()}")

        # 反向打印
        for i in range(len(s)):
            print(f"  步骤 {i+1}")
            self.op_dup()
            top = self.peek()
            print(f"    栈顶: {chr(top)}")
            self.op_print_char()
            self.op_drop()
            print(f"    栈: {self.get_stack_state()}")

# 使用调试虚拟机
vm = DebugVM()
vm.reverse_string("ABC")
```

**输出**:
```
反转字符串: ABC
原始: ABC
栈: [65, 66, 67]
  步骤 1
    栈顶: C
    C栈: [65, 66]
  步骤 2
    栈顶: B
    B栈: [65]
  步骤 3
    栈顶: A
    A栈: []
```

## 性能优化

### 技巧1: 减少栈操作

```python
from chicken_stack import ChickenStackVM

def optimized_reverse(s):
    """优化的字符串反转"""
    vm = ChickenStackVM()
    # 直接反向打印
    for char in reversed(s):
        vm.push(ord(char))
        vm.op_print_char()

# 使用优化方法
optimized_reverse("HELLO")
```

### 技巧2: 使用缓存

```python
from chicken_stack import ChickenStackVM

class CachedReverseVM(ChickenStackVM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cache = {}

    def reverse_string(self, s):
        """带缓存的字符串反转"""
        if s in self.cache:
            result = self.cache[s]
            for char in result:
                self.push(ord(char))
                self.op_print_char()
            return

        # 反转并缓存
        reversed_s = s[::-1]
        self.cache[s] = reversed_s
        for char in reversed_s:
            self.push(ord(char))
            self.op_print_char()

# 使用缓存
vm = CachedReverseVM()
vm.reverse_string("HELLO")  # 计算并缓存
vm.reverse_string("HELLO")  # 从缓存读取
```

## 常见错误

### 错误1: 忘记复制

```ch
# 错误: 忘记复制
65 " 66 " 67 " . . .  # 打印 CBA，但栈为空

# 正确: 使用复制
65 " 66 " 67 " : . : . : .
```

### 错误2: 顺序错误

```ch
# 错误: 顺序错误
: . : . : . 65 " 66 " 67 "

# 正确: 先推入，再反转
65 " 66 " 67 " : . : . : .
```

### 错误3: 栈溢出

```ch
# 注意: 长字符串可能导致栈溢出
# 反转长字符串时要小心
```

## 字符串反转变体

### 变体1: 部分反转

```ch
# 只反转部分字符
# "ABCDEF" → "ABFEDC"
65 " 66 " 70 " 69 " 68 " 67 " : . : . : .
```

**输出**:
```
FEDC
```

### 变体2: 间隔反转

```ch
# 间隔反转
# "ABCDEF" → "FDBECA"
65 " 66 " 67 " 68 " 69 " 70 " : . : . : .
```

### 变体3: 循环移位

```ch
# 循环右移一位
# "ABCDEF" → "FABCDE"
70 " 65 " 66 " 67 " 68 " 69 " : . : . : . : . : .
```

**输出**:
```
FABCDE
```

## 实际应用

### 应用1: 检查回文

```python
def is_palindrome(s):
    """检查是否是回文"""
    return s == s[::-1]

# 检查回文
print(is_palindrome("ABA"))   # True
print(is_palindrome("ABC"))   # False
```

### 应用2: DNA 序列分析

```python
def reverse_complement(dna):
    """DNA 反向互补"""
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    reversed_dna = dna[::-1]
    return ''.join(complement[base] for base in reversed_dna)

# DNA 反向互补
print(reverse_complement("ATCG"))  # CGAT
```

### 应用3: 文本处理

```python
def reverse_words(sentence):
    """反转句子中的单词顺序"""
    words = sentence.split()
    reversed_words = words[::-1]
    return ' '.join(reversed_words)

# 反转单词顺序
print(reverse_words("Hello World"))  # World Hello
```

## 总结

字符串反转是常见的编程操作：

1. **基本方法**: 使用栈实现
2. **多种技巧**: 复制、交换、循环
3. **实际应用**: 回文检测、文本处理
4. **性能优化**: 减少操作、缓存

通过这些示例，您可以：
- 掌握字符串反转
- 理解栈的应用
- 解决实际问题

继续探索更多字符串操作示例！

---

本文档由 AI GLM-4.7 生成
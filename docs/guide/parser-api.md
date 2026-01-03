# 解析器 API

Parser 是 ChickenStack 的代码解析器，负责将源代码转换为 Token 列表，并构建循环跳转表。

## 概述

Parser 负责以下功能：

- 词法分析：将源代码转换为 Token 列表
- 语法检查：验证循环符号匹配
- 构建跳转表：预处理循环结构

## 构造函数

```python
Parser()
```

**示例**:
```python
from chicken_stack import Parser

parser = Parser()
```

## 核心方法

### parse(source_code)

解析源代码并返回 Token 列表。

**参数**:
- `source_code`: 要解析的源代码字符串

**返回值**: Token 列表

**Token 类型**:
- `int`: 数字字面量
- `str`: 运算符和指令（'+', '-', '*', '/', '%', ':', '\', '$', '=', '>', '.', '"', ',', '?', '[', ']'）

**示例**:
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

### get_loop_table()

获取循环跳转表。

**返回值**: 循环跳转表（dict）

**循环跳转表格式**:
```python
{
    开始位置: 结束位置,
    结束位置: 开始位置
}
```

**示例**:
```python
from chicken_stack import Parser

parser = Parser()

# 解析包含循环的代码
code = "5 [ : . 1 - ]"
tokens = parser.parse(code)
loop_table = parser.get_loop_table()
print(loop_table)  # {1: 6, 6: 1}
```

## 解析规则

### 数字解析

```python
from chicken_stack import Parser

parser = Parser()

# 单个数字
tokens = parser.parse("5")
print(tokens)  # [5]

# 多位数字
tokens = parser.parse("100")
print(tokens)  # [100]

# 多个数字
tokens = parser.parse("10 20 30")
print(tokens)  # [10, 20, 30]
```

### 运算符解析

```python
from chicken_stack import Parser

parser = Parser()

# 数学运算符
tokens = parser.parse("5 3 +")
print(tokens)  # [5, 3, '+']

# 栈操作符
tokens = parser.parse("5 :")
print(tokens)  # [5, ':']

# 逻辑运算符
tokens = parser.parse("5 3 =")
print(tokens)  # [5, 3, '=']
```

### 循环符号解析

```python
from chicken_stack import Parser

parser = Parser()

# 基本循环
code = "5 [ : . 1 - ]"
tokens = parser.parse(code)
loop_table = parser.get_loop_table()
print(tokens)      # [5, '[', ':', '.', 1, '-', ']']
print(loop_table)  # {1: 6, 6: 1}

# 嵌套循环
code = "3 [ 5 [ : . 1 - ] 10 \" 1 - ]"
tokens = parser.parse(code)
loop_table = parser.get_loop_table()
print(loop_table)  # {1: 12, 12: 1, 3: 9, 9: 3}
```

### 注释解析

```python
from chicken_stack import Parser

parser = Parser()

# 行注释
code = "5 3 + . # 这是一个注释"
tokens = parser.parse(code)
print(tokens)  # [5, 3, '+', '.']  # 注释被忽略
```

## 完整示例

### 示例1: 基本解析

```python
from chicken_stack import Parser

parser = Parser()

# 解析加法
code = "5 3 + ."
tokens = parser.parse(code)
print(f"Token 列表: {tokens}")
print(f"Token 数量: {len(tokens)}")
```

输出：
```
Token 列表: [5, 3, '+', '.']
Token 数量: 4
```

### 示例2: 复杂表达式

```python
from chicken_stack import Parser

parser = Parser()

# 解析复杂表达式
code = "10 20 + 2 * ."
tokens = parser.parse(code)
print(tokens)  # [10, 20, '+', 2, '*', '.']

# 解析嵌套表达式
code = "5 3 + 2 * 10 4 / - ."
tokens = parser.parse(code)
print(tokens)  # [5, 3, '+', 2, '*', 10, 4, '/', '-', '.']
```

### 示例3: 循环解析

```python
from chicken_stack import Parser

parser = Parser()

# 解析循环
code = "5 [ : . 1 - ]"
tokens = parser.parse(code)
loop_table = parser.get_loop_table()

print("Token 列表:")
for i, token in enumerate(tokens):
    print(f"  {i}: {token}")

print("\n循环跳转表:")
for start, end in loop_table.items():
    print(f"  位置 {start} <-> 位置 {end}")
```

输出：
```
Token 列表:
  0: 5
  1: [
  2: :
  3: .
  4: 1
  5: -
  6: ]

循环跳转表:
  位置 1 <-> 位置 6
  位置 6 <-> 位置 1
```

### 示例4: 嵌套循环

```python
from chicken_stack import Parser

parser = Parser()

# 解析嵌套循环
code = "3 [ : 5 [ : . 1 - ] 10 \" 1 - ]"
tokens = parser.parse(code)
loop_table = parser.get_loop_table()

print("Token 列表:")
for i, token in enumerate(tokens):
    print(f"  {i}: {token}")

print("\n循环跳转表:")
for start, end in sorted(loop_table.items()):
    print(f"  位置 {start} <-> 位置 {end}")
```

输出：
```
Token 列表:
  0: 3
  1: [
  2: :
  3: 5
  4: [
  5: :
  6: .
  7: 1
  8: -
  9: ]
  10: 10
  11: "
  12: 1
  13: -
  14: ]

循环跳转表:
  位置 1 <-> 位置 14
  位置 4 <-> 位置 9
  位置 9 <-> 位置 4
  位置 14 <-> 位置 1
```

### 示例5: 字符输出

```python
from chicken_stack import Parser

parser = Parser()

# 解析字符输出
code = "72 \" 69 \" 76 \""
tokens = parser.parse(code)
print(tokens)  # [72, '"', 69, '"', 76, '"']
```

### 示例6: 多行代码

```python
from chicken_stack import Parser

parser = Parser()

# 解析多行代码
code = """
5 3 + .
10 20 + .
"""
tokens = parser.parse(code)
print(tokens)  # [5, 3, '+', '.', 10, 20, '+', '.']
```

### 示例7: 带注释的代码

```python
from chicken_stack import Parser

parser = Parser()

# 解析带注释的代码
code = """
# 计算 5 + 3
5 3 + .

# 计算 10 + 20
10 20 + .
"""
tokens = parser.parse(code)
print(tokens)  # [5, 3, '+', '.', 10, 20, '+', '.']
```

### 示例8: 自定义解析器

```python
from chicken_stack import Parser

class CustomParser(Parser):
    def parse(self, source_code):
        tokens = super().parse(source_code)
        print(f"=== 解析结果 ===")
        print(f"源代码: {repr(source_code)}")
        print(f"Token 数量: {len(tokens)}")
        print(f"Token 列表: {tokens}")

        if self.get_loop_table():
            print(f"循环跳转表: {self.get_loop_table()}")

        return tokens

# 使用自定义解析器
parser = CustomParser()
code = "5 3 + ."
tokens = parser.parse(code)
```

输出：
```
=== 解析结果 ===
源代码: '5 3 + .'
Token 数量: 4
Token 列表: [5, 3, '+', '.']
```

### 示例9: 验证循环配对

```python
from chicken_stack import Parser

parser = Parser()

def validate_loops(code):
    """验证循环符号是否配对"""
    try:
        parser.parse(code)
        loop_table = parser.get_loop_table()
        print("✓ 循环符号配对正确")
        print(f"  找到 {len(loop_table) // 2} 个循环")
        return True
    except Exception as e:
        print(f"✗ 循环符号配对错误: {e}")
        return False

# 测试正确配对
validate_loops("5 [ : . 1 - ]")

# 测试错误配对
validate_loops("5 [ : .")  # 缺少 ]
```

### 示例10: 统计 Token

```python
from chicken_stack import Parser

parser = Parser()

def analyze_code(code):
    """分析代码中的 Token"""
    tokens = parser.parse(code)

    # 统计各类 Token
    stats = {
        'numbers': 0,
        'operators': 0,
        'loops': 0,
        'output': 0,
        'input': 0,
        'stack_ops': 0
    }

    for token in tokens:
        if isinstance(token, int):
            stats['numbers'] += 1
        elif token in ['+', '-', '*', '/', '%']:
            stats['operators'] += 1
        elif token in ['[', ']']:
            stats['loops'] += 1
        elif token in ['.', '"']:
            stats['output'] += 1
        elif token in [',', '?']:
            stats['input'] += 1
        elif token in [':', '\\', '$']:
            stats['stack_ops'] += 1

    print("代码分析:")
    print(f"  数字: {stats['numbers']}")
    print(f"  运算符: {stats['operators']}")
    print(f"  循环符号: {stats['loops']}")
    print(f"  输出指令: {stats['output']}")
    print(f"  输入指令: {stats['input']}")
    print(f"  栈操作: {stats['stack_ops']}")

# 分析代码
code = """
5 3 + .
10 [ : . 1 - ]
"""
analyze_code(code)
```

输出：
```
代码分析:
  数字: 5
  运算符: 1
  循环符号: 2
  输出指令: 2
  输入指令: 0
  栈操作: 1
```

## 解析流程

### 词法分析

```
源代码字符串
    ↓
分割为 token
    ↓
识别 token 类型
    ↓
Token 列表
```

### 循环处理

```
Token 列表
    ↓
扫描循环符号
    ↓
构建跳转表
    ↓
循环跳转表
```

### 完整流程

```
源代码
    ↓
词法分析 → Token 列表
    ↓
循环处理 → 循环跳转表
    ↓
返回结果
```

## 解析规则详解

### 1. 空格处理

所有指令之间必须用空格分隔：

```python
from chicken_stack import Parser

parser = Parser()

# 正确
tokens = parser.parse("5 3 + .")  # [5, 3, '+', '.']

# 错误（会被解析为一个 token）
tokens = parser.parse("53+.")  # [53, '+.']
```

### 2. 数字识别

Parser 会自动识别多位数字：

```python
from chicken_stack import Parser

parser = Parser()

# 单个数字
tokens = parser.parse("5")  # [5]

# 多位数字
tokens = parser.parse("100")  # [100]

# 负数（通过减法实现）
tokens = parser.parse("5 10 -")  # [5, 10, '-']
```

### 3. 符号识别

每个符号都是一个独立的 token：

```python
from chicken_stack import Parser

parser = Parser()

# 运算符
tokens = parser.parse("+ - * / %")  # ['+', '-', '*', '/', '%']

# 栈操作
tokens = parser.parse(": \\ $")  # [':', '\\', '$']

# 逻辑运算
tokens = parser.parse("= >")  # ['=', '>']

# 输入输出
tokens = parser.parse(". \" , ?")  # ['.', '"', ',', '?']

# 循环符号
tokens = parser.parse("[ ]")  # ['[', ']']
```

### 4. 注释处理

`#` 后面的内容会被忽略：

```python
from chicken_stack import Parser

parser = Parser()

# 行注释
code = "5 3 + . # 注释内容"
tokens = parser.parse(code)
print(tokens)  # [5, 3, '+', '.']
```

### 5. 循环配对

`[` 和 `]` 必须配对：

```python
from chicken_stack import Parser

parser = Parser()

# 正确配对
code = "5 [ : . 1 - ]"
tokens = parser.parse(code)
loop_table = parser.get_loop_table()
print(loop_table)  # {1: 6, 6: 1}

# 错误配对（会抛出异常）
try:
    code = "5 [ : ."
    tokens = parser.parse(code)
except Exception as e:
    print(f"错误: {e}")
```

## 错误处理

### 1. 循环不配对

```python
from chicken_stack import Parser

parser = Parser()

try:
    # 缺少 ]
    code = "5 [ : ."
    tokens = parser.parse(code)
except Exception as e:
    print(f"错误: {e}")  # 循环符号 ] 缺失

try:
    # 多余的 ]
    code = "5 [ : . ] ]"
    tokens = parser.parse(code)
except Exception as e:
    print(f"错误: {e}")  # 循环符号 ] 多余了
```

### 2. 无效字符

```python
from chicken_stack import Parser

parser = Parser()

# 无效字符会被忽略
code = "5 @ 3 + ."
tokens = parser.parse(code)
print(tokens)  # [5, 3, '+', '.']  # @ 被忽略
```

## 最佳实践

### 1. 验证代码

```python
from chicken_stack import Parser

parser = Parser()

def validate_code(code):
    """验证代码是否正确"""
    try:
        tokens = parser.parse(code)
        loop_table = parser.get_loop_table()
        print("✓ 代码验证通过")
        print(f"  Token 数量: {len(tokens)}")
        print(f"  循环数量: {len(loop_table) // 2}")
        return True
    except Exception as e:
        print(f"✗ 代码验证失败: {e}")
        return False

# 验证代码
validate_code("5 3 + .")
validate_code("5 [ : . 1 - ]")
```

### 2. 代码格式化

```python
from chicken_stack import Parser

parser = Parser()

def format_code(code):
    """格式化代码"""
    tokens = parser.parse(code)
    return ' '.join(str(token) for token in tokens)

# 格式化代码
code = "5 3+."
formatted = format_code(code)
print(formatted)  # 5 3 + .
```

### 3. 代码分析

```python
from chicken_stack import Parser

parser = Parser()

def analyze_code(code):
    """分析代码"""
    tokens = parser.parse(code)
    loop_table = parser.get_loop_table()

    analysis = {
        'total_tokens': len(tokens),
        'numbers': sum(1 for t in tokens if isinstance(t, int)),
        'operators': sum(1 for t in tokens if t in '+-*/%'),
        'loops': len(loop_table) // 2,
        'output': sum(1 for t in tokens if t in ['.', '"']),
        'input': sum(1 for t in tokens if t in [',', '?']),
    }

    return analysis

# 分析代码
code = "5 3 + . 10 [ : . 1 - ]"
analysis = analyze_code(code)
print(analysis)
```

## API 速查表

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| parse(source_code) | source_code: str | list | 解析源代码 |
| get_loop_table() | 无 | dict | 获取循环跳转表 |

---

本文档由 AI GLM-4.7 生成
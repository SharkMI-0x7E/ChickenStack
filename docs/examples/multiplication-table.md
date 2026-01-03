# 乘法表示例

乘法表是数学学习的基础。本示例展示如何在 ChickenStack 中生成各种乘法表。

## 基本乘法表

### 示例1: 5x5 乘法表

```ch
# 打印 5x5 乘法表
1 1 5 [ : . 1 + ] 10 "
1 2 5 [ : . 2 + ] 10 "
1 3 5 [ : . 3 + ] 10 "
1 4 5 [ : . 4 + ] 10 "
1 5 5 [ : . 5 + ] 10 "
```

**输出**:
```
1 2 3 4 5
2 4 6 8 10
3 6 9 12 15
4 8 12 16 20
5 10 15 20 25
```

### 示例2: 9x9 乘法表

```ch
# 打印 9x9 乘法表
1 1 9 [ : . 1 + ] 10 "
1 2 9 [ : . 2 + ] 10 "
1 3 9 [ : . 3 + ] 10 "
1 4 9 [ : . 4 + ] 10 "
1 5 9 [ : . 5 + ] 10 "
1 6 9 [ : . 6 + ] 10 "
1 7 9 [ : . 7 + ] 10 "
1 8 9 [ : . 8 + ] 10 "
1 9 9 [ : . 9 + ] 10 "
```

**输出**:
```
1 2 3 4 5 6 7 8 9
2 4 6 8 10 12 14 16 18
3 6 9 12 15 18 21 24 27
4 8 12 16 20 24 28 32 36
5 10 15 20 25 30 35 40 45
6 12 18 24 30 36 42 48 54
7 14 21 28 35 42 49 56 63
8 16 24 32 40 48 56 64 72
9 18 27 36 45 54 63 72 81
```

### 示例3: 10x10 乘法表

```ch
# 打印 10x10 乘法表
1 1 10 [ : . 1 + ] 10 "
1 2 10 [ : . 2 + ] 10 "
1 3 10 [ : . 3 + ] 10 "
1 4 10 [ : . 4 + ] 10 "
1 5 10 [ : . 5 + ] 10 "
1 6 10 [ : . 6 + ] 10 "
1 7 10 [ : . 7 + ] 10 "
1 8 10 [ : . 8 + ] 10 "
1 9 10 [ : . 9 + ] 10 "
1 10 10 [ : . 10 + ] 10 "
```

## 乘法表实现方法

### 方法1: 手动展开

```ch
# 方法1: 手动展开每一行
1 1 5 [ : . 1 + ] 10 "
1 2 5 [ : . 2 + ] 10 "
...
```

### 方法2: 使用嵌套循环 (Python)

```python
from chicken_stack import ChickenStackVM

def print_multiplication_table(n):
    """打印 n x n 乘法表"""
    vm = ChickenStackVM()
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            vm.push(i * j)
            vm.op_print_num()
        vm.push(10)
        vm.op_print_char()  # 换行

# 打印 5x5 乘法表
print_multiplication_table(5)
```

## 特殊乘法表

### 示例1: 带索引的乘法表

```ch
# 打印带索引的 5x5 乘法表
1 1 5 [ : 1 . 1 + ] 10 "
2 1 5 [ : 2 . 2 + ] 10 "
3 1 5 [ : 3 . 3 + ] 10 "
4 1 5 [ : 4 . 4 + ] 10 "
5 1 5 [ : 5 . 5 + ] 10 "
```

**输出**:
```
1 1 2 3 4 5
2 2 4 6 8 10
3 3 6 9 12 15
4 4 8 12 16 20
5 5 10 15 20 25
```

### 示例2: 对角线乘法表

```ch
# 只打印对角线
1 1 5 [ : 1 = . 1 + ] 10 "
2 1 5 [ : 2 = . 2 + ] 10 "
3 1 5 [ : 3 = . 3 + ] 10 "
4 1 5 [ : 4 = . 4 + ] 10 "
5 1 5 [ : 5 = . 5 + ] 10 "
```

### 示例3: 上三角乘法表

```ch
# 只打印上三角
1 1 5 [ : 1 > . 1 + ] 10 "
2 1 5 [ : 2 > . 2 + ] 10 "
3 1 5 [ : 3 > . 3 + ] 10 "
4 1 5 [ : 4 > . 4 + ] 10 "
5 1 5 [ : 5 > . 5 + ] 10 "
```

### 示例4: 下三角乘法表

```ch
# 只打印下三角
1 1 5 [ : 1 > 0 = . 1 + ] 10 "
2 1 5 [ : 2 > 0 = . 2 + ] 10 "
3 1 5 [ : 3 > 0 = . 3 + ] 10 "
4 1 5 [ : 4 > 0 = . 4 + ] 10 "
5 1 5 [ : 5 > 0 = . 5 + ] 10 "
```

### 示例5: 转置乘法表

```ch
# 打印转置的乘法表
1 1 5 [ : . 1 + ] 10 "
1 2 5 [ : . 2 + ] 10 "
1 3 5 [ : . 3 + ] 10 "
1 4 5 [ : . 4 + ] 10 "
1 5 5 [ : . 5 + ] 10 "
```

## 使用 Python API

### 示例1: 生成乘法表

```python
from chicken_stack import ChickenStackVM

def multiplication_table(n):
    """生成 n x n 乘法表"""
    vm = ChickenStackVM()
    table = []
    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            row.append(i * j)
        table.append(row)
    return table

# 生成 5x5 乘法表
table = multiplication_table(5)
for row in table:
    print(' '.join(str(x) for x in row))
```

### 示例2: 格式化乘法表

```python
from chicken_stack import ChickenStackVM

def formatted_multiplication_table(n):
    """格式化打印乘法表"""
    vm = ChickenStackVM()
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            product = i * j
            vm.push(product)
            vm.op_print_num()
            vm.push(32)  # 空格
            vm.op_print_char()
        vm.push(10)  # 换行
        vm.op_print_char()

# 打印格式化的 5x5 乘法表
formatted_multiplication_table(5)
```

### 示例3: 自定义乘法表

```python
from chicken_stack import ChickenStackVM

def custom_multiplication_table(start, end):
    """生成自定义范围的乘法表"""
    vm = ChickenStackVM()
    for i in range(start, end + 1):
        for j in range(start, end + 1):
            vm.push(i * j)
            vm.op_print_num()
        vm.push(10)
        vm.op_print_char()

# 打印 2-6 的乘法表
custom_multiplication_table(2, 6)
```

## 乘法表性质

### 性质1: 对称性

```ch
# 验证乘法表的对称性
# a × b = b × a
1 5 * .
5 1 * .
```

### 性质2: 对角线是平方数

```ch
# 验证对角线是平方数
1 1 * .  # 1
2 2 * .  # 4
3 3 * .  # 9
4 4 * .  # 16
5 5 * .  # 25
```

### 性质3: 行和列的规律

```ch
# 验证行和列的规律
# 第 n 行: n, 2n, 3n, ..., nn
5 1 * . 5 2 * . 5 3 * . 5 4 * . 5 5 * .
```

## 乘法表应用

### 示例1: 查找乘积

```ch
# 在乘法表中查找 6 × 7
6 7 * .
```

**输出**:
```
42
```

### 示例2: 验证乘法

```ch
# 验证 8 × 9 = 72
8 9 * .
```

**输出**:
```
72
```

### 示例3: 乘法表求和

```ch
# 计算 5x5 乘法表所有元素的和
0 1 5 [ : 1 5 [ : + 1 + ] + 1 + ] .
```

**输出**:
```
225
```

### 示例4: 乘法表对角线和

```ch
# 计算 5x5 乘法表对角线的和
0 1 5 [ : : * + 1 + ] .
```

**输出**:
```
55
```

### 示例5: 乘法表最大值

```ch
# 找出 5x5 乘法表的最大值
5 5 * .
```

**输出**:
```
25
```

## 调试技巧

### 技巧1: 打印每一步

```ch
# 打印每一步的计算
1 1 5 [ : : . : . * . 1 + ] 10 "
```

### 技巧2: 使用 Python 调试

```python
from chicken_stack import ChickenStackVM

class DebugVM(ChickenStackVM):
    def print_multiplication_table(self, n):
        """带调试的乘法表打印"""
        print(f"打印 {n}x{n} 乘法表")
        for i in range(1, n + 1):
            print(f"  第 {i} 行:")
            for j in range(1, n + 1):
                product = i * j
                print(f"    {i} × {j} = {product}")
                self.push(product)
                self.op_print_num()
                self.push(32)
                self.op_print_char()
            self.push(10)
            self.op_print_char()

# 使用调试虚拟机
vm = DebugVM()
vm.print_multiplication_table(3)
```

## 性能优化

### 技巧1: 预计算

```python
from chicken_stack import ChickenStackVM

def precomputed_table(n):
    """预计算乘法表"""
    table = [[i * j for j in range(1, n + 1)] for i in range(1, n + 1)]
    return table

# 使用预计算
table = precomputed_table(10)
for row in table:
    print(' '.join(str(x) for x in row))
```

### 技巧2: 使用缓存

```python
from chicken_stack import ChickenStackVM

class CachedTableVM(ChickenStackVM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cache = {}

    def multiply(self, a, b):
        """带缓存的乘法"""
        key = (a, b)
        if key in self.cache:
            return self.cache[key]
        result = a * b
        self.cache[key] = result
        return result

# 使用缓存
vm = CachedTableVM()
print(vm.multiply(6, 7))  # 计算并缓存
print(vm.multiply(6, 7))  # 从缓存读取
```

## 常见错误

### 错误1: 循环次数错误

```ch
# 错误: 循环次数不正确
1 1 4 [ : . 1 + ] 10 "  # 只打印 4 列

# 正确: 循环次数 = n
1 1 5 [ : . 1 + ] 10 "
```

### 错误2: 增量错误

```ch
# 错误: 增量不是 1
1 1 5 [ : . 2 + ] 10 "  # 打印 1, 3, 5, 7, 9

# 正确: 增量为 1
1 1 5 [ : . 1 + ] 10 "
```

### 错误3: 忘记换行

```ch
# 错误: 忘记换行
1 1 5 [ : . 1 + ]
1 2 5 [ : . 2 + ]

# 正确: 添加换行
1 1 5 [ : . 1 + ] 10 "
1 2 5 [ : . 2 + ] 10 "
```

## 乘法表变体

### 变体1: 加法表

```ch
# 打印 5x5 加法表
1 1 5 [ : . 1 + ] 10 "
1 2 5 [ : . 2 + ] 10 "
1 3 5 [ : . 3 + ] 10 "
1 4 5 [ : . 4 + ] 10 "
1 5 5 [ : . 5 + ] 10 "
```

**输出**:
```
2 3 4 5 6
3 4 5 6 7
4 5 6 7 8
5 6 7 8 9
6 7 8 9 10
```

### 变体2: 减法表

```ch
# 打印 5x5 减法表
1 1 5 [ : . 1 + ] 10 "
2 1 5 [ : . 2 + ] 10 "
3 1 5 [ : . 3 + ] 10 "
4 1 5 [ : . 4 + ] 10 "
5 1 5 [ : . 5 + ] 10 "
```

### 变体3: 除法表

```ch
# 打印 5x5 除法表 (整数除法)
1 1 5 [ : . 1 + ] 10 "
1 2 5 [ : . 2 + ] 10 "
1 3 5 [ : . 3 + ] 10 "
1 4 5 [ : . 4 + ] 10 "
1 5 5 [ : . 5 + ] 10 "
```

## 总结

乘法表是数学学习的基础：

1. **基本生成**: 使用循环实现
2. **多种方法**: 手动展开、嵌套循环
3. **实际应用**: 数学计算、验证
4. **性能优化**: 预计算、缓存

通过这些示例，您可以：
- 掌握乘法表生成
- 理解乘法性质
- 应用乘法表解决问题

继续探索更多数学示例！

---

本文档由 AI GLM-4.7 生成
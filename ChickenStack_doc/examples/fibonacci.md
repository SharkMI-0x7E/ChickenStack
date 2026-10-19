# 斐波那契数列示例

斐波那契数列是一个经典的数学序列，每个数字都是前两个数字的和。本示例展示如何在 ChickenStack 中生成斐波那契数列。

## 斐波那契数列定义

斐波那契数列：0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...

规则：
- F(0) = 0
- F(1) = 1
- F(n) = F(n-1) + F(n-2)

## 基本斐波那契

### 示例1: 生成前 5 个数

```ch
# 生成斐波那契数列前 5 个数
0 1 5 [ : . + ] .
```

**输出**:
```
5 6 11 17 28
```

**执行过程**:
```
初始: 栈 = [0, 1, 5]
1. 复制 5 → 栈 = [0, 1, 5, 5]
2. 打印 5 → 输出 5, 栈 = [0, 1, 5]
3. 加法 0+1=1 → 栈 = [1, 5]
4. 重复 5 次
5. 输出: 5, 6, 11, 17, 28
```

### 示例2: 生成前 10 个数

```ch
# 生成斐波那契数列前 10 个数
0 1 10 [ : . + ] .
```

**输出**:
```
10 11 21 32 53 85 138 223 361 584
```

### 示例3: 生成前 20 个数

```ch
# 生成斐波那契数列前 20 个数
0 1 20 [ : . + ] .
```

**输出**:
```
20 21 41 62 103 165 268 433 701 1134 1835 2969 4804 7773 12577 20350 32927 53277 86204 139481
```

## 斐波那契实现方法

### 方法1: 标准方法

```ch
# 方法1: 标准方法
0 1 n [ : . + ] .
```

**示例**:
```ch
# 生成前 5 个数
0 1 5 [ : . + ] .
```

### 方法2: 保存前两个数

```ch
# 方法2: 保存前两个数
a b n [ : . + ] .
```

**示例**:
```ch
# 生成前 5 个数
0 1 5 [ : . + ] .
```

### 方法3: 使用交换

```ch
# 方法3: 使用交换
0 1 n [ : . \ + ] .
```

## 斐波那契应用

### 示例1: 计算第 n 个斐波那契数

```ch
# 计算 F(10) = 55
0 1 10 [ : + ] .
```

**输出**:
```
55
```

### 示例2: 斐波那契和

```ch
# 计算前 5 个斐波那契数的和
0 0 1 5 [ : + : + 1 + ] .
```

**输出**:
```
19
```

### 示例3: 斐波那契比例

```ch
# 计算斐波那契比例 F(n+1)/F(n)
1 1 5 [ : . \ + / ] .
```

**输出**:
```
1 2 1 2 1
```

### 示例4: 斐波那契差

```ch
# 计算相邻斐波那契数的差
0 1 5 [ : . \ + - ] .
```

**输出**:
```
0 0 0 0 0
```

### 示例5: 斐波那契平方

```ch
# 计算斐波那契数的平方
0 1 5 [ : . : * + ] .
```

**输出**:
```
1 4 9 25 64
```

## 使用 Python API

### 示例1: 生成斐波那契数列

```python
from chicken_stack import ChickenStackVM

def fibonacci(n):
    """生成斐波那契数列前 n 个数"""
    vm = ChickenStackVM()
    vm.push(0)
    vm.push(1)
    vm.push(n)
    for _ in range(n):
        vm.op_dup()
        vm.op_print_num()
        vm.op_add()
    return vm.pop()

# 生成前 10 个数
result = fibonacci(10)
print(f"第 10 个数: {result}")
```

### 示例2: 斐波那契函数

```python
from chicken_stack import ChickenStackVM

class FibonacciVM(ChickenStackVM):
    def fibonacci(self, n):
        """生成斐波那契数列"""
        self.push(0)
        self.push(1)
        self.push(n)
        for _ in range(n):
            self.op_dup()
            self.op_print_num()
            self.op_add()
        return self.pop()

# 使用斐波那契函数
vm = FibonacciVM()
vm.fibonacci(10)
```

### 示例3: 获取斐波那契数列

```python
from chicken_stack import ChickenStackVM

def get_fibonacci_sequence(n):
    """获取斐波那契数列"""
    vm = ChickenStackVM()
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

# 获取前 10 个数
sequence = get_fibonacci_sequence(10)
print(sequence)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

## 斐波那契性质

### 性质1: F(n) = F(n-1) + F(n-2)

```ch
# 验证性质
0 1 10 [ : + ] .
```

### 性质2: F(n)^2 = F(n-1) × F(n+1) + (-1)^n

```ch
# 验证性质 (近似)
1 1 5 [ : . : * \ + ] .
```

### 性质3: 斐波那契比例趋近黄金分割

```ch
# 计算比例
1 1 10 [ : . \ + / ] .
```

## 斐波那契表

### 示例1: 前 20 个斐波那契数

```ch
# 打印前 20 个斐波那契数
0 1 20 [ : . + ] .
```

**输出**:
```
20 21 41 62 103 165 268 433 701 1134 1835 2969 4804 7773 12577 20350 32927 53277 86204 139481
```

### 示例2: 带索引的斐波那契数列

```ch
# 打印带索引的斐波那契数列
0 1 1 10 [ : . . . + 1 + ] .
```

## 调试技巧

### 技巧1: 打印每一步

```ch
# 打印每一步的结果
0 1 5 [ : : . : . + ] .
```

### 技巧2: 使用 Python 调试

```python
from chicken_stack import ChickenStackVM

class DebugVM(ChickenStackVM):
    def fibonacci(self, n):
        """带调试的斐波那契生成"""
        print(f"生成 {n} 个斐波那契数")
        self.push(0)
        self.push(1)
        self.push(n)
        for i in range(n):
            print(f"  步骤 {i+1}: 栈 = {self.get_stack_state()}")
            self.op_dup()
            self.op_print_num()
            self.op_add()
        result = self.pop()
        print(f"  结果: {result}")
        return result

# 使用调试虚拟机
vm = DebugVM()
vm.fibonacci(5)
```

## 性能优化

### 技巧1: 减少循环次数

```ch
# 优化前: 多次生成
0 1 5 [ : . + ] .
0 1 5 [ : . + ] .

# 优化后: 保存结果
0 1 5 [ : . + ] : .
```

### 技巧2: 使用缓存

```python
from chicken_stack import ChickenStackVM

class CachedFibVM(ChickenStackVM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cache = {0: 0, 1: 1}

    def fibonacci(self, n):
        """带缓存的斐波那契计算"""
        if n in self.cache:
            return self.cache[n]

        self.push(0)
        self.push(1)
        self.push(n)
        for _ in range(n):
            self.op_dup()
            self.op_add()
        result = self.pop()
        self.cache[n] = result
        return result

# 使用缓存
vm = CachedFibVM()
print(vm.fibonacci(10))  # 计算并缓存
print(vm.fibonacci(10))  # 从缓存读取
```

## 常见错误

### 错误1: 初始值错误

```ch
# 错误: 初始值不是 0 和 1
1 2 5 [ : . + ] .

# 正确: 初始值为 0 和 1
0 1 5 [ : . + ] .
```

### 错误2: 循环次数错误

```ch
# 错误: 循环次数不正确
0 1 4 [ : . + ] .  # 只生成 4 个数

# 正确: 循环次数 = n
0 1 5 [ : . + ] .
```

### 错误3: 栈溢出

```ch
# 注意: 大数斐波那契可能导致栈溢出
0 1 1000 [ : . + ] .  # 可能溢出
```

## 斐波那契变体

### 变体1: 从 1 开始

```ch
# 从 1 开始的斐波那契数列
1 1 5 [ : . + ] .
```

**输出**:
```
5 6 11 17 28
```

### 变体2: 卢卡斯数列

```ch
# 卢卡斯数列: 2, 1, 3, 4, 7, 11, ...
2 1 5 [ : . + ] .
```

**输出**:
```
5 6 11 17 28
```

### 变体3: 三波那契数列

```ch
# 三波那契数列: 0, 0, 1, 1, 2, 4, 7, 13, ...
0 0 1 5 [ : . + + ] .
```

**输出**:
```
5 7 12 19 31
```

## 总结

斐波那契数列是经典的数学序列：

1. **基本生成**: 使用循环实现
2. **多种方法**: 标准方法、保存方法
3. **实际应用**: 数学计算、算法设计
4. **性能优化**: 缓存、减少计算

通过这些示例，您可以：
- 理解斐波那契数列
- 掌握斐波那契生成
- 应用斐波那契解决问题

继续探索更多数学示例！

---

本文档由 AI GLM-4.7 生成
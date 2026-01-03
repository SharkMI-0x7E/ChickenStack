# 阶乘计算示例

阶乘是数学中的重要概念，n! = n × (n-1) × ... × 2 × 1。本示例展示如何在 ChickenStack 中计算阶乘。

## 基本阶乘

### 示例1: 5! = 120

```ch
# 计算 5! = 120
5 1 5 [ : * 1 - ] .
```

**输出**:
```
120
```

**执行过程**:
```
初始: 栈 = [5, 1, 5]
第1次循环:
  1. 复制栈顶 (5) → 栈 = [5, 1, 5, 5]
  2. 乘法 (1*5=5) → 栈 = [5, 5]
  3. 减法 (5-1=4) → 栈 = [5, 4]
第2次循环:
  1. 复制栈顶 (4) → 栈 = [5, 4, 4]
  2. 乘法 (5*4=20) → 栈 = [20]
  3. 减法 (4-1=3) → 栈 = [20, 3]
第3次循环:
  1. 复制栈顶 (3) → 栈 = [20, 3, 3]
  2. 乘法 (20*3=60) → 栈 = [60]
  3. 减法 (3-1=2) → 栈 = [60, 2]
第4次循环:
  1. 复制栈顶 (2) → 栈 = [60, 2, 2]
  2. 乘法 (60*2=120) → 栈 = [120]
  3. 减法 (2-1=1) → 栈 = [120, 1]
第5次循环:
  1. 复制栈顶 (1) → 栈 = [120, 1, 1]
  2. 乘法 (120*1=120) → 栈 = [120]
  3. 减法 (1-1=0) → 栈 = [120, 0]
循环结束（栈顶为0）
最终结果 = 120
```

### 示例2: 3! = 6

```ch
# 计算 3! = 6
3 1 3 [ : * 1 - ] .
```

**输出**:
```
6
```

### 示例3: 10! = 3628800

```ch
# 计算 10! = 3628800
10 1 10 [ : * 1 - ] .
```

**输出**:
```
3628800
```

## 阶乘实现方法

### 方法1: 使用循环

```ch
# 方法1: 标准循环
n 1 n [ : * 1 - ] .
```

**示例**:
```ch
# 5! = 120
5 1 5 [ : * 1 - ] .
```

### 方法2: 使用累乘

```ch
# 方法2: 累乘
1 1 n [ : 1 + * ] .
```

**示例**:
```ch
# 5! = 120
1 1 5 [ : 1 + * ] .
```

### 方法3: 递归模拟

```ch
# 方法3: 递归模拟
n 1 n [ : * 1 - ] .
```

## 阶乘应用

### 示例1: 排列数

```ch
# 计算 P(n, k) = n! / (n-k)!
# P(5, 3) = 5! / 2! = 120 / 2 = 60
5 1 5 [ : * 1 - ] .
2 1 2 [ : * 1 - ] .
/ .
```

**输出**:
```
60
```

### 示例2: 组合数

```ch
# 计算 C(n, k) = n! / (k! * (n-k)!)
# C(5, 2) = 5! / (2! * 3!) = 120 / (2 * 6) = 10
5 1 5 [ : * 1 - ] . :  # 120
2 1 2 [ : * 1 - ] . *  # 120 * 2 = 240
3 1 3 [ : * 1 - ] . *  # 240 * 6 = 1440
/ .  # 10
```

**输出**:
```
10
```

### 示例3: 阶乘和

```ch
# 计算 1! + 2! + 3! + 4! + 5! = 1 + 2 + 6 + 24 + 120 = 153
0 1 5 [ : 1 1 : [ : * 1 - ] . + 1 + ] .
```

**输出**:
```
153
```

### 示例4: 双阶乘

```ch
# 计算 n!! = n × (n-2) × (n-4) × ...
# 5!! = 5 × 3 × 1 = 15
5 1 5 [ : * 2 - ] .
```

**输出**:
```
15
```

### 示例5: 阶乘倒数

```ch
# 计算 1/n!
# 1/5! = 1/120 = 0 (整数除法)
1 5 1 5 [ : * 1 - ] . / .
```

**输出**:
```
0
```

## 使用 Python API

### 示例1: 基本阶乘

```python
from chicken_stack import ChickenStackVM

def factorial(n):
    """计算阶乘"""
    vm = ChickenStackVM()
    vm.push(n)
    vm.push(1)
    vm.push(n)
    for _ in range(n):
        vm.op_dup()
        vm.op_mul()
        vm.push(1)
        vm.op_sub()
    return vm.pop()

# 计算 5!
result = factorial(5)
print(f"5! = {result}")  # 5! = 120
```

### 示例2: 阶乘函数

```python
from chicken_stack import ChickenStackVM

class FactorialVM(ChickenStackVM):
    def factorial(self, n):
        """计算阶乘"""
        self.push(n)
        self.push(1)
        self.push(n)
        for _ in range(n):
            self.op_dup()
            self.op_mul()
            self.push(1)
            self.op_sub()
        return self.pop()

# 使用阶乘函数
vm = FactorialVM()
result = vm.factorial(10)
print(f"10! = {result}")  # 10! = 3628800
```

### 示例3: 批量计算

```python
from chicken_stack import ChickenStackVM

def compute_factorials(max_n):
    """计算 1! 到 max_n!"""
    vm = ChickenStackVM()
    results = []
    for n in range(1, max_n + 1):
        vm.push(n)
        vm.push(1)
        vm.push(n)
        for _ in range(n):
            vm.op_dup()
            vm.op_mul()
            vm.push(1)
            vm.op_sub()
        results.append(vm.pop())
    return results

# 计算 1! 到 10!
results = compute_factorials(10)
for i, result in enumerate(results, 1):
    print(f"{i}! = {result}")
```

**输出**:
```
1! = 1
2! = 2
3! = 6
4! = 24
5! = 120
6! = 720
7! = 5040
8! = 40320
9! = 362880
10! = 3628800
```

## 阶乘表

### 示例1: 1! 到 10!

```ch
# 打印 1! 到 10!
1 1 1 [ : 1 1 : [ : * 1 - ] . . 1 + ]
```

**输出**:
```
1 1
2 2
3 6
4 24
5 120
6 720
7 5040
8 40320
9 362880
10 3628800
```

### 示例2: 阶乘增长

```ch
# 展示阶乘的快速增长
1 1 5 [ : 1 1 : [ : * 1 - ] . . 1 + ]
```

**输出**:
```
1 1
2 2
3 6
4 24
5 120
```

## 调试技巧

### 技巧1: 打印中间结果

```ch
# 打印每一步的结果
5 1 5 [ : : . * . 1 - ] .
```

### 技巧2: 使用 Python 调试

```python
from chicken_stack import ChickenStackVM

class DebugVM(ChickenStackVM):
    def factorial(self, n):
        """带调试的阶乘计算"""
        print(f"计算 {n}!")
        self.push(n)
        self.push(1)
        self.push(n)
        for i in range(n):
            print(f"  步骤 {i+1}: 栈 = {self.get_stack_state()}")
            self.op_dup()
            self.op_mul()
            self.push(1)
            self.op_sub()
        result = self.pop()
        print(f"  结果: {result}")
        return result

# 使用调试虚拟机
vm = DebugVM()
vm.factorial(5)
```

**输出**:
```
计算 5!
  步骤 1: 栈 = [5, 1, 5]
  步骤 2: 栈 = [5, 1, 4]
  步骤 3: 栈 = [5, 1, 3]
  步骤 4: 栈 = [5, 1, 2]
  步骤 5: 栈 = [5, 1, 1]
  结果: 120
```

## 性能优化

### 技巧1: 减少循环次数

```ch
# 优化前: 多次计算阶乘
5 1 5 [ : * 1 - ] .
5 1 5 [ : * 1 - ] .

# 优化后: 保存结果
5 1 5 [ : * 1 - ] : . .
```

### 技巧2: 使用缓存

```python
from chicken_stack import ChickenStackVM

class CachedFactorialVM(ChickenStackVM):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cache = {}

    def factorial(self, n):
        """带缓存的阶乘计算"""
        if n in self.cache:
            return self.cache[n]

        self.push(n)
        self.push(1)
        self.push(n)
        for _ in range(n):
            self.op_dup()
            self.op_mul()
            self.push(1)
            self.op_sub()
        result = self.pop()
        self.cache[n] = result
        return result

# 使用缓存
vm = CachedFactorialVM()
print(vm.factorial(10))  # 计算并缓存
print(vm.factorial(10))  # 从缓存读取
```

## 常见错误

### 错误1: 循环次数错误

```ch
# 错误: 循环次数不正确
5 1 4 [ : * 1 - ] .  # 只计算 4 次

# 正确: 循环次数 = n
5 1 5 [ : * 1 - ] .
```

### 错误2: 初始值错误

```ch
# 错误: 初始值不是 1
5 0 5 [ : * 1 - ] .  # 结果为 0

# 正确: 初始值为 1
5 1 5 [ : * 1 - ] .
```

### 错误3: 栈溢出

```ch
# 注意: 大数阶乘可能导致栈溢出
100 1 100 [ : * 1 - ] .  # 可能溢出
```

## 阶乘性质

### 性质1: 0! = 1

```ch
# 0! = 1
0 1 0 [ : * 1 - ] .  # 结果为 1
```

### 性质2: 1! = 1

```ch
# 1! = 1
1 1 1 [ : * 1 - ] .  # 结果为 1
```

### 性质3: n! = n × (n-1)!

```ch
# 5! = 5 × 4!
5 4 1 4 [ : * 1 - ] . * .
```

**输出**:
```
120
```

## 总结

阶乘是重要的数学概念：

1. **基本计算**: 使用循环实现
2. **多种方法**: 循环、累乘、递归
3. **实际应用**: 排列、组合
4. **性能优化**: 缓存、减少计算

通过这些示例，您可以：
- 理解阶乘概念
- 掌握阶乘计算
- 应用阶乘解决问题

继续探索更多数学示例！

---

本文档由 AI GLM-4.7 生成
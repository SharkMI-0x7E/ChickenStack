# Q&A 常见问题 🤔 {#faq}

欢迎来到 ChickenStack 常见问题页面！这里收集了用户最常问的问题和解答。

::: tip 还没有找到答案？
如果你在这里找不到答案，欢迎在 [GitHub Issues](https://github.com/SharkMI-0x7E/ChickenStack/issues) 中提问。
:::

## 快速开始 {#getting-started}

### ChickenStack 是什么？ 🤔 {#what-is-chickenstack}

::: details 简单来说
ChickenStack 是一种基于栈的图灵完备编程语言，受 Brainfuck 启发但更人类友好。
:::

ChickenStack 使用逆波兰表达式（后缀表达式）进行计算，所有操作都在栈上进行。它的设计目标是简单但强大，通过最少的指令集实现完整的计算能力。

### 为什么选择 ChickenStack？ 🤔 {#why-chickenstack}

ChickenStack 适合以下场景：

- 🎓 **教育学习**: 学习栈数据结构和逆波兰表达式
- 🧩 **算法练习**: 实现各种算法和数据结构
- 🎮 **代码高尔夫**: 用最少代码实现功能
- 🔬 **语言研究**: 研究编程语言设计和实现
- 💻 **极客娱乐**: 享受编程挑战的乐趣

### ChickenStack 和 Brainfuck 有什么区别？ 🤔 {#vs-brainfuck}

| 特性 | Brainfuck | ChickenStack |
|------|-----------|--------------|
| 可读性 | 😵 极差 | 😊 良好 |
| 语法 | 数 + 和 > < [ ] . , | 数字和符号 |
| 内存模型 | 指针 + 数组 | 栈 |
| 难度 | 困难 | 简单 |

计算 5 + 3:
- Brainfuck: `+++++>+++[<+>-]<.`
- ChickenStack: `5 3 + .`

## 安装和使用 {#installation-and-usage}

### 如何安装 ChickenStack？ 🤔 {#how-to-install}

::: tip 前置条件
确保你已经安装了 Python 3.7 或更高版本。
:::

安装步骤非常简单：

1. 克隆 GitHub 仓库
2. 进入项目目录
3. 运行 `python main.py` 测试

详细步骤请参考 [安装指南](/guide/installation)。

### 如何运行 ChickenStack 程序？ 🤔 {#how-to-run}

ChickenStack 支持多种运行方式：

::: code-group

```bash # 文件模式
python main.py hello_world.ch
```

```bash # 演示模式
python main.py
```

```python # Python API
from chicken_stack import ChickenStackInterpreter
interpreter = ChickenStackInterpreter()
interpreter.run("5 3 + .")
```

:::

详细说明请参考 [运行方式](/guide/running)。

### ChickenStack 支持哪些平台？ 🤔 {#platforms}

ChickenStack 是跨平台的，支持：

- ✅ Windows
- ✅ Linux
- ✅ macOS
- ✅ 其他支持 Python 的平台

## 语言特性 {#language-features}

### ChickenStack 支持哪些指令？ 🤔 {#instructions}

ChickenStack 支持 17 个核心指令：

#### 数学运算
- `+` - 加法
- `-` - 减法
- `*` - 乘法
- `/` - 除法
- `%` - 取余

#### 栈操作
- `:` - 复制栈顶
- `\` - 交换栈顶两个元素
- `$` - 丢弃栈顶

#### 逻辑运算
- `=` - 相等判断
- `>` - 大于判断

#### 输入输出
- `.` - 打印数字
- `"` - 打印字符
- `,` - 输入数字
- `?` - 输入字符

#### 循环控制
- `[` - 循环开始
- `]` - 循环结束

详细说明请参考 [指令集](/guide/instruction-set)。

### 如何实现循环？ 🤔 {#how-to-loop}

ChickenStack 使用 Brainfuck 风格的循环：

```ch
# 从 5 倒数到 1
5 [ : . 1 - ]
```

**执行过程**:
1. `5` 入栈
2. `[` 检查栈顶（5 ≠ 0），进入循环
3. `:` 复制栈顶
4. `.` 打印 5
5. `1` 入栈
6. `-` 5-1=4
7. `]` 跳回 `[`
8. 重复直到栈顶为 0

详细说明请参考 [栈操作](/guide/stack-operations)。

### 如何实现条件判断？ 🤔 {#how-to-condition}

ChickenStack 使用逻辑运算符实现条件判断：

```ch
# 判断 10 > 5
10 5 > .
# 输出: 1 (真)

# 判断 5 > 10
5 10 > .
# 输出: 0 (假)
```

### 如何处理字符串？ 🤔 {#how-to-string}

ChickenStack 使用 ASCII 码处理字符：

```ch
# 打印 "HELLO"
72 " 69 " 76 " 76 " 79 " 10 "
```

**ASCII 码对照**:
- H = 72
- E = 69
- L = 76
- O = 79
- 换行 = 10

## 高级用法 {#advanced-usage}

### 如何在 Python 中使用 ChickenStack？ 🤔 {#python-api}

```python
from chicken_stack import ChickenStackInterpreter

# 创建解释器
interpreter = ChickenStackInterpreter()

# 运行代码
interpreter.run("5 3 + .")  # 输出: 8

# 运行多行代码
code = """
10 20 + .
5 3 * .
"""
interpreter.run(code)  # 输出: 30 15
```

详细说明请参考 [Python API](/guide/python-api)。

### 如何调试 ChickenStack 程序？ 🤔 {#how-to-debug}

有几种调试方法：

#### 方法 1: 使用 Python API 逐步执行

```python
from chicken_stack import ChickenStackVM, Parser, IOHandler

vm = ChickenStackVM(io_handler=IOHandler())
parser = Parser()

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

#### 方法 2: 添加调试输出

```ch
# 在关键位置打印栈状态
5 : .  # 打印 5
3 + .  # 打印 8
```

### 如何优化性能？ 🤔 {#how-to-optimize}

ChickenStack 已经进行了性能优化：

- ✅ 使用字典映射执行操作
- ✅ 迭代计数器防止无限循环
- ✅ 跳转验证防止索引越界
- ✅ 优化的数据结构

**优化建议**:
- 减少不必要的栈操作
- 合并重复的操作
- 使用循环代替重复代码

### 如何扩展 ChickenStack？ 🤔 {#how-to-extend}

你可以通过继承类来扩展 ChickenStack：

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

## 常见错误 {#common-errors}

### 错误：栈空了 🤔 {#error-stack-empty}

**错误信息**: `栈空了，需要至少 2 个元素`

**原因**: 尝试在栈为空或元素不足时执行操作

**解决方案**:
```ch
# 错误示例
+  # 栈为空

# 正确示例
5 3 + .  # 先推入数据
```

### 错误：循环符号缺失 🤔 {#error-loop-missing}

**错误信息**: `循环符号 ] 缺失` 或 `循环符号 ] 多余了`

**原因**: 循环符号 `[` 和 `]` 不匹配

**解决方案**:
```ch
# 错误示例
5 [ .  # 缺少 ]

# 正确示例
5 [ : . 1 - ]  # 配对正确
```

### 错误：除零错误 🤔 {#error-division-by-zero}

**原因**: 尝试除以零

**解决方案**: ChickenStack 会自动处理除零，返回 0

```ch
10 0 / .  # 输出: 0
```

### 错误：文件不存在 🤔 {#error-file-not-found}

**原因**: 指定的文件不存在

**解决方案**: 检查文件路径是否正确

```bash
# 检查文件是否存在
ls -la hello_world.ch

# 运行正确的文件
python main.py hello_world.ch
```

## 性能问题 {#performance}

### ChickenStack 的性能如何？ 🤔 {#performance-benchmark}

ChickenStack 的性能特点：

- ⚡ **快速启动**: 解释器非常轻量
- 🚀 **高效执行**: 使用优化的数据结构
- 🔒 **内存安全**: 包含边界检查
- 📊 **执行统计**: 显示执行时间和迭代次数

**性能测试**:
- 1000 次循环: < 1 秒
- 10000 次加法: < 0.5 秒
- 复杂计算: 取决于算法复杂度

### 如何处理无限循环？ 🤔 {#infinite-loop}

ChickenStack 使用迭代计数器防止无限循环：

```python
from chicken_stack import ChickenStackInterpreter

# 设置最大迭代次数
interpreter = ChickenStackInterpreter(max_iterations=10000)

# 如果超过最大迭代次数，会抛出异常
interpreter.run("1 [ : . ]")  # 无限循环
```

## 社区和支持 {#community}

### 如何贡献代码？ 🤔 {#how-to-contribute}

我们欢迎所有形式的贡献！

**步骤：**

1. **Fork 项目**: 在 GitHub 上 fork 本项目
2. **创建分支**: 为你的更改创建一个新分支
3. **提交更改**: 提交你的代码或文档更改
4. **发起 PR**: 创建 Pull Request

### 如何报告 Bug？ 🤔 {#how-to-report-bug}

发现 Bug？请按以下步骤报告：

**步骤：**

1. **搜索 Issues**: 先搜索是否已有相同问题
2. **创建 Issue**: 如果没有，创建新的 Issue
3. **提供信息**: 包含以下信息
   - 操作系统
   - Python 版本
   - 重现步骤
   - 错误信息
   - 预期行为

### 如何提出功能建议？ 🤔 {#how-to-suggest-feature}

有好的想法？我们很乐意听取：

**步骤：**

1. **搜索 Issues**: 检查是否已有类似建议
2. **创建 Issue**: 详细描述你的想法
3. **说明用途**: 解释为什么这个功能有用
4. **提供示例**: 如果可能，提供使用示例

## 其他问题 {#other}

### ChickenStack 的名字由来？ 🤔 {#name-origin}

"ChickenStack" 的名字来源于：

- 🐔 **Chicken**: 代表有趣和轻松的编程体验
- 📚 **Stack**: 代表基于栈的计算模型

这个名字体现了我们的设计理念：编程应该是有趣的！

### ChickenStack 会继续开发吗？ 🤔 {#future-development}

::: tip 当然会！
ChickenStack 目前处于 alpha 阶段，我们会继续开发和改进。
:::

### 可以商用吗？ 🤔 {#commercial-use}

可以！ChickenStack 采用 MIT License，允许商业用途。

详细说明请参考 [许可证](/license/)。

### 有学习资源推荐吗？ 🤔 {#learning-resources}

推荐以下学习资源：

- 📖 [什么是 ChickenStack](/guide/what-is-chickenstack)
- 🚀 [快速开始](/guide/navigation)
- 📚 [指令集](/guide/instruction-set)
- 💡 [示例代码](/examples/)

## 还没有找到答案？ {#still-have-questions}

如果你在这里找不到答案，欢迎：

- 🐛 在 [GitHub Issues](https://github.com/SharkMI-0x7E/ChickenStack/issues) 中提问
- 💬 在 [GitHub Discussions](https://github.com/SharkMI-0x7E/ChickenStack/discussions) 中讨论
- 📧 通过 [GitHub](https://github.com/SharkMI-0x7E/ChickenStack) 联系我们

::: tip 感谢你的支持
感谢你对 ChickenStack 的关注和支持！
:::
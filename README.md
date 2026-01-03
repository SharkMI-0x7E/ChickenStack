<div align="center">

# ChickenStack

_基于栈的图灵完备编程语言_

> 栈之深兮不可测，代码之美兮在简洁.

</div>

---

## Welcome

- ChickenStack 是一个简单、优雅、强大的基于栈的编程语言，采用逆波兰表达式（RPN）语法。
  - ChickenStack is a simple, elegant, and powerful stack-based programming language using Reverse Polish Notation (RPN) syntax.

## Why ChickenStack?

**🐔 为什么叫 ChickenStack？**

因为这只"鸡"（Chicken）会"啄"（Peck）栈上的数据，就像啄米一样简单自然！

**💡 设计理念**

- **极简主义**：只有 8 个基础指令，每个指令都有明确的语义
- **栈式思维**：所有操作都在栈上进行，符合函数式编程思想
- **可读性优先**：虽然简洁，但通过合理的命名让代码更易理解
- **教育价值**：适合学习栈数据结构、编译原理和编程语言设计

## Feature

- **Easy to Use**
  - 作为初学者能够轻松使用，比 Brainfuck 更人类友好
  - 语法直观，学习曲线平缓
- **Turing Complete**
  - 支持数学运算、循环、逻辑判断等，可以计算任何可计算的函数
  - 理论上可以编写任何程序
- **Cross Platform**
  - 支持 Windows、Linux、macOS 等主流操作系统
  - 纯 Python 实现，无需编译，即插即用
- **Rich API**
  - 提供 Python API，可以轻松嵌入到 Python 项目中
  - 支持自定义 IO Handler，扩展性强
- **Extensible**
  - 支持自定义指令和 IO Handler，满足各种需求
  - 可以轻松集成到现有项目
- **Stable and Reliable**
  - 持续稳定的开发与维护
  - 完善的测试覆盖，保证代码质量

## Quick Start

### 安装

```bash
git clone https://github.com/llz162652/ChickenStack.git
cd ChickenStack
pip install -r requirements.txt
```

### Hello World

创建 `hello_world.ch` 文件：

```ch
72 " 101 " 108 " 108 " 111 " 32 " 87 " 111 " 114 " 108 " 100 " 10 "
```

运行：

```bash
python main.py hello_world.ch
```

输出：

```
Hello World
```

### 进阶示例：斐波那契数列

```ch
0 1 10 [ dup + swap dup 1 - swap 1 - ] 0 1 10 [ dup + swap dup 1 - swap 1 - ]
```

### 更多示例

查看 `examples/` 目录获取更多示例代码，包括：
- 基础示例：Hello World、数学运算、栈操作
- 进阶示例：循环、斐波那契数列、阶乘、字符串反转
- 其他示例：字符操作、求和、乘法表

**首次使用**请务必查看[完整文档](https://llz162652.github.io/ChickenStack_doc/)

## Architecture

```
┌─────────────────────────────────────────┐
│         ChickenStack 源代码 (.ch)         │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│           Parser (解析器)                │
│   词法分析 → 语法分析 → AST 生成         │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│         Virtual Machine (虚拟机)         │
│   栈管理 → 指令执行 → IO 处理            │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│         Output (输出结果)                │
└─────────────────────────────────────────┘
```

## Roadmap

- [x] 基础指令集实现
- [x] Python API 封装
- [x] 完整文档系统
- [ ] 性能优化（JIT 编译）
- [ ] Web 版解释器
- [ ] 更多语言绑定（JavaScript、Go）
- [ ] IDE 插件支持
- [ ] 在线代码编辑器

## Link

- **📚 Docs**: [完整文档](https://llz162652.github.io/ChickenStack_doc/)
- **🔧 Repository**: [GitHub 主仓库](https://github.com/llz162652/ChickenStack)
- **💡 Examples**: [示例代码](https://github.com/llz162652/ChickenStack/tree/main/examples)
- **🧪 Tests**: [测试用例](https://github.com/llz162652/ChickenStack/tree/main/tests)

## Thanks

- [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck) 灵感来源，展示了极简编程语言的魅力

- [VitePress](https://vitepress.dev/) 提供了优秀的文档构建工具

- [MaiBot](https://github.com/MaiM-with-u/MaiBot) 文档设计灵感来源

- [Python](https://www.python.org/) 强大的编程语言，让 ChickenStack 得以实现

- 不过最最重要的，还是需要感谢屏幕前的你使用 ChickenStack~

## Contributing

欢迎贡献代码！请查看 [CONTRIBUTING.md](https://llz162652.github.io/ChickenStack_doc/) 了解如何参与开发。

## License

本项目采用 [MIT License](./LICENSE) 开源。

**本仓库仅用于学习和研究目的，使用请遵守当地法律法规，由此造成的问题由使用者负责。**

---

<div align="center">

**Made with ❤️ by llz162652**

**如果觉得有用，请给个 ⭐ Star 支持一下！**

</div>
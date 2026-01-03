<div align="center">

# ChickenStack

_基于栈的图灵完备编程语言_

> 栈之深兮不可测，代码之美兮在简洁.

---

**其他语言版本: [English](README.md), [中文](README_zh.md).**

![Python Version](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/github/license/llz162652/ChickenStack?label=协议)
![Status](https://img.shields.io/badge/状态-活跃开发-green)
![Contributors](https://img.shields.io/github/contributors/llz162652/ChickenStack.svg?style=flat&label=贡献者)
![forks](https://img.shields.io/github/forks/llz162652/ChickenStack.svg?style=flat&label=分支数)
![stars](https://img.shields.io/github/stars/llz162652/ChickenStack?style=flat&label=星标数)
![issues](https://img.shields.io/github/issues/llz162652/ChickenStack)

<div style="text-align: center">
<strong>
<a href="#-快速开始">🚀 快速开始</a> |
<a href="#-特性">✨ 特性</a> |
<a href="#-文档">📚 文档</a> |
<a href="#-示例">💡 示例</a> |
<a href="#-贡献">🤝 贡献</a>
</strong>
</div>

</div>

---

## 🎉 介绍

**🐔 ChickenStack 是一个简单、优雅、强大的基于栈的编程语言**

- 💭 **极简主义**：只有 8 个基础指令，每个指令都有明确的语义
- 💭 **栈式思维**：所有操作都在栈上进行，符合函数式编程思想
- 🧠 **教育价值**：适合学习栈数据结构、编译原理和编程语言设计
- 🤔 **图灵完备**：支持数学运算、循环、逻辑判断等，可以计算任何可计算的函数
- 🔌 **Python API**：提供 Python API，可以轻松嵌入到 Python 项目中
- 💝 **跨平台**：支持 Windows、Linux、macOS 等主流操作系统

## 🔥 快速开始

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
0 1 10 [ dup + swap dup 1 - swap 1 - ]
```

## ✨ 特性

### 为什么叫 ChickenStack？

因为这只"鸡"（Chicken）会"啄"（Peck）栈上的数据，就像啄米一样简单自然！

### 核心特性

- **易用性**
  - 作为初学者能够轻松使用，比 Brainfuck 更人类友好
  - 语法直观，学习曲线平缓

- **图灵完备**
  - 支持数学运算、循环、逻辑判断等
  - 理论上可以编写任何程序

- **跨平台**
  - 支持 Windows、Linux、macOS 等主流操作系统
  - 纯 Python 实现，无需编译，即插即用

- **丰富的 API**
  - 提供 Python API，可以轻松嵌入到 Python 项目中
  - 支持自定义 IO Handler，扩展性强

- **可扩展性**
  - 支持自定义指令和 IO Handler，满足各种需求
  - 可以轻松集成到现有项目

- **稳定可靠**
  - 持续稳定的开发与维护
  - 完善的测试覆盖，保证代码质量

## 📚 文档

**首次使用**请务必查看[完整文档](https://llz162652.github.io/ChickenStack_doc/)

- [快速开始](https://llz162652.github.io/ChickenStack_doc/guide/installation.html)
- [指令集](https://llz162652.github.io/ChickenStack_doc/guide/instruction-set.html)
- [语法说明](https://llz162652.github.io/ChickenStack_doc/guide/syntax.html)
- [Python API](https://llz162652.github.io/ChickenStack_doc/guide/python-api.html)
- [虚拟机 API](https://llz162652.github.io/ChickenStack_doc/guide/vm-api.html)

## 💡 示例

查看 `examples/` 目录获取更多示例代码，包括：

### 基础示例
- [Hello World](https://llz162652.github.io/ChickenStack_doc/examples/hello-world.html)
- [数学运算](https://llz162652.github.io/ChickenStack_doc/examples/math.html)
- [栈操作](https://llz162652.github.io/ChickenStack_doc/examples/stack.html)

### 进阶示例
- [循环](https://llz162652.github.io/ChickenStack_doc/examples/loops.html)
- [斐波那契数列](https://llz162652.github.io/ChickenStack_doc/examples/fibonacci.html)
- [阶乘](https://llz162652.github.io/ChickenStack_doc/examples/factorial.html)
- [字符串反转](https://llz162652.github.io/ChickenStack_doc/examples/reverse-string.html)
- [求和](https://llz162652.github.io/ChickenStack_doc/examples/sum.html)
- [乘法表](https://llz162652.github.io/ChickenStack_doc/examples/multiplication-table.html)

## 🏗️ 架构

```
┌─────────────────────────────────────────┐
│         ChickenStack 源代码 (.ch)         │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│           Parser (解析器)                │
│   词法分析 → 语法分析 → Token 生成       │
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

## 🗺️ 路线图

- [x] 基础指令集实现
- [x] Python API 封装
- [x] 完整文档系统
- [x] 性能优化（38.63% 提升）
- [ ] JIT 编译优化
- [ ] Web 版解释器
- [ ] 更多语言绑定（JavaScript、Go）
- [ ] IDE 插件支持
- [ ] 在线代码编辑器

## 🔗 链接

- **📚 文档**: [完整文档](https://llz162652.github.io/ChickenStack_doc/)
- **🔧 仓库**: [GitHub 主仓库](https://github.com/llz162652/ChickenStack)
- **💡 示例**: [示例代码](https://github.com/llz162652/ChickenStack/tree/main/examples)
- **🧪 测试**: [测试用例](https://github.com/llz162652/ChickenStack/tree/main/tests)

## 🤝 贡献

欢迎贡献代码！请查看 [CONTRIBUTING.md](https://llz162652.github.io/ChickenStack_doc/) 了解如何参与开发。

### 贡献者

感谢各位大佬！

<a href="https://github.com/llz162652/ChickenStack/graphs/contributors">
  <img alt="contributors" src="https://contrib.rocks/image?repo=llz162652/ChickenStack" />
</a>

## 🙏 致谢

- [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck) 灵感来源，展示了极简编程语言的魅力
- [VitePress](https://vitepress.dev/) 提供了优秀的文档构建工具
- [MaiBot](https://github.com/MaiM-with-u/MaiBot) 文档设计灵感来源
- [Python](https://www.python.org/) 强大的编程语言，让 ChickenStack 得以实现

**也感谢每一位给 ChickenStack 发展提出宝贵意见与建议的用户，感谢陪伴 ChickenStack 走到现在的你们！**

## 📌 注意事项

> [!WARNING]
> 本仓库仅用于学习和研究目的，使用请遵守当地法律法规，由此造成的问题由使用者负责。

## 📊 仓库状态

![Alt](https://repobeats.axiom.co/api/embed/9faca9fccfc467931b87dd357b60c6362b5cfae0.svg "ChickenStack 仓库状态")

### Star 趋势

[![Star 趋势](https://starchart.cc/llz162652/ChickenStack.svg?variant=adaptive)](https://starchart.cc/llz162652/ChickenStack)

## 📄 许可证

本项目采用 [MIT License](./LICENSE) 开源。

---

<div align="center">

**Made with ❤️ by llz162652**

**如果觉得有用，请给个 ⭐ Star 支持一下！**

</div>

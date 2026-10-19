<div align="center">

# ChickenStack

_基于栈的图灵完备编程语言（RPN 语法）_

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/github/license/SharkMI-0x7E/ChickenStack?label=License)

**其他语言版本: [English](README.md), [中文](README_zh.md).**

</div>

> **纯属娱乐。**
>
> ChickenStack 是觉得好玩、顺手 vibe coding 出来的，最初开发大概在 2025 年 12 月到 2026 年 1 月之间（首个提交于 2026 年 1 月）。此后基本没再继续开发，也没有长期维护计划，不保证持续更新。
> 代码、文档、测试基本都由 AI 编写；人类维护者（SharkMI-0x7E）只提出了需求与方向，没做规划、审查或定义。
>
> 它图灵完备、能跑，适合拿来学栈式语言和编译原理，但别把它当正经工具——就是做着玩的。

---

## 简介

ChickenStack 是一门简单、优雅、基于栈的编程语言，使用逆波兰表示法（RPN）语法。它受 Brainfuck 启发，但比 Brainfuck 更人类友好：仅有少量基础指令，却图灵完备，适合学习栈数据结构、编译原理与编程语言设计。（名字来源：这只"鸡"会"啄"栈上的数据，就像啄米一样简单自然。）

- 极简主义：少量基础指令，每个指令语义明确
- 栈式思维：所有操作都在栈上进行
- 图灵完备：支持数学运算、循环、逻辑判断，可计算任何可计算函数
- Python API：提供 Python API，可嵌入 Python 项目
- 跨平台：纯 Python 实现，支持 Windows、Linux、macOS
- 可扩展：支持自定义指令与 IO Handler

## 工作原理

执行流程：源码（`.ch`）→ Parser（词法分析、语法分析，生成 Token）→ 虚拟机（栈管理、指令执行、IO 处理）→ 输出结果。纯 Python 实现，无需编译，即插即用。

## 快速开始

### 安装

```bash
git clone https://github.com/SharkMI-0x7E/ChickenStack.git
cd ChickenStack
pip install -r requirements.txt
```

### Hello World

创建 `hello_world.ch`：

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

## 文档

首次使用请查看[完整文档](https://SharkMI-0x7E.github.io/ChickenStack_doc/)：

- [快速开始](https://SharkMI-0x7E.github.io/ChickenStack_doc/guide/installation.html)
- [指令集](https://SharkMI-0x7E.github.io/ChickenStack_doc/guide/instruction-set.html)
- [语法说明](https://SharkMI-0x7E.github.io/ChickenStack_doc/guide/syntax.html)
- [Python API](https://SharkMI-0x7E.github.io/ChickenStack_doc/guide/python-api.html)
- [虚拟机 API](https://SharkMI-0x7E.github.io/ChickenStack_doc/guide/vm-api.html)

> 面向 AI 协作者（含各类 AI 编程助手）：本仓库附带 [`AGENTS.md`](./AGENTS.md) 协作入口，以及 [`PROJECT.md`](./PROJECT.md)（项目事实）与 [`CLAUDE.md`](./CLAUDE.md)（AI 行为准则）。改动前请先读这三个文件。

## 示例

查看 `examples/` 目录获取更多示例代码：

- [Hello World](https://SharkMI-0x7E.github.io/ChickenStack_doc/examples/hello-world.html)
- [数学运算](https://SharkMI-0x7E.github.io/ChickenStack_doc/examples/math.html)
- [栈操作](https://SharkMI-0x7E.github.io/ChickenStack_doc/examples/stack.html)
- [循环](https://SharkMI-0x7E.github.io/ChickenStack_doc/examples/loops.html)
- [斐波那契数列](https://SharkMI-0x7E.github.io/ChickenStack_doc/examples/fibonacci.html)
- [阶乘](https://SharkMI-0x7E.github.io/ChickenStack_doc/examples/factorial.html)
- [字符串反转](https://SharkMI-0x7E.github.io/ChickenStack_doc/examples/reverse-string.html)
- [求和](https://SharkMI-0x7E.github.io/ChickenStack_doc/examples/sum.html)
- [乘法表](https://SharkMI-0x7E.github.io/ChickenStack_doc/examples/multiplication-table.html)

## 贡献

欢迎提交 Bug 报告与 Pull Request。

### 开发者与致谢

本项目是重度 AI 辅助开发。代码、文档、测试与项目规划绝大部分由 AI 完成；人类维护者仅提出需求与方向。

**AI 开发者**
- GLM-4.7 — 初始版本的代码生成、测试、文档与性能优化
- Hy3 — 仓库结构清理、AI 协作文档体系与后续维护

**使用的工具**
- IFOW CLI
- WorkBuddy

**人类维护者**
- SharkMI-0x7E — 提出需求与方向

## 致谢

- [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck) — 灵感来源，展示了极简编程语言的魅力
- [VitePress](https://vitepress.dev/) — 文档构建工具
- [Python](https://www.python.org/) — 让 ChickenStack 得以实现的语言

## 注意事项

> 本仓库仅用于学习和研究目的，使用请遵守当地法律法规，由此造成的问题由使用者负责。

## 许可证

本项目采用 [MIT License](./LICENSE) 开源。

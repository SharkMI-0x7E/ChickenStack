<div align="center">

# ChickenStack

_基于栈的图灵完备编程语言_

> 栈之深兮不可测，代码之美兮在简洁.

</div>

---

## Welcome

- ChickenStack 是一个简单、优雅、强大的基于栈的编程语言，采用逆波兰表达式（RPN）语法。
  - ChickenStack is a simple, elegant, and powerful stack-based programming language using Reverse Polish Notation (RPN) syntax.

## Feature

- **Easy to Use**
  - 作为初学者能够轻松使用，比 Brainfuck 更人类友好
- **Turing Complete**
  - 支持数学运算、循环、逻辑判断等，可以计算任何可计算的函数
- **Cross Platform**
  - 支持 Windows、Linux、macOS 等主流操作系统
- **Rich API**
  - 提供 Python API，可以轻松嵌入到 Python 项目中
- **Extensible**
  - 支持自定义指令和 IO Handler，满足各种需求
- **Stable and Reliable**
  - 持续稳定的开发与维护

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

### 更多示例

查看 `examples/` 目录获取更多示例代码。

**首次使用**请务必查看[完整文档](https://llz162652.github.io/ChickenStack_doc/)

## Link

| Docs | [![Documentation](https://img.shields.io/badge/docs-on-Github.IO-orange)](https://llz162652.github.io/ChickenStack_doc/) |
|:-:|:-:|

| Repository | [![GitHub](https://img.shields.io/badge/repo-on-Github-black)](https://github.com/llz162652/ChickenStack) |
|:-:|:-:|

| Examples | [![Examples](https://img.shields.io/badge/examples-on-Github-blue)](https://github.com/llz162652/ChickenStack/tree/main/examples) |
|:-:|:-:|

## Thanks

- [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck) 灵感来源，展示了极简编程语言的魅力

- [VitePress](https://vitepress.dev/) 提供了优秀的文档构建工具

- [MaiBot](https://github.com/MaiM-with-u/MaiBot) 文档设计灵感来源

- 不过最最重要的，还是需要感谢屏幕前的你使用 ChickenStack~

---

## License

本项目采用 [MIT License](./LICENSE) 开源。

**本仓库仅用于学习和研究目的，使用请遵守当地法律法规，由此造成的问题由使用者负责。**
# ChickenStack

基于栈的图灵完备编程语言

ChickenStack 是一个简单、优雅、强大的基于栈的编程语言，采用逆波兰表达式（RPN）语法。它比 Brainfuck 更人类友好，易于理解和调试，同时保持图灵完备性，可以计算任何可计算的函数。

## 特性

- 🐔 **基于栈** - 采用逆波兰表达式，所有操作都在栈上进行，逻辑清晰
- 🚀 **图灵完备** - 支持数学运算、循环、逻辑判断等，可以计算任何可计算的函数
- 🎯 **简单易学** - 使用直观的符号，比 Brainfuck 更人类友好，易于理解和调试
- 🌐 **跨平台** - 支持 Windows、Linux、macOS 等主流操作系统
- 📦 **Python API** - 可以轻松嵌入到 Python 项目中，提供完整的 API 接口
- 🔧 **可扩展** - 支持自定义指令和 IO Handler，满足各种需求

## 快速开始

### 安装

```bash
git clone https://github.com/yourusername/ChickenStack.git
cd ChickenStack
```

### Hello World

```ch
72 " 101 " 108 " 108 " 111 " 32 " 87 " 111 " 114 " 108 " 100 " 10 "
```

### 运行

```bash
python main.py hello_world.ch
```

## 文档

详细文档请查看项目中的 `doc/` 目录，或运行以下命令启动本地文档服务器：

```bash
cd doc
npm install
npm run dev
```

在线文档即将上线...

## 许可证

MIT License

---

**特别感谢：**
- 本项目文档系统使用 [VitePress](https://vitepress.dev/) 构建
- Powered by AI GLM-4.7

# 安装指南

## 环境要求

在安装 ChickenStack 之前，请确保您的系统满足以下要求：

- **Python 版本**: 3.7 或更高版本
- **操作系统**: Windows、Linux 或 macOS
- **依赖**: 无需额外依赖（仅使用 Python 标准库）

### 检查 Python 版本

在终端或命令提示符中运行以下命令检查您的 Python 版本：

```bash
python --version
# 或
python3 --version
```

如果版本低于 3.7，请先升级 Python。

## 安装方法

### 方法一：克隆 GitHub 仓库

这是获取 ChickenStack 最简单的方法：

```bash
# 克隆仓库（请替换为实际的仓库地址）
git clone https://github.com/yourusername/ChickenStack.git

# 进入项目目录
cd ChickenStack

# 验证安装
python main.py
```

**注意**: 如果项目尚未发布到 GitHub，请使用以下方式：

```bash
# 直接下载或复制项目文件夹
# 确保项目目录包含以下文件：
# - chicken_stack/ (核心模块)
# - main.py (主入口)
# - hello_world.ch (示例文件)
```

### 方法二：下载 ZIP 文件

1. 访问 GitHub 仓库：https://github.com/yourusername/chickenstack
2. 点击 "Code" 按钮
3. 选择 "Download ZIP"
4. 解压下载的文件
5. 进入解压后的目录

### 方法三：从 PyPI 安装（计划中）

```bash
# 使用 pip 安装
pip install chickenstack

# 验证安装
python -c "import chicken_stack; print('安装成功！')"
```

## 验证安装

安装完成后，运行以下命令验证安装是否成功：

```bash
# 运行演示模式
python main.py

# 运行 Hello World 示例
python main.py hello_world.ch

# 运行完整示例
python main.py comprehensive_example.ch
```

如果看到输出，说明安装成功！

## 目录结构

安装后的目录结构如下：

```
chickenstack/
├── chicken_stack/
│   ├── __init__.py      # 模块入口
│   ├── io_handler.py    # 输入输出处理
│   ├── parser.py        # 代码解析器
│   └── vm.py            # 虚拟机核心
├── main.py              # 主入口
├── hello_world.ch       # Hello World 示例
├── comprehensive_example.ch  # 完整示例
├── api_example.py       # API 使用示例
└── QUICKSTART.py        # 快速入门指南
```

## 配置

ChickenStack 无需额外配置即可运行。但如果需要自定义行为，可以修改以下设置：

### 自定义 IO Handler

```python
from chicken_stack import ChickenStackVM, IOHandler

# 创建自定义 IO Handler
io = IOHandler()

# 创建虚拟机
vm = ChickenStackVM(io_handler=io)
```

### 设置栈大小限制

```python
from chicken_stack import ChickenStackVM

class LimitedVM(ChickenStackVM):
    def __init__(self, max_stack_size=1000, **kwargs):
        super().__init__(**kwargs)
        self.max_stack_size = max_stack_size

    def push(self, value):
        if len(self.stack) >= self.max_stack_size:
            raise Exception(f"栈溢出：超过最大栈大小 {self.max_stack_size}")
        super().push(value)
```

## 常见问题

### Q: Windows 控制台显示乱码怎么办？

在 Windows 上，可能需要设置控制台编码为 UTF-8：

```bash
# 在命令提示符中
chcp 65001

# 或在 PowerShell 中
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

### Q: 如何在 Linux/macOS 上使用？

Linux 和 macOS 用户可能需要使用 `python3` 命令：

```bash
python3 main.py hello_world.ch
```

### Q: 可以在虚拟环境中使用吗？

可以，建议使用虚拟环境：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 运行 ChickenStack
python main.py
```

### Q: 如何卸载？

如果通过 PyPI 安装：

```bash
pip uninstall chickenstack
```

如果通过克隆仓库安装，只需删除项目目录即可。

## 下一步

安装完成后，建议您：

1. 阅读 [快速开始指南](./getting-started.md)
2. 运行 [Hello World 示例](../examples/hello-world.md)
3. 查看 [指令集说明](./instruction-set.md)
4. 尝试编写自己的 ChickenStack 程序

## 获取帮助

如果在安装过程中遇到问题：

1. 查阅 [常见问题](../reference/faq.md)
2. 在 GitHub 上提交 Issue
3. 加入社区 Discord 或论坛

---

本文档由 AI GLM-4.7 生成
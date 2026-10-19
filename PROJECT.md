# PROJECT

> 项目事实的唯一真相源。**只放事实**（不放准则 → `CLAUDE.md`；不放历史 bug → `docs/ai/INDEX.md`）。
> 换项目时，改这一个文件就够了。

## 项目是什么
- **名称**：ChickenStack
- **类型**：CLI / 库（图灵完备栈式编程语言 + 纯 Python 解释器）
- **一句话描述**：一门栈式 + 逆波兰（RPN）的图灵完备编程语言，用直观符号替代 Brainfuck 的指针操作，附纯 Python 解释器。
- **目标用户 / 使用场景**：想了解 / 教学栈式语言原理的开发者与 AI 教育场景；通过 `.ch` 源码或 Python API 运行。
- **形态**：本地（开源，GitHub 仓库；非部署服务）

## 怎么跑
- **安装依赖**：无（仅 Python 标准库；开发可选 pytest / black / flake8）
- **开发运行**：`py main.py examples/hello_world.ch`（无参进演示模式）
- **构建 / 打包**：无（纯脚本式，无 pyproject / setup）
- **测试**：`py tests/run_comprehensive_tests.py` / `py test_optimization.py` / `py test_guessing_game.py`

## 技术栈
- **语言 / 版本**：Python（实际运行 3.12；源码用 3.9+ 语法如 `list[Token]`；`requirements.txt` 声明 `>=3.7`，待核实修正）
- **主要依赖**：无运行时依赖（标准库）；开发依赖 `pytest>=7` / `black>=23` / `flake8>=6`
- **数据存储**：无（无持久化；测试产物写入 `tests/results/*.json`）
- **外部服务**：文档站（VitePress + GitHub Pages）源码在独立仓库 `ChickenStack_doc`（本仓库同级目录），部署于 https://SharkMI-0x7E.github.io/ChickenStack_doc/

## 版本控制
- **类型**：git
- **远程**：有；`origin` https://github.com/SharkMI-0x7E/ChickenStack.git ；`doc` https://github.com/SharkMI-0x7E/ChickenStack_doc.git
- **主分支**：main

## 边界
- 本文件只记录**事实**。行为准则 → `CLAUDE.md`；bug 经验 → `docs/ai/INDEX.md`。
- 数字类事实（行数、性能、覆盖率）**尽量不写**；要写必须写明统计口径与日期。

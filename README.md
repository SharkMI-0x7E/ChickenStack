<div align="center">

# ChickenStack

_A Turing-complete stack-based programming language (RPN syntax)_

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/github/license/SharkMI-0x7E/ChickenStack?label=License)

**Read this in other languages: [English](./README.md), [中文](./README_zh.md).**

</div>

> **Just for fun.**
>
> ChickenStack was vibe-coded just because it seemed fun, originally built around December 2025 to January 2026 (first commit in January 2026). It has not been actively developed since, and there is no long-term maintenance plan or guarantee of ongoing updates.
> The code, docs, and tests were mostly written by AI; the human maintainer (SharkMI-0x7E) only proposed the requirements and direction — no planning, review, or spec work.
>
> It is Turing complete and it runs, and it is fine for learning stack-based languages and compiler principles. But don't treat it as a serious tool — it was made for fun.

---

## Introduction

ChickenStack is a simple, elegant, stack-based programming language using Reverse Polish Notation (RPN). Inspired by Brainfuck but more human-friendly, it has only a handful of basic instructions yet is Turing complete — useful for learning stack data structures, compiler principles, and programming language design. (The name: the "chicken" pecks data on the stack, just like pecking rice — simple and natural.)

- Minimalism: a few basic instructions with clear semantics
- Stack-based: all operations happen on the stack
- Turing complete: math, loops, logic — any computable function
- Python API: embed into Python projects
- Cross-platform: pure Python, runs on Windows, Linux, macOS
- Extensible: custom instructions and IO handlers

## How it works

Pipeline: source (`.ch`) → Parser (lexing, parsing, token generation) → Virtual Machine (stack management, instruction execution, IO handling) → output. Pure Python, no compilation needed.

## Quick Start

### Installation

```bash
git clone https://github.com/SharkMI-0x7E/ChickenStack.git
cd ChickenStack
pip install -r requirements.txt
```

### Hello World

Create `hello_world.ch`:

```ch
72 " 101 " 108 " 108 " 111 " 32 " 87 " 111 " 114 " 108 " 100 " 10 "
```

Run:

```bash
python main.py hello_world.ch
```

Output:

```
Hello World
```

### Advanced example: Fibonacci

```ch
0 1 10 [ dup + swap dup 1 - swap 1 - ]
```

## Documentation

For first-time users, see the [full documentation](https://SharkMI-0x7E.github.io/ChickenStack_doc/):

- [Quick Start](https://SharkMI-0x7E.github.io/ChickenStack_doc/guide/installation.html)
- [Instruction Set](https://SharkMI-0x7E.github.io/ChickenStack_doc/guide/instruction-set.html)
- [Syntax](https://SharkMI-0x7E.github.io/ChickenStack_doc/guide/syntax.html)
- [Python API](https://SharkMI-0x7E.github.io/ChickenStack_doc/guide/python-api.html)
- [VM API](https://SharkMI-0x7E.github.io/ChickenStack_doc/guide/vm-api.html)

> For AI collaborators (including AI coding assistants): this repo ships an [`AGENTS.md`](./AGENTS.md) entry point, plus [`PROJECT.md`](./PROJECT.md) (project facts) and [`CLAUDE.md`](./CLAUDE.md) (AI behavior rules). Read these before making changes.

## Examples

See the `examples/` directory for more:

- [Hello World](https://SharkMI-0x7E.github.io/ChickenStack_doc/examples/hello-world.html)
- [Math Operations](https://SharkMI-0x7E.github.io/ChickenStack_doc/examples/math.html)
- [Stack Operations](https://SharkMI-0x7E.github.io/ChickenStack_doc/examples/stack.html)
- [Loops](https://SharkMI-0x7E.github.io/ChickenStack_doc/examples/loops.html)
- [Fibonacci](https://SharkMI-0x7E.github.io/ChickenStack_doc/examples/fibonacci.html)
- [Factorial](https://SharkMI-0x7E.github.io/ChickenStack_doc/examples/factorial.html)
- [String Reverse](https://SharkMI-0x7E.github.io/ChickenStack_doc/examples/reverse-string.html)
- [Sum](https://SharkMI-0x7E.github.io/ChickenStack_doc/examples/sum.html)
- [Multiplication Table](https://SharkMI-0x7E.github.io/ChickenStack_doc/examples/multiplication-table.html)

## Contributing

Bug reports and pull requests are welcome.

### Developers and acknowledgments

This project is heavily AI-assisted. Code, documentation, tests, and project planning were mostly written by AI; the human maintainer only proposed requirements and direction.

**AI Developers**
- GLM-4.7 — initial code generation, testing, documentation, and performance optimization
- Hy3 — repository restructuring, AI collaboration docs system, and ongoing maintenance

**Tools used**
- IFOW CLI
- WorkBuddy

**Human maintainer**
- SharkMI-0x7E — proposed requirements and direction

## Acknowledgments

- [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck) — inspiration, showing the charm of minimalist languages
- [VitePress](https://vitepress.dev/) — documentation builder
- [Python](https://www.python.org/) — the language that made ChickenStack possible

## Notice

> This repository is for learning and research purposes only. Comply with local laws and regulations when using it; the user is responsible for any problems caused by its use.

## License

This project is open sourced under [MIT License](./LICENSE).

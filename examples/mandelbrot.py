"""
Mandelbrot 集 ASCII 渲染入口。

中文标题由 Python 打印；图形计算全部在 examples/mandelbrot.ch 里用 ChickenStack 完成。

运行: py examples/mandelbrot.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import ChickenStackInterpreter


def main() -> None:
    print("Mandelbrot 集 · ASCII 渲染")
    print("计算全部由 ChickenStack 完成（定点整数运算，无浮点）")
    print()

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mandelbrot.ch")
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    interp = ChickenStackInterpreter(max_iterations=5_000_000)
    interp.run(code, verbose=False)


if __name__ == "__main__":
    main()

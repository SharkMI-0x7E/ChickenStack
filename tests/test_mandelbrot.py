"""
Mandelbrot 渲染回归测试：校验输出尺寸与基本内容。

运行: py tests/test_mandelbrot.py
"""

import contextlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import ChickenStackInterpreter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "examples", "mandelbrot.ch")


def test_render():
    with open(SOURCE, "r", encoding="utf-8") as f:
        code = f.read()
    interp = ChickenStackInterpreter(max_iterations=5_000_000)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        interp.run(code, verbose=False)
    lines = [line for line in buf.getvalue().splitlines() if line]
    assert len(lines) == 30, f"期望 30 行，实际 {len(lines)}"
    assert all(len(line) == 80 for line in lines), "存在非 80 列的行"
    assert "@" in buf.getvalue() and "." in buf.getvalue(), "缺少明暗字符"


def main():
    test_render()
    print("PASS test_render (80x30)")


if __name__ == "__main__":
    main()

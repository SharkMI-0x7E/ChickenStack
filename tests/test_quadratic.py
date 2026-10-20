"""
二次函数采样的回归测试：验证 .ch 算出的关键点。

运行: py tests/test_quadratic.py
"""

import contextlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import ChickenStackInterpreter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "examples", "quadratic.ch")
SCALE = 10


class QueuedIO:
    def __init__(self, values):
        self.values = list(values)

    def get_num(self):
        return self.values.pop(0)

    def get_char(self):
        raise NotImplementedError


def sample(a, b, c, x_min, x_max):
    with open(SOURCE, "r", encoding="utf-8") as f:
        code = f.read()
    interp = ChickenStackInterpreter(max_iterations=5_000_000)
    interp.io_handler = QueuedIO([a, b, c, x_min, x_max])
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        interp.run(code, verbose=False)
    points = []
    for line in buf.getvalue().splitlines():
        parts = line.split()
        if len(parts) >= 2:
            points.append((int(parts[0]) / SCALE, int(parts[1]) / SCALE))
    return points


def test_points():
    points = sample(1, -2, -3, -5, 5)
    assert len(points) == 101, len(points)
    rounded = {(round(x, 1), round(y, 1)) for x, y in points}
    assert (-1.0, 0.0) in rounded, "缺根 x=-1"
    assert (3.0, 0.0) in rounded, "缺根 x=3"
    assert (1.0, -4.0) in rounded, "缺顶点 (1,-4)"
    assert (0.0, -3.0) in rounded, "缺 y 截距 (0,-3)"


def main():
    test_points()
    print("PASS test_points (101 点，根/顶点/截距正确)")


if __name__ == "__main__":
    main()

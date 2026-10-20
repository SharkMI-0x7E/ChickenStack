"""
猜数字游戏的回归测试：用假 IO 模拟用户回答，验证二分法收敛到正确结果。

运行: py tests/test_game.py
"""

import contextlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import ChickenStackInterpreter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.join(ROOT, "examples", "guess_number.ch")


class FakeIO:
    def __init__(self, answers):
        self.answers = list(answers)

    def get_num(self):
        return self.answers.pop(0)

    def get_char(self):
        raise NotImplementedError


def play(answers):
    with open(GAME, "r", encoding="utf-8") as f:
        code = f.read()
    interp = ChickenStackInterpreter()
    interp.io_handler = FakeIO(answers)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        interp.run(code)
    return buf.getvalue()


def test_guess_42():
    out = play([0, 1, 1, 0, 1, 1, 0])
    assert "你想的数是 42" in out, out


def test_guess_1():
    out = play([0, 0, 0, 0, 0, 0])
    assert "你想的数是 1" in out, out


def test_guess_100():
    out = play([1, 1, 1, 1, 1, 1, 0])
    assert "你想的数是 100" in out, out


def main():
    tests = [test_guess_42, test_guess_1, test_guess_100]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"{len(tests)} 个猜数字测试通过")


if __name__ == "__main__":
    main()

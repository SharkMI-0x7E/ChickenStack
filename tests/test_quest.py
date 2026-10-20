"""
《鸡舍大冒险》的回归测试：用假 IO 模拟四条路线，验证三种结局。

运行: py tests/test_quest.py
"""

import contextlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import ChickenStackInterpreter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.join(ROOT, "examples", "chicken_quest.ch")


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


def test_perfect_ending():
    # 厨房 -> 战斗 -> 拿钥匙 -> 不买药 -> 开宝箱
    out = play([1, 1, 2, 1])
    assert "完美结局" in out, out


def test_trap_survive():
    # 后院 -> 拿金币 -> 不买药 -> 没钥匙硬开（HP 10-5=5）
    out = play([2, 1, 2, 1])
    assert "活了下来" in out, out


def test_trap_death():
    # 厨房 -> 战斗后 HP4 -> 拿金币 -> 不买药 -> 硬开（HP -1）
    out = play([1, 2, 2, 1])
    assert "眼前一黑" in out, out


def test_leave_ending():
    # 后院 -> 拿钥匙 -> 不买药 -> 离开
    out = play([2, 2, 2, 2])
    assert "最终：HP 10" in out, out


def main():
    tests = [
        test_perfect_ending,
        test_trap_survive,
        test_trap_death,
        test_leave_ending,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"{len(tests)} 个冒险测试通过")


if __name__ == "__main__":
    main()

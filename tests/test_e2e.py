"""
端到端测试：验证解释器对完整程序的实际输出。

运行: py tests/test_e2e.py
"""

import io
import os
import sys
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import ChickenStackInterpreter


def run_capture(code: str) -> str:
    """运行代码并返回程序本身的输出（去掉 run() 打印的启动/结束摘要）。"""
    buf = io.StringIO()
    interpreter = ChickenStackInterpreter()
    with redirect_stdout(buf):
        interpreter.run(code)
    return buf.getvalue().split("运行结束")[0]


def test_arithmetic():
    out = run_capture("10 20 + 2 * .")
    assert "60" in out, f"期望输出 60，实际: {out!r}"


def test_simple_add():
    out = run_capture("10 20 + .")
    assert "30" in out, f"期望输出 30，实际: {out!r}"


def test_countdown_loop():
    out = run_capture("5 [ : . 1 - ]")
    assert "5 4 3 2 1" in out, f"期望输出 5 4 3 2 1，实际: {out!r}"


def test_hello_chars():
    out = run_capture('72 " 69 " 76 " 76 " 79 " 10 "')
    assert "HELLO" in out, f"期望输出 HELLO，实际: {out!r}"


def main():
    tests = [
        test_arithmetic,
        test_simple_add,
        test_countdown_loop,
        test_hello_chars,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"{len(tests)} 个端到端测试通过")


if __name__ == "__main__":
    main()

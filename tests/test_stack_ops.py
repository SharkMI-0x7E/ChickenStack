"""
栈操作扩展测试: rot(@), over(&), pick(!)

运行: py tests/test_stack_ops.py
"""

import contextlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chicken_stack import ChickenStackVM, Parser, TokenType
from main import ChickenStackInterpreter


def test_rot():
    vm = ChickenStackVM()
    for value in (1, 2, 3):
        vm.push(value)
    vm.op_rot()
    assert vm.get_stack_state() == [2, 3, 1]


def test_over():
    vm = ChickenStackVM()
    vm.push(1)
    vm.push(2)
    vm.op_over()
    assert vm.get_stack_state() == [1, 2, 1]


def test_pick_depth_one():
    vm = ChickenStackVM()
    for value in (10, 20, 30):
        vm.push(value)
    vm.push(1)
    vm.op_pick()
    assert vm.get_stack_state() == [10, 20, 30, 20]


def test_pick_depth_zero():
    vm = ChickenStackVM()
    vm.push(7)
    vm.push(0)
    vm.op_pick()
    assert vm.get_stack_state() == [7, 7]


def test_pick_out_of_range():
    vm = ChickenStackVM()
    vm.push(1)
    vm.push(99)
    try:
        vm.op_pick()
        assert False, "应当抛出 ValueError"
    except ValueError:
        pass


def test_parser_symbols():
    tokens = Parser().parse("1 2 3 @ & !")
    assert [token.type for token in tokens] == [
        TokenType.INTEGER,
        TokenType.INTEGER,
        TokenType.INTEGER,
        TokenType.ROT,
        TokenType.OVER,
        TokenType.PICK,
    ]


def _run(code):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ChickenStackInterpreter().run(code)
    return buf.getvalue().split("运行结束")[0]


def test_e2e_rot():
    assert "1 3 2" in _run("1 2 3 @ . . .")


def test_e2e_over():
    assert "1 2 1" in _run("1 2 & . . .")


def test_e2e_pick():
    assert "20 30 20 10" in _run("10 20 30 1 ! . . . .")


def main():
    tests = [
        test_rot,
        test_over,
        test_pick_depth_one,
        test_pick_depth_zero,
        test_pick_out_of_range,
        test_parser_symbols,
        test_e2e_rot,
        test_e2e_over,
        test_e2e_pick,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"{len(tests)} 个栈操作测试通过")


if __name__ == "__main__":
    main()

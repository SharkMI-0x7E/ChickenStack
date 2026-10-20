"""
字节码编译器与解释器的一致性测试。

编译器的唯一验收标准是：同一段源码，两种执行方式输出必须逐字符相同。
另外检查生成的 Python 源码结构、迭代上限、越界检查。

运行: py tests/test_compiler.py
"""

import contextlib
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from chicken_stack.compiler import compile_source
from main import ChickenStackInterpreter

LIMIT = 50_000_000


class QueuedIO:
    def __init__(self, values=()):
        self.values = list(values)

    def get_num(self):
        return self.values.pop(0)

    def get_char(self):
        return self.values.pop(0)


def run_interpreter(code, inputs=None):
    interpreter = ChickenStackInterpreter(max_iterations=LIMIT)
    if inputs is not None:
        interpreter.io_handler = QueuedIO(inputs)
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        interpreter.run(code, verbose=False)
    return buffer.getvalue()


def run_compiled(code, inputs=None):
    program = compile_source(code)
    handler = QueuedIO(inputs) if inputs is not None else None
    return program.run(handler, LIMIT)


def check(source, inputs=None):
    expected = run_interpreter(source, inputs)
    actual = run_compiled(source, inputs)
    assert actual == expected, (
        f"{source!r}\n  解释器: {expected!r}\n  编译器: {actual!r}"
    )
    return actual


def test_arithmetic():
    for source in (
        "5 3 + .",
        "10 20 + 2 * .",
        "20 4 / .",
        "7 2 / .",
        "17 5 % .",
        "~5 .",
        "5 ~ .",
        "100 50 5 / - 10 + .",
    ):
        check(source)


def test_stack_ops():
    for source in (
        "5 : . .",
        "1 2 \\ . .",
        "1 2 3 @ . . .",
        "3 5 & . . .",
        "10 20 30 1 ! . . . .",
        "10 20 $ .",
    ):
        check(source)


def test_control_flow():
    check("5 [ : . 1 - ]")
    check('1 { 65 " | 66 " } 10 "')
    check('0 { 65 " | 66 " } 10 "')
    check("3 { 'yes' | 'no' } 10 \"")
    check("0 T 1 A 5 [ t a + T a 1 + A a 5 > 0 = ] t .")
    check('3 [ 3 [ 1 . 1 - ] $ 10 " 1 - ]')


def test_strings_and_registers():
    check("'hello' 10 \"")
    check("'a' 'b' 10 \"")
    check('65 T t " 10 "')
    check("10 T 20 A t a + .")


def test_floats():
    for source in (
        "3.14 .",
        "1.5 2.5 + .",
        "~3.5 .",
        "1.5 2 * .",
        "10.0 4 / .",
        "0.1 0.2 + .",
        "2.5 2 % .",
        "1.5 1.5 = .",
        "65.0 \"",
        "10 T 1.5 A t .",
    ):
        check(source)


def test_example_files():
    for name in ("hello_world.ch", "fizzbuzz.ch", "chicken.ch"):
        path = os.path.join(ROOT, "examples", name)
        with open(path, encoding="utf-8") as handle:
            check(handle.read())


def test_quadratic_example():
    path = os.path.join(ROOT, "examples", "quadratic.ch")
    with open(path, encoding="utf-8") as handle:
        check(handle.read(), inputs=[1, -2, -3, -5, 5])


def test_generated_source():
    slots = compile_source("5 3 + .")
    assert "v0 = 5" in slots.source, slots.source
    assert "v0 += v1" in slots.source, slots.source
    assert "s.append" not in slots.source, slots.source

    lists = compile_source("5 3 + .", use_slots=False)
    assert "s.append(5)" in lists.source, lists.source
    assert "s[-1] += b" in lists.source, lists.source

    loop = compile_source("1 [ 1 - ]").source
    assert "while True:" in loop, loop
    assert "break" in loop, loop

    branch = compile_source("1 { 2 | 3 }").source
    assert "if v0 != 0:" in branch, branch
    assert "else:" in branch, branch

    assert compile_source("5 3 + .").token_count == 4


def test_slot_modes_agree():
    """栈槽模式与 list 模式必须输出完全一致。"""
    for source in (
        "5 3 + .",
        "5 [ : . 1 - ]",
        "1 2 3 @ . . .",
        "3 5 & . . .",
        "1 { 65 \" | 66 \" } 10 \"",
        "0 T 1 A 5 [ t a + T a 1 + A a 5 > 0 = ] t .",
        "65 A 26 [ a \" a 1 + A 1 - ]",
        "10 20 30 1 ! . . . .",
    ):
        slots = compile_source(source, use_slots=True).run(None, LIMIT)
        lists = compile_source(source, use_slots=False).run(None, LIMIT)
        assert slots == lists, f"{source!r}: 栈槽 {slots!r} != list {lists!r}"


def test_slot_fallback():
    """含 ! 的程序无法静态分析，应自动退回 list 模式。"""
    program = compile_source("10 20 30 1 ! . . . .")
    assert "s.append" in program.source, program.source
    assert program.run(None, LIMIT) == "20 30 20 10 "


def test_iteration_limit():
    program = compile_source("1 [ ]")
    try:
        program.run(None, 1000)
    except RuntimeError as exc:
        assert "迭代" in str(exc) or "超时" in str(exc), exc
    else:
        raise AssertionError("死循环未触发迭代上限")


def test_pick_out_of_range():
    program = compile_source("1 5 ! .")
    try:
        program.run(None, 10000)
    except ValueError as exc:
        assert "越界" in str(exc), exc
    else:
        raise AssertionError("pick 越界未报错")


def main():
    tests = [
        ("arithmetic", test_arithmetic),
        ("stack_ops", test_stack_ops),
        ("control_flow", test_control_flow),
        ("strings_and_registers", test_strings_and_registers),
        ("floats", test_floats),
        ("example_files", test_example_files),
        ("quadratic_example", test_quadratic_example),
        ("generated_source", test_generated_source),
        ("slot_modes_agree", test_slot_modes_agree),
        ("slot_fallback", test_slot_fallback),
        ("iteration_limit", test_iteration_limit),
        ("pick_out_of_range", test_pick_out_of_range),
    ]
    for name, func in tests:
        func()
        print(f"PASS test_{name}")
    print(f"PASS 全部 {len(tests)} 组用例 (compiler)")


if __name__ == "__main__":
    main()

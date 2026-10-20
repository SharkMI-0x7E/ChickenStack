"""
表达式解析 / 定点求值 / ChickenStack 代码生成的回归测试。

被测模块: examples/live_plot.py

运行: py tests/test_live_plot.py
"""

import contextlib
import io
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "examples"))

from main import ChickenStackInterpreter

import live_plot

SCALE = 10000
TOL = 0.002
INT_RE = re.compile(r"-?\d+")


# ---------------------------------------------------------------- 工具函数

def token_cats(tokens):
    return [cat for cat, _ in tokens]


def token_ops(tokens):
    return [str(value) for cat, value in tokens if cat == "op"]


def token_nums(tokens):
    return [float(value) for cat, value in tokens if cat == "num"]


def token_names(tokens):
    return [str(value) for cat, value in tokens if cat == "name"]


def eval_text(text, x=0.0):
    return live_plot.float_eval(live_plot.parse(text), x)


def chicken_ints(source):
    """跑一段 ChickenStack 源码，返回其输出中出现的所有整数。"""
    interp = ChickenStackInterpreter(max_iterations=5_000_000)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        interp.run(source, verbose=False)
    out = buf.getvalue()
    numbers = [int(m) for m in INT_RE.findall(out)]
    return numbers, out


def run_emit(text, x_fixed=0):
    """把 emit() 的指令接到寄存器 X 上跑一遍，取最后一个输出整数。"""
    instrs = live_plot.emit(live_plot.parse(text))
    source = f"{live_plot._literal(x_fixed)} X\n{' '.join(instrs)}\n.\n"
    numbers, out = chicken_ints(source)
    assert numbers, f"emit({text!r}) 没有输出任何数字，程序输出: {out!r}"
    return numbers[-1], instrs


def raises_syntax_error(text):
    try:
        live_plot.parse(text)
    except SyntaxError:
        return True
    return False


# ---------------------------------------------------------------- 用例

def test_tokenize():
    tokens = live_plot.tokenize("1+2*3")
    assert isinstance(tokens, list), type(tokens)
    assert all(isinstance(t, tuple) and len(t) == 2 for t in tokens), tokens
    assert token_cats(tokens) == ["num", "op", "num", "op", "num"], tokens
    assert token_nums(tokens) == [1.0, 2.0, 3.0], tokens
    assert token_ops(tokens) == ["+", "*"], tokens

    # 隐式乘法只拆词，不在这里补 *
    tokens = live_plot.tokenize("2x")
    assert token_cats(tokens) == ["num", "name"], tokens
    assert token_nums(tokens) == [2.0], tokens
    assert token_names(tokens) == ["x"], tokens

    # 全角括号与全角运算符
    tokens = live_plot.tokenize("（1＋2）×3÷4")
    assert token_nums(tokens) == [1.0, 2.0, 3.0, 4.0], tokens
    assert token_ops(tokens) == ["(", "+", ")", "*", "/"], tokens

    tokens = live_plot.tokenize("（2x）")
    assert token_ops(tokens) == ["(", ")"], tokens
    assert token_names(tokens) == ["x"], tokens

    # 空表达式
    for text in ("", "   ", "\t\n"):
        try:
            live_plot.tokenize(text)
        except SyntaxError:
            pass
        else:
            raise AssertionError(f"tokenize({text!r}) 未抛 SyntaxError")


def test_ast_shapes():
    node = live_plot.parse("1")
    assert node[0] == "num" and isinstance(node, tuple), node
    assert abs(float(node[1]) - 1.0) < 1e-12, node

    node = live_plot.parse("x")
    assert node == ("var", "x"), node

    node = live_plot.parse("-x")
    assert node[0] == "neg" and node[1] == ("var", "x"), node

    node = live_plot.parse("1+2")
    assert node[0] == "bin" and node[1] == "+", node
    assert node[2] == ("num", node[2][1]) and node[3][0] == "num", node

    node = live_plot.parse("2^3")
    assert node[0] == "pow", node
    assert isinstance(node[2], int) and node[2] == 3, node


def test_precedence():
    assert eval_text("1+2*3") == 7.0
    assert abs(eval_text("2^3^2") - 512.0) < 1e-9, "幂应右结合"
    assert abs(eval_text("2^3*2") - 16.0) < 1e-9
    assert abs(eval_text("(1+2)*3") - 9.0) < 1e-9
    assert abs(eval_text("(1+2)^2") - 9.0) < 1e-9
    assert abs(eval_text("8/4/2") - 1.0) < 1e-9, "除法应左结合"
    assert abs(eval_text("2-3-4") + 5.0) < 1e-9, "减法应左结合"
    # 一元负号优先级低于幂：-(x^2) 而不是 (-x)^2
    assert abs(eval_text("-x^2", 2) + 4.0) < 1e-9, "-x^2 在 x=2 时应为 -4"
    assert abs(eval_text("-2^2") + 4.0) < 1e-9
    assert abs(eval_text("(-x)^2", 2) - 4.0) < 1e-9
    assert abs(eval_text("2*-3") + 6.0) < 1e-9


def test_implicit_mul():
    assert abs(eval_text("2x", 3) - 6.0) < 1e-9
    assert abs(eval_text("3(x+1)", 2) - 9.0) < 1e-9
    assert abs(eval_text("x(x-1)", 5) - 20.0) < 1e-9
    assert abs(eval_text("2x^2", 3) - 18.0) < 1e-9, "2x^2 = 2*(x^2)"
    assert abs(eval_text("2(x+1)(x-1)", 3) - 16.0) < 1e-9


def test_constants():
    assert abs(eval_text("pi") - math.pi) < 1e-9
    assert abs(eval_text("e") - math.e) < 1e-9
    assert abs(eval_text("2pi", 0) - 2 * math.pi) < 1e-9


def test_fixed_matches_float():
    exprs = [
        "x^2-2x+1",
        "3(x-1)+1/3",
        "x^3/7",
        "pi*x+1",
        "(x+1)/(x-3)",
        "-x^2+4x-1",
        "1/(x+2)",
        "x(x-1)/2",
    ]
    xs = [-3.5, -1.0, 0.5, 2.25, 7.0]

    for text in exprs:
        node = live_plot.parse(text)
        for x in xs:
            x_fixed = int(round(x * SCALE))
            fixed = live_plot.fixed_eval(node, x_fixed)
            assert isinstance(fixed, int), f"{text} @x={x}: fixed_eval 应返回 int，实际 {type(fixed)}"
            approx = fixed / SCALE
            exact = live_plot.float_eval(node, x)
            diff = abs(approx - exact)
            assert diff < TOL, f"{text} @x={x}: fixed={approx} float={exact} 差 {diff}"

    # 定点除零
    try:
        live_plot.fixed_eval(live_plot.parse("1/x"), 0)
    except ZeroDivisionError:
        pass
    else:
        raise AssertionError("fixed_eval(1/x, 0) 未抛 ZeroDivisionError")


def test_sample_matches_float():
    node = live_plot.parse("x^2-2x+1")
    points = live_plot.sample(node, -2, 2, 41)
    assert isinstance(points, list), type(points)
    assert len(points) == 41, len(points)

    assert abs(points[0][0] - (-2.0)) < 1e-9, points[0]
    assert abs(points[-1][0] - 2.0) < 1e-9, points[-1]

    for index, point in enumerate(points):
        assert point is not None, f"第 {index} 个点不该是 None"
        x, y = point
        expected_x = -2.0 + 4.0 * index / 40
        assert abs(x - expected_x) < 1e-9, f"第 {index} 个点 x={x}，期望 {expected_x}"
        expected_y = live_plot.float_eval(node, x)
        assert abs(y - expected_y) < TOL, f"@{x}: sample={y} float_eval={expected_y}"

    # 默认点数 241
    assert len(live_plot.sample(node, -1, 1)) == 241

    # 换一个含除法与常量的表达式
    node = live_plot.parse("(x+1)/(x-3)")
    for point in live_plot.sample(node, 4, 8, 33):
        assert point is not None, point
        x, y = point
        assert abs(y - live_plot.float_eval(node, x)) < TOL, point


def test_sample_singularity():
    # 201 点、步长 0.01 时定点网格恰好落在 x=0 上
    node = live_plot.parse("1/x")
    points = live_plot.sample(node, -1, 1, 201)
    assert len(points) == 201, len(points)

    nones = [i for i, p in enumerate(points) if p is None]
    assert nones, "跨越 0 的区间上 1/x 应产生 None"
    for i in nones:
        x = -1.0 + 2.0 * i / 200
        assert abs(x) < 1e-9, f"只有 x=0 处应无法求值，实际第 {i} 点 x={x} 也是 None"

    keep = [(i, p) for i, p in enumerate(points) if p is not None]
    assert len(keep) == 200, len(keep)
    for index, (x, y) in keep:
        assert abs(y - 1.0 / x) < TOL, (index, x, y)


def test_emit_runs_on_chickenstack():
    # emit 的中间值都是放大 SCALE 倍的定点数
    got, instrs = run_emit("1+2*3")
    assert isinstance(instrs, list) and all(isinstance(s, str) for s in instrs), instrs
    assert got == 7 * SCALE, f"1+2*3 编译执行得到 {got}"

    got, _ = run_emit("2^3^2")
    assert got == 512 * SCALE, f"2^3^2 编译执行得到 {got}"

    got, _ = run_emit("x*x+1", x_fixed=2 * SCALE)
    assert got == 5 * SCALE, f"x*x+1 在 x=2 时得到 {got}"

    got, _ = run_emit("-(2+3)*4")
    assert got == -20 * SCALE, f"-(2+3)*4 编译执行得到 {got}"

    got, _ = run_emit("x^2-2x+1", x_fixed=3 * SCALE)
    assert got == 4 * SCALE, f"x^2-2x+1 在 x=3 时得到 {got}"

    got, _ = run_emit("100/x", x_fixed=4 * SCALE)
    assert got == 25 * SCALE, f"100/x 在 x=4 时得到 {got}"


def test_build_program():
    node = live_plot.parse("x^2")
    source = live_plot.build_program(node, 0, SCALE, 0, 3)
    assert isinstance(source, str), type(source)

    numbers, out = chicken_ints(source)
    assert numbers, f"build_program 没有输出数字，程序输出: {out!r}"

    # 期望 k = 0..3 -> x = 0,1,2,3 -> y = 0,1,4,9（均以 SCALE 放大）
    if len(numbers) == 8:
        xs_fixed, ys_fixed = numbers[0::2], numbers[1::2]
        assert xs_fixed == [0, SCALE, 2 * SCALE, 3 * SCALE], xs_fixed
    else:
        assert len(numbers) == 4, f"应输出 4 个采样点，实际 {len(numbers)} 个: {numbers}"
        ys_fixed = numbers

    expected = [0, SCALE, 4 * SCALE, 9 * SCALE]
    for index, (got, want) in enumerate(zip(ys_fixed, expected)):
        assert abs(got - want) <= 1, f"第 {index} 个点是 {got}，期望 {want}"


def test_math_functions():
    exprs = {
        "sin(x)": math.sin,
        "cos(x)": math.cos,
        "abs(x)": abs,
        "sqrt(x)": lambda v: math.sqrt(v) if v >= 0 else 0.0,
    }
    xs = [-2.5, -1.0, 0.0, 0.5, 1.0, 1.5708, 2.0, 3.0]
    for text, reference in exprs.items():
        node = live_plot.parse(text)
        for x in xs:
            got = live_plot.fixed_eval(node, int(round(x * SCALE))) / SCALE
            want = reference(x)
            assert abs(got - want) < TOL, f"{text} @x={x}: 定点 {got} vs math {want}"

    # 定点实现与 ChickenStack 的实际执行必须逐位一致
    for text in ("sin(x)", "cos(x)", "sqrt(x^2+1)", "2sin(3x)", "abs(sin(x))"):
        node = live_plot.parse(text)
        for x in (-2.0, 0.0, 0.7, 1.5708, 2.5):
            x_fixed = int(round(x * SCALE))
            expected = live_plot.fixed_eval(node, x_fixed)
            got, _ = run_emit(text, x_fixed=x_fixed)
            assert got == expected, f"{text} @x={x}: ChickenStack {got} vs fixed_eval {expected}"

    # tan 在 π/2 附近应该给出巨大值而不是崩溃
    tangent = live_plot.fixed_eval(live_plot.parse("tan(x)"), int(round(1.5707 * SCALE)))
    assert abs(tangent) > 100 * SCALE, tangent

    # 函数调用必须带括号
    for bad in ("sin x", "sinx", "cos 1", "sqrt"):
        assert raises_syntax_error(bad), f"parse({bad!r}) 未抛 SyntaxError"


def test_syntax_errors():
    bad = ["", "   ", "1+", "(1+2", "*3", "2^^3", "1+*2", ")"]
    for text in bad:
        assert raises_syntax_error(text), f"parse({text!r}) 未抛 SyntaxError"

    # 合法表达式反例，确保上面的用例不是因为全盘报错才"通过"
    for text in ("1+2", "-x", "2x", "pi"):
        assert not raises_syntax_error(text), f"parse({text!r}) 误报 SyntaxError"


def main():
    tests = [
        ("tokenize", test_tokenize),
        ("ast_shapes", test_ast_shapes),
        ("precedence", test_precedence),
        ("implicit_mul", test_implicit_mul),
        ("constants", test_constants),
        ("fixed_matches_float", test_fixed_matches_float),
        ("sample_matches_float", test_sample_matches_float),
        ("sample_singularity", test_sample_singularity),
        ("emit_runs_on_chickenstack", test_emit_runs_on_chickenstack),
        ("build_program", test_build_program),
        ("math_functions", test_math_functions),
        ("syntax_errors", test_syntax_errors),
    ]
    for name, func in tests:
        func()
        print(f"PASS test_{name}")
    print(f"PASS 全部 {len(tests)} 组用例 (live_plot)")


if __name__ == "__main__":
    main()

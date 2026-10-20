"""
确定性属性测试。

1. 随机生成只含整数和 + - * 的 RPN 表达式，解释器输出应与 Python 计算一致。
2. 随机字符串喂给解析器，只允许 SyntaxError/ValueError/TypeError，不允许 IndexError/KeyError。

运行: py tests/test_property.py
"""

import contextlib
import io
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chicken_stack import Parser
from main import ChickenStackInterpreter


def eval_rpn(tokens):
    stack = []
    for token in tokens:
        if isinstance(token, int):
            stack.append(token)
        else:
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            else:
                stack.append(a * b)
    return stack[0] if len(stack) == 1 else None


def to_source(tokens):
    parts = []
    for token in tokens:
        if isinstance(token, int):
            parts.append(str(token) if token >= 0 else f"~{-token}")
        else:
            parts.append(token)
    return " ".join(parts) + " ."


def run_capture(code):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ChickenStackInterpreter().run(code, verbose=False)
    return buf.getvalue()


def gen_expr(rng):
    tokens = []
    depth = 0
    for _ in range(rng.randint(3, 12)):
        if depth < 2 or rng.random() < 0.6:
            tokens.append(rng.randint(-20, 20))
            depth += 1
        else:
            tokens.append(rng.choice(["+", "-", "*"]))
            depth -= 1
    while depth > 1:
        tokens.append(rng.choice(["+", "-", "*"]))
        depth -= 1
    return tokens


def test_arithmetic_property():
    rng = random.Random(20261020)
    checked = 0
    for _ in range(300):
        tokens = gen_expr(rng)
        expected = eval_rpn(tokens)
        if expected is None:
            continue
        source = to_source(tokens)
        out = run_capture(source)
        match = re.search(r"-?\d+", out)
        assert match is not None, (source, out)
        actual = int(match.group())
        assert actual == expected, (source, expected, actual, out)
        checked += 1
    assert checked >= 250, f"有效样本过少: {checked}"


def test_parser_never_crashes():
    rng = random.Random(20261020)
    alphabet = "0123456789+-*/%:\\$=><.\"?,[]{}|'~ abcxyzABCXYZ#\n"
    parser = Parser()
    for _ in range(500):
        source = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40)))
        try:
            parser.parse(source)
        except (SyntaxError, ValueError, TypeError):
            pass
        except Exception as exc:
            raise AssertionError(
                f"解析器抛出未预期异常 {type(exc).__name__}: {source!r}"
            ) from exc


def main():
    tests = [test_arithmetic_property, test_parser_never_crashes]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"{len(tests)} 个属性测试通过")


if __name__ == "__main__":
    main()

"""
实时函数绘图

在输入框里敲表达式（例如 x^2 - 2x - 3），服务端把它解析成语法树、编译为
ChickenStack 后缀代码，再交给解释器逐点采样，浏览器拿到坐标后立刻重绘。

分工：表达式解析与代码生成在 Python，每个采样点的数值计算在 ChickenStack。

运行:
  py examples/live_plot.py
浏览器打开 http://127.0.0.1:8765
"""

import contextlib
import io
import json
import math
import os
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import ChickenStackInterpreter

SCALE = 10000          # 定点比例，1.0 对应 10000
MAX_POWER = 64         # 幂次展开上限，超过就不画了
DEFAULT_COUNT = 241    # 默认采样点数
MAX_COUNT = 2001
DEFAULT_PORT = 8765

PI_FIXED = int(round(math.pi * SCALE))
HALF_PI_FIXED = int(round(math.pi / 2 * SCALE))
TWO_PI_FIXED = PI_FIXED * 2

# 这些函数全部由 ChickenStack 定点运算实现，不调用 Python 的 math
FUNCTIONS = ("sin", "cos", "tan", "sqrt", "abs")
SQRT_STEPS = 10        # 牛顿迭代次数

# 解释器写入的是全局 stdout，多线程并发会串台
_SAMPLE_LOCK = threading.Lock()


# 词法分析

_FULLWIDTH = str.maketrans({
    "（": "(", "）": ")", "＋": "+", "－": "-", "—": "-",
    "×": "*", "＊": "*", "／": "/", "÷": "/", "＾": "^",
    "　": " ", "，": ",",
})


def tokenize(text):
    """把表达式拆成 (类别, 值) 序列，类别为 num / name / op。"""
    text = text.translate(_FULLWIDTH)
    tokens = []
    i = 0
    length = len(text)
    while i < length:
        ch = text[i]
        if ch.isspace() or ch == ",":
            i += 1
            continue
        if ch.isdigit() or ch == ".":
            start = i
            dots = 0
            while i < length and (text[i].isdigit() or text[i] == "."):
                if text[i] == ".":
                    dots += 1
                    if dots > 1:
                        raise SyntaxError("数字里出现了多个小数点")
                i += 1
            try:
                tokens.append(("num", float(text[start:i])))
            except ValueError:
                raise SyntaxError(f"无法识别的数字: {text[start:i]}")
            continue
        if ch.isalpha():
            start = i
            while i < length and text[i].isalnum():
                i += 1
            tokens.append(("name", text[start:i].lower()))
            continue
        if ch in "+-*/^()":
            tokens.append(("op", ch))
            i += 1
            continue
        raise SyntaxError(f"不认识的字符: {ch}")
    if not tokens:
        raise SyntaxError("表达式是空的")
    return tokens


def _ends_value(token):
    kind, value = token
    return kind in ("num", "name") or (kind == "op" and value == ")")


def _starts_value(token):
    kind, value = token
    return kind in ("num", "name") or (kind == "op" and value == "(")


def _with_implicit_mul(tokens):
    """在相邻的值之间补乘号，支持 2x、3(x+1)、x(x-1) 这类写法。"""
    result = []
    for token in tokens:
        if result and _ends_value(result[-1]) and _starts_value(token):
            previous = result[-1]
            is_call = (
                previous[0] == "name"
                and previous[1] in FUNCTIONS
                and token == ("op", "(")
            )
            if not is_call:
                result.append(("op", "*"))
        result.append(token)
    return result


# 语法分析


class _ExprParser:
    """递归下降解析中缀表达式，产出元组表示的语法树。"""

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def _peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _take(self):
        token = self._peek()
        self.pos += 1
        return token

    def parse(self):
        node = self._expr()
        token = self._peek()
        if token is not None:
            raise SyntaxError(f"多余的内容: {token[1]}")
        return node

    def _expr(self):
        node = self._term()
        while True:
            token = self._peek()
            if token and token[0] == "op" and token[1] in "+-":
                self._take()
                node = ("bin", token[1], node, self._term())
            else:
                return node

    def _term(self):
        node = self._unary()
        while True:
            token = self._peek()
            if token and token[0] == "op" and token[1] in "*/":
                self._take()
                node = ("bin", token[1], node, self._unary())
            else:
                return node

    def _unary(self):
        token = self._peek()
        if token and token[0] == "op" and token[1] in "+-":
            self._take()
            operand = self._unary()
            return ("neg", operand) if token[1] == "-" else operand
        return self._power()

    def _power(self):
        base = self._atom()
        token = self._peek()
        if token and token[0] == "op" and token[1] == "^":
            self._take()
            exponent = self._unary()
            return ("pow", base, _as_exponent(exponent))
        return base

    def _atom(self):
        token = self._take()
        if token is None:
            raise SyntaxError("表达式意外结束")
        kind, value = token
        if kind == "num":
            return ("num", value)
        if kind == "name":
            if value == "x":
                return ("var", "x")
            if value == "pi":
                return ("num", math.pi)
            if value == "e":
                return ("num", math.e)
            if value in FUNCTIONS:
                opening = self._take()
                if opening != ("op", "("):
                    raise SyntaxError(f"{value} 后面要跟括号，例如 {value}(x)")
                argument = self._expr()
                closing = self._take()
                if closing != ("op", ")"):
                    raise SyntaxError(f"{value}(...) 的括号没有闭合")
                return ("call", value, argument)
            raise SyntaxError(
                f"不认识的变量: {value}（支持 x、pi、e 和 {', '.join(FUNCTIONS)}）"
            )
        if kind == "op" and value == "(":
            node = self._expr()
            closing = self._take()
            if closing != ("op", ")"):
                raise SyntaxError("括号没有闭合")
            return node
        raise SyntaxError(f"这里不能出现 '{value}'")


def _contains_x(node):
    kind = node[0]
    if kind == "var":
        return True
    if kind == "num":
        return False
    if kind == "neg":
        return _contains_x(node[1])
    if kind == "bin":
        return _contains_x(node[2]) or _contains_x(node[3])
    if kind == "pow":
        return _contains_x(node[1])
    if kind == "call":
        return _contains_x(node[2])
    raise ValueError(f"未知节点类型: {kind}")


def _as_exponent(node):
    """指数必须是整数常量，定点运算没有开方。"""
    if _contains_x(node):
        raise SyntaxError("指数里不能出现 x")
    value = float_eval(node, 0.0)
    if abs(value - round(value)) > 1e-9:
        raise SyntaxError("指数只支持整数")
    exponent = int(round(value))
    if abs(exponent) > MAX_POWER:
        raise SyntaxError(f"指数绝对值不能超过 {MAX_POWER}")
    return exponent


def parse(text):
    """中缀表达式 -> 语法树。"""
    return _ExprParser(_with_implicit_mul(tokenize(text))).parse()


# 求值：浮点参考实现与定点实现


def float_eval(node, x):
    kind = node[0]
    if kind == "num":
        return node[1]
    if kind == "var":
        return x
    if kind == "neg":
        return -float_eval(node[1], x)
    if kind == "bin":
        operator = node[1]
        left = float_eval(node[2], x)
        right = float_eval(node[3], x)
        if operator == "+":
            return left + right
        if operator == "-":
            return left - right
        if operator == "*":
            return left * right
        if right == 0:
            raise ZeroDivisionError("除以零")
        return left / right
    if kind == "pow":
        base = float_eval(node[1], x)
        exponent = node[2]
        if base == 0 and exponent < 0:
            raise ZeroDivisionError("0 的负数次幂")
        return base ** exponent
    if kind == "call":
        name = node[1]
        value = float_eval(node[2], x)
        if name == "sin":
            return math.sin(value)
        if name == "cos":
            return math.cos(value)
        if name == "tan":
            return math.tan(value)
        if name == "abs":
            return abs(value)
        if value < 0:
            raise ValueError("负数不能开平方")
        return math.sqrt(value)
    raise ValueError(f"未知节点类型: {kind}")


def _fixed_sin(value):
    """定点正弦：先把角度归约到 [-π/2, π/2]，再展开泰勒级数。"""
    turns = value // TWO_PI_FIXED
    angle = value - turns * TWO_PI_FIXED
    if angle > PI_FIXED:
        angle -= TWO_PI_FIXED
    if angle > HALF_PI_FIXED:
        angle = PI_FIXED - angle
    if angle < -HALF_PI_FIXED:
        angle = -PI_FIXED - angle

    total = angle
    term = angle
    square = angle * angle // SCALE
    for index, divisor in enumerate((6, 20, 42, 72, 110)):
        term = term * square // (SCALE * divisor)
        total = total - term if index % 2 == 0 else total + term
    return total


def _fixed_sqrt(value):
    """定点开方：牛顿迭代，初值取 (x+1)/2 让大小数都收敛得动。"""
    if value <= 0:
        return 0
    guess = (value + SCALE) // 2
    for _ in range(SQRT_STEPS):
        guess = (guess + value * SCALE // guess) // 2
    return guess


def fixed_eval(node, x_fixed):
    """定点求值，运算顺序与 emit 生成的指令序列逐位对齐。"""
    kind = node[0]
    if kind == "num":
        return int(round(node[1] * SCALE))
    if kind == "var":
        return x_fixed
    if kind == "neg":
        return -fixed_eval(node[1], x_fixed)
    if kind == "bin":
        operator = node[1]
        left = fixed_eval(node[2], x_fixed)
        right = fixed_eval(node[3], x_fixed)
        if operator == "+":
            return left + right
        if operator == "-":
            return left - right
        if operator == "*":
            return left * right // SCALE
        if right == 0:
            raise ZeroDivisionError("除以零")
        return left * SCALE // right
    if kind == "pow":
        base = node[1]
        exponent = node[2]
        if exponent == 0:
            return SCALE
        value = fixed_eval(base, x_fixed)
        if exponent > 0:
            for _ in range(exponent - 1):
                value = value * fixed_eval(base, x_fixed) // SCALE
            return value
        for _ in range(-exponent - 1):
            value = value * fixed_eval(base, x_fixed) // SCALE
        if value == 0:
            raise ZeroDivisionError("除以零")
        return SCALE * SCALE // value
    if kind == "call":
        name = node[1]
        value = fixed_eval(node[2], x_fixed)
        if name == "sin":
            return _fixed_sin(value)
        if name == "cos":
            return _fixed_sin(value + HALF_PI_FIXED)
        if name == "tan":
            cosine = _fixed_sin(value + HALF_PI_FIXED)
            if cosine == 0:
                raise ZeroDivisionError("tan 在这一点无定义")
            return _fixed_sin(value) * SCALE // cosine
        if name == "abs":
            return value if value >= 0 else -value
        return _fixed_sqrt(value)
    raise ValueError(f"未知节点类型: {kind}")


# 编译成 ChickenStack 后缀代码


def _literal(value):
    """ChickenStack 用 ~ 表示负数，-5 必须写成 ~5。"""
    return f"~{-value}" if value < 0 else str(value)


def _emit_power(base, exponent, out):
    if exponent == 0:
        out.append(str(SCALE))
        return
    if exponent > 0:
        emit(base, out)
        for _ in range(exponent - 1):
            emit(base, out)
            out.extend(["*", str(SCALE), "/"])
        return
    emit(base, out)
    for _ in range(-exponent - 1):
        emit(base, out)
        out.extend(["*", str(SCALE), "/"])
    out.extend([str(SCALE), str(SCALE), "*", "\\", "/"])


def _emit_sin_body(out):
    """栈顶是角度，算完后栈顶是正弦。R/Q/T/A 四个寄存器供函数内部专用。"""
    out.append("R")
    out.extend(["r", str(TWO_PI_FIXED), "/", str(TWO_PI_FIXED), "*", "~", "r", "+", "R"])
    out.extend(["r", str(PI_FIXED), ">", "{", "r", str(TWO_PI_FIXED), "-", "R", "|", "}"])
    out.extend(["r", str(HALF_PI_FIXED), ">", "{", str(PI_FIXED), "r", "-", "R", "|", "}"])
    out.extend([
        "r", _literal(-HALF_PI_FIXED), ">", "{", "|",
        _literal(-PI_FIXED), "r", "-", "R", "}",
    ])
    out.extend(["r", "T"])
    out.extend(["r", "A"])
    out.extend(["r", "r", "*", str(SCALE), "/", "Q"])
    for index, divisor in enumerate((6, 20, 42, 72, 110)):
        out.extend(["t", "q", "*", str(SCALE * divisor), "/", "T"])
        out.extend(["a", "t", "-" if index % 2 == 0 else "+", "A"])
    out.append("a")


def _emit_sqrt_body(out):
    """栈顶是非负数，用牛顿迭代求平方根；负数按 0 处理。"""
    out.append("R")
    out.extend(["r", "0", ">", "{"])
    out.extend(["r", str(SCALE), "+", "2", "/", "T"])
    for _ in range(SQRT_STEPS):
        out.extend(["t", "r", str(SCALE), "*", "t", "/", "+", "2", "/", "T"])
    out.append("t")
    out.extend(["|", "0", "}"])


def _emit_call(name, argument, out):
    emit(argument, out)
    if name == "abs":
        out.extend(["R", "r", "0", ">", "{", "r", "|", "r", "~", "}"])
    elif name == "sqrt":
        _emit_sqrt_body(out)
    elif name == "sin":
        _emit_sin_body(out)
    elif name == "cos":
        out.extend([str(HALF_PI_FIXED), "+"])
        _emit_sin_body(out)
    else:  # tan = sin / cos
        emit(("call", "sin", argument), out)
        out.extend([str(SCALE), "*"])
        emit(("call", "cos", argument), out)
        out.append("/")


def emit(node, out=None):
    """语法树 -> ChickenStack 指令列表，所有中间值都是放大 SCALE 倍的定点数。"""
    if out is None:
        out = []
    kind = node[0]
    if kind == "num":
        out.append(_literal(int(round(node[1] * SCALE))))
    elif kind == "var":
        out.append("x")
    elif kind == "neg":
        emit(node[1], out)
        out.append("~")
    elif kind == "bin":
        operator = node[1]
        if operator in "+-":
            emit(node[2], out)
            emit(node[3], out)
            out.append(operator)
        elif operator == "*":
            emit(node[2], out)
            emit(node[3], out)
            out.extend(["*", str(SCALE), "/"])
        else:
            emit(node[2], out)
            out.extend([str(SCALE), "*"])
            emit(node[3], out)
            out.append("/")
    elif kind == "pow":
        _emit_power(node[1], node[2], out)
    elif kind == "call":
        _emit_call(node[1], node[2], out)
    else:
        raise ValueError(f"未知节点类型: {kind}")
    return out


def grid(x_min, x_max, count):
    """返回定点化的起点与步长。"""
    step = (x_max - x_min) / (count - 1)
    return int(round(x_min * SCALE)), int(round(step * SCALE))


def build_program(node, x0, step_i, k_start, k_stop):
    """生成采样程序：k 从 k_start 循环到 k_stop，每轮输出一行 "x y"。"""
    body = " ".join(emit(node))
    lines = [
        f"{k_start} K",
        "1",
        "[",
        "  $",
        f"  {_literal(x0)} {step_i} k * + X",
        f"  {body}",
        "  Y",
        "  x .",
        "  y .",
        '  10 "',
        "  k 1 + K",
        f"  k {k_stop} > 0 =",
        "]",
        "$",
    ]
    return "\n".join(lines)


def _run_program(code):
    """交给 ChickenStack 执行，把 "x y" 格式的输出解析成浮点坐标。"""
    with _SAMPLE_LOCK:
        interpreter = ChickenStackInterpreter(max_iterations=5_000_000)
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            interpreter.run(code, verbose=False)
    text = buffer.getvalue()
    if "运行错误" in text:
        detail = text.split("运行错误:", 1)[-1].splitlines()[0].strip()
        raise RuntimeError(detail)
    points = []
    for line in text.splitlines():
        parts = line.split()
        if len(parts) == 2:
            points.append((int(parts[0]) / SCALE, int(parts[1]) / SCALE))
    return points


def sample(node, x_min, x_max, count=DEFAULT_COUNT):
    """
    采样 count 个点，返回 [(x, y), ...]，无法求值的位置为 None。

    先用定点预演找出除零点，把区间切成若干段分别交给 ChickenStack，
    这样 1/x 这类函数能画出两侧分支而不是从中间连一条假线。
    """
    if not x_max > x_min:
        raise ValueError("x 的上限必须大于下限")
    if count < 2:
        raise ValueError("采样点至少要 2 个")

    x0, step_i = grid(x_min, x_max, count)
    alive = []
    for k in range(count):
        x_fixed = x0 + k * step_i
        try:
            fixed_eval(node, x_fixed)
            alive.append(True)
        except (ZeroDivisionError, OverflowError):
            alive.append(False)

    segments = []
    k = 0
    while k < count:
        if not alive[k]:
            k += 1
            continue
        start = k
        while k + 1 < count and alive[k + 1]:
            k += 1
        segments.append((start, k))
        k += 1

    if not segments:
        raise ValueError("整个区间都无法求值，检查是不是处处除以零")

    points = []
    cursor = 0
    for start, stop in segments:
        while cursor < start:
            points.append(None)
            cursor += 1
        chunk = _run_program(build_program(node, x0, step_i, start, stop))
        expected = stop - start + 1
        if len(chunk) != expected:
            raise RuntimeError(f"采样点数量不符：期望 {expected}，实得 {len(chunk)}")
        points.extend(chunk)
        cursor = stop + 1
    while cursor < count:
        points.append(None)
        cursor += 1
    return points


# HTTP 服务


def _error(message):
    return {"ok": False, "error": message}


def handle_plot(query):
    """处理一次绘图请求，返回可直接序列化的字典。"""
    expression = (query.get("expr") or [""])[0].strip()
    if not expression:
        return _error("表达式是空的")
    try:
        x_min = float((query.get("xmin") or ["-5"])[0])
        x_max = float((query.get("xmax") or ["5"])[0])
        count = int((query.get("n") or [str(DEFAULT_COUNT)])[0])
    except ValueError:
        return _error("区间参数不是数字")
    if not (math.isfinite(x_min) and math.isfinite(x_max)):
        return _error("区间参数不是有效数字")
    if not x_max > x_min:
        return _error("x 的上限必须大于下限")
    if x_max - x_min > 1e6:
        return _error("x 区间太大，缩小一点")
    count = max(2, min(count, MAX_COUNT))

    started = time.perf_counter()
    try:
        node = parse(expression)
        points = sample(node, x_min, x_max, count)
    except SyntaxError as exc:
        return _error(f"语法错误：{exc}")
    except ZeroDivisionError:
        return _error("整个区间都除以零")
    except (ValueError, RuntimeError) as exc:
        return _error(str(exc))
    elapsed = (time.perf_counter() - started) * 1000

    x0, step_i = grid(x_min, x_max, count)
    code = build_program(node, x0, step_i, 0, count - 1)

    return {
        "ok": True,
        "expr": expression,
        "xmin": x_min,
        "xmax": x_max,
        "count": count,
        "ms": round(elapsed, 2),
        "tokens": len(code.split()),
        "code": code,
        "points": [None if p is None else [round(p[0], 6), round(p[1], 6)] for p in points],
    }


class PlotHandler(BaseHTTPRequestHandler):
    server_version = "ChickenStackPlot/1.0"

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            self._reply(200, "text/html; charset=utf-8", PAGE.encode("utf-8"))
            return
        if parsed.path == "/api/plot":
            payload = handle_plot(parse_qs(parsed.query))
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self._reply(200, "application/json; charset=utf-8", body)
            return
        self._reply(404, "text/plain; charset=utf-8", "找不到这个地址".encode("utf-8"))

    def _reply(self, status, content_type, body):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass


PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>实时函数绘图 · ChickenStack</title>
<style>
  *, *::before, *::after { box-sizing: border-box; }
  :root { color-scheme: light; }
  body {
    margin: 0; background: #eef1f6; color: #111827;
    font-family: "Microsoft YaHei", "PingFang SC", system-ui, -apple-system, sans-serif;
    -webkit-font-smoothing: antialiased;
  }
  .shell { max-width: 1020px; margin: 0 auto; padding: 30px 18px 48px; }
  header h1 { margin: 0 0 6px; font-size: 21px; font-weight: 700; letter-spacing: .2px; }
  header p { margin: 0 0 8px; font-size: 13px; color: #6b7280; }
  header p.hint { margin: 0 0 18px; font-size: 12.5px; color: #9aa3af; line-height: 1.65; }
  header p.hint b { color: #6b7280; font-weight: 600; font-family: ui-monospace, Consolas, monospace; }
  .card {
    background: #fff; border-radius: 16px; padding: 18px 18px 14px;
    box-shadow: 0 12px 34px rgba(15, 23, 42, .07);
  }
  .bar { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }
  #expr {
    flex: 1 1 340px; min-width: 200px;
    font: 16px/1.35 ui-monospace, "Cascadia Mono", Consolas, "Courier New", monospace;
    color: #111827; background: #fbfcfe;
    padding: 11px 14px; border: 2px solid #e2e6ee; border-radius: 11px;
    outline: none; transition: border-color .15s ease, box-shadow .15s ease;
  }
  #expr:focus { border-color: #d9480f; box-shadow: 0 0 0 3px rgba(217, 72, 15, .13); }
  #expr.bad { border-color: #dc2626; box-shadow: 0 0 0 3px rgba(220, 38, 38, .12); }
  .rng { display: flex; align-items: center; gap: 6px; font-size: 13px; color: #4b5563; }
  .rng input {
    width: 76px; font: 14px ui-monospace, Consolas, monospace; color: #111827;
    padding: 8px 9px; border: 1.5px solid #e2e6ee; border-radius: 9px;
    background: #fbfcfe; outline: none; transition: border-color .15s;
  }
  .rng input:focus { border-color: #d9480f; }
  .presets { display: flex; gap: 8px; flex-wrap: wrap; margin: 14px 0 4px; }
  .presets button {
    font: 13px/1 "Microsoft YaHei", system-ui, sans-serif;
    color: #475569; background: #f3f5f9; border: 1px solid #e5e9f0;
    padding: 7px 12px; border-radius: 999px; cursor: pointer;
    transition: background .15s, color .15s, border-color .15s;
  }
  .presets button:hover { background: #fdf1ea; color: #c2410c; border-color: #f6d0bb; }
  #stage { margin-top: 8px; }
  #stage svg { width: 100%; height: auto; display: block; }
  .status { margin-top: 6px; font-size: 12.5px; color: #6b7280; min-height: 19px; }
  .status.err { color: #dc2626; }
  details.code { margin-top: 10px; border-top: 1px solid #eef1f6; padding-top: 10px; }
  details.code summary {
    cursor: pointer; font-size: 12.5px; color: #6b7280; outline: none;
    list-style: none; user-select: none;
  }
  details.code summary::-webkit-details-marker { display: none; }
  details.code summary::before { content: "\\25B8  "; color: #9aa3af; }
  details.code[open] summary::before { content: "\\25BE  "; }
  details.code pre {
    margin: 10px 0 0; padding: 12px 14px; border-radius: 10px;
    background: #0f172a; color: #e2e8f0;
    font: 12.5px/1.65 ui-monospace, Consolas, monospace;
    overflow-x: auto; white-space: pre;
  }
</style>
</head>
<body>
<div class="shell">
  <header>
    <h1>实时函数绘图</h1>
    <p>输入表达式即可看到曲线：后缀代码由 Python 生成，每个采样点由 ChickenStack 虚拟机求值</p>
    <p class="hint">支持 + - * / ^、括号、隐式乘法（2x、3(x+1)），以及 <b>sin</b> <b>cos</b> <b>tan</b> <b>sqrt</b> <b>abs</b> —— 这些函数同样由 ChickenStack 用定点运算算出，Python 只负责翻译</p>
  </header>
  <div class="card">
    <div class="bar">
      <input id="expr" value="x^2 - 2x - 3" spellcheck="false" autocomplete="off" placeholder="例如 x^3 - 3x">
      <div class="rng">
        <span>x</span>
        <input id="xmin" type="number" value="-5" step="0.5">
        <span>到</span>
        <input id="xmax" type="number" value="5" step="0.5">
      </div>
    </div>
    <div class="presets" id="presets"></div>
    <div id="stage"></div>
    <div class="status" id="status">准备就绪</div>
    <details class="code">
      <summary>看看它编译出来的 ChickenStack 源码</summary>
      <pre id="code"></pre>
    </details>
  </div>
</div>
<script>
const W = 960, H = 540, PL = 68, PR = 28, PT = 26, PB = 56;

const exprEl = document.getElementById('expr');
const xminEl = document.getElementById('xmin');
const xmaxEl = document.getElementById('xmax');
const stageEl = document.getElementById('stage');
const statusEl = document.getElementById('status');
const codeEl = document.getElementById('code');

let timer = null;
let view = null;
let current = null;

function niceStep(span, target) {
  const raw = span / target;
  if (!(raw > 0)) return 1;
  const mag = Math.pow(10, Math.floor(Math.log10(raw)));
  const n = raw / mag;
  return (n <= 1 ? 1 : n <= 2 ? 2 : n <= 5 ? 5 : 10) * mag;
}

function fmt(v) {
  if (Math.abs(v) < 1e-9) return '0';
  const a = Math.abs(v);
  if (a >= 100000 || a < 0.001) return v.toExponential(1);
  return String(Math.round(v * 1000) / 1000);
}

function showError(msg) {
  exprEl.classList.add('bad');
  statusEl.className = 'status err';
  statusEl.textContent = msg;
}

function render(data) {
  const pts = data.points;
  const xs = [], ys = [];
  for (const p of pts) { if (p) { xs.push(p[0]); ys.push(p[1]); } }
  if (!ys.length) { showError('区间里没有有效点'); return; }
  ys.sort((a, b) => a - b);

  let xLo = Math.min(data.xmin, ...xs);
  let xHi = Math.max(data.xmax, ...xs);
  if (xHi - xLo < 1e-9) { xLo -= 1; xHi += 1; }

  const qLo = ys[Math.floor(ys.length * 0.02)];
  const qHi = ys[Math.min(ys.length - 1, Math.ceil(ys.length * 0.98))];
  let yLo = ys[0], yHi = ys[ys.length - 1];
  const full = yHi - yLo, tight = qHi - qLo;
  if (tight > 0 && full > 8 * tight) { yLo = qLo - tight * 0.25; yHi = qHi + tight * 0.25; }
  if (yHi - yLo < 1e-9) { yLo -= 1; yHi += 1; }
  const padY = (yHi - yLo) * 0.06;
  yLo -= padY;
  yHi += padY;

  const pw = W - PL - PR, ph = H - PT - PB;
  const sx = (x) => PL + (x - xLo) / (xHi - xLo) * pw;
  const sy = (y) => PT + (yHi - y) / (yHi - yLo) * ph;
  view = { sx, sy, xLo, xHi, yLo, yHi, pw, ph };

  const out = [];
  out.push('<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="函数图像">');
  out.push('<defs><clipPath id="clip"><rect x="' + PL + '" y="' + PT + '" width="' + pw + '" height="' + ph + '"/></clipPath></defs>');
  out.push('<rect width="' + W + '" height="' + H + '" fill="#ffffff"/>');

  const stx = niceStep(xHi - xLo, 10);
  const sty = niceStep(yHi - yLo, 8);
  for (let i = Math.ceil(xLo / stx); i <= Math.floor(xHi / stx); i++) {
    const v = i * stx, X = sx(v);
    out.push('<line x1="' + X.toFixed(1) + '" y1="' + PT + '" x2="' + X.toFixed(1) + '" y2="' + (PT + ph) + '" stroke="#eceff4" stroke-width="1"/>');
    out.push('<text x="' + X.toFixed(1) + '" y="' + (PT + ph + 20) + '" text-anchor="middle" font-size="11.5" fill="#9aa3af">' + fmt(v) + '</text>');
  }
  for (let i = Math.ceil(yLo / sty); i <= Math.floor(yHi / sty); i++) {
    const v = i * sty, Y = sy(v);
    out.push('<line x1="' + PL + '" y1="' + Y.toFixed(1) + '" x2="' + (PL + pw) + '" y2="' + Y.toFixed(1) + '" stroke="#eceff4" stroke-width="1"/>');
    out.push('<text x="' + (PL - 10) + '" y="' + (Y + 4).toFixed(1) + '" text-anchor="end" font-size="11.5" fill="#9aa3af">' + fmt(v) + '</text>');
  }

  if (yLo <= 0 && 0 <= yHi) {
    const Y = sy(0);
    out.push('<line x1="' + PL + '" y1="' + Y.toFixed(1) + '" x2="' + (PL + pw) + '" y2="' + Y.toFixed(1) + '" stroke="#b6bec9" stroke-width="1.4"/>');
  }
  if (xLo <= 0 && 0 <= xHi) {
    const X = sx(0);
    out.push('<line x1="' + X.toFixed(1) + '" y1="' + PT + '" x2="' + X.toFixed(1) + '" y2="' + (PT + ph) + '" stroke="#b6bec9" stroke-width="1.4"/>');
  }

  let d = '', pen = false;
  for (const p of pts) {
    if (!p) { pen = false; continue; }
    const X = sx(p[0]).toFixed(2), Y = sy(p[1]).toFixed(2);
    d += pen ? 'L' + X + ' ' + Y : 'M' + X + ' ' + Y;
    pen = true;
  }
  out.push('<path d="' + d + '" fill="none" stroke="#d9480f" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" clip-path="url(#clip)"/>');

  // 极值点与零点
  const extrema = [], zeros = [];
  for (let i = 1; i < pts.length - 1; i++) {
    const a = pts[i - 1], b = pts[i], c = pts[i + 1];
    if (!a || !b || !c) continue;
    const before = b[1] - a[1], after = c[1] - b[1];
    if (before * after < 0) extrema.push({ point: b, top: before > 0 });
  }
  for (let i = 0; i < pts.length - 1; i++) {
    const a = pts[i], b = pts[i + 1];
    if (!a || !b) continue;
    if (a[1] === 0) {
      if (!zeros.length || Math.abs(zeros[zeros.length - 1] - a[0]) > 1e-9) zeros.push(a[0]);
    } else if ((a[1] < 0) !== (b[1] < 0)) {
      zeros.push(a[0] + (b[0] - a[0]) * (a[1] / (a[1] - b[1])));
    }
  }

  if (extrema.length <= 8) {
    for (const item of extrema) {
      out.push(
        '<circle cx="' + sx(item.point[0]).toFixed(1) + '" cy="' + sy(item.point[1]).toFixed(1) +
        '" r="3.6" fill="' + (item.top ? '#1d4ed8' : '#7c3aed') +
        '" stroke="#ffffff" stroke-width="1.4" clip-path="url(#clip)"/>'
      );
    }
  }
  if (zeros.length <= 8) {
    for (const value of zeros) {
      out.push(
        '<circle cx="' + sx(value).toFixed(1) + '" cy="' + sy(0).toFixed(1) +
        '" r="3.4" fill="#059669" stroke="#ffffff" stroke-width="1.2" clip-path="url(#clip)"/>'
      );
    }
  }

  out.push('<rect x="' + PL + '" y="' + PT + '" width="' + pw + '" height="' + ph + '" fill="none" stroke="#dde2ea"/>');

  out.push('<g id="cursor" style="display:none">');
  out.push('<line id="ctangent" stroke="#1d4ed8" stroke-width="1.4" stroke-dasharray="6 4" clip-path="url(#clip)"/>');
  out.push('<line id="cvline" y1="' + PT + '" y2="' + (PT + ph) + '" stroke="#d9480f" stroke-width="1" stroke-dasharray="4 4"/>');
  out.push('<circle id="cdot" r="4" fill="#d9480f" stroke="#fff" stroke-width="2"/>');
  out.push('<rect id="ctagbg" rx="6" ry="6" fill="#111827" opacity="0.92"/>');
  out.push('<text id="ctagtext" font-size="12" fill="#ffffff" font-family="ui-monospace, Consolas, monospace"></text>');
  out.push('</g>');
  out.push('</svg>');

  stageEl.innerHTML = out.join('');
  bindHover();
  return { extrema: extrema.length, zeros: zeros.length };
}

function bindHover() {
  const svg = stageEl.querySelector('svg');
  if (!svg) return;
  const cursor = svg.querySelector('#cursor');
  const vline = svg.querySelector('#cvline');
  const dot = svg.querySelector('#cdot');
  const tangent = svg.querySelector('#ctangent');
  const tagbg = svg.querySelector('#ctagbg');
  const tagtext = svg.querySelector('#ctagtext');

  svg.addEventListener('mousemove', (ev) => {
    if (!view || !current) return;
    const box = svg.getBoundingClientRect();
    const mx = (ev.clientX - box.left) / box.width * W;
    const my = (ev.clientY - box.top) / box.height * H;
    if (mx < PL || mx > PL + view.pw || my < PT || my > PT + view.ph) {
      cursor.style.display = 'none';
      return;
    }
    const xVal = view.xLo + (mx - PL) / view.pw * (view.xHi - view.xLo);
    let best = null, bestD = Infinity;
    for (const p of current.points) {
      if (!p) continue;
      const d = Math.abs(p[0] - xVal);
      if (d < bestD) { bestD = d; best = p; }
    }
    if (!best) { cursor.style.display = 'none'; return; }

    const X = view.sx(best[0]), Y = view.sy(best[1]);
    cursor.style.display = '';
    vline.setAttribute('x1', X); vline.setAttribute('x2', X);
    dot.setAttribute('cx', X); dot.setAttribute('cy', Y);

    const index = current.points.indexOf(best);
    let slope = null;
    if (index > 0 && index < current.points.length - 1) {
      const back = current.points[index - 1], ahead = current.points[index + 1];
      if (back && ahead && ahead[0] !== back[0]) {
        slope = (ahead[1] - back[1]) / (ahead[0] - back[0]);
      }
    }
    if (slope !== null && isFinite(slope)) {
      const reach = (view.xHi - view.xLo) * 0.11;
      tangent.setAttribute('x1', view.sx(best[0] - reach));
      tangent.setAttribute('y1', view.sy(best[1] - slope * reach));
      tangent.setAttribute('x2', view.sx(best[0] + reach));
      tangent.setAttribute('y2', view.sy(best[1] + slope * reach));
      tangent.style.display = '';
    } else {
      tangent.style.display = 'none';
    }

    let label = '(' + fmt(best[0]) + ', ' + fmt(best[1]) + ')';
    if (slope !== null && isFinite(slope)) label += '  斜率 ' + fmt(slope);
    tagtext.textContent = label;
    const w = label.length * 7.2 + 16;
    let tx = X + 12, ty = Y - 32;
    if (tx + w > PL + view.pw) tx = X - w - 12;
    if (ty < PT + 4) ty = Y + 14;
    tagbg.setAttribute('x', tx); tagbg.setAttribute('y', ty);
    tagbg.setAttribute('width', w); tagbg.setAttribute('height', 24);
    tagtext.setAttribute('x', tx + 8); tagtext.setAttribute('y', ty + 16.5);
  });

  svg.addEventListener('mouseleave', () => { cursor.style.display = 'none'; });
}

async function refresh() {
  const expr = exprEl.value.trim();
  const xmin = parseFloat(xminEl.value);
  const xmax = parseFloat(xmaxEl.value);
  if (!expr) { showError('先输入一个表达式'); return; }
  if (!isFinite(xmin) || !isFinite(xmax)) { showError('区间要填数字'); return; }
  if (xmax <= xmin) { showError('x 的上限要大于下限'); return; }

  const query = 'expr=' + encodeURIComponent(expr) + '&xmin=' + xmin + '&xmax=' + xmax;
  try {
    const res = await fetch('/api/plot?' + query, { cache: 'no-store' });
    const data = await res.json();
    if (!data.ok) { showError(data.error); return; }
    exprEl.classList.remove('bad');
    current = data;
    const marks = render(data);
    statusEl.className = 'status';
    let status = '采样 ' + data.count + ' 点 · 编译出 ' + data.tokens + ' 条指令 · 求值 ' + data.ms.toFixed(1) + ' ms';
    if (marks && marks.extrema && marks.extrema <= 8) status += ' · 极值 ' + marks.extrema + ' 个';
    if (marks && marks.zeros && marks.zeros <= 8) status += ' · 零点 ' + marks.zeros + ' 个';
    statusEl.textContent = status;
    codeEl.textContent = data.code;
    history.replaceState(null, '', '?expr=' + encodeURIComponent(expr) + '&xmin=' + xmin + '&xmax=' + xmax);
  } catch (err) {
    showError('请求失败：' + err);
  }
}

function schedule() {
  clearTimeout(timer);
  timer = setTimeout(refresh, 110);
}

const PRESETS = [
  ['x^2 - 2x - 3', '抛物线', -5, 5],
  ['sin(x)', '正弦波', -6.3, 6.3],
  ['sin(x)/x', '辛格函数', -15, 15],
  ['sin(x^2)', '调频波', -8, 8],
  ['abs(sin(x))', '整流波', -6.3, 6.3],
  ['sin(x)+sin(3x)/3+sin(5x)/5', '方波逼近', -9.4, 9.4],
  ['sqrt(x)', '开方', -1, 9],
  ['1/x', '双曲线', -4, 4],
  ['(x-1)(x+2)(x-3)', '三个根', -3.5, 3.5]
];

const presetsEl = document.getElementById('presets');
for (const item of PRESETS) {
  const button = document.createElement('button');
  button.textContent = item[0];
  button.title = item[1];
  button.onclick = () => {
    exprEl.value = item[0];
    xminEl.value = item[2];
    xmaxEl.value = item[3];
    clearTimeout(timer);
    refresh();
  };
  presetsEl.appendChild(button);
}

const params = new URLSearchParams(location.search);
if (params.get('expr')) exprEl.value = params.get('expr');
if (params.get('xmin')) xminEl.value = params.get('xmin');
if (params.get('xmax')) xmaxEl.value = params.get('xmax');

exprEl.addEventListener('input', schedule);
xminEl.addEventListener('input', schedule);
xmaxEl.addEventListener('input', schedule);
exprEl.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') { clearTimeout(timer); refresh(); }
});

refresh();
</script>
</body>
</html>"""


def main():
    args = sys.argv[1:]
    open_browser = "--no-browser" not in args
    args = [item for item in args if item != "--no-browser"]

    port = DEFAULT_PORT
    if args:
        try:
            port = int(args[0])
        except ValueError:
            print(f"端口参数不是整数: {args[0]}")
            return

    try:
        server = ThreadingHTTPServer(("127.0.0.1", port), PlotHandler)
    except OSError as exc:
        print(f"端口 {port} 用不了: {exc}")
        print(f"换一个端口: py examples/live_plot.py {port + 1}")
        return

    url = f"http://127.0.0.1:{port}"
    print(f"实时函数绘图已启动: {url}")
    print("在页面里输入表达式即可看到曲线，Ctrl+C 停止")
    if open_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

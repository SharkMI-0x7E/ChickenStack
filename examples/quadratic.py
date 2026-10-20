"""
二次函数可视化：核心采样在 examples/quadratic.ch，Python 负责输入、坐标轴与中文标注。

运行:
  py examples/quadratic.py
  py examples/quadratic.py 1 -2 -3 -5 5
"""

import contextlib
import html
import io
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import ChickenStackInterpreter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "examples", "quadratic.ch")
OUTPUT = os.path.join(ROOT, "examples", "quadratic_plot.html")
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
            try:
                points.append((int(parts[0]) / SCALE, int(parts[1]) / SCALE))
            except ValueError:
                pass
    return points


def fmt(value):
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.2f}".rstrip("0").rstrip(".")


def format_equation(a, b, c):
    if a == 0:
        parts = ["y ="]
        if b:
            parts.append(f"{'' if b > 0 else '-'}{fmt(abs(b))}x")
        if c:
            parts.append(f"{'+' if c > 0 else '-'} {fmt(abs(c))}")
        return " ".join(parts) if len(parts) > 1 else "y = 0"

    def coef(value):
        return "" if value == 1 else "-" if value == -1 else str(value)

    parts = [f"y = {coef(a)}x²"]
    if b:
        parts.append(f"{'+' if b > 0 else '-'} {coef(abs(b))}x")
    if c:
        parts.append(f"{'+' if c > 0 else '-'} {fmt(abs(c))}")
    return " ".join(parts)


def nice_step(span):
    raw = span / 10
    if raw <= 0:
        return 1
    mag = 10 ** math.floor(math.log10(raw))
    for multiple in (1, 2, 5, 10):
        if raw <= multiple * mag:
            return multiple * mag
    return 10 * mag


def ticks(lo, hi):
    step = nice_step(hi - lo)
    start = math.ceil(lo / step) * step
    values = []
    value = start
    while value <= hi + 1e-9:
        values.append(round(value, 10))
        value += step
    return values


def build_svg(a, b, c, points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    if y_max - y_min < 1:
        mid = (y_max + y_min) / 2
        y_min, y_max = mid - 0.5, mid + 0.5
    pad_x = (x_max - x_min) * 0.05 or 1
    pad_y = (y_max - y_min) * 0.10 or 1
    x_min -= pad_x
    x_max += pad_x
    y_min -= pad_y
    y_max += pad_y

    width, height = 900, 600
    left, right, top, bottom = 70, 40, 50, 70
    plot_w = width - left - right
    plot_h = height - top - bottom

    def sx(x):
        return left + (x - x_min) / (x_max - x_min) * plot_w

    def sy(y):
        return top + (y_max - y) / (y_max - y_min) * plot_h

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="100%" role="img" aria-label="二次函数图像">',
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>',
    ]

    for x in ticks(x_min, x_max):
        px = sx(x)
        parts.append(
            f'<line x1="{px:.1f}" y1="{top}" x2="{px:.1f}" y2="{top + plot_h}" '
            f'stroke="#e6e9ef" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{px:.1f}" y="{top + plot_h + 22}" text-anchor="middle" '
            f'font-size="12" fill="#6b7280">{fmt(x)}</text>'
        )
    for y in ticks(y_min, y_max):
        py = sy(y)
        parts.append(
            f'<line x1="{left}" y1="{py:.1f}" x2="{left + plot_w}" y2="{py:.1f}" '
            f'stroke="#e6e9ef" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{left - 10}" y="{py + 4:.1f}" text-anchor="end" '
            f'font-size="12" fill="#6b7280">{fmt(y)}</text>'
        )

    if x_min <= 0 <= x_max:
        px = sx(0)
        parts.append(
            f'<line x1="{px:.1f}" y1="{top}" x2="{px:.1f}" y2="{top + plot_h}" '
            f'stroke="#374151" stroke-width="1.5"/>'
        )
        parts.append(f'<text x="{px + 8:.1f}" y="{top + 18}" font-size="13" fill="#374151">y</text>')
    if y_min <= 0 <= y_max:
        py = sy(0)
        parts.append(
            f'<line x1="{left}" y1="{py:.1f}" x2="{left + plot_w}" y2="{py:.1f}" '
            f'stroke="#374151" stroke-width="1.5"/>'
        )
        parts.append(
            f'<text x="{left + plot_w - 8:.1f}" y="{py - 8:.1f}" text-anchor="end" '
            f'font-size="13" fill="#374151">x</text>'
        )

    polyline = " ".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in points)
    parts.append(
        f'<polyline points="{polyline}" fill="none" stroke="#d9480f" '
        f'stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'
    )

    if a != 0:
        vx = -b / (2 * a)
        vy = a * vx * vx + b * vx + c
        px, py = sx(vx), sy(vy)
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="#1d4ed8"/>')
        parts.append(
            f'<text x="{px + 9:.1f}" y="{py - 9:.1f}" font-size="13" fill="#1d4ed8">'
            f"顶点 ({fmt(vx)}, {fmt(vy)})</text>"
        )
        disc = b * b - 4 * a * c
        if disc >= 0:
            roots = [(-b - math.sqrt(disc)) / (2 * a), (-b + math.sqrt(disc)) / (2 * a)]
            for root in roots:
                px, py = sx(root), sy(0)
                parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="#059669"/>')
                parts.append(
                    f'<text x="{px + 7:.1f}" y="{py - 7:.1f}" font-size="12" fill="#059669">'
                    f"根 {fmt(root)}</text>"
                )

    parts.append(
        f'<rect x="{left}" y="{top}" width="{plot_w}" height="{plot_h}" '
        f'fill="none" stroke="#d1d5db" stroke-width="1"/>'
    )
    parts.append(
        f'<text x="{left}" y="30" font-size="20" font-weight="600" fill="#111827">'
        f"二次函数图像</text>"
    )
    parts.append(
        f'<text x="{left + plot_w}" y="30" text-anchor="end" font-size="13" fill="#6b7280">'
        f"核心采样：ChickenStack · 绘图：Python</text>"
    )
    parts.append(
        f'<text x="{left}" y="{top + plot_h + 50}" font-size="16" fill="#111827">'
        f"{html.escape(format_equation(a, b, c))}</text>"
    )
    parts.append("</svg>")
    return "\n".join(parts)


def write_html(svg, title):
    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
  :root {{ color-scheme: light; }}
  body {{ margin: 0; background: #eef1f5; font-family: "Microsoft YaHei", "PingFang SC", system-ui, sans-serif; }}
  .wrap {{ max-width: 960px; margin: 24px auto 8px; background: #fff; border-radius: 14px;
           box-shadow: 0 8px 28px rgba(15, 23, 42, .08); padding: 18px 20px 8px; }}
  .tip {{ max-width: 960px; margin: 0 auto 24px; color: #6b7280; font-size: 13px; text-align: center; }}
</style>
</head>
<body>
<div class="wrap">{svg}</div>
<div class="tip">核心采样由 ChickenStack 完成（0.1 步长），坐标轴与标注由 Python 绘制。</div>
</body>
</html>"""
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(doc)


def ask_int(prompt, default):
    raw = input(f"{prompt} [{default}]: ").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        print("请输入整数，使用默认值")
        return default


def main():
    args = sys.argv[1:]
    if len(args) >= 5:
        try:
            a, b, c, x_min, x_max = (int(v) for v in args[:5])
        except ValueError:
            print("参数必须是 5 个整数: a b c x_min x_max")
            return
    else:
        print("二次函数 y = ax² + bx + c")
        a = ask_int("a", 1)
        b = ask_int("b", -2)
        c = ask_int("c", -3)
        x_min = ask_int("x 最小值", -5)
        x_max = ask_int("x 最大值", 5)

    if x_min > x_max:
        x_min, x_max = x_max, x_min

    points = sample(a, b, c, x_min, x_max)
    if not points:
        print("采样失败：ChickenStack 没有输出有效点")
        return

    write_html(build_svg(a, b, c, points), f"二次函数 {format_equation(a, b, c)}")

    print(f"函数: {format_equation(a, b, c)}")
    if a != 0:
        vx = -b / (2 * a)
        vy = a * vx * vx + b * vx + c
        disc = b * b - 4 * a * c
        print(f"顶点: ({fmt(vx)}, {fmt(vy)})")
        print(f"判别式: {disc}")
        if disc > 0:
            r1 = (-b - math.sqrt(disc)) / (2 * a)
            r2 = (-b + math.sqrt(disc)) / (2 * a)
            print(f"根: {fmt(r1)}, {fmt(r2)}")
        elif disc == 0:
            print(f"根: {fmt(-b / (2 * a))}（重根）")
        else:
            print("根: 无实根")
    else:
        print("a = 0，图像是一条直线")
    print(f"采样点: {len(points)} 个（x 从 {x_min} 到 {x_max}，步长 0.1）")
    print(f"图像: {OUTPUT}")


if __name__ == "__main__":
    main()

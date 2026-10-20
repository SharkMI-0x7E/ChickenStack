"""
ChickenStack 解析器性能基准。

预热后重复测量，报告 median / mean / min / max / std（毫秒）。
只打印结果、不落盘；单机单次测量不足以证明“优化有效”，请勿据此下结论。

运行: py tests/benchmark_parser.py
"""

import os
import statistics
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chicken_stack import Parser

CASES = [
    ("简单数学", "10 20 + ."),
    ("小循环", "5 [ : . 1 - ]"),
    ("中等循环", "100 [ : . 1 - ]"),
    ("字符串", '72 " 101 " 108 " 108 " 111 " 10 "'),
]

WARMUP = 20
REPEATS = 300


def bench(code, repeats, warmup):
    parser = Parser()
    for _ in range(warmup):
        parser.parse(code)
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        parser.parse(code)
        samples.append((time.perf_counter() - start) * 1000)
    samples.sort()
    return samples


def main():
    print(f"解析器基准: warmup={WARMUP}, repeats={REPEATS}")
    print(f"{'case':<10} {'median':>10} {'mean':>10} {'min':>10} {'max':>10} {'std':>10}")
    for name, code in CASES:
        samples = bench(code, REPEATS, WARMUP)
        print(
            f"{name:<10} {statistics.median(samples):>10.4f} "
            f"{statistics.mean(samples):>10.4f} {samples[0]:>10.4f} "
            f"{samples[-1]:>10.4f} {statistics.pstdev(samples):>10.4f}"
        )
    print("\n注：微秒级差异受机器抖动影响，请勿用单次结果证明优化有效。")


if __name__ == "__main__":
    main()

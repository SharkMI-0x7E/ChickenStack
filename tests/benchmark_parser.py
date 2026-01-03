"""
🐔 ChickenStack 解析器性能基准测试
====================================

本脚本用于测试解析器的性能，对比优化前后的解析速度。

## 运行方法

```bash
python tests/benchmark_parser.py
```

## 测试用例

1. 简单数学运算
2. 小循环
3. 中等循环
4. 大循环
5. 字符串打印
"""

import time
import sys
import os
import json
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chicken_stack import Parser


def ensure_results_dir():
    """确保测试结果目录存在"""
    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    return results_dir


def benchmark_parser():
    """运行解析器性能基准测试"""
    parser = Parser()

    # 测试用例
    test_cases = [
        ("简单数学运算", "10 20 + ."),
        ("小循环", "5 [ : . 1 - ]"),
        ("中等循环", "100 [ : . 1 - ]"),
        ("大循环", "1000 [ 1 + ]"),
        ("字符串打印", '72 " 101 " 108 " 108 " 111 " 32 " 87 " 111 " 114 " 108 " 100 " 33 " 10 "'),
    ]

    # 运行20次测试
    num_runs = 20
    all_results = []

    print("ChickenStack 解析器性能基准测试")
    print("=" * 90)
    print(f"测试次数: {num_runs}")
    print("=" * 90)

    for run in range(num_runs):
        print(f"\n[第 {run + 1}/{num_runs} 次测试]")
        run_results = {}

        for name, code in test_cases:
            # 预热
            for _ in range(10):
                parser.parse(code)
                parser.reset()

            # 测试
            iterations = 10000
            start = time.perf_counter()
            for _ in range(iterations):
                parser.parse(code)
                parser.reset()
            elapsed = time.perf_counter() - start

            avg_time = elapsed / iterations * 1000  # 毫秒
            run_results[name] = {
                'avg_time_ms': avg_time,
                'total_time_s': elapsed
            }

        all_results.append(run_results)

    # 计算平均值
    print("\n" + "=" * 90)
    print("[平均结果]")
    print("=" * 90)
    print(f"{'测试用例':<30} {'平均时间 (ms)':<20} {'最小值 (ms)':<20} {'最大值 (ms)':<20}")
    print("=" * 90)

    summary = {}
    for name, code in test_cases:
        times = [run[name]['avg_time_ms'] for run in all_results]
        avg = sum(times) / len(times)
        min_val = min(times)
        max_val = max(times)

        summary[name] = {
            'average_ms': avg,
            'min_ms': min_val,
            'max_ms': max_val,
            'all_values': times
        }

        print(f"{name:<30} {avg:<20.6f} {min_val:<20.6f} {max_val:<20.6f}")

    print("=" * 90)

    # 计算总平均时间
    total_avg = sum(r['average_ms'] for r in summary.values())
    print(f"{'总平均时间':<30} {total_avg:<20.6f}")
    print("=" * 90)

    # 性能评估
    print("\n[性能评估]")
    print("-" * 90)
    if total_avg < 1.0:
        print("[EXCELLENT] 性能优秀！解析速度非常快。")
    elif total_avg < 5.0:
        print("[GOOD] 性能良好！解析速度符合预期。")
    elif total_avg < 10.0:
        print("[AVERAGE] 性能一般。可以考虑进一步优化。")
    else:
        print("[POOR] 性能较差。建议进行性能优化。")
    print("-" * 90)

    # 保存结果到文件
    results_dir = ensure_results_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"benchmark_{timestamp}.json"
    filepath = os.path.join(results_dir, filename)

    result_data = {
        'timestamp': timestamp,
        'num_runs': num_runs,
        'summary': summary,
        'all_runs': all_results,
        'total_average_ms': total_avg
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)

    print(f"\n[结果已保存] {filepath}")


if __name__ == "__main__":
    benchmark_parser()
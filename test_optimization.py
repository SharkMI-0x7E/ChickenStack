"""
简单的解析器测试脚本
验证优化后的解析器是否正常工作
"""

import sys
import os
import json
import time
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def ensure_results_dir():
    """确保测试结果目录存在"""
    results_dir = os.path.join(os.path.dirname(__file__), 'tests', 'results')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    return results_dir


def run_tests():
    """运行测试"""
    from chicken_stack import Parser

    # 测试用例
    test_cases = [
        ("简单数学运算", "10 20 + ."),
        ("循环", "5 [ : . 1 - ]"),
        ("字符串", '72 " 69 " 76 " 76 " 79 "'),
        ("注释", "10 20 + . # 这是一个注释"),
        ("大数字", "999999999 ."),
    ]

    # 运行20次测试
    num_runs = 20
    all_results = []

    print("ChickenStack 解析器优化验证测试")
    print("=" * 90)
    print(f"测试次数: {num_runs}")
    print("=" * 90)

    for run in range(num_runs):
        print(f"\n[第 {run + 1}/{num_runs} 次测试]")
        run_results = {}
        passed = 0
        failed = 0

        try:
            from chicken_stack import Parser

            # 测试 1: 简单数学运算
            parser = Parser()
            start = time.perf_counter()
            tokens = parser.parse("10 20 + .")
            elapsed = time.perf_counter() - start
            run_results['简单数学运算'] = {
                'passed': True,
                'token_count': len(tokens),
                'time_ms': elapsed * 1000
            }
            passed += 1

            # 测试 2: 循环
            parser.reset()
            start = time.perf_counter()
            tokens = parser.parse("5 [ : . 1 - ]")
            elapsed = time.perf_counter() - start
            run_results['循环'] = {
                'passed': True,
                'token_count': len(tokens),
                'loop_table': parser.get_loop_table(),
                'time_ms': elapsed * 1000
            }
            passed += 1

            # 测试 3: 字符串
            parser.reset()
            start = time.perf_counter()
            tokens = parser.parse('72 " 69 " 76 " 76 " 79 "')
            elapsed = time.perf_counter() - start
            run_results['字符串'] = {
                'passed': True,
                'token_count': len(tokens),
                'time_ms': elapsed * 1000
            }
            passed += 1

            # 测试 4: 注释
            parser.reset()
            start = time.perf_counter()
            tokens = parser.parse("10 20 + . # 这是一个注释")
            elapsed = time.perf_counter() - start
            run_results['注释'] = {
                'passed': True,
                'token_count': len(tokens),
                'time_ms': elapsed * 1000
            }
            passed += 1

            # 测试 5: 大数字
            parser.reset()
            start = time.perf_counter()
            tokens = parser.parse("999999999 .")
            elapsed = time.perf_counter() - start
            run_results['大数字'] = {
                'passed': True,
                'token_count': len(tokens),
                'time_ms': elapsed * 1000
            }
            passed += 1

            run_results['summary'] = {
                'passed': passed,
                'failed': failed,
                'total': passed + failed
            }

            print(f"    通过: {passed}/{passed + failed}")

        except Exception as e:
            run_results['error'] = str(e)
            failed += 1
            print(f"    错误: {e}")

        all_results.append(run_results)

    # 计算平均值
    print("\n" + "=" * 90)
    print("[平均结果]")
    print("=" * 90)
    print(f"{'测试用例':<30} {'平均时间 (ms)':<20} {'最小值 (ms)':<20} {'最大值 (ms)':<20}")
    print("=" * 90)

    summary = {}
    for name, code in test_cases:
        times = []
        for run in all_results:
            if name in run and 'time_ms' in run[name]:
                times.append(run[name]['time_ms'])

        if times:
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

    # 统计通过率
    total_passed = sum(r.get('summary', {}).get('passed', 0) for r in all_results)
    total_tests = sum(r.get('summary', {}).get('total', 0) for r in all_results)
    pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

    print(f"\n[通过率] {total_passed}/{total_tests} ({pass_rate:.2f}%)")

    if pass_rate == 100:
        print("\n[SUCCESS] 所有测试通过！解析器优化成功！")
    else:
        print(f"\n[WARNING] 有 {total_tests - total_passed} 个测试失败")

    # 保存结果到文件
    results_dir = ensure_results_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"optimization_{timestamp}.json"
    filepath = os.path.join(results_dir, filename)

    result_data = {
        'timestamp': timestamp,
        'num_runs': num_runs,
        'summary': summary,
        'all_runs': all_results,
        'total_average_ms': total_avg,
        'pass_rate': pass_rate,
        'total_passed': total_passed,
        'total_tests': total_tests
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=2, ensure_ascii=False)

    print(f"\n[结果已保存] {filepath}")


if __name__ == "__main__":
    run_tests()
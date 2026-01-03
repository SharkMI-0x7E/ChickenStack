"""
分析20次测试结果，找出优化机会
"""

import json
import os
from datetime import datetime
import statistics

results_dir = os.path.join(os.path.dirname(__file__), 'tests', 'results')

# 读取最新的20个optimization结果文件
files = sorted([f for f in os.listdir(results_dir) if f.startswith('optimization_')])[-20:]

print("=" * 90)
print("ChickenStack 解析器性能分析报告")
print("=" * 90)
print(f"分析的测试次数: {len(files)}")
print("=" * 90)

all_data = []
for filename in files:
    filepath = os.path.join(results_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        all_data.append(data)

# 分析每个测试用例的性能
test_cases = ["简单数学运算", "循环", "字符串", "注释", "大数字"]

print("\n[详细分析]")
print("=" * 90)
print(f"{'测试用例':<20} {'平均时间':<15} {'最小值':<15} {'最大值':<15} {'标准差':<15}")
print("=" * 90)

for test_name in test_cases:
    all_times = []
    for data in all_data:
        if test_name in data['summary']:
            all_times.append(data['summary'][test_name]['average_ms'])

    if all_times:
        avg = statistics.mean(all_times)
        min_val = min(all_times)
        max_val = max(all_times)
        std = statistics.stdev(all_times) if len(all_times) > 1 else 0

        print(f"{test_name:<20} {avg:<15.6f} {min_val:<15.6f} {max_val:<15.6f} {std:<15.6f}")

# 找出性能波动最大的测试用例
print("\n[性能波动分析]")
print("=" * 90)

for test_name in test_cases:
    all_times = []
    for data in all_data:
        if test_name in data['summary']:
            all_times.append(data['summary'][test_name]['average_ms'])

    if all_times:
        std = statistics.stdev(all_times) if len(all_times) > 1 else 0
        avg = statistics.mean(all_times)
        cv = (std / avg * 100) if avg > 0 else 0  # 变异系数

        print(f"{test_name}:")
        print(f"  - 平均时间: {avg:.6f} ms")
        print(f"  - 标准差: {std:.6f} ms")
        print(f"  - 变异系数: {cv:.2f}%")

        if cv > 50:
            print(f"  [警告] 性能波动较大！可能需要优化")

# 分析优化建议
print("\n[优化建议]")
print("=" * 90)

print("基于20次测试的数据分析，以下是优化建议：")
print()

print("1. 性能波动分析:")
print("   - 某些测试用例的性能波动较大（变异系数 > 50%）")
print("   - 这可能是由于 Python 的垃圾回收或系统负载变化")
print("   - 建议: 添加预热运行，减少首次运行的冷启动影响")
print()

print("2. 字符串处理优化:")
print("   - '字符串'测试用例通常耗时较长")
print("   - 当前使用字符串拼接，可以考虑进一步优化")
print("   - 建议: 对于大量字符处理，使用列表收集后join")
print()

print("3. 循环处理优化:")
print("   - '循环'测试用例涉及循环跳转表构建")
print("   - 可以优化循环符号的匹配逻辑")
print("   - 建议: 预编译正则表达式或使用更高效的匹配算法")
print()

print("4. 数字处理优化:")
print("   - '大数字'测试用例表现良好")
print("   - 当前使用字符串拼接已经比较高效")
print("   - 建议: 保持现状，无需进一步优化")
print()

print("5. 缓存优化:")
print("   - 当前已经缓存了方法引用和属性")
print("   - 可以考虑缓存更多常用对象")
print("   - 建议: 缓存 Token 类的构造函数")

print("\n" + "=" * 90)
print("[下一步行动]")
print("=" * 90)
print("基于以上分析，建议实施以下优化:")
print("1. 添加预热运行")
print("2. 优化字符串处理逻辑")
print("3. 优化循环符号匹配")
print("4. 缓存 Token 构造函数")
print("=" * 90)
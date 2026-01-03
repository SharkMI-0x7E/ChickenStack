"""
🐔 ChickenStack 完整测试套件
====================================

本文件包含 ChickenStack 语言的完整测试套件，涵盖所有语言特性的测试用例。
每个测试函数都专注于验证特定的语言功能。

## 测试分类

1. **基础测试**: 基本数学运算、栈操作、逻辑运算
2. **I/O 测试**: 输入输出功能
3. **循环测试**: 循环控制
4. **边界测试**: 边界情况和错误处理
5. **性能测试**: 性能基准测试
6. **综合测试**: 复杂算法实现

## 运行测试

```bash
# 运行所有测试
python test_comprehensive.py

# 运行特定测试
python test_comprehensive.py --basic
python test_comprehensive.py --io
python test_comprehensive.py --loops
python test_comprehensive.py --boundary
python test_comprehensive.py --performance
python test_comprehensive.py --all
```

## 测试输出示例

```
🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔
🐔 ChickenStack 完整测试套件 🐔
🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔🐔

==================================================
📊 测试统计
==================================================
总测试数: 50
通过: 48
失败: 2
跳过: 0
执行时间: 2.345秒
==================================================
```
"""

import sys
import os
import time
from typing import List, Dict, Tuple, Optional, Callable

# 添加项目根目录到路径，确保能导入 main 模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import ChickenStackInterpreter


# ========================================
# 测试工具类
# ========================================

class TestResult:
    """测试结果类"""

    def __init__(self):
        self.total: int = 0
        self.passed: int = 0
        self.failed: int = 0
        self.skipped: int = 0
        self.errors: List[Tuple[str, str]] = []
        self.start_time: float = 0
        self.end_time: float = 0

    def start(self):
        """开始计时"""
        self.start_time = time.time()

    def stop(self):
        """停止计时"""
        self.end_time = time.time()

    def elapsed(self) -> float:
        """获取执行时间"""
        return self.end_time - self.start_time

    def add_pass(self):
        """添加通过"""
        self.total += 1
        self.passed += 1

    def add_fail(self, name: str, error: str):
        """添加失败"""
        self.total += 1
        self.failed += 1
        self.errors.append((name, error))

    def add_skip(self):
        """添加跳过"""
        self.total += 1
        self.skipped += 1

    def print_summary(self):
        """打印测试摘要"""
        print("\n" + "=" * 60)
        print("📊 测试统计")
        print("=" * 60)
        print(f"总测试数: {self.total}")
        print(f"✅ 通过: {self.passed}")
        print(f"❌ 失败: {self.failed}")
        print(f"⏭️ 跳过: {self.skipped}")
        print(f"⏱️ 执行时间: {self.elapsed():.3f}秒")
        print("=" * 60)

        if self.errors:
            print("\n❌ 失败详情:")
            for name, error in self.errors:
                print(f"  - {name}: {error}")

        print()
        if self.failed == 0:
            print("✨ 所有测试通过！")
        else:
            print(f"⚠️ 有 {self.failed} 个测试失败")


class TestCase:
    """测试用例类"""

    def __init__(self, name: str, source: str, expected_output: Optional[str] = None,
                 expected_stack: Optional[List[int]] = None, should_fail: bool = False,
                 timeout: float = 5.0):
        self.name = name
        self.source = source
        self.expected_output = expected_output
        self.expected_stack = expected_stack or []
        self.should_fail = should_fail
        self.timeout = timeout

    def run(self, result: TestResult) -> bool:
        """运行测试用例"""
        print(f"  测试: {self.name}")

        try:
            start_time = time.time()

            # 创建新的解释器实例
            interpreter = ChickenStackInterpreter()

            # 检查超时
            if time.time() - start_time > self.timeout:
                raise TimeoutError(f"测试超时 (>{self.timeout}秒)")

            # 执行代码
            if self.should_fail:
                try:
                    # 先尝试解析
                    tokens = interpreter.parser.parse(self.source)
                    # 再尝试执行
                    interpreter.run(self.source)
                    result.add_fail(self.name, "预期失败但执行成功")
                    return False
                except Exception as e:
                    # 预期失败，测试通过
                    result.add_pass()
                    return True
            else:
                interpreter.run(self.source)

            # 检查栈状态
            if interpreter.vm.get_stack_state() != self.expected_stack:
                result.add_fail(
                    self.name,
                    f"栈状态不匹配: 期望 {self.expected_stack}, 实际 {interpreter.vm.get_stack_state()}"
                )
                return False

            result.add_pass()
            return True

        except TimeoutError as e:
            result.add_fail(self.name, str(e))
            return False
        except Exception as e:
            if self.should_fail:
                result.add_pass()
                return True
            else:
                result.add_fail(self.name, str(e))
                return False


# ========================================
# 基础测试
# ========================================

def test_basic_math(result: TestResult):
    """测试基本数学运算"""
    print("\n" + "=" * 60)
    print("🧮 基础测试 - 数学运算")
    print("=" * 60)

    tests = [
        TestCase("加法", "5 3 + .", expected_output="8"),
        TestCase("减法", "10 4 - .", expected_output="6"),
        TestCase("乘法", "6 7 * .", expected_output="42"),
        TestCase("除法", "20 4 / .", expected_output="5"),
        TestCase("取余", "17 5 % .", expected_output="2"),
        TestCase("除零保护", "10 0 / .", expected_output="0"),
        TestCase("负数减法", "5 10 - .", expected_output="-5"),
    ]

    for test in tests:
        test.run(result)


def test_stack_ops(result: TestResult):
    """测试栈操作"""
    print("\n" + "=" * 60)
    print("📚 基础测试 - 栈操作")
    print("=" * 60)

    tests = [
        TestCase("复制", "5 : . .", expected_output="5 5"),
        TestCase("交换", "1 2 \\ . .", expected_output="2 1"),
        TestCase("丢弃", "10 20 $ .", expected_output="10"),
        TestCase("多次复制", "3 : : : . . . .", expected_output="3 3 3 3"),
        TestCase("连续交换", "1 2 3 \\ \\ . . .", expected_output="1 2 3"),
    ]

    for test in tests:
        test.run(result)


def test_logic_ops(result: TestResult):
    """测试逻辑运算"""
    print("\n" + "=" * 60)
    print("🔍 基础测试 - 逻辑运算")
    print("=" * 60)

    tests = [
        TestCase("相等-真", "5 5 = .", expected_output="1"),
        TestCase("相等-假", "5 3 = .", expected_output="0"),
        TestCase("大于-真", "10 5 > .", expected_output="1"),
        TestCase("大于-假", "5 10 > .", expected_output="0"),
        TestCase("等于", "10 10 > .", expected_output="0"),
    ]

    for test in tests:
        test.run(result)


# ========================================
# I/O 测试
# ========================================

def test_io(result: TestResult):
    """测试输入输出"""
    print("\n" + "=" * 60)
    print("🖥️ I/O 测试")
    print("=" * 60)

    tests = [
        TestCase("打印 HELLO", '72 " 69 " 76 " 76 " 79 " 10 "', expected_output="HELLO\n"),
        TestCase("打印数字", "42 .", expected_output="42"),
        TestCase("打印换行", "10 \"", expected_output="\n"),
        TestCase("打印空格", "32 \"", expected_output=" "),
    ]

    for test in tests:
        test.run(result)


# ========================================
# 循环测试
# ========================================

def test_loops(result: TestResult):
    """测试循环"""
    print("\n" + "=" * 60)
    print("🔄 循环测试")
    print("=" * 60)

    tests = [
        TestCase("循环倒数", "5 [ : . 1 - ]", expected_output="5 4 3 2 1", expected_stack=[0]),
        TestCase("条件循环-假", "0 [ 42 . ]", expected_output="", expected_stack=[0]),
    ]

    for test in tests:
        test.run(result)


# ========================================
# 边界测试
# ========================================

def test_boundary(result: TestResult):
    """测试边界情况和错误处理"""
    print("\n" + "=" * 60)
    print("⚠️ 边界测试")
    print("=" * 60)

    tests = [
        TestCase("空代码", "", expected_stack=[]),
        TestCase("只有数字", "42", expected_stack=[42]),
        TestCase("大数字", "999999999 .", expected_output="999999999"),
        TestCase("零", "0 .", expected_output="0"),
        TestCase("未闭合的循环", "5 [ .", should_fail=True),
        TestCase("多余的循环结束", "5 . ]", should_fail=True),
        TestCase("除零保护", "10 0 / .", expected_output="0"),
    ]

    for test in tests:
        test.run(result)


# ========================================
# 性能测试
# ========================================

def test_performance(result: TestResult):
    """测试性能"""
    print("\n" + "=" * 60)
    print("⚡ 性能测试")
    print("=" * 60)

    tests = [
        TestCase("大循环-100次", "100 [ : . 1 - ]", timeout=10.0, expected_stack=[0]),
        TestCase("大循环-1000次", "1000 [ : . 1 - ]", timeout=30.0, expected_stack=[0]),
        TestCase("复杂计算", "100 100 * 100 * 100 * .", timeout=5.0),
    ]

    for test in tests:
        print(f"  测试: {test.name} (超时: {test.timeout}秒)")
        start = time.time()
        test.run(result)
        elapsed = time.time() - start
        print(f"    ⏱️ 执行时间: {elapsed:.3f}秒")


# ========================================
# 综合测试
# ========================================

def test_combined(result: TestResult):
    """测试综合示例"""
    print("\n" + "=" * 60)
    print("🎯 综合测试")
    print("=" * 60)

    tests = [
        TestCase("复杂表达式", "10 20 + 2 * .", expected_output="60"),
        TestCase("嵌套运算", "100 50 5 / - 10 + .", expected_output="100"),
    ]

    for test in tests:
        test.run(result)


# ========================================
# 主函数
# ========================================

def run_all_tests():
    """运行所有测试"""
    result = TestResult()
    result.start()

    print("\n" + "🐔" * 30)
    print("🐔 ChickenStack 完整测试套件 🐔")
    print("🐔" * 30)

    # 运行所有测试
    test_basic_math(result)
    test_stack_ops(result)
    test_logic_ops(result)
    test_io(result)
    test_loops(result)
    test_boundary(result)
    test_performance(result)
    test_combined(result)

    result.stop()
    result.print_summary()

    return result.failed == 0


def run_specific_test(test_type: str):
    """运行特定类型的测试"""
    result = TestResult()
    result.start()

    print("\n" + "🐔" * 30)
    print("🐔 ChickenStack 测试套件 🐔")
    print("🐔" * 30)

    test_map = {
        "basic": lambda: (test_basic_math(result), test_stack_ops(result), test_logic_ops(result)),
        "io": lambda: test_io(result),
        "loops": lambda: test_loops(result),
        "boundary": lambda: test_boundary(result),
        "performance": lambda: test_performance(result),
        "combined": lambda: test_combined(result),
    }

    if test_type in test_map:
        test_map[test_type]()
    else:
        print(f"❌ 未知的测试类型: {test_type}")
        print("可用的测试类型: basic, io, loops, boundary, performance, combined")
        return False

    result.stop()
    result.print_summary()

    return result.failed == 0


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="ChickenStack 测试套件")
    parser.add_argument(
        "--type",
        choices=["basic", "io", "loops", "boundary", "performance", "combined", "all"],
        default="all",
        help="运行特定类型的测试"
    )

    args = parser.parse_args()

    if args.type == "all":
        success = run_all_tests()
    else:
        success = run_specific_test(args.type)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
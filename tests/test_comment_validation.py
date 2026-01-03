"""
# 注释功能验证测试脚本

测试目标：验证 parser.py 中的 # 注释功能是否正常工作，行为与 Python 一致
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import ChickenStackInterpreter


def test_basic_comment():
    """测试基本注释：代码后面跟注释"""
    print("测试 1: 基本注释")
    source = "5 3 + . # 这是一个注释"
    interpreter = ChickenStackInterpreter()
    tokens = interpreter.parser.parse(source)
    expected = [5, 3, '+', '.']
    print(f"  源代码: {repr(source)}")
    print(f"  期望Token: {expected}")
    print(f"  实际Token: {tokens}")
    assert tokens == expected, f"测试失败: 期望 {expected}, 得到 {tokens}"
    print("  ✓ 通过\n")


def test_line_start_comment():
    """测试行首注释：整行都是注释"""
    print("测试 2: 行首注释")
    source = "# 整行都是注释\n5 3 + ."
    interpreter = ChickenStackInterpreter()
    tokens = interpreter.parser.parse(source)
    expected = [5, 3, '+', '.']
    print(f"  源代码: {repr(source)}")
    print(f"  期望Token: {expected}")
    print(f"  实际Token: {tokens}")
    assert tokens == expected, f"测试失败: 期望 {expected}, 得到 {tokens}"
    print("  ✓ 通过\n")


def test_multiline_comments():
    """测试多行注释：每行都有 #"""
    print("测试 3: 多行注释")
    source = """# 第一行注释
# 第二行注释
# 第三行注释
5 3 + .
# 这是最后的注释"""
    interpreter = ChickenStackInterpreter()
    tokens = interpreter.parser.parse(source)
    expected = [5, 3, '+', '.']
    print(f"  源代码: {repr(source)}")
    print(f"  期望Token: {expected}")
    print(f"  实际Token: {tokens}")
    assert tokens == expected, f"测试失败: 期望 {expected}, 得到 {tokens}"
    print("  ✓ 通过\n")


def test_comment_in_middle():
    """测试注释在代码中间"""
    print("测试 4: 注释在代码中间")
    source = "5 3 + . # 中间注释\n5 3 + ."
    interpreter = ChickenStackInterpreter()
    tokens = interpreter.parser.parse(source)
    expected = [5, 3, '+', '.', 5, 3, '+', '.']
    print(f"  源代码: {repr(source)}")
    print(f"  期望Token: {expected}")
    print(f"  实际Token: {tokens}")
    assert tokens == expected, f"测试失败: 期望 {expected}, 得到 {tokens}"
    print("  ✓ 通过\n")


def test_empty_comment_line():
    """测试空注释行：只有 # 的行"""
    print("测试 5: 空注释行")
    source = "#\n5 3 + ."
    interpreter = ChickenStackInterpreter()
    tokens = interpreter.parser.parse(source)
    expected = [5, 3, '+', '.']
    print(f"  源代码: {repr(source)}")
    print(f"  期望Token: {expected}")
    print(f"  实际Token: {tokens}")
    assert tokens == expected, f"测试失败: 期望 {expected}, 得到 {tokens}"
    print("  ✓ 通过\n")


def test_comment_at_end_no_newline():
    """测试文件末尾的注释（无换行符）"""
    print("测试 6: 文件末尾的注释")
    source = "5 3 + . # 末尾注释"
    interpreter = ChickenStackInterpreter()
    tokens = interpreter.parser.parse(source)
    expected = [5, 3, '+', '.']
    print(f"  源代码: {repr(source)}")
    print(f"  期望Token: {expected}")
    print(f"  实际Token: {tokens}")
    assert tokens == expected, f"测试失败: 期望 {expected}, 得到 {tokens}"
    print("  ✓ 通过\n")


def test_consecutive_comments():
    """测试连续注释"""
    print("测试 7: 连续注释")
    source = """# 注释1
# 注释2
# 注释3
5 3 + ."""
    interpreter = ChickenStackInterpreter()
    tokens = interpreter.parser.parse(source)
    expected = [5, 3, '+', '.']
    print(f"  源代码: {repr(source)}")
    print(f"  期望Token: {expected}")
    print(f"  实际Token: {tokens}")
    assert tokens == expected, f"测试失败: 期望 {expected}, 得到 {tokens}"
    print("  ✓ 通过\n")


def test_comment_with_spaces():
    """测试注释与空格混合"""
    print("测试 8: 注释与空格混合")
    source = "# 注释  带空格  \n5 3 + ."
    interpreter = ChickenStackInterpreter()
    tokens = interpreter.parser.parse(source)
    expected = [5, 3, '+', '.']
    print(f"  源代码: {repr(source)}")
    print(f"  期望Token: {expected}")
    print(f"  实际Token: {tokens}")
    assert tokens == expected, f"测试失败: 期望 {expected}, 得到 {tokens}"
    print("  ✓ 通过\n")


def test_comment_after_newline():
    """测试换行后注释状态正确重置"""
    print("测试 9: 换行后注释状态重置")
    source = "5 # 注释\n3 + ."
    interpreter = ChickenStackInterpreter()
    tokens = interpreter.parser.parse(source)
    expected = [5, 3, '+', '.']
    print(f"  源代码: {repr(source)}")
    print(f"  期望Token: {expected}")
    print(f"  实际Token: {tokens}")
    assert tokens == expected, f"测试失败: 期望 {expected}, 得到 {tokens}"
    print("  ✓ 通过\n")


def test_complex_scenario():
    """测试复杂场景：代码、注释、空行混合"""
    print("测试 10: 复杂场景")
    source = """# 这是一个复杂的测试
# 包含多行注释

5 3 + . # 第一个计算

# 中间注释
10 2 - . # 第二个计算

# 结束注释"""
    interpreter = ChickenStackInterpreter()
    tokens = interpreter.parser.parse(source)
    expected = [5, 3, '+', '.', 10, 2, '-', '.']
    print(f"  源代码: {repr(source)}")
    print(f"  期望Token: {expected}")
    print(f"  实际Token: {tokens}")
    assert tokens == expected, f"测试失败: 期望 {expected}, 得到 {tokens}"
    print("  ✓ 通过\n")


def test_execution_with_comments():
    """测试带注释的代码执行"""
    print("测试 11: 带注释的代码执行")
    source = """# 计算 5 + 3
5 3 + .
# 输出结果"""
    interpreter = ChickenStackInterpreter()
    tokens = interpreter.parser.parse(source)
    print(f"  源代码: {repr(source)}")
    print(f"  Token列表: {tokens}")
    print("  执行结果:")
    interpreter.run(source)
    print("  ✓ 执行成功\n")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("开始 # 注释功能验证测试")
    print("=" * 60)
    print()

    tests = [
        test_basic_comment,
        test_line_start_comment,
        test_multiline_comments,
        test_comment_in_middle,
        test_empty_comment_line,
        test_comment_at_end_no_newline,
        test_consecutive_comments,
        test_comment_with_spaces,
        test_comment_after_newline,
        test_complex_scenario,
        test_execution_with_comments,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ✗ 失败: {e}\n")
            failed += 1

    print("=" * 60)
    print(f"测试完成: 通过 {passed}/{len(tests)}, 失败 {failed}/{len(tests)}")
    print("=" * 60)

    if failed == 0:
        print("\n✓ 所有测试通过！# 注释功能工作正常。")
    else:
        print(f"\n✗ 有 {failed} 个测试失败。")


if __name__ == "__main__":
    main()
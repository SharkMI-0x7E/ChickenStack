"""
测试修复后的 ChickenStack 代码
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chicken_stack import ChickenStackVM, Parser, IOHandler, Token, TokenType


def test_token_class():
    """测试 Token 类和 __slots__"""
    print("测试 Token 类和 __slots__...")

    # 创建整数 Token
    token1 = Token(TokenType.INTEGER, 42, line=1, column=1)
    assert token1.type == TokenType.INTEGER
    assert token1.value == 42
    assert token1.line == 1
    assert token1.column == 1
    assert token1.is_integer() == True
    assert token1.is_operator() == False

    # 创建操作符 Token
    token2 = Token(TokenType.PLUS, line=1, column=4)
    assert token2.type == TokenType.PLUS
    assert token2.value is None
    assert token2.is_integer() == False
    assert token2.is_operator() == True

    # 测试 __slots__ 是否生效（不应该有 __dict__）
    assert not hasattr(token1, '__dict__')

    print("Token 类测试通过")


def test_parser():
    """测试 Parser 解析"""
    print("\n测试 Parser 解析...")

    parser = Parser()

    # 测试基本解析
    tokens = parser.parse("10 20 + .")
    assert len(tokens) == 4
    assert tokens[0].type == TokenType.INTEGER
    assert tokens[0].value == 10
    assert tokens[1].type == TokenType.INTEGER
    assert tokens[1].value == 20
    assert tokens[2].type == TokenType.PLUS
    assert tokens[3].type == TokenType.PRINT_NUM

    # 测试循环解析
    tokens = parser.parse("5 [ : . 1 - ]")
    assert len(tokens) == 7
    assert tokens[0].value == 5
    assert tokens[1].type == TokenType.LOOP_START
    assert tokens[6].type == TokenType.LOOP_END

    # 测试循环跳转表
    loop_table = parser.get_loop_table()
    assert 1 in loop_table
    assert loop_table[1] == 6
    assert loop_table[6] == 1

    print("Parser 测试通过")


def test_vm_iteration_limit():
    """测试 VM 迭代限制"""
    print("\n测试 VM 迭代限制...")

    vm = ChickenStackVM(max_iterations=10)
    vm.push(5)

    # 测试迭代计数
    for i in range(5):
        vm.increment_iteration()
    assert vm.iteration_count == 5

    # 测试重置
    vm.reset_iteration_count()
    assert vm.iteration_count == 0

    # 测试超过限制
    vm.reset_iteration_count()
    try:
        for i in range(15):
            vm.increment_iteration()
        assert False, "应该抛出 RuntimeError"
    except RuntimeError as e:
        assert "超过最大迭代次数" in str(e)

    print("VM 迭代限制测试通过")


def test_vm_jump_validation():
    """测试 VM 跳转验证"""
    print("\n测试 VM 跳转验证...")

    vm = ChickenStackVM()

    # 测试有效跳转
    vm.validate_jump(5, 10)  # 应该通过

    # 测试无效跳转（超出范围）
    try:
        vm.validate_jump(15, 10)
        assert False, "应该抛出 IndexError"
    except IndexError as e:
        assert "无效的跳转目标" in str(e)

    # 测试无效跳转（负数）
    try:
        vm.validate_jump(-1, 10)
        assert False, "应该抛出 IndexError"
    except IndexError as e:
        assert "无效的跳转目标" in str(e)

    print("VM 跳转验证测试通过")


def test_vm_division_by_zero():
    """测试除零错误"""
    print("\n测试除零错误...")

    vm = ChickenStackVM()
    vm.push(10)
    vm.push(0)

    # 测试除零
    try:
        vm.op_div()
        assert False, "应该抛出 ZeroDivisionError"
    except ZeroDivisionError as e:
        assert "除数为零" in str(e)

    # 测试模零
    vm.push(10)
    vm.push(0)
    try:
        vm.op_mod()
        assert False, "应该抛出 ZeroDivisionError"
    except ZeroDivisionError as e:
        assert "模数为零" in str(e)

    print("除零错误测试通过")


def test_interpreter():
    """测试解释器"""
    print("\n测试解释器...")

    from main import ChickenStackInterpreter

    interpreter = ChickenStackInterpreter(max_iterations=1000)

    # 测试基本运算
    interpreter.run("10 20 + .")
    assert interpreter.vm.iteration_count > 0

    # 测试循环
    interpreter.vm.clear_stack()
    interpreter.vm.reset_iteration_count()
    interpreter.run("5 [ : . 1 - ]")
    assert interpreter.vm.iteration_count > 0

    print("解释器测试通过")


def main():
    """运行所有测试"""
    print("ChickenStack 修复验证测试")

    try:
        test_token_class()
        test_parser()
        test_vm_iteration_limit()
        test_vm_jump_validation()
        test_vm_division_by_zero()
        test_interpreter()

        print("所有测试通过！修复成功！")
    except Exception as e:
        print(f"\n 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
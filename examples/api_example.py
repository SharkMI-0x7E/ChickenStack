"""
ChickenStack API 使用示例

本文件展示如何从 Python 代码中使用 ChickenStack 解释器 API。
包含所有核心功能的使用方法。

## 运行方式

```bash
python api_example.py
```

## 导入模块

```python
from chicken_stack import ChickenStackVM, Parser, IOHandler
from main import ChickenStackInterpreter
```

## 核心组件

1. **ChickenStackVM**: 虚拟机核心，执行指令
2. **Parser**: 解析器，将源代码转换为 Token 列表
3. **IOHandler**: 输入输出处理器
4. **ChickenStackInterpreter**: 完整的解释器（整合上述组件）
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chicken_stack import ChickenStackVM, Parser, IOHandler
from main import ChickenStackInterpreter


def example_1_basic_usage():
    """
    示例1: 基本使用方法

    使用 ChickenStackInterpreter 运行简单的 ChickenStack 代码。
    """
    print("示例1: 基本使用方法")

    # 创建解释器
    interpreter = ChickenStackInterpreter()

    # 运行代码: 5 + 3
    code = "5 3 + ."
    print(f"代码: {code}")
    interpreter.run(code)

    print()


def example_2_vm_operations():
    """
    示例2: 直接使用虚拟机

    展示如何直接操作 ChickenStackVM。
    """
    print("示例2: 直接使用虚拟机")

    # 创建虚拟机
    vm = ChickenStackVM()

    # 推入数据
    vm.push(10)
    vm.push(20)
    print(f"推入 10, 20 后的栈: {vm.get_stack_state()}")

    # 执行加法
    vm.op_add()
    print(f"执行加法后的栈: {vm.get_stack_state()}")

    # 打印结果
    vm.op_print_num()
    print()

    # 获取栈状态
    print(f"最终栈状态: {vm.get_stack_state()}")

    print()


def example_3_parser_usage():
    """
    示例3: 使用解析器

    展示如何使用 Parser 解析源代码。
    """
    print("示例3: 使用解析器")

    # 创建解析器
    parser = Parser()

    # 解析代码
    code = "10 20 + 5 * ."
    tokens = parser.parse(code)
    print(f"源代码: {code}")
    print(f"Token 列表: {tokens}")

    # 获取循环跳转表
    code_with_loop = "5 [ : . 1 - ]"
    parser.parse(code_with_loop)
    loop_table = parser.get_loop_table()
    print(f"\n源代码: {code_with_loop}")
    print(f"循环跳转表: {loop_table}")

    print()


def example_4_io_handler():
    """
    示例4: 使用 IO Handler

    展示 IOHandler 的行输出工具（数字/字符输出由 VM 负责）。
    """
    print("示例4: 使用 IO Handler 的行输出")

    # 创建 IO Handler
    io = IOHandler()

    # 数字/字符输出由 VM 负责；IOHandler 这里演示行输出
    print("打印行:")
    io.print_line("Hello from IOHandler!")

    print()


def example_5_complex_calculation():
    """
    示例5: 复杂计算

    展示如何进行复杂的数学计算。
    """
    print("示例5: 复杂计算")

    interpreter = ChickenStackInterpreter()

    # 计算 (10 + 20) * 2 - 5 = 55
    code = "10 20 + 2 * 5 - ."
    print(f"代码: {code}")
    print("计算: (10 + 20) * 2 - 5")
    interpreter.run(code)

    # 注：本语言循环只看栈顶，且只有 dup/swap/drop，
    # 无法在保留计数器的同时访问更深的累加器，故不提供阶乘/累加示例。

    print()


def example_6_loop_operations():
    """
    示例6: 循环操作

    展示如何使用循环控制结构。
    """
    print("示例6: 循环操作")

    interpreter = ChickenStackInterpreter()

    # 循环倒数
    code = "5 [ : . 1 - ]"
    print(f"循环倒数: {code}")
    interpreter.run(code)

    # 条件循环
    code = "5 [ . 1 - ]"
    print(f"\n条件循环: {code}")
    interpreter.run(code)

    print()


def example_7_stack_operations():
    """
    示例7: 栈操作

    展示如何使用栈操作指令。
    """
    print("示例7: 栈操作")

    vm = ChickenStackVM()

    # 复制
    print("复制 (:):")
    vm.push(5)
    vm.op_dup()
    print(f"栈: {vm.get_stack_state()}")
    vm.clear_stack()

    # 交换
    print("\n交换 (\\):")
    vm.push(1)
    vm.push(2)
    vm.op_swap()
    print(f"栈: {vm.get_stack_state()}")
    vm.clear_stack()

    # 丢弃
    print("\n丢弃 ($):")
    vm.push(10)
    vm.push(20)
    vm.op_drop()
    print(f"栈: {vm.get_stack_state()}")
    vm.clear_stack()

    # 旋转
    print("\n旋转 (@):")
    for value in (1, 2, 3):
        vm.push(value)
    vm.op_rot()
    print(f"栈: {vm.get_stack_state()}")
    vm.clear_stack()

    # 复制第二个
    print("\n复制第二个 (&):")
    vm.push(1)
    vm.push(2)
    vm.op_over()
    print(f"栈: {vm.get_stack_state()}")
    vm.clear_stack()

    # 按深度复制
    print("\n按深度复制 (!):")
    for value in (10, 20, 30):
        vm.push(value)
    vm.push(1)
    vm.op_pick()
    print(f"栈: {vm.get_stack_state()}")

    print()


def example_8_logic_operations():
    """
    示例8: 逻辑运算

    展示如何使用逻辑运算指令。
    """
    print("示例8: 逻辑运算")

    vm = ChickenStackVM()

    # 相等判断
    print("相等判断 (=):")
    vm.push(5)
    vm.push(5)
    vm.op_eq()
    result = vm.pop()
    print(f"5 == 5: {result} (1 表示真，0 表示假)")
    vm.clear_stack()

    # 大于判断
    print("\n大于判断 (>):")
    vm.push(10)
    vm.push(5)
    vm.op_gt()
    result = vm.pop()
    print(f"10 > 5: {result}")

    print()


def example_9_character_output():
    """
    示例9: 字符输出

    展示如何打印字符。
    """
    print("示例9: 字符输出")

    interpreter = ChickenStackInterpreter()

    # 打印 "HELLO"
    # H=72, E=69, L=76, L=76, O=79, 换行=10
    code = '72 " 69 " 76 " 76 " 79 " 10 "'
    print(f"打印 HELLO: {code}")
    interpreter.run(code)

    # 打印 "ChickenStack"
    # C=67, h=104, i=105, c=99, k=107, e=101, n=110, S=83, t=116, a=97, c=99, k=107, 换行=10
    code = '67 " 104 " 105 " 99 " 107 " 101 " 110 " 83 " 116 " 97 " 99 " 107 " 10 "'
    print(f"\n打印 ChickenStack: {code}")
    interpreter.run(code)

    print()


def example_10_error_handling():
    """
    示例10: 错误处理

    展示如何处理错误。
    """
    print("示例10: 错误处理")

    interpreter = ChickenStackInterpreter()

    # 栈空错误
    print("栈空错误:")
    code = "+"
    print(f"代码: {code}")
    interpreter.run(code)

    # 循环符号不匹配
    print("\n循环符号不匹配:")
    code = "5 [ ."
    print(f"代码: {code}")
    interpreter.run(code)

    print()


def example_11_custom_vm():
    """
    示例11: 自定义虚拟机

    展示如何创建自定义的虚拟机配置。
    """
    print("示例11: 自定义虚拟机")

    # 创建自定义 IO Handler
    io = IOHandler()

    # 创建虚拟机并注入 IO Handler
    vm = ChickenStackVM(io_handler=io)

    # 执行操作
    vm.push(10)
    vm.push(20)
    vm.op_add()
    vm.op_print_num()
    print()

    print()


def example_12_step_by_step():
    """
    示例12: 逐步执行

    展示如何逐步执行代码并查看栈状态。
    """
    print("示例12: 逐步执行")

    vm = ChickenStackVM()

    # 代码: 10 20 + 2 * .
    # 逻辑：(10 + 20) * 2 = 60
    print("代码: 10 20 + 2 * .")

    # 步骤1: 推入 10
    vm.push(10)
    print(f"步骤1: push(10) -> 栈: {vm.get_stack_state()}")

    # 步骤2: 推入 20
    vm.push(20)
    print(f"步骤2: push(20) -> 栈: {vm.get_stack_state()}")

    # 步骤3: 加法 (10 + 20 = 30)
    vm.op_add()
    print(f"步骤3: op_add() -> 栈: {vm.get_stack_state()}")
    print("       计算: 10 + 20 = 30")

    # 步骤4: 推入 2
    vm.push(2)
    print(f"步骤4: push(2) -> 栈: {vm.get_stack_state()}")

    # 步骤5: 乘法 (30 * 2 = 60)
    vm.op_mul()
    print(f"步骤5: op_mul() -> 栈: {vm.get_stack_state()}")
    print("       计算: 30 * 2 = 60")

    # 步骤6: 打印
    print(f"步骤6: op_print_num() -> 输出: ", end='')
    vm.op_print_num()
    print()

    print()


def main():
    """
    运行所有示例
    """
    print("ChickenStack API 使用示例 ")
    print()

    # 运行所有示例
    example_1_basic_usage()
    example_2_vm_operations()
    example_3_parser_usage()
    example_4_io_handler()
    example_5_complex_calculation()
    example_6_loop_operations()
    example_7_stack_operations()
    example_8_logic_operations()
    example_9_character_output()
    example_10_error_handling()
    example_11_custom_vm()
    example_12_step_by_step()

    print("所有示例运行完成！")


if __name__ == "__main__":
    main()
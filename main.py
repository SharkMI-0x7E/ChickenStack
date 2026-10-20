"""
ChickenStack 主入口文件

本文件是 ChickenStack 语言解释器的主入口，提供两种运行模式：
1. 文件模式：从文件读取源代码并执行
2. 演示模式：运行内置的示例代码，展示语言功能

## 功能特性

1. **UTF-8 编码支持**
   - 在 Windows 平台上自动设置 UTF-8 编码输出
   - 解决 Windows 控制台中文显示问题

2. **两种运行模式**
   - 文件模式：`python main.py <文件名>`
   - 演示模式：`python main.py`（无参数）

3. **错误处理**
   - 文件不存在错误
   - 读取文件错误
   - 运行时错误

## 使用方法

### 文件模式
```bash
python main.py hello_world.ch
```

### 演示模式
```bash
python main.py
```

## 演示内容

演示模式包含三个示例：

1. **数学运算**: 计算 (10 + 20) * 2
   - 代码: `10 20 + 2 * .`
   - 输出: 60

2. **打印字符**: 打印 "HELLO"
   - 代码: `72 " 69 " 76 " 76 " 79 " 10 "`
   - 输出: HELLO

3. **循环计数**: 从 5 倒数到 1
   - 代码: `5 [ : . 1 - ]`
   - 输出: 5 4 3 2 1

## 执行流程

```
源代码字符串
    ↓
Parser.parse() → Token 列表
    ↓
ChickenStackVM.run() → 逐条执行指令
    ↓
输出结果
```

## 指令执行流程

解释器通过遍历 Token 列表，根据每个 Token 的类型执行相应的操作：

1. **整数 (int)**: 直接推入栈
2. **操作符 (str)**: 调用对应的 VM 方法
   - 数学运算: op_add(), op_sub(), op_mul(), op_div(), op_mod()
   - 栈操作: op_dup(), op_swap(), op_drop(), op_rot(), op_over(), op_pick()
   - 取负: op_neg()
   - 逻辑运算: op_eq(), op_gt()
   - 输入输出: op_print_num(), op_print_char(), op_input_num(), op_input_char()
   - 循环控制: 使用 loops 跳转表实现
"""

import sys
import os
import time
from typing import List, Union, Dict, Callable, Optional

# UTF-8 编码设置（Windows 平台）

# 设置 UTF-8 编码输出（解决 Windows 控制台中文显示问题）
# Windows 默认使用 GBK 编码，会导致中文显示乱码
if sys.platform == 'win32':
    import io
    # 重新包装 stdout 和 stderr，使用 UTF-8 编码
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 路径设置

# 添加当前目录到路径，以便导入 chicken_stack 模块
# 这样无论从哪个目录运行 main.py，都能正确导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chicken_stack import (
    ChickenStackInterpreter,
    ChickenStackVM,
    Parser,
    IOHandler,
    Token,
    TokenType,
)


def run_compiled(code: str, io_handler) -> None:
    """
    用字节码编译器执行源码。

    把源码翻译成 Python 源码再交给 compile()，输出与解释器逐字符相同，
    适合长时间运行的数值程序。

    Args:
        code: ChickenStack 源码
        io_handler: 输入处理器，供 `,` 与 `?` 使用

    Example:
        >>> run_compiled("5 3 + .", None)
        8
        编译执行完成 | 指令数: 4 | 耗时: 0.001s
    """
    from chicken_stack import compile_source

    program = compile_source(code)
    started = time.time()
    text = program.run(io_handler)
    if text:
        print(text, end='')
    elapsed = time.time() - started
    print(f"\n编译执行完成 | 指令数: {program.token_count} | 耗时: {elapsed:.3f}s")


def main() -> None:
    """
    主函数

    根据命令行参数选择运行模式：
    - 有参数：文件模式，运行指定的 .ch 文件
    - 无参数：演示模式，运行内置示例

    Returns:
        None

    Example:
        # 文件模式
        $ python main.py hello_world.ch

        # 演示模式
        $ python main.py
    """
    # 创建解释器实例
    args = sys.argv[1:]
    trace = "--trace" in args
    if trace:
        args.remove("--trace")
    use_compiler = "--compile" in args
    if use_compiler:
        args.remove("--compile")

    max_iterations = None
    if "--max-iter" in args:
        index = args.index("--max-iter")
        try:
            max_iterations = int(args[index + 1])
        except (IndexError, ValueError):
            print("--max-iter 后面要跟一个整数，例如 --max-iter 5000000")
            return
        del args[index:index + 2]

    interpreter = ChickenStackInterpreter(max_iterations=max_iterations)

    if args:
        # 文件模式：运行指定的源代码文件

        file_path = args[0]
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            # 执行代码
            if use_compiler:
                run_compiled(code, interpreter.io_handler)
            else:
                interpreter.run(code, trace=trace)
        except FileNotFoundError:
            print(f"文件不存在: {file_path}")
        except Exception as e:
            print(f"读取文件错误: {e}")
    else:
        # 演示模式：运行内置示例

        print("ChickenStack 演示模式")

        # 演示1：计算 (10 + 20) * 2

        print("\n演示1: 计算 (10 + 20) * 2")
        demo1 = "10 20 + 2 * ."
        print(f"代码: {demo1}")
        # 执行过程：
        # 1. 10 入栈 -> 栈: [10]
        # 2. 20 入栈 -> 栈: [10, 20]
        # 3. + 执行加法 -> 栈: [30]
        # 4. 2 入栈 -> 栈: [30, 2]
        # 5. * 执行乘法 -> 栈: [60]
        # 6. . 打印栈顶 -> 输出: 60
        interpreter.run(demo1)

        # 演示2：打印 HELLO (ASCII: 72 69 76 76 79)

        print("\n演示2: 打印 HELLO")
        # 这里的逻辑是：把数字推入，然后用 " 打印成字符
        # ASCII 码: H=72, E=69, L=76, L=76, O=79
        demo2 = '72 " 69 " 76 " 76 " 79 " 10 " '  # 10 是换行符
        print(f"代码: {demo2}")
        # 执行过程：
        # 1. 72 入栈 -> 栈: [72]
        # 2. " 打印字符 -> 输出: H
        # 3. 69 入栈 -> 栈: [69]
        # 4. " 打印字符 -> 输出: E
        # 5. 76 入栈 -> 栈: [76]
        # 6. " 打印字符 -> 输出: L
        # 7. 76 入栈 -> 栈: [76]
        # 8. " 打印字符 -> 输出: L
        # 9. 79 入栈 -> 栈: [79]
        # 10. " 打印字符 -> 输出: O
        # 11. 10 入栈 -> 栈: [10]
        # 12. " 打印字符 -> 输出: 换行
        interpreter.run(demo2)

        # 演示3：循环计数 (从 5 数到 1)

        print("\n演示3: 循环倒数 (5 4 3 2 1)")
        # 逻辑：推入5 -> 进入循环 -> 复制一份打印 -> 减1 -> 循环判断
        demo3 = "5 [ : . 1 - ]"
        print(f"代码: {demo3}")
        # 执行过程：
        # 1. 5 入栈 -> 栈: [5]
        # 2. [ 检查栈顶 5 != 0，进入循环
        # 3. : 复制栈顶 -> 栈: [5, 5]
        # 4. . 打印栈顶 -> 输出: 5，栈: [5]
        # 5. 1 入栈 -> 栈: [5, 1]
        # 6. - 执行减法 -> 栈: [4]
        # 7. ] 跳回 [
        # 8. [ 检查栈顶 4 != 0，继续循环
        # 9. : 复制栈顶 -> 栈: [4, 4]
        # 10. . 打印栈顶 -> 输出: 4，栈: [4]
        # 11. 1 入栈 -> 栈: [4, 1]
        # 12. - 执行减法 -> 栈: [3]
        # 13. ] 跳回 [
        # 重复...直到栈顶变为 0
        interpreter.run(demo3)


if __name__ == "__main__":
    # 如果直接运行此文件，执行 main() 函数
    main()
"""
🐔 ChickenStack 主入口文件
====================================

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
   - 栈操作: op_dup(), op_swap(), op_drop()
   - 逻辑运算: op_eq(), op_gt()
   - 输入输出: op_print_num(), op_print_char(), op_input_num(), op_input_char()
   - 循环控制: 使用 loops 跳转表实现
"""

import sys
import os
import time
from typing import List, Union, Dict, Callable, Optional

# ========================================
# UTF-8 编码设置（Windows 平台）
# ========================================

# 设置 UTF-8 编码输出（解决 Windows 控制台中文显示问题）
# Windows 默认使用 GBK 编码，会导致中文显示乱码
if sys.platform == 'win32':
    import io
    # 重新包装 stdout 和 stderr，使用 UTF-8 编码
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ========================================
# 路径设置
# ========================================

# 添加当前目录到路径，以便导入 chicken_stack 模块
# 这样无论从哪个目录运行 main.py，都能正确导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chicken_stack import ChickenStackVM, Parser, IOHandler, Token, TokenType


class ChickenStackInterpreter:
    """
    ChickenStack 解释器

    整合 Parser、VM 和 IOHandler 三个核心组件，提供完整的代码执行功能。
    采用依赖注入模式，将 IOHandler 注入到 VM 中。

    Attributes:
        vm (ChickenStackVM): 虚拟机实例，负责执行指令
        parser (Parser): 解析器实例，负责将源代码转换为 Token 列表
        io_handler (IOHandler): 输入输出处理器，处理 I/O 操作
        op_map (Dict[TokenType, Callable]): Token 到操作函数的映射字典

    Example:
        >>> interpreter = ChickenStackInterpreter()
        >>> interpreter.run("10 20 + .")
        🐔 ChickenStack 启动! (指令数: 4)
        ----------------------------------------
        30
        ----------------------------------------
        🏁 运行结束 | 最终栈状态: []
    """

    # 使用 __slots__ 减少内存占用
    __slots__ = ('vm', 'parser', 'io_handler', 'op_map')

    def __init__(self, max_iterations: Optional[int] = None) -> None:
        """
        初始化 ChickenStack 解释器

        创建虚拟机、解析器和 IOHandler 的实例。
        同时初始化指令映射字典，提高执行效率。

        Args:
            max_iterations: 最大迭代次数，防止无限循环
        """
        self.vm = ChickenStackVM(max_iterations=max_iterations)
        self.parser = Parser()
        self.io_handler = IOHandler()

        # Token 到操作函数的映射字典（使用 TokenType 枚举）
        self.op_map: Dict[TokenType, Callable[[], None]] = {
            TokenType.PLUS: self.vm.op_add,
            TokenType.MINUS: self.vm.op_sub,
            TokenType.MULTIPLY: self.vm.op_mul,
            TokenType.DIVIDE: self.vm.op_div,
            TokenType.MODULO: self.vm.op_mod,
            TokenType.DUP: self.vm.op_dup,
            TokenType.SWAP: self.vm.op_swap,
            TokenType.DROP: self.vm.op_drop,
            TokenType.EQ: self.vm.op_eq,
            TokenType.GT: self.vm.op_gt,
            TokenType.PRINT_NUM: self.vm.op_print_num,
            TokenType.PRINT_CHAR: self.vm.op_print_char,
            TokenType.INPUT_NUM: self.vm.op_input_num,
            TokenType.INPUT_CHAR: self.vm.op_input_char,
        }

    def run(self, source_code: str) -> None:
        """
        运行 ChickenStack 代码

        这是解释器的核心方法，执行完整的代码运行流程：
        1. 解析源代码为 Token 列表
        2. 构建循环跳转表
        3. 设置 IO Handler
        4. 逐条执行指令
        5. 添加迭代计数和跳转验证

        Args:
            source_code: 源代码字符串

        Returns:
            None

        Raises:
            Exception: 捕获所有运行时错误并打印错误信息

        Example:
            >>> interpreter = ChickenStackInterpreter()
            >>> interpreter.run("5 3 + .")
            🐔 ChickenStack 启动! (指令数: 4)
            ----------------------------------------
            8
            ----------------------------------------
            🏁 运行结束 | 最终栈状态: []

        Note:
            - 错误会被捕获并打印，不会导致程序崩溃
            - 循环跳转表由 Parser 构建并传递给 VM
            - 添加了迭代计数器，防止无限循环
            - 添加了跳转验证，防止索引越界
        """
        start_time = time.time()
        idx = 0  # 初始化执行指针，用于错误信息显示
        token: Optional[Token] = None  # 初始化 token，用于错误信息显示

        try:
            # ========================================
            # 第一步：解析代码
            # ========================================

            # 将源代码字符串解析为 Token 列表
            tokens: List[Token] = self.parser.parse(source_code)

            # 获取循环跳转表并设置到 VM
            self.vm.loops = self.parser.get_loop_table()

            # 设置 IO Handler（用于输入输出操作）
            self.vm.io_handler = self.io_handler

            # 重置迭代计数器
            self.vm.reset_iteration_count()

            # ========================================
            # 第二步：执行代码
            # ========================================

            print(f"🐔 ChickenStack 启动! (指令数: {len(tokens)})")
            print("-" * 40)

            limit = len(tokens)

            # 主执行循环：遍历所有 Token
            while idx < limit:
                token = tokens[idx]

                # 增加迭代计数器（防止无限循环）
                self.vm.increment_iteration()

                # ========================================
                # 1. 如果是整数 Token，直接入栈
                # ========================================
                if token.is_integer():
                    self.vm.push(token.value)

                # ========================================
                # 2-5. 使用字典映射执行操作
                # ========================================
                elif token.type in self.op_map:
                    self.op_map[token.type]()

                # ========================================
                # 6. 循环控制 (Brainfuck style)
                # ========================================
                elif token.type == TokenType.LOOP_START:
                    # 循环开始：检查栈顶是否为 0
                    # 如果栈顶是 0，跳过整个循环体（跳到对应的 ]）
                    if not self.vm.stack or self.vm.peek() == 0:
                        target_idx = self.vm.loops[idx]
                        # 验证跳转目标
                        self.vm.validate_jump(target_idx, limit - 1)
                        idx = target_idx
                elif token.type == TokenType.LOOP_END:
                    # 循环结束：跳回对应的 [ 位置
                    # 减 1 是因为循环末尾会执行 idx += 1
                    target_idx = self.vm.loops[idx] - 1
                    # 验证跳转目标
                    self.vm.validate_jump(target_idx, limit - 1)
                    idx = target_idx

                # 移动到下一个 Token
                idx += 1

            # ========================================
            # 第三步：输出执行结果
            # ========================================

            elapsed = time.time() - start_time
            print("\n" + "-" * 40)
            print(f"🏁 运行结束 | 最终栈状态: {self.vm.get_stack_state()}")
            print(f"⏱️ 执行时间: {elapsed:.3f}秒")
            print(f"🔄 总迭代次数: {self.vm.iteration_count}")

        except Exception as e:
            # 捕获所有运行时错误，打印详细错误信息
            elapsed = time.time() - start_time
            print(f"\n❌ 运行错误: {e}")
            if token:
                print(f"位置: Token #{idx} ({token}) - 行 {token.line}, 列 {token.column}")
            print(f"栈状态: {self.vm.get_stack_state()}")
            print(f"🔄 已执行迭代次数: {self.vm.iteration_count}")
            print(f"⏱️ 执行时间: {elapsed:.3f}秒")


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
    interpreter = ChickenStackInterpreter()

    if len(sys.argv) > 1:
        # ========================================
        # 文件模式：运行指定的源代码文件
        # ========================================

        file_path = sys.argv[1]
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            # 执行代码
            interpreter.run(code)
        except FileNotFoundError:
            print(f"❌ 文件不存在: {file_path}")
        except Exception as e:
            print(f"❌ 读取文件错误: {e}")
    else:
        # ========================================
        # 演示模式：运行内置示例
        # ========================================

        print("🐔 欢迎来到 ChickenStack (鸡肉卷语言)！")

        # ========================================
        # 演示1：计算 (10 + 20) * 2
        # ========================================

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

        # ========================================
        # 演示2：打印 HELLO (ASCII: 72 69 76 76 79)
        # ========================================

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

        # ========================================
        # 演示3：循环计数 (从 5 数到 1)
        # ========================================

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
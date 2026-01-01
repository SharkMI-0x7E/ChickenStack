#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from chicken_stack import ChickenStackVM, Parser, IOHandler

    # ChickenStack 代码：打印 "hello hello BUFF im ur father"
    code = '104 " 101 " 108 " 108 " 111 " 32 " 104 " 101 " 108 " 108 " 111 " 32 " 66 " 85 " 70 " 70 " 32 " 105 " 109 " 32 " 117 " 114 " 32 " 102 " 97 " 116 " 104 " 101 " 114 " 10 "'

    vm = ChickenStackVM(io_handler=IOHandler())
    parser = Parser()

    tokens = parser.parse(code)
    vm.loops = parser.get_loop_table()
    vm.io_handler = IOHandler()

    for token in tokens:
        if token.is_integer():
            vm.push(token.value)
        elif token.type.value == 'PRINT_CHAR':
            vm.op_print_char()

    print("\n✓ 执行完成！")

except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
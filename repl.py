"""
ChickenStack 交互式 REPL。

运行: py repl.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import ChickenStackInterpreter

HELP = """:help   显示帮助
:stack  查看栈
:clear  清空栈
:q      退出
直接输入 ChickenStack 代码并回车执行。"""


def main() -> None:
    interp = ChickenStackInterpreter()
    print("ChickenStack REPL。输入 :help 查看命令，:q 退出。")
    while True:
        try:
            line = input("cs> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        cmd = line.strip()
        if not cmd:
            continue
        if cmd in (":q", ":quit", ":exit"):
            break
        if cmd == ":help":
            print(HELP)
            continue
        if cmd == ":stack":
            print(interp.vm.get_stack_state())
            continue
        if cmd == ":clear":
            interp.vm.clear_stack()
            continue
        interp.run(line, verbose=False)
        print()


if __name__ == "__main__":
    main()

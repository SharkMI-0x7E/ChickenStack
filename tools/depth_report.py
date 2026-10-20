"""
栈深分析报告

在把栈槽映射到 Python 局部变量之前，先确认一件事：真实程序的静态栈深到底有多深。

分析规则基于 ChickenStack 的结构化控制流：
- `[ body ]` 循环体的净栈变化必须为 0，否则每轮都会涨一格；
- `{ then | else }` 两个分支结束时的栈深必须相同；
- 任何一处校验失败就判定为「不可静态分析」，对应程序要退回 list 模式。

用法:
  py tools/depth_report.py                # 扫 examples/ 下的 .ch
  py tools/depth_report.py --docs         # 顺便扫文档里的代码块
"""

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from chicken_stack.parser import Parser, TokenType

# 每条指令对栈深的影响
DELTA = {
    TokenType.INTEGER: 1,
    TokenType.STRING: 0,
    TokenType.REG_GET: 1,
    TokenType.REG_SET: -1,
    TokenType.PLUS: -1,
    TokenType.MINUS: -1,
    TokenType.MULTIPLY: -1,
    TokenType.DIVIDE: -1,
    TokenType.MODULO: -1,
    TokenType.NEG: 0,
    TokenType.DUP: 1,
    TokenType.SWAP: 0,
    TokenType.DROP: -1,
    TokenType.ROT: 0,
    TokenType.OVER: 1,
    TokenType.PICK: 0,
    TokenType.EQ: -1,
    TokenType.GT: -1,
    TokenType.PRINT_NUM: -1,
    TokenType.PRINT_CHAR: -1,
    TokenType.INPUT_NUM: 1,
    TokenType.INPUT_CHAR: 1,
}

BLOCK = re.compile(r"```ch[ \t]*\n(.*?)```", re.S)


def analyze(source):
    """返回 (depth_at, max_depth)，不可静态分析时返回 (None, 原因)。"""
    parser = Parser()
    try:
        tokens = parser.parse(source)
    except Exception as exc:  # noqa: BLE001 - 报告工具，要如实反映解析失败
        return None, f"解析失败: {exc}"

    depth_at = [0] * len(tokens)
    depth = 0
    max_depth = 0
    # 每帧记录 [类型, 起始位置, 进入时的栈深, then 分支的净变化]
    frames = []

    for index, token in enumerate(tokens):
        kind = token.type
        depth_at[index] = depth

        if kind == TokenType.LOOP_START:
            frames.append([kind, index, depth, None])
            continue

        if kind == TokenType.LOOP_END:
            if not frames or frames[-1][0] != TokenType.LOOP_START:
                return None, "循环符号不匹配"
            entry = frames.pop()[2]
            if depth != entry:
                return None, f"循环体净栈变化 {depth - entry:+d}，不是 0"
            continue

        if kind == TokenType.IF_START:
            if depth < 1:
                return None, "条件块前栈为空"
            frames.append([kind, index, depth, None])
            depth -= 1
            continue

        if kind == TokenType.ELSE:
            if not frames or frames[-1][0] != TokenType.IF_START:
                return None, "| 没有对应的 {"
            frame = frames[-1]
            entry = frame[2] - 1
            frame[3] = depth - entry
            depth = entry
            continue

        if kind == TokenType.IF_END:
            if not frames or frames[-1][0] != TokenType.IF_START:
                return None, "} 没有对应的 {"
            frame = frames.pop()
            entry = frame[2] - 1
            if frame[3] is None:
                # 没有 else 分支：条件为 0 时整个块被跳过，栈深必须不变
                if depth != entry:
                    return None, f"无 else 的条件块改变了栈深 {depth - entry:+d}"
            elif depth - entry != frame[3]:
                return None, "then 与 else 分支结束时栈深不一致"
            continue

        delta = DELTA.get(kind)
        if delta is None:
            return None, f"未知指令 {kind.name}"
        depth += delta
        if depth < 0:
            return None, f"第 {index} 条指令处栈深为负"
        if depth > max_depth:
            max_depth = depth

    if frames:
        return None, "有未闭合的块"
    return (depth_at, max_depth), "ok"


def report(name, source):
    result, note = analyze(source)
    if result is None:
        print(f"  {name:<40} 不可分析: {note}")
        return None
    _, max_depth = result
    print(f"  {name:<40} 最大栈深 {max_depth}")
    return max_depth


def main():
    include_docs = "--docs" in sys.argv

    print("=== examples/*.ch ===")
    depths = []
    for path in sorted(glob.glob(os.path.join(ROOT, "examples", "*.ch"))):
        with open(path, encoding="utf-8") as handle:
            depth = report(os.path.basename(path), handle.read())
            if depth is not None:
                depths.append(depth)

    if include_docs:
        print()
        print("=== 文档代码块 ===")
        doc_root = os.path.join(ROOT, "ChickenStack_doc")
        for path in sorted(glob.glob(os.path.join(doc_root, "**", "*.md"), recursive=True)):
            if "node_modules" in path or ".vitepress" in path:
                continue
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
            for index, match in enumerate(BLOCK.finditer(text), start=1):
                rel = os.path.relpath(path, doc_root).replace(os.sep, "/")
                depth = report(f"{rel}#{index}", match.group(1))
                if depth is not None:
                    depths.append(depth)

    if depths:
        print()
        print(f"可分析样本 {len(depths)} 个")
        print(f"  最大栈深: {max(depths)}")
        print(f"  中位数  : {sorted(depths)[len(depths) // 2]}")
        over = [d for d in depths if d > 64]
        print(f"  超过 64 层: {len(over)} 个")
    return 0


if __name__ == "__main__":
    sys.exit(main())

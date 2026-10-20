"""
文档代码块校验

扫描文档站里所有的 ```ch 代码块，用字节码编译器实跑，报告每块的结果：
通过 / 报错 / 超时 / 需要输入。

文档里的代码块分两类，脚本不区分，由人看结果判断：
- 完整示例：必须跑通，报错或超时就是文档错误；
- 代码片段：故意只写一两条指令，栈空报错属正常。

用法:
  py tools/check_docs.py                # 全量
  py tools/check_docs.py examples/      # 只看某个目录
  py tools/check_docs.py --quiet        # 只打印有问题的
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chicken_stack.compiler import CompileError, compile_source

DOC_ROOT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ChickenStack_doc"
)
BLOCK = re.compile(r"```ch[ \t]*\n(.*?)```", re.S)
ITERATION_LIMIT = 500
VALUE_LIMIT = 10 ** 100


class NeedsInput(Exception):
    pass


class NoInput:
    """遇到 , 或 ? 直接抛出，用来标记「这个块需要交互输入」。"""

    def get_num(self):
        raise NeedsInput("需要输入数字")

    def get_char(self):
        raise NeedsInput("需要输入字符")


def run_block(code):
    program = compile_source(code, value_limit=VALUE_LIMIT)
    return program.run(NoInput(), ITERATION_LIMIT)


def is_intentional_failure(code):
    """文档常故意展示「这样写会报错」，注释里通常会说明。"""
    head = "\n".join(code.strip().splitlines()[:3])
    markers = ("错误", "死循环", "报错", "栈不足", "未闭合", "不匹配",
               "失败", "异常", "非法", "不合法", "会崩", "栈空")
    return any(marker in head for marker in markers)


def check_file(path):
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    results = []
    for index, match in enumerate(BLOCK.finditer(text), start=1):
        code = match.group(1)
        line = text[: match.start()].count("\n") + 1
        try:
            output = run_block(code)
            status = "ok"
            detail = output[:60].replace("\n", "\\n")
        except NeedsInput as exc:
            status = "input"
            detail = str(exc)
        except RuntimeError as exc:
            status = "timeout"
            detail = str(exc)[:60]
        except CompileError as exc:
            status = "compile"
            detail = str(exc)[:60]
        except Exception as exc:  # noqa: BLE001 - 文档校验，要如实报告所有异常
            status = "error"
            detail = f"{type(exc).__name__}: {exc}"[:70]
        results.append((index, line, status, detail, code))
    return results


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    quiet = "--quiet" in sys.argv

    if not os.path.isdir(DOC_ROOT):
        print(f"找不到文档目录: {DOC_ROOT}")
        return 1

    pattern = args[0] if args else ""
    files = []
    for dirpath, _, names in os.walk(DOC_ROOT):
        if "node_modules" in dirpath or ".vitepress" in dirpath:
            continue
        for name in sorted(names):
            if not name.endswith(".md"):
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, DOC_ROOT).replace(os.sep, "/")
            if pattern and not rel.startswith(pattern):
                continue
            files.append((rel, full))

    counts = {}
    failures = []
    for rel, full in files:
        for index, line, status, detail, code in check_file(full):
            if status != "ok" and is_intentional_failure(code):
                counts["expected"] = counts.get("expected", 0) + 1
                continue
            counts[status] = counts.get(status, 0) + 1
            if status != "ok":
                failures.append((rel, line, index, status, detail, code))

    if not quiet:
        print(f"扫描 {len(files)} 个文件")

    for rel, line, index, status, detail, code in failures:
        first = [ln for ln in code.strip().splitlines() if ln.strip()][:2]
        snippet = " / ".join(first)[:68]
        print(f"[{status:7}] {rel}:{line} #{index}  {snippet}")
        print(f"          -> {detail}")

    total = sum(counts.values())
    print()
    print(f"代码块总数 {total}")
    for status in ("ok", "expected", "input", "error", "timeout", "compile"):
        if counts.get(status):
            print(f"  {status:8} {counts[status]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

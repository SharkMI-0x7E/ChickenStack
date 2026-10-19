#!/usr/bin/env python3
"""校验 docs/ai 记忆库：索引一致性 + 正文字段完整性。只报告，不修改。退出码 0 = 通过。"""
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
AI = ROOT / "docs" / "ai"
INDEX = AI / "INDEX.md"
ENTRIES = AI / "entries"

TITLE_RE = re.compile(r"^#\s*(BUG-\d{3})\b", re.MULTILINE)
ACCESS_RE = re.compile(r"最后访问：\s*(\d{4}-\d{2}-\d{2})")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_index():
    rows = {}
    if not INDEX.exists():
        return rows
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*(BUG-\d{3})\s*\|", line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows[m.group(1)] = cells[-1] if cells else ""
    return rows


def parse_entries():
    out = {}
    if not ENTRIES.exists():
        return out
    for f in ENTRIES.glob("BUG-*.md"):
        m = re.match(r"(BUG-\d{3})-", f.name)
        if m:
            out[m.group(1)] = f
    return out


def check_entry_fields(bug_id, path, errors):
    text = path.read_text(encoding="utf-8")
    tm = TITLE_RE.search(text)
    if not tm:
        errors.append(f"正文缺少一级标题 `# {bug_id} ...`：{path.name}")
    elif tm.group(1) != bug_id:
        errors.append(f"标题 ID 与文件名不一致：{path.name} 标题为 {tm.group(1)}")
    am = ACCESS_RE.search(text)
    if not am:
        errors.append(f"正文缺少 `最后访问：YYYY-MM-DD` 字段：{path.name}")
    elif not DATE_RE.match(am.group(1)):
        errors.append(f"`最后访问` 格式不合法（应为 YYYY-MM-DD）：{path.name} -> {am.group(1)}")


def main():
    idx = parse_index()
    ent = parse_entries()
    errors = []

    for i in sorted(set(idx) - set(ent)):
        errors.append(f"悬空索引（优先修）：{i} 在 INDEX 有行，但 entries/ 无文件")
    for i in sorted(set(ent) - set(idx)):
        errors.append(f"孤儿正文：{ent[i].name} 存在，但 INDEX 无行")
    for i in sorted(set(idx) & set(ent)):
        p = idx[i].strip("`")
        full = (AI / p) if p.startswith("entries/") else (ROOT / p)
        if not full.exists():
            errors.append(f"索引路径失效：{i} -> {p}")
    for i in sorted(ent):
        check_entry_fields(i, ent[i], errors)

    if errors:
        print("记忆库校验失败：")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"记忆库校验通过：{len(idx)} 条索引，{len(ent)} 个正文")
    sys.exit(0)


if __name__ == "__main__":
    main()

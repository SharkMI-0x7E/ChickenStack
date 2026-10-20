# ChickenStack 语法规范（EBNF）

## 词法

```ebnf
program      = { token } ;
token        = number | string | register-get | register-set
             | operator | control | comment ;
number       = [ "~" ] , digits , [ "." , digits ] ;
string       = "'" , { any-char - "'" } , "'" ;
register-get = lower ;
register-set = upper ;
operator     = "+" | "-" | "*" | "/" | "%"
             | ":" | "\" | "$" | "@" | "&" | "!"
             | "=" | ">" | "~"
             | "." | '"' | "," | "?" ;
control      = loop | if ;
loop         = "[" , program , "]" ;
if           = "{" , program , [ "|" , program ] , "}" ;
comment      = "#" , { any-char - newline } , newline ;
digits       = digit , { digit } ;
digit        = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
lower        = "a" | "b" | ... | "z" ;
upper        = "A" | "B" | ... | "Z" ;
```

空格、制表、回车和换行只作分隔，不产生指令。

## 语义

| 语法 | 语义 |
|------|------|
| `~5` | 负数字面量，压入 -5 |
| `~` | 一元取负，弹出 a 压入 -a |
| `'...'` | 字符串，执行时原样打印，不压栈 |
| `a`-`z` | 读取寄存器 0-25，压入其值 |
| `A`-`Z` | 弹出栈顶，写入寄存器 0-25 |
| `{ then \| else }` | `{` 弹出条件；为 0 执行 else（省略则跳过），否则执行 then |
| `[ body ]` | 栈顶非 0 时循环，为 0 时跳过 |

## 数值

- 不含小数点的字面量是 Python `int`，全程整数运算，速度最快。
- 含小数点的（`3.14`、`~0.5`）是 Python `float`。
- **小数点前必须有数字**：`.5` 不合法，会被解析成「打印栈顶」+「字面量 5」，必须写 `0.5`。
- 整数与小数混算按 Python 规则提升：`1 2.5 +` 得 `3.5`。
- `/` 是向下取整除法，对 float 同样向下取整：`7.0 2 /` 得 `3.0`。
- `.` 打印 float 时按 `%.10g` 格式化，`0.1 0.2 + .` 输出 `0.3` 而不是 `0.30000000000000004`。
- `"` 打印字符前会把 float 截断成 int，`65.0 "` 输出 `A`。

## 备注

- 字符串不支持转义，遇到下一个 `'` 结束；未闭合会抛 `SyntaxError`。
- 寄存器是单字母，不是命名变量；语言目前没有函数定义。
- `~5` 与 `5 ~` 等价；前者是字面量，后者是运行时取负。

## 两种执行方式

`main.py` / `ChickenStackInterpreter` 逐 token 解释执行，适合调试与短程序。

`chicken_stack/compiler.py` 把源码翻译成等价的 Python 源码，交给内置 `compile()`
生成 code object，适合长时间运行的数值程序。

编译前会做栈深分析：`[ ]` 循环体的净栈变化必须为 0，`{ | }` 两条分支结束时的栈深
必须相同。分析通过后，每个栈槽直接映射成 Python 局部变量（`v0`、`v1`……），不再有
list 的 append / pop；含 `!` 的程序索引在运行时才确定，会自动退回 list 模式。

Mandelbrot 演示（80×30，188 条指令）：解释器约 3.2 秒，编译后约 0.06 秒（CPU 时间）。

```python
from chicken_stack import compile_source

source = open("examples/mandelbrot.ch", encoding="utf-8").read()
program = compile_source(source)
output = program.run()          # 返回程序打印的全部文本
```

同一段源码在两种执行方式下输出逐字符相同，由 `tests/test_compiler.py` 校验。
编译器不支持逐 token 追踪（`--trace`），且迭代上限按循环轮次统计，而非执行的指令条数。

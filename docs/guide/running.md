# 运行方式

ChickenStack 提供多种运行代码的方式，您可以根据需要选择最适合的方式。

## 方式一：运行 .ch 文件

这是最常用的方式，适合运行已保存的 ChickenStack 程序文件。

### 基本用法

```bash
# 运行单个文件
python main.py hello_world.ch

# 运行完整示例
python main.py comprehensive_example.ch

# 运行自定义程序
python main.py my_program.ch
```

### 运行多个文件

```bash
# 依次运行多个文件
python main.py file1.ch
python main.py file2.ch
python main.py file3.ch
```

### 示例

创建 `test.ch` 文件：

```ch
# 测试程序
5 3 + .
10 20 + .
72 " 69 " 76 " 76 " 79 " 10 "
```

运行：

```bash
python main.py test.ch
```

输出：
```
8 30 HELLO
```

## 方式二：演示模式

运行内置演示，展示 ChickenStack 的各种功能。

```bash
# 运行演示模式
python main.py
```

这将运行预定义的演示程序，展示：
- 基本数学运算
- 栈操作
- 字符输出
- 循环控制
- 复杂计算

## 方式三：从 Python 代码调用

在 Python 程序中直接使用 ChickenStack 解释器。

### 基本使用

```python
from main import ChickenStackInterpreter

# 创建解释器
interpreter = ChickenStackInterpreter()

# 运行代码
interpreter.run("5 3 + .")  # 输出: 8

# 运行多行代码
code = """
10 20 + .
5 3 * .
"""
interpreter.run(code)  # 输出: 30 15
```

### 运行文件内容

```python
from main import ChickenStackInterpreter

# 创建解释器
interpreter = ChickenStackInterpreter()

# 读取文件内容
with open('my_program.ch', 'r', encoding='utf-8') as f:
    code = f.read()

# 运行代码
interpreter.run(code)
```

### 错误处理

```python
from main import ChickenStackInterpreter

interpreter = ChickenStackInterpreter()

try:
    # 可能出错的代码
    interpreter.run("+")  # 栈空错误
except Exception as e:
    print(f"捕获错误: {e}")
```

## 方式四：使用虚拟机 API

直接使用虚拟机 API 进行更细粒度的控制。

### 基本操作

```python
from chicken_stack import ChickenStackVM, IOHandler

# 创建虚拟机
vm = ChickenStackVM(io_handler=IOHandler())

# 推入数据
vm.push(10)
vm.push(20)

# 执行运算
vm.op_add()

# 打印结果
vm.op_print_num()  # 输出: 30

# 查看栈状态
print(vm.get_stack_state())  # 输出: []
```

### 复杂操作

```python
from chicken_stack import ChickenStackVM, IOHandler

vm = ChickenStackVM(io_handler=IOHandler())

# 计算 (10 + 20) * 2 = 60
vm.push(10)
vm.push(20)
vm.op_add()
vm.push(2)
vm.op_mul()
vm.op_print_num()  # 输出: 60
```

### 逐步执行

```python
from chicken_stack import ChickenStackVM, Parser, IOHandler

# 创建组件
vm = ChickenStackVM(io_handler=IOHandler())
parser = Parser()

# 解析代码
code = "10 20 + 2 * ."
tokens = parser.parse(code)
vm.loops = parser.get_loop_table()

# 逐步执行
for token in tokens:
    if isinstance(token, int):
        vm.push(token)
        print(f"推入 {token}, 栈: {vm.get_stack_state()}")
    elif token == '+':
        vm.op_add()
        print(f"执行加法, 栈: {vm.get_stack_state()}")
    elif token == '*':
        vm.op_mul()
        print(f"执行乘法, 栈: {vm.get_stack_state()}")
    elif token == '.':
        print(f"输出: ", end='')
        vm.op_print_num()
        print()
```

输出：
```
推入 10, 栈: [10]
推入 20, 栈: [10, 20]
执行加法, 栈: [30]
推入 2, 栈: [30, 2]
执行乘法, 栈: [60]
输出: 60
```

## 方式五：使用解析器

单独使用解析器来分析和预处理代码。

### 解析代码

```python
from chicken_stack import Parser

# 创建解析器
parser = Parser()

# 解析代码
code = "10 20 + ."
tokens = parser.parse(code)
print(tokens)  # 输出: [10, 20, '+', '.']
```

### 获取循环跳转表

```python
from chicken_stack import Parser

parser = Parser()

# 解析包含循环的代码
code = "5 [ : . 1 - ]"
tokens = parser.parse(code)
loop_table = parser.get_loop_table()
print(loop_table)  # 输出: {1: 6, 6: 1}
```

### 自定义解析器

```python
from chicken_stack import Parser

class CustomParser(Parser):
    def parse(self, source_code):
        tokens = super().parse(source_code)
        print(f"解析到 {len(tokens)} 个 token")
        return tokens

# 使用自定义解析器
parser = CustomParser()
tokens = parser.parse("5 3 + .")
```

## 方式六：交互式模式

创建简单的交互式解释器。

### 基本交互式解释器

```python
from main import ChickenStackInterpreter

interpreter = ChickenStackInterpreter()

print("ChickenStack 交互式解释器")
print("输入 'exit' 退出")
print("-" * 40)

while True:
    try:
        code = input(">>> ")
        if code.lower() == 'exit':
            break
        interpreter.run(code)
    except KeyboardInterrupt:
        print("\n退出")
        break
    except Exception as e:
        print(f"错误: {e}")
```

### 增强版交互式解释器

```python
from main import ChickenStackInterpreter
from chicken_stack import ChickenStackVM

interpreter = ChickenStackInterpreter()

print("ChickenStack 交互式解释器 v1.0")
print("命令: run, stack, exit")
print("-" * 40)

while True:
    try:
        cmd = input(">>> ").strip()
        
        if cmd.lower() == 'exit':
            break
        elif cmd.lower() == 'stack':
            print(f"栈: {interpreter.vm.get_stack_state()}")
        elif cmd.lower().startswith('run '):
            filename = cmd[4:].strip()
            with open(filename, 'r', encoding='utf-8') as f:
                interpreter.run(f.read())
        else:
            interpreter.run(cmd)
    except KeyboardInterrupt:
        print("\n退出")
        break
    except Exception as e:
        print(f"错误: {e}")
```

## 方式七：批处理

批量运行多个程序。

### 批处理脚本

**Windows (batch_run.bat)**:
```batch
@echo off
echo 开始批处理运行...
python main.py program1.ch
python main.py program2.ch
python main.py program3.ch
echo 批处理完成！
pause
```

**Linux/macOS (batch_run.sh)**:
```bash
#!/bin/bash
echo "开始批处理运行..."
python main.py program1.ch
python main.py program2.ch
python main.py program3.ch
echo "批处理完成！"
```

### Python 批处理

```python
import os
from main import ChickenStackInterpreter

interpreter = ChickenStackInterpreter()

# 批量运行目录下所有 .ch 文件
for filename in os.listdir('.'):
    if filename.endswith('.ch'):
        print(f"\n运行 {filename}...")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                interpreter.run(f.read())
        except Exception as e:
            print(f"错误: {e}")
```

## 方式八：Web 服务

创建简单的 Web 服务来运行 ChickenStack 代码。

### Flask Web 服务

```python
from flask import Flask, request, jsonify
from main import ChickenStackInterpreter

app = Flask(__name__)
interpreter = ChickenStackInterpreter()

@app.route('/run', methods=['POST'])
def run_code():
    code = request.json.get('code', '')
    try:
        interpreter.run(code)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(port=5000)
```

使用：
```bash
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code": "5 3 + ."}'
```

## 性能考虑

### 大程序优化

```python
from main import ChickenStackInterpreter
import time

interpreter = ChickenStackInterpreter()

# 预编译
code = open('large_program.ch', 'r').read()

# 测量执行时间
start = time.time()
interpreter.run(code)
end = time.time()
print(f"执行时间: {end - start:.3f} 秒")
```

### 内存管理

```python
from main import ChickenStackInterpreter

# 对于大程序，可以创建新的解释器实例
def run_program(code):
    interpreter = ChickenStackInterpreter()
    interpreter.run(code)
    # 解释器会自动清理
```

## 调试运行

### 调试模式

```python
from main import ChickenStackInterpreter

class DebugInterpreter(ChickenStackInterpreter):
    def run(self, source_code):
        tokens = self.parser.parse(source_code)
        self.vm.loops = self.parser.get_loop_table()
        self.vm.io_handler = self.io_handler

        print(f"Token 列表: {tokens}")
        print(f"循环跳转表: {self.vm.loops}")
        print("-" * 40)

        for i, token in enumerate(tokens):
            print(f"执行 Token #{i}: {token}")
            if isinstance(token, int):
                self.vm.push(token)
            elif token in self.op_map:
                self.op_map[token]()
            elif token == '[':
                if not self.vm.stack or self.vm.peek() == 0:
                    i = self.vm.loops[i]
            elif token == ']':
                i = self.vm.loops[i] - 1
            print(f"栈状态: {self.vm.get_stack_state()}\n")

# 使用调试解释器
interpreter = DebugInterpreter()
interpreter.run("5 3 + .")
```

## 常见问题

### Q: 如何重置解释器状态？

```python
from main import ChickenStackInterpreter

# 创建新的解释器实例
interpreter = ChickenStackInterpreter()

# 或手动清空栈
interpreter.vm.stack = []
```

### Q: 如何捕获输出？

```python
from chicken_stack import IOHandler, ChickenStackVM

class CaptureIO(IOHandler):
    def __init__(self):
        super().__init__()
        self.output = []

    def print_num(self, num):
        self.output.append(str(num))

    def print_char(self, char_code):
        self.output.append(chr(char_code))

# 使用自定义 IO
io = CaptureIO()
vm = ChickenStackVM(io_handler=io)
vm.push(5)
vm.push(3)
vm.op_add()
vm.op_print_num()
print(f"捕获的输出: {io.output}")  # 输出: ['8']
```

### Q: 如何限制执行时间？

```python
import signal
from contextlib import contextmanager
from main import ChickenStackInterpreter

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutError("执行超时")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

# 使用时间限制
interpreter = ChickenStackInterpreter()
try:
    with time_limit(5):  # 限制 5 秒
        interpreter.run("1 [ : . ]")  # 无限循环
except TimeoutError:
    print("程序执行超时")
```

---

本文档由 AI GLM-4.7 生成
from chicken_stack import Parser

# 读取文件
import os
file_path = 'hello_world.ch'
if not os.path.exists(file_path):
    print(f"文件不存在: {file_path}")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 解析代码
p = Parser()
tokens = p.parse(code)

print(f"Token count: {len(tokens)}")
print(f"First 30 tokens: {tokens[:30]}")
print(f"Tokens at position 50-80: {tokens[50:80]}")
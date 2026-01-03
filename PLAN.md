# ChickenStack 解析器进一步优化计划

## 目标
在保持完全兼容性的前提下，进一步优化解析器性能，预期提升 10-20%。

## 当前性能基准
- 平均时间：0.013954 ms
- 已完成优化：字典查找、空格检查、方法引用缓存、数字处理、循环表构建
- 性能提升：约 27%

## 优化方案

### 优化点 1：Token 方法中的集合优化（高优先级）

**位置**：`chicken_stack/parser.py` 第 85-125 行

**问题**：每次调用 `is_operator()` 等方法时，都会创建新的集合对象

**优化方法**：
- 将集合提升到类级别，使用 `frozenset` 避免被修改
- 所有 Token 实例共享同一个集合对象

**修改内容**：
```python
class Token:
    __slots__ = ('type', 'value', 'line', 'column')
    
    # 类级别的常量集合
    _OPERATOR_TYPES = frozenset({
        TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY,
        TokenType.DIVIDE, TokenType.MODULO
    })
    
    _STACK_OP_TYPES = frozenset({TokenType.DUP, TokenType.SWAP, TokenType.DROP})
    
    _LOGIC_OP_TYPES = frozenset({TokenType.EQ, TokenType.GT})
    
    _IO_OP_TYPES = frozenset({
        TokenType.PRINT_NUM, TokenType.PRINT_CHAR,
        TokenType.INPUT_NUM, TokenType.INPUT_CHAR
    })
    
    _LOOP_TYPES = frozenset({TokenType.LOOP_START, TokenType.LOOP_END})
    
    def is_operator(self) -> bool:
        return self.type in self._OPERATOR_TYPES
    
    def is_stack_op(self) -> bool:
        return self.type in self._STACK_OP_TYPES
    
    def is_logic_op(self) -> bool:
        return self.type in self._LOGIC_OP_TYPES
    
    def is_io_op(self) -> bool:
        return self.type in self._IO_OP_TYPES
    
    def is_loop(self) -> bool:
        return self.type in self._LOOP_TYPES
```

**预期提升**：5-10%
**风险**：低
**兼容性**：完全兼容

---

### 优化点 2：Parser.parse() 中的常量优化（高优先级）

**位置**：`chicken_stack/parser.py` 第 175-195 行

**问题**：每次调用 `parse()` 方法时，都会创建新的 `WHITESPACE` 集合和 `char_to_token` 字典

**优化方法**：
- 将常量提升到类级别
- 使用 `frozenset` 和字典字面量

**修改内容**：
```python
class Parser:
    __slots__ = ('loops',)
    MAX_LOOP_DEPTH = 100
    
    # 类级别的常量
    _WHITESPACE = frozenset({' ', '\t', '\r'})
    
    _CHAR_TO_TOKEN = {
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.MULTIPLY,
        '/': TokenType.DIVIDE,
        '%': TokenType.MODULO,
        ':': TokenType.DUP,
        '\\': TokenType.SWAP,
        '$': TokenType.DROP,
        '=': TokenType.EQ,
        '>': TokenType.GT,
        '.': TokenType.PRINT_NUM,
        '"': TokenType.PRINT_CHAR,
        ',': TokenType.INPUT_NUM,
        '?': TokenType.INPUT_CHAR,
        '[': TokenType.LOOP_START,
        ']': TokenType.LOOP_END,
    }
    
    def parse(self, source_code: str) -> list[Token]:
        # ...
        # 直接使用类级别的常量
        if char not in self._WHITESPACE:
            token_type = self._CHAR_TO_TOKEN.get(char)
            # ...
```

**预期提升**：5-10%
**风险**：低
**兼容性**：完全兼容

---

### 优化点 3：Token 创建的一致性优化（低优先级）

**位置**：`chicken_stack/parser.py` 第 220-235 行

**问题**：缓存了 `token_integer = Token` 但只用于一个地方，其他地方仍然使用 `Token(...)`

**优化方法**：统一使用缓存的 Token 类引用

**修改内容**：
```python
# 统一使用缓存的 Token 类引用
token_integer = Token

# 所有 Token 创建都使用缓存的引用
tokens_append(token_integer(TokenType.INTEGER, value, line, start_column))
tokens_append(token_integer(token_type, line=line, column=column))
```

**预期提升**：1-2%
**风险**：低
**兼容性**：完全兼容

---

## 实施步骤

1. **步骤 1**：实施优化点 1（Token 方法中的集合优化）
2. **步骤 2**：实施优化点 2（Parser.parse() 中的常量优化）
3. **步骤 3**：实施优化点 3（Token 创建的一致性优化）
4. **步骤 4**：运行 20 次测试验证性能
5. **步骤 5**：对比优化前后的测试结果

## 预期结果

- 总体性能提升：10-20%
- 所有测试通过（100/100）
- API 完全兼容
- 代码可读性保持或提升

## 关键文件

- `chicken_stack/parser.py` - 唯一需要修改的文件

## 验证方法

```bash
# 运行优化验证测试（20次）
python test_optimization.py

# 运行综合测试（20次）
python tests/run_comprehensive_tests.py

# 运行性能基准测试（20次）
python tests/benchmark_parser.py
```

## 风险评估

所有优化都是低风险：
- 不改变 API 接口
- 不影响功能逻辑
- 只改变内部实现
- 易于回滚
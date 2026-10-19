from chicken_stack import Parser, ChickenStackVM, IOHandler, Token, TokenType

class MockIOHandler(IOHandler):
    def __init__(self, inputs):
        super().__init__()
        self.inputs = list(inputs)
        self.idx = 0
    def get_num(self):
        print(f"  [输入: {self.inputs[self.idx]}]", end='', flush=True)
        val = self.inputs[self.idx]
        self.idx += 1
        return val
    def get_char(self):
        return b'\r'

def run_game(inputs, label):
    parser = Parser()
    with open('examples/guessing_game.ch', 'r', encoding='utf-8') as f:
        code = f.read()
    tokens = parser.parse(code)
    
    vm = ChickenStackVM(max_iterations=50000)
    io = MockIOHandler(inputs)
    vm.io_handler = io
    vm.loops = parser.get_loop_table()
    
    idx = 0
    limit = len(tokens)
    while idx < limit:
        token = tokens[idx]
        if token.is_integer():
            vm.push(token.value)
        elif token.type == TokenType.LOOP_START:
            if not vm.stack or vm.peek() == 0:
                idx = vm.loops[idx]
        elif token.type == TokenType.LOOP_END:
            idx = vm.loops[idx] - 1
        elif token.type == TokenType.DUP: vm.op_dup()
        elif token.type == TokenType.SWAP: vm.op_swap()
        elif token.type == TokenType.DROP: vm.op_drop()
        elif token.type == TokenType.EQ: vm.op_eq()
        elif token.type == TokenType.GT: vm.op_gt()
        elif token.type == TokenType.MINUS: vm.op_sub()
        elif token.type == TokenType.PRINT_CHAR: vm.op_print_char()
        elif token.type == TokenType.INPUT_NUM: vm.op_input_num()
        idx += 1
        if idx > 10000:
            print("  [安全停止: 迭代过多]")
            break
    
    print(f"\n  栈: {vm.get_stack_state()} | 迭代: {vm.iteration_count}")
    return vm

print("-" * 50)
print("测试1: 一次就猜对 (输入 42)")
print("-" * 50)
run_game([42], "test1")

print("\n测试2: 猜太小 -> 猜对 (输入 20, 42)")
run_game([20, 42], "test2")

print("\n测试3: 猜太大 -> 猜对 (输入 80, 42)")
run_game([80, 42], "test3")

print("\n测试4: 多轮猜测 (10 -> 60 -> 30 -> 50 -> 42)")
run_game([10, 60, 30, 50, 42], "test4")

print("\n" + "-" * 50)
print("全部测试完成!")
print("-" * 50)

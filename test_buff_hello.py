from main import ChickenStackInterpreter

code = '104 " 101 " 108 " 108 " 111 " 32 " 104 " 101 " 108 " 108 " 111 " 32 " 66 " 85 " 70 " 70 " 32 " 105 " 109 " 32 " 117 " 114 " 32 " 102 " 97 " 116 " 104 " 101 " 114 " 10 "'

interpreter = ChickenStackInterpreter()
interpreter.run(code)
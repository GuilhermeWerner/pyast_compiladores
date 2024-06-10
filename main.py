import ast
from printer.printer import ExprPrinter

code = """
def foo(a, b):
    return a + b

foo(1, 2)
"""

if __name__ == '__main__':
    tree = ast.parse(code)
    printer = ExprPrinter()
    printer.visit(tree)
    # print(ast.dump(tree))
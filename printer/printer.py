import ast

class ExprPrinter(ast.NodeVisitor):
    def generic_visit(self, node):  # Lida com o caso base - todos os nós
        print(type(node).__name__)
        self.visit_children(node)

    # Esta função visita os nós que são FunctionDef
    def visit_FunctionDef(self, node):
        print(type(node).__name__)
        print(f"\tArgumentos da função:")
        for item in node.args.args:
            print(f"\t{item.arg}")
        self.visit_children(node)

    # Esta função visita os nós que são Call
    def visit_Call(self, node):
        print(type(node).__name__)
        print(f"\tParâmetros da chamada:")
        for item in node.args:
            print(f"\t{item}")
        self.visit_children(node)

    def visit_children(self, node):  # Visita os nós filhos
        for field, value in ast.iter_fields(node):
            if isinstance(value, list): # múltiplos filhos
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)    
            else:
                if isinstance(value, ast.AST): # filho único
                    self.visit(value) 
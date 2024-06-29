import ast
import sys
from graphviz import Digraph
from pathlib import Path

# Função que desenha o grafo da árvore sintática abstrata
def draw_graph(node, parent=None, global_scope=None):
    global dot
    
    node_name = str(node.__class__.__name__)
    
    # Adiciona o nome da função ao global_scope (utilizado para ligar as chamadas de função aos FunctionDef)
    if isinstance(node, ast.FunctionDef):
        global_scope[node.name] = node
    
    dot.node(str(id(node)), node_name)
    
    # Ligação entre os nós
    if parent:
        dot.edge(str(id(parent)), str(id(node)))
    
    # Ligação das chamadas de função aos FunctionDef
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in global_scope:
                dot.edge(str(id(node)), str(id(global_scope[func_name])), color='green')
        
        # Ligação das constantes aos argumentos dos FunctionDef
        if isinstance(node.func, ast.Name) and func_name in global_scope:
            func_def = global_scope[func_name]
            for i, arg in enumerate(node.args):
                if isinstance(arg, ast.Constant) and i < len(func_def.args.args):
                    arg_name = func_def.args.args[i].arg
                    dot.edge(str(id(arg)), str(id(func_def.args.args[i])), color='red')
    
    for child in ast.iter_child_nodes(node):
        draw_graph(child, node, global_scope)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_python_file>")
    else:
        file_path = sys.argv[1]
        
    file_content = Path(file_path).read_text()
    tree = ast.parse(file_content)
    print(ast.dump(tree, indent=4))
    dot = Digraph()
    global_scope = {}
    
    draw_graph(tree, global_scope=global_scope)
    
    # Configurações do grafo
    dot.format = 'png'
    dot.graph_attr['rankdir'] = 'TD'
    dot.node_attr['shape'] = 'square'
    dot.render('ast')

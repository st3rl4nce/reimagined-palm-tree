from pycparser import  c_ast, parse_file

class ArrayVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.array_decls = {}

    def visit_ArrayDecl(self, node):
        array_name = node.type.declname
        array_size = node.dim.value
        array_scope = node.coord
        self.array_decls[array_name] = (array_size, array_scope)

class ArrayRefVisitor(c_ast.NodeVisitor):
    def __init__(self, array_decls):
        self.array_decls = array_decls

    def get_variable_value(self, node, var_name):
        parent = node.parent
        while not isinstance(parent, c_ast.FuncDef):
            if isinstance(parent, c_ast.Decl) and parent.name == var_name:
                if isinstance(parent.init, c_ast.Constant):
                    return parent.init.value
                else:
                    return None
            parent = parent.parent
        if isinstance(parent, c_ast.Compound):
            for decl in parent.decls:
                if isinstance(decl, c_ast.Decl) and decl.name == var_name:
                    if isinstance(decl.init, c_ast.Constant):
                        return decl.init.value
                    else:
                        return None
        return None
    def visit_ArrayRef(self, node):
        array_name = node.name.name
        # array index can be a constant or a variable
        if isinstance(node.subscript, c_ast.Constant):
            index_value = node.subscript.value
        elif isinstance(node.subscript, c_ast.ID):
            index_value = node.subscript.name
            # calculate the value of the variable at the given instance
            index_value = self.get_variable_value(node, index_value)

        else:
            return

        array_size, array_scope = self.array_decls[array_name]
        # typecast index_value to int and array_size to int
        index_value = int(index_value)
        array_size = int(array_size)
        if index_value >= array_size:
            print(f"Error: Array index out of bounds in {array_scope.file} at {node.coord}. Array '{array_name}' of size {array_size} accessed with index {index_value}.")

def check_array_out_of_bounds(filename):
    ast = parse_file(filename, use_cpp=True)
    array_visitor = ArrayVisitor()
    array_visitor.visit(ast)

    array_ref_visitor = ArrayRefVisitor(array_visitor.array_decls)
    array_ref_visitor.visit(ast)


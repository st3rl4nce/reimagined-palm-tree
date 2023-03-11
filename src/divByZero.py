from pycparser import c_parser, c_ast

# Define a visitor class that searches for division by zero errors
class DivByZeroVisitor(c_ast.NodeVisitor):
    def visit_BinaryOp(self, node):
        if node.op == '/':
            if isinstance(node.right, c_ast.Constant) and node.right.value == '0':
                print("Division by zero error at line", node.coord)
            elif isinstance(node.right, c_ast.UnaryOp) and isinstance(node.right.expr, c_ast.Constant) and node.right.op == '-':
                if node.right.expr.value == '0':
                    print("Division by zero error at line", node.coord)
            elif isinstance(node.right, c_ast.BinaryOp) and node.right.op in ['+', '-']:
                left = node.right.left
                right = node.right.right
                if isinstance(left, c_ast.Constant) and left.value == '0':
                    if isinstance(right, c_ast.Constant) and right.value == '0' and node.right.op == '-':
                        print("Division by zero error at line", node.coord)
                    elif isinstance(right, c_ast.UnaryOp) and isinstance(right.expr, c_ast.Constant) and right.op == '-':
                        if right.expr.value == '0':
                            print("Division by zero error at line", node.coord)
                elif isinstance(right, c_ast.Constant) and right.value == '0':
                    if isinstance(left, c_ast.Constant) and left.value == '0':
                        print("Division by zero error at line", node.coord)
                    elif isinstance(left, c_ast.UnaryOp) and isinstance(left.expr, c_ast.Constant) and left.op == '-':
                        if left.expr.value == '0':
                            print("Division by zero error at line", node.coord)
            elif isinstance(node.right, c_ast.ID):
                var_name = node.right.name
                var_decl = self.get_variable_declaration(node, var_name)
                if var_decl is not None:
                    if isinstance(var_decl.type, c_ast.PtrDecl):
                        print("Possible division by zero error at line", node.coord, "(indirect division by zero through pointer)")
                    elif isinstance(var_decl.type, c_ast.TypeDecl) and isinstance(var_decl.type.type, c_ast.ArrayDecl):
                        array_size = self.get_array_size(var_decl.type.type)
                        if isinstance(array_size, int) and array_size > 0:
                            print("Possible division by zero error at line", node.coord, "(division by uninitialized or out-of-bounds array element)")
        self.generic_visit(node)

    def get_variable_declaration(self, node, var_name):
        parent = node.parent
        while not isinstance(parent, c_ast.FuncDef):
            if isinstance(parent, c_ast.Decl) and parent.name == var_name:
                return parent
            parent = parent.parent
        if isinstance(parent, c_ast.Compound):
            for decl in parent.decls:
                if isinstance(decl, c_ast.Decl) and decl.name == var_name:
                    return decl
        return None

    def get_array_size(self, array_type):
        if isinstance(array_type.dim, c_ast.Constant):
            return int(array_type.dim.value)
        elif isinstance(array_type.dim, c_ast.ID):
            var_name = array_type.dim.name
            var_decl = self.get_variable_declaration(array_type, var_name)
            if isinstance(var_decl, c_ast.Decl) and isinstance(var_decl.type, c_ast.TypeDecl) and isinstance(var_decl.type.type, c_ast.ArrayDecl):
                return self.get_array_size(var_decl.type.type)
        return

# main
def check_division_by_zero(filename):
    # Parse the input file
    parser = c_parser.CParser()
    ast = parser.parse(open(filename).read())

    # Search for division by zero errors
    visitor = DivByZeroVisitor()
    visitor.visit(ast)
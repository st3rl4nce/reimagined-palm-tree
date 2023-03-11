from pycparser import c_ast, parse_file

def find_uninitialized_variables(filename):
    ast = parse_file(filename=filename, use_cpp=False, cpp_path='gcc',
            cpp_args=['-E', r'-Iutils/fake_libc_include'])
    uninitialized_vars = []

    class VariableVisitor(c_ast.NodeVisitor):
        def visit_Decl(self, node):
            if node.init is None:
                # if function declaration, skip
                if isinstance(node.type, c_ast.FuncDecl):
                    return
                uninitialized_vars.append(node.name)

    visitor = VariableVisitor()
    visitor.visit(ast)
    return uninitialized_vars

def check_uninitialized_variables(filename):
    uninitialized_vars = find_uninitialized_variables(filename)

    if len(uninitialized_vars) == 0:
        print("No uninitialized variables found")
    else:
        print("Uninitialized variables found: ", uninitialized_vars)

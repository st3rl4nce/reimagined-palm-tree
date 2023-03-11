from pycparser import c_parser, c_ast

# Define a visitor class that traverses the AST and finds all variable declarations
class VariableDeclarationsVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.variables = set()

    def visit_Decl(self, node):
        if isinstance(node.type.type, c_ast.IdentifierType):
            self.variables.add(node.name)

# Define a visitor class that traverses the AST and finds all variable references
class VariableReferencesVisitor(c_ast.NodeVisitor):
    def __init__(self):
        self.variables = set()

    def visit_ID(self, node):
        self.variables.add(node.name)

# Define a function that finds unused variables in a C program
def find_unused_variables(filename):
    # Parse the C program using Pycparser
    parser = c_parser.CParser()
    ast = parser.parse(open(filename, 'r').read())

    # Traverse the AST and find all variable declarations
    declarations_visitor = VariableDeclarationsVisitor()
    declarations_visitor.visit(ast)

    # Traverse the AST and find all variable references
    references_visitor = VariableReferencesVisitor()
    references_visitor.visit(ast)

    # Find the unused variables in the C program
    unused_variables = list(declarations_visitor.variables-references_visitor.variables)

    # Return the unused variables
    return unused_variables

# Test the program
def check_unused_variables(filename):
    unused_variables = find_unused_variables(filename)
    if(len(unused_variables) == 0):
        print("No unused variables found")
    else:
        print("Unused variables in {}: {}".format(filename, unused_variables))

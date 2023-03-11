import ply.lex as lex
import ply.yacc as yacc
import pycparser

# Define the tokens for the lexer
tokens = (
    'ID',
    'INT',
    'FLOAT',
    'DOUBLE',
    'CHAR',
    'ASSIGN',
    'SEMICOLON',
)

# Define the regular expressions for each token
t_ASSIGN = r'='
t_SEMICOLON = r';'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_DOUBLE(t):
    r'\d+\.\d+[eE][+-]?\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CHAR(t):
    r"'.'"
    t.value = str(t.value)[1:-1]
    return t

# Define the error function for the lexer
def t_error(t):
    print("Lexer error on line %d: Invalid token %r" % (t.lineno, t.value[0]))
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Define the grammar for the parser
def p_statement(p):
    '''statement : ID ASSIGN expression SEMICOLON
                 | ID SEMICOLON'''
    pass

def p_expression(p):
    '''expression : INT
                  | FLOAT
                  | DOUBLE
                  | CHAR
                  | ID'''
    pass

# Define the error function for the parser
def p_error(p):
    if p:
        print("Parser error on line %d: Syntax error at token %r" % (p.lineno, p.value))
    else:
        print("Parser error: Unexpected end of input")

# Build the parser
parser = yacc.yacc()

# define a function to get code out of a function definition
def get_code_from_fxn(c_program, fxn_name):
    ast = pycparser.parse_file(c_program, use_cpp=False)
    for node in ast.ext:
        if isinstance(node, pycparser.c_ast.FuncDef):
            if node.decl.name == fxn_name:
                return node.body.block_items

# define a function to check type compatibitlity
def check_type_compatibility(c_program, lhs_type, rhs_type):
    # float and double are compatible
    if lhs_type == 'float' and rhs_type == 'double':
        return True
    elif lhs_type == 'double' and rhs_type == 'float':
        return True
    # we can assign int to float but not vice versa
    # elif (lhs_type == 'float' or lhs_type == 'double') and rhs_type == 'int':
    #     return True
    # elif lhs_type == 'int' and rhs_type == 'char':
    #     return True
    # elif lhs_type == 'char' and rhs_type == 'int':
    #     return True
    # if both are the same type, they are compatible
    elif lhs_type == rhs_type:
        return True
    return False

# function to get the type of a variable
def get_type_of_variable(c_program, var_name):
    ast = pycparser.parse_file(c_program, use_cpp=False)
    for node in ast.ext:
        # if funcDef, go inside
        if isinstance(node, pycparser.c_ast.FuncDef):
            for node2 in node.body.block_items:
                # if declaration, check if the variable is the one we want
                if isinstance(node2, pycparser.c_ast.Decl):
                    # if arraydecl, skip
                    if isinstance(node2.type, pycparser.c_ast.ArrayDecl):
                        continue
                    if node2.name == var_name.name:
                        return node2.type.type.names[0]
        else:
            if isinstance(node, pycparser.c_ast.Decl):
                # if arraydecl, skip
                if isinstance(node.type, pycparser.c_ast.ArrayDecl):
                    continue
                if node.name == var_name.name:
                    return node.type.type.names[0]
    return None

# function to get type of array
def get_type_of_array(c_program, array_name):
    ast = pycparser.parse_file(c_program, use_cpp=False)
    for node in ast.ext:
        # if funcDef, go inside
        if isinstance(node, pycparser.c_ast.FuncDef):
            for node2 in node.body.block_items:
                # if declaration, check if the variable is the one we want
                if isinstance(node2, pycparser.c_ast.Decl):
                    # if arraydecl, skip
                    if isinstance(node2.type, pycparser.c_ast.ArrayDecl):
                        if node2.name == array_name.name:
                            return node2.type.type.type.names[0]
        else:
            if isinstance(node, pycparser.c_ast.Decl):
                # if arraydecl, skip
                if isinstance(node.type, pycparser.c_ast.ArrayDecl):
                    if node.name == array_name.name:
                        return node.type.type.type.names[0]
    return None

# funtion to get the type of a function
def get_type_of_function(c_program, fxn_name):
    ast = pycparser.parse_file(c_program, use_cpp=False)
    for node in ast.ext:
        # if funcDef, go inside
        if isinstance(node, pycparser.c_ast.FuncDef):
            if node.decl.name == fxn_name:
                return node.decl.type.type.type.names[0]
    return None

# function to detect type mismatches
def check_type_mismatches(c_program):
    ast = pycparser.parse_file(c_program, use_cpp=False)
    for node in ast.ext:
        # if function definition, get the code out of it
        if isinstance(node, pycparser.c_ast.FuncDef):
            code = node.body.block_items
        else:
            continue
        # for each line of code, check for type mismatch
        for line in code:
            # if assignment statement, check for type mismatch
            if isinstance(line, pycparser.c_ast.Assignment):
                # get the type of the left hand side
                # if arrayref, get the type of the array
                if isinstance(line.lvalue, pycparser.c_ast.ArrayRef):
                    lhs_type = get_type_of_array(c_program, line.lvalue.name)
                else:
                    lhs_type = get_type_of_variable(c_program, line.lvalue)
                # get the type of the right hand side
                # rhs can be an expression or variable or constant
                # if expression, we can't do anything without acually executing the code, so we can ignore it for static analysis
                if isinstance(line.rvalue, pycparser.c_ast.BinaryOp):
                    continue
                # if unary, get the type of the variable
                elif isinstance(line.rvalue, pycparser.c_ast.UnaryOp):
                    rhs_type = 'int'
                elif isinstance(line.rvalue, pycparser.c_ast.ArrayRef):
                    rhs_type = get_type_of_array(c_program, line.rvalue.name)
                elif isinstance(line.rvalue, pycparser.c_ast.Constant):
                    rhs_type = line.rvalue.type
                else:
                    rhs_type = get_type_of_variable(c_program, line.rvalue)
                # if the types are not the same, print error
                if check_type_compatibility(c_program, lhs_type, rhs_type) == False:
                    print("Type mismatch on line %s: %s = %s" % (line.coord, lhs_type, rhs_type))
            # if declaration statement, check for type mismatch
            elif isinstance(line, pycparser.c_ast.Decl):
                # get the type of the variable
                var_type = get_type_of_variable(c_program, line)
                # if the variable has an initializer, get the type of the initializer
                if line.init:
                    # if binaryOp, rhs is definitely an expression, so we can ignore it for static analysis
                    if isinstance(line.init, pycparser.c_ast.BinaryOp):
                        continue
                    elif isinstance(line.init, pycparser.c_ast.UnaryOp):
                        init_type = 'int'
                    else:
                        init_type = line.init.type
                    # if the types are not the same, print error
                    if var_type != init_type:
                        print("Type mismatch on line %s: %s = %s" % (line.coord, var_type, init_type))
            # if return statement, check for type mismatch
            elif isinstance(line, pycparser.c_ast.Return):
                # get the type of the return value
                # if binaryOp, rhs is definitely an expression, so we can ignore it for static analysis
                if isinstance(line.expr, pycparser.c_ast.BinaryOp):
                    continue
                elif isinstance(line.expr, pycparser.c_ast.UnaryOp):
                    return_type = 'int'
                elif isinstance(line.expr, pycparser.c_ast.ArrayRef):
                    return_type = get_type_of_array(c_program, line.expr.name)
                elif isinstance(line.expr, pycparser.c_ast.Constant):
                    return_type = line.expr.type
                else:
                    return_type = get_type_of_variable(c_program, line.expr)
                # get the type of the function
                func_type = get_type_of_function(c_program, node.decl.name)
                # if the types are not the same, print error
                if func_type != return_type:
                    print("Type mismatch on line %s: function return type: %s, return value type: %s" % (line.coord, func_type, return_type))

from enum import Enum, auto
from globalTypes import TokenType

class PT(Enum):             # ParserTypes (PT)
    program = "<program>"
    dec_list = "<declaration-list>"
    dec = "<declaration>"                
    dec_p = "<declaration-prime>"
    type_specifier = "<type-specifier>"
    params = "<params>"
    param_list = "<param-list>"
    param_list_p = "<param-list-prime>"     
    param = "<param>"
    param_p = "<param-prime>"
    compound_stmt = "<compound-stmt>"
    local_decs = "<local-declarations>"
    var_dec = "<var-declaration>"
    var_dec_p = "<var-declaration-prime>"
    stmt_list = "<statement-list>"          
    stmt = "<statement>"
    expr_stmt = "<expression-stmt>"          
    selection_stmt = "<selection-stmt>"
    selection_stmt_p = "<selection-stmt-prime>"
    iteration_stmt = "<iteration-stmt>"
    return_stmt = "<return-stmt>"
    return_stmt_p = "<return-stmt-prime>"
    expr = "<expression>"
    expr_p = "<expression-prime>"
    var = "<var>"
    var_p = "<var-prime>"
    simple_expr = "<simple-expression>"
    simple_expr_p = "<simple-expression-prime>"
    relop = "<relop>"
    additive_expr = "<additive-expression>"
    additive_expr_p = "<additive-expression-prime>"
    addop = "<addop>"
    term = "<term>"
    term_p = "<term-prime>"
    mulop = "<mulop>"
    factor = "<factor>"
    factor_p = "<factor-prime>"
    args = "<args>"
    arg_list = "<arg-list>"
    arg_list_p = "<arg-list-prime>"
    lambda_pass = "λ"

def get_row(token):
    if token == PT.program:
        return 0
    elif token == PT.dec_list:
        return 1
    elif token == PT.dec:
        return 2
    elif token == PT.dec_p:
        return 3
    elif token == PT.type_specifier:
        return 4
    elif token == PT.params:
        return 5
    elif token == PT.param_list:
        return 6
    elif token == PT.param_list_p:
        return 7
    elif token == PT.param:
        return 8
    elif token == PT.param_p:
        return 9
    elif token == PT.compound_stmt:
        return 10
    elif token == PT.local_decs:
        return 11
    elif token == PT.var_dec:
        return 12
    elif token == PT.var_dec_p:
        return 13
    elif token == PT.stmt_list:
        return 14
    elif token == PT.stmt:
        return 15
    elif token == PT.expr_stmt:
        return 16
    elif token == PT.selection_stmt:
        return 17
    elif token == PT.selection_stmt_p:
        return 18
    elif token == PT.iteration_stmt:
        return 19
    elif token == PT.return_stmt:
        return 20
    elif token == PT.return_stmt_p:
        return 21
    elif token == PT.expr:
        return 22
    elif token == PT.expr_p:
        return 23
    elif token == PT.var:
        return 24
    elif token == PT.var_p:
        return 25
    elif token == PT.simple_expr:
        return 26
    elif token == PT.simple_expr_p:
        return 27
    elif token == PT.relop:
        return 28
    elif token == PT.additive_expr:
        return 29
    elif token == PT.additive_expr_p:
        return 30
    elif token == PT.addop:
        return 31
    elif token == PT.term:
        return 32
    elif token == PT.term_p:
        return 33
    elif token == PT.mulop:
        return 34
    elif token == PT.factor:
        return 35
    elif token == PT.factor_p:
        return 36
    elif token == PT.args:
        return 37
    elif token == PT.arg_list:
        return 38
    elif token == PT.arg_list_p:
        return 39
    else:
        raise ValueError("Unrecognized parser row: ", token)
    
def get_column(token, token_string):
    # Small custom mapping, based on your parsing table structure
    if token == TokenType.RESERVED:
        if token_string == "int":
            return 13 
        if token_string == "void":
            return 14
        elif token_string == "if":
            return 9
        elif token_string == "else":
            return 10
        elif token_string == "while":
            return 11
        elif token_string == "return":
            return 12
    elif token == TokenType.ID:
        return 25
    elif token == TokenType.NUM:
        return 26
    elif token == TokenType.OPS:
        if token_string == "+":
            return 15
        if token_string == "-":
            return 16
        if token_string == "*":
            return 17
        if token_string == "/":
            return 18
    elif token == TokenType.PUN_SEP:
        if token_string == "(":
            return 0
        if token_string == ")":
            return 1
        if token_string == ";":
            return 4
        if token_string == ",":
            return 5
        if token_string == "{":
            return 6
        if token_string == "}":
            return 7
        if token_string == "[":
            return 2
        if token_string == "]":
            return 3
    elif token == TokenType.COMP:
        if token_string == "<=":
            return 19
        if token_string == "<":
            return 20
        if token_string == ">":
            return 21
        if token_string == ">=":
            return 22
        if token_string == "==":
            return 23
        if token_string == "!=":
            return 24
    elif token == TokenType.ASG:
        return 8
    elif token == TokenType.ENDFILE:
        return 27
    raise ValueError(f"Unrecognized parser col: {token}")


parsingTable = [
    [[],[],[],[],[],[],[],[],[],[],[],[],[],[PT.dec_list],[PT.dec_list],[],[],[],[],[],[],[],[],[],[],[],[],[PT.lambda_pass]],
    [[],[],[],[],[],[],[],[],[],[],[],[],[],[PT.dec, PT.dec_list],[PT.dec, PT.dec_list],[],[],[],[],[],[],[],[],[],[],[],[],[PT.lambda_pass]],
    [[],[],[],[],[],[],[],[],[],[],[],[],[],[PT.type_specifier, TokenType.ID, PT.dec_p],[PT.type_specifier, TokenType.ID, PT.dec_p],[],[],[],[],[],[],[],[],[],[],[],[],[]],
    [["(", PT.params, ")", PT.compound_stmt],[],["[", TokenType.NUM, "]", ";"],[],[";"],[",", TokenType.ID, PT.dec_p],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[],[],[],[],[],["int"],["void"],[],[],[],[],[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[],[],[],[],[],[PT.param_list],["void"],[],[],[],[],[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[],[],[],[],[],[PT.param, PT.param_list_p],[PT.param, PT.param_list_p],[],[],[],[],[],[],[],[],[],[],[],[],[]],
    [[],[PT.lambda_pass],[],[],[],[",", PT.param ,PT.param_list_p],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[],[],[],[],[],[PT.type_specifier, TokenType.ID, PT.param_p],[PT.type_specifier, TokenType.ID, PT.param_p],[],[],[],[],[],[],[],[],[],[],[],[],[]],
    [[],[PT.lambda_pass],["[", "]"],[],[],[PT.lambda_pass],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],["{", PT.local_decs, PT.stmt_list, "}"],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
    [[PT.lambda_pass],[],[],[],[PT.lambda_pass],[],[PT.lambda_pass],[PT.lambda_pass],[],[PT.lambda_pass],[],[PT.lambda_pass],[PT.lambda_pass],[PT.var_dec, PT.local_decs],[PT.var_dec, PT.local_decs],[],[],[],[],[],[],[],[],[],[],[PT.lambda_pass],[PT.lambda_pass],[]],
    [[],[],[],[],[],[],[],[],[],[],[],[],[],[PT.type_specifier, TokenType.ID, PT.var_dec_p],[PT.type_specifier, TokenType.ID, PT.var_dec_p],[],[],[],[],[],[],[],[],[],[],[],[],[]],
    [[],[],["[", TokenType.NUM, "]", ";"],[],[";"],[",", TokenType.ID, PT.var_dec_p],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
    [[PT.stmt, PT.stmt_list],[],[],[],[PT.stmt, PT.stmt_list],[],[PT.stmt, PT.stmt_list],[PT.lambda_pass],[],[PT.stmt, PT.stmt_list],[],[PT.stmt, PT.stmt_list],[PT.stmt, PT.stmt_list],[],[],[],[],[],[],[],[],[],[],[],[],[PT.stmt, PT.stmt_list],[PT.stmt, PT.stmt_list],[]],
    [[PT.expr_stmt],[],[],[],[PT.expr_stmt],[],[PT.compound_stmt],[],[],[PT.selection_stmt],[],[PT.iteration_stmt],[PT.return_stmt],[],[],[],[],[],[],[],[],[],[],[],[],[PT.expr_stmt],[PT.expr_stmt],[]],
    [[PT.expr, ";"],[],[],[],[";"],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[PT.expr, ";"],[PT.expr, ";"],[]],
    [[],[],[],[],[],[],[],[],[],["if", "(", PT.expr, ")", PT.stmt, PT.selection_stmt_p ],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
    [[PT.lambda_pass],[],[],[],[PT.lambda_pass],[],[PT.lambda_pass],[PT.lambda_pass],[],[PT.lambda_pass],["else", PT.stmt],[PT.lambda_pass],[PT.lambda_pass],[],[],[],[],[],[],[],[],[],[],[],[],[PT.lambda_pass],[PT.lambda_pass],[]],
    [[],[],[],[],[],[],[],[],[],[],[],["while", "(", PT.expr, ")", PT.stmt],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[],[],[],[],["return", PT.return_stmt_p],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
    [[PT.expr, ";"],[],[],[],[";"],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[PT.expr, ";"],[PT.expr, ";"],[]],
    [[PT.simple_expr, PT.expr_p],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[PT.simple_expr, PT.expr_p],[PT.simple_expr, PT.expr_p],[]],
    [[],[PT.lambda_pass],[],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[],[],["=", PT.expr],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
    [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[TokenType.ID, PT.var_p],[],[]],
    [[],[PT.lambda_pass],["[" , PT.expr, "]"],[PT.lambda_pass],[PT.lambda_pass],[],[],[],[PT.lambda_pass],[],[],[],[],[],[],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[],[],[]],
    [[PT.additive_expr, PT.simple_expr_p],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[PT.additive_expr, PT.simple_expr_p],[PT.additive_expr, PT.simple_expr_p],[]],
    [[],[PT.lambda_pass],[],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[],[],[],[],[],[],[],[],[],[],[],[],[],[PT.relop, PT.additive_expr],[PT.relop, PT.additive_expr],[PT.relop, PT.additive_expr],[PT.relop, PT.additive_expr],[PT.relop, PT.additive_expr],[PT.relop, PT.additive_expr],[],[],[]],
    [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],["<="],["<"],[">"],[">="],["=="],["!="],[],[],[]],
    [[PT.term, PT.additive_expr_p],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[PT.term, PT.additive_expr_p],[PT.term, PT.additive_expr_p],[]],
    [[],[PT.lambda_pass],[],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[],[],[],[],[],[],[],[],[],[PT.addop, PT.term, PT.additive_expr_p],[PT.addop, PT.term, PT.additive_expr_p],[],[],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[],[],[]],
    [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],["+"],["-"],[],[],[],[],[],[],[],[],[],[],[]],
    [[PT.factor, PT.term_p],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[PT.factor, PT.term_p],[PT.factor, PT.term_p],[]],
    [[],[PT.lambda_pass],[],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[],[],[],[],[],[],[],[],[],[PT.lambda_pass],[PT.lambda_pass],[PT.mulop, PT.factor, PT.term_p],[PT.mulop, PT.factor, PT.term_p],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[PT.lambda_pass],[],[],[]],
    [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],["*"],["/"],[],[],[],[],[],[],[],[],[]],
    [["(", PT.expr, ")"],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[TokenType.ID, PT.factor_p],[TokenType.NUM],[]],
    [["(", PT.args, ")"],[PT.var_p],[PT.var_p],[PT.var_p],[PT.var_p],[PT.var_p],[],[],[],[],[],[],[],[],[],[PT.var_p],[PT.var_p],[PT.var_p],[PT.var_p],[PT.var_p],[PT.var_p],[PT.var_p],[PT.var_p],[PT.var_p],[PT.var_p],[],[],[]],
    [[PT.arg_list],[PT.lambda_pass],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[PT.arg_list],[PT.arg_list],[],[]],
    [[PT.expr, PT.arg_list_p],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[PT.expr, PT.arg_list_p],[PT.expr, PT.arg_list_p],[]],
    [[],[PT.lambda_pass],[],[],[],[",", PT.expr, PT.arg_list_p],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],
]
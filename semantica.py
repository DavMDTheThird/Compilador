"""
Autores:
    - David Medina Domínguez
        Matricula: A01783155
    - Juan Pablo Cruz Rodríguez
        Matricula: A01783208

Objetivo:
    Creación de una semantica basica para el lenguaje de C-

Instrucciones:
    - tabla(tree, imprime = True)
        o La cual recibe tree, el Árbol Sintáctico Abstracto (AST, por sus siglas en inglés) creado por el parser
        (proyecto 2) y una variable imprime que por default es verdadera (si es verdadera imprime la tabla o 
        tablas de símbolos generadas).
        o Como salida genera la tabla o tablas de símbolos, una por cada bloque.
        
    - semantica(tree, imprime = True)
        o La cual recibe tree, el Árbol Sintáctico Abstracto (AST, por sus siglas en inglés) creado por el parser
        (proyecto 2) y una variable imprime que por default es verdadera. Esta variable la pasa cuando llame a la
        función tabla.
        o Llama a la función tabla y utiliza la tabla o tablas de símbolos que genera.
        o Utiliza reglas lógicas de inferencia para implementar la semántica de C-. Ver descripción de la semántica 
        de C- en el documento en Bb)
"""

global dev2
dev2 = False

from Parser import *
import copy


def globalesSemantica(prog, pos, long, line_ = 0):
    global programa, posicion, progLong, line, symbol_tables
    programa = prog
    posicion = pos
    progLong = long
    line = line_
    globalesParser(programa, posicion, progLong)


# Elemento de una declaracion -------------------------------------------------------------------
class DecElement:
    def __init__(self, symbol, type, arr=None):
        self.symbol = symbol
        self.type = type
        self.arr = arr
        self.dec = None

    def __str__(self):
        arr_str = ""
        if self.arr == 0:
            arr_str = "[]"
        elif self.arr:
            arr_str = f"[{self.arr}]"

        return f"{self.type} {self.symbol}{arr_str}"
        

# Elemento de la tabla de simbolos -------------------------------------------------------------------
class TableElement:
    def __init__(self, symbol:DecElement, type=None, line=None, param=None, size=None, returnE=None):
        self.symbol = symbol
        self.line = line
        self.type = type
        self.param = param
        self.size = size
        self.returnE = returnE

    def __str__(self):
        # Parameters: print as comma-separated DecElement if present
        if isinstance(self.param, list):
            params_str = ", ".join(str(p[0]) if isinstance(p, list) else str(p) for p in self.param)
        else:
            params_str = "----"
        symbol_str = f"{self.symbol}" if self.symbol else "----"
        type_str = str(self.type) if self.type else "----"
        line_str = str(self.line) if self.line else "----"
        size_str = str(self.size) if self.size else "----"
        returnE_str = str(self.returnE) if self.returnE else "----"

        return (f"{symbol_str:<13} | {type_str:<10} | {line_str:<10} | "
                f"{params_str:<30} | {size_str:<5} | {returnE_str:<10}")

# Tabla de simbolos ----------------------------------------------------------------------------------
class SymbolTable:
    def __init__(self, name="Global"):
        self.name = name
        self.elements = []  # List of TableElement objects

    def __str__(self):
        output = f"\nBlock {self.name}:\n"
        output += f"{'Symbol':<13} | {'Type':<10} | {'Line':<10} | {'Parameters':<30} | {'Size':<5} | {'Return':<10}\n"
        output += "-" * 100 + "\n"
        for elem in self.elements:
            output += str(elem) + "\n"
        return output

def debug_print(node, lst = []):
    nodetest = node
    if lst:
        for i in lst:
            nodetest = next((x for x in nodetest.children if x.symbol == i), None)

    if not nodetest: 
        print("ERROR: not found")
        nodetest = node
        return

    print(f"UNUNUNUNUNUNUNUNUNUNUNUNUNUNNUN~{node.symbol}:", end=" ")
    for child in nodetest.children:
        print(f"{child.symbol}", end=", ")
    print("")

def get_node(node, lst = []):
    nodetest = node
    if lst:
        for i in lst:
            if nodetest:
                nodetest = next((x for x in nodetest.children if x.symbol == i), None)
            else:
                nodetest = None
                break

    if not nodetest: 
        # print(f"ERROR: not found while searching {lst}")
        pass

    return nodetest

def get_VarParam_info(node):
    type = None

    matchType = get_node(node, [PT.type_specifier])
    if matchType and matchType.children:
        matchType = matchType.children[0].symbol

    matchValue = get_node(node, [TokenType.ID])
    if matchValue and matchValue.children:
        matchValue = matchValue.children[0].symbol
        
    arr_type = is_array(node)
    func_type, _ = is_function(node)
    
    # Check if it's an array (arr_type is 0 for parameter arrays or a number for sized arrays)
    if arr_type is not None:
        type = "array"
    elif func_type:
        type = "function"
    else:
        type = "variable"

    element = DecElement(matchValue, matchType, arr_type)
    return element, type

def is_function(node):
    param_lst = []


    match = get_node(node, [PT.dec_p])
    # Si la declaracion es una funcion:
    if get_node(match, ["("]):
        # Los parametros de la funcion:
        match = get_node(match, [PT.params, PT.param_list])
        if match:
            param = get_node(match, [PT.param])
            if param:
                paramDec, param_Form = get_VarParam_info(param)

                param_lst.append([paramDec, param_Form])

            # Itera por todas las N cantidad de parametros
            match = get_node(match, [PT.param_list_p])
            while match:

                param = get_node(match, [PT.param])
                if param:
                    paramDec, param_Form = get_VarParam_info(param)
                    param_lst.append([paramDec, param_Form])

                match = get_node(match, [PT.param_list_p])

            return True, param_lst
        else:
            return True, param_lst    
    else:
        return False, param_lst
    
def is_array(node):
    # Check for array parameter (has [] in declaration)
    param_arr = get_node(node, [PT.param_p, "["])
    if param_arr:
        # Parameter arrays are marked with 0 (size unknown)
        return 0

    # Check for array variable declaration (has [NUM] in declaration)
    var_arr = get_node(node, [PT.dec_p, "["])
    if var_arr:
        num_node = get_node(node, [PT.dec_p, TokenType.NUM])
        if num_node:
            size = num_node.children[0].symbol
            # Check for negative array size
            if int(size) <= 0:
                var_name = get_node(node, [TokenType.ID])
                if var_name and var_name.children:
                    print(f"Error: Array '{var_name.children[0].symbol}' declared with invalid size {size} on line {node.line}")
                return None
            return size
    
    # Not an array
    return None

def is_decVariable(node):
    var_lst = []
    
    var_type = get_node(node, [PT.type_specifier]).children[0].symbol

    if get_node(node, [PT.dec_p, ","]) or get_node(node, [PT.dec_p, ";"]):

        if get_node(node, [PT.dec_p, "["]):
            varDec = get_node(node, [TokenType.ID]).children[0].symbol
            arr_val = get_node(node, [PT.dec_p, TokenType.NUM]).children[0].symbol
            var_lst.append([DecElement(varDec, var_type, arr_val), "array"])

        else:
            while node:
                if get_node(node, [";"]): break

                varDec = get_node(node, [TokenType.ID]).children[0].symbol

                var_lst.append([DecElement(varDec, var_type), "variable"])

                node = get_node(node, [PT.dec_p])
            
        return True, var_lst
    
    # It does the same as the one before, but within a function (different follow up states)
    elif get_node(node, [PT.var_dec_p, ","]) or get_node(node, [PT.var_dec_p, ";"]):

        if get_node(node, [PT.var_dec_p, "["]):
            varDec = get_node(node, [TokenType.ID]).children[0].symbol
            arr_val = get_node(node, [PT.var_dec_p, TokenType.NUM]).children[0].symbol
            var_lst.append([DecElement(varDec, var_type, arr_val), "array"])

        else:
            while node:
                if get_node(node, [";"]): break

                varDec = get_node(node, [TokenType.ID]).children[0].symbol

                var_lst.append([DecElement(varDec, var_type), "variable"])

                node = get_node(node, [PT.var_dec_p])
            
        return True, var_lst

    else:
        return False, var_lst


# --------------------------------------------------------------------------------------------------------------

def pre_order(node, declaration = False, new_table:SymbolTable = None, endTableElement = None):
    nextChildren = copy.copy(node)

    if node is None:
        return

    if declaration == False and node.symbol == PT.dec:
        declaration = True

        nodeDec, node_Form =  get_VarParam_info(node)
        func, func_params = is_function(node)
        decVar, decVar_lst = is_decVariable(node)

        if func:
            new_table = SymbolTable(nodeDec.symbol)
            new_table.elements.append(TableElement(nodeDec, node_Form, node.line, func_params, None, nodeDec.type))
            # Also add function declaration to global scope
            symbol_tables[0].elements.append(TableElement(nodeDec, node_Form, node.line, func_params, None, nodeDec.type))
            
            # This is to add the final table at the end of the function
            endTableElement = get_node(node, [PT.dec_p, PT.compound_stmt, "}"])
            # Stop iterating over the function declaration, and continue to its <compound statement>
            match = get_node(node, [PT.dec_p, PT.compound_stmt])
            if match:
                nextChildren = match

            for element in func_params:
                # param_dec = element[0]
                # # Check if the parameter is an array (has [] in declaration)
                # if param_dec.arr is not None:
                #     param_type = "array"
                # else:
                #     param_type = "variable"
                new_table.elements.append(TableElement(element[0], element[1], node.line, None, None, None))

        elif decVar:
            # Don't Iterate over what already was processed
            nextChildren.children = []

            if not new_table:
                for element in decVar_lst:
                    symbol_tables[0].elements.append(TableElement(element[0], element[1], node.line, None, element[0].arr, None))
            else:
                print("                                          LO DUDO                                                               ")
                # Aqui agregar a la subtabla new_table (por si se define una funcion adentro de una funcion)
                pass

    elif declaration:
        if node == endTableElement:
            symbol_tables.append(new_table)
        
        else:
            # basically: the local_dec, var_dec that are inside a function
            if node.symbol == PT.var_dec:
                decVar, decVar_lst = is_decVariable(node)
                for decElem in decVar_lst:
                    new_table.elements.append(TableElement(decElem[0], decElem[1], node.line, None, decElem[0].arr, None))

                nextChildren.children = []
                    

            if dev2: print(f"YES: {node.symbol}")
            pass

    else:
        # if True: print(f"{node.line}. NOT: {node.symbol}")
        pass

    
    # Traverse children
    for child in nextChildren.children:
        pre_order(child, declaration, new_table, endTableElement)

    if not node.children:
        if dev2: print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        pass


# --------------------------------------------------------------------------------------------------------------
# tree_root =  Abstract Syntax Tree
# La salida genera una tabla o tablas de símbolos, una por cada bloque
def tabla(tree_root, imprime=True):
    global symbol_tables
    symbol_tables = []
    symbol_tables.append(SymbolTable()) # Add the global table

    pre_order(tree_root)
    
    if imprime:
        print("\nSymbol Tables:")
        for table in symbol_tables:
            print(table)

    return symbol_tables



# --------------------------------------------------------------------------------------------------------------
def get_variable_info(var_name: str, current_function_table: SymbolTable = None) -> tuple:
    """Helper function to get variable type and array status from symbol tables"""
    # Check function scope first if we're in one
    if current_function_table:
        for elem in current_function_table.elements:
            if elem.symbol.symbol == var_name:
                return elem.symbol.type, elem.type == "array"
    
    # Check global scope
    for elem in symbol_tables[0].elements:
        if elem.symbol.symbol == var_name:
            return elem.symbol.type, elem.type == "array"
    
    return None, None

def get_function_info(func_name: str) -> tuple:
    """Helper function to get function declaration info from symbol tables"""
    # Check global scope for function declaration
    for elem in symbol_tables[0].elements:
        if elem.symbol.symbol == func_name and elem.type == "function":
            return elem.param, elem.returnE  # Return parameters and return type
    return None, None

def get_argument_list(node):
    """Get list of arguments from a function call node"""
    arg_list = []
    
    # Get first argument
    first_arg = get_node(node, [PT.args, PT.arg_list])
    if first_arg and first_arg.children:
        arg_list.append(first_arg.children[0])
    
    # Get rest of arguments
    current = get_node(node, [PT.args, PT.arg_list, PT.arg_list_p])
    while current:
        arg = get_node(current, [PT.expr])
        if arg:
            arg_list.append(arg)
        current = get_node(current, [PT.arg_list_p])
    
    return arg_list

def check_function_call(node, func_name, current_function_table):
    """Check semantic correctness of a function call"""
    # Get function declaration info
    func_elem = None
    for elem in symbol_tables[0].elements:
        if elem.symbol.symbol == func_name and elem.type == "function":
            func_elem = elem
            break

    if func_elem is None:
        print(f"Error: Called undefined function '{func_name}' on line {node.line}")
        return

    # Get and check arguments
    arg_list = get_argument_list(node)
    formal_params = func_elem.param
    
    # Check number of arguments
    if len(arg_list) != len(formal_params):
        print(f"Error: Function '{func_name}' called with {len(arg_list)} arguments but declared with {len(formal_params)} parameters on line {node.line}")
        return

    # Check each argument
    check_function_arguments(func_name, arg_list, formal_params, node.line, current_function_table)

def check_function_arguments(func_name, arg_list, formal_params, line, current_function_table):
    """Check type compatibility of function arguments"""
    for i, (arg_expr, param) in enumerate(zip(arg_list, formal_params)):
        # Get parameter info
        if isinstance(param, list):
            param_dec = param[0]
        else:
            param_dec = param
        param_type = param_dec.type
        param_is_array = param_dec.arr is not None
        param_name = param_dec.symbol
        
        # Find actual argument node
        actual_node = find_id_or_num(arg_expr)
        if not actual_node:
            continue

        # Check argument type and compatibility
        check_argument_compatibility(actual_node, param_type, param_is_array, param_name, i+1, func_name, line, current_function_table)

def check_argument_compatibility(arg_node, expected_type, expected_array, param_name, arg_num, func_name, line, current_function_table):
    """Check if an argument is compatible with the expected parameter type"""
    if arg_node.symbol == TokenType.ID:
        arg_name = arg_node.children[0].symbol
        arg_type, arg_is_array = get_variable_info(arg_name, current_function_table)
        
        if arg_type is None:
            print(f"Error: Undefined variable '{arg_name}' used as argument {arg_num} in call to '{func_name}' on line {line}")
            return
            
        # Array compatibility check
        if expected_array and not arg_is_array:
            print(f"Error: Function '{func_name}' call on line {line} has wrong argument order. "
                  f"Parameter {arg_num} ('{param_name}') expects an array but got non-array variable '{arg_name}'. "
                  f"Did you mean to pass the array as the first argument?")
        elif not expected_array and arg_is_array:
            print(f"Error: Function '{func_name}' call on line {line} has wrong argument order. "
                  f"Parameter {arg_num} ('{param_name}') expects a non-array but got array '{arg_name}'. "
                  f"The array should be the first argument.")
        
        # Type compatibility check
        if arg_type != expected_type:
            print(f"Error: Function '{func_name}' parameter {arg_num} ('{param_name}') type mismatch: "
                  f"expected {expected_type} but got {arg_type} on line {line}")
    
    elif arg_node.symbol == TokenType.NUM:
        if expected_array:
            print(f"Error: Function '{func_name}' parameter {arg_num} ('{param_name}') "
                  f"expects an array but got a number literal on line {line}")

def get_parent_node(node, symbols):
    """
    Traverse up the tree looking for parent nodes matching the given symbols.
    Args:
        node: The starting node
        symbols: List of symbols to match in order from immediate parent upwards
    Returns:
        The matching node or None if not found
    """
    current = node
    for symbol in symbols:
        if not current or not current.parent:
            return None
        current = current.parent
        if current.symbol != symbol:
            return None
    return current

def check_variable_usage(node, current_function_table):
    """Check semantic correctness of variable usage"""
    if node.symbol == TokenType.ID:
        var_name = node.children[0].symbol
        # Skip if this is part of a declaration
        if not (node.parent and node.parent.symbol in [PT.dec, PT.var_dec, PT.param]):
            # Check if it's a function call
            is_function_call = get_node(node.parent, [PT.factor_p, "("])
            
            var_type, _ = get_variable_info(var_name, current_function_table)
            if var_type is None:
                print(f"Error: Variable '{var_name}' used on line {node.line} but not declared")
            # Only report void error if it's not a function being called
            elif var_type == "void" and not is_function_call:
                print(f"Error: Variable '{var_name}' on line {node.line} is void and cannot be used in expressions")

def check_array_operations(node, current_function_table):
    """Check semantic correctness of array operations"""
    if node.symbol == PT.var_p:
        # Check array indexing
        if get_node(node, ["["]):
            array_node = get_node(node.parent, [TokenType.ID])
            if array_node:
                array_name = array_node.children[0].symbol
                # Verify it's actually an array
                if not get_variable_info(array_name, current_function_table)[1]:
                    print(f"Error: Variable '{array_name}' on line {node.line} is not an array but used with indexing")
                
                # Check index expression
                index_expr = get_node(node, [TokenType.ID])
                if index_expr:
                    index_type = get_variable_info(index_expr.children[0].symbol, current_function_table)[0]
                    if index_type == "void":
                        print(f"Error: Cannot use void variable '{index_expr.children[0].symbol}' as array index on line {node.line}")

def semantic_preStep(node, current_function_table=None):
    """Main semantic analysis function"""
    if node is None:
        return

    # Check function calls
    if node.symbol == PT.factor_p:
        if node.children and node.children[0].symbol == "(":
            if node.parent and node.parent.children:
                func_name = node.parent.children[0].children[0].symbol
                check_function_call(node, func_name, current_function_table)

    # Check variable usage
    check_variable_usage(node, current_function_table)

    # Check array operations
    check_array_operations(node, current_function_table)

    # Check return statements
    check_return_statements(node, current_function_table)

    # Check arithmetic operations
    check_arithmetic_operations(node, current_function_table)

    # Check boolean conditions
    check_boolean_conditions(node, current_function_table)

    # Traverse children
    for child in node.children:
        # If we enter a function definition, pass its symbol table
        if node.symbol == PT.dec:
            func_id_node = get_node(node, [TokenType.ID])
            if func_id_node and func_id_node.children:
                func_name = func_id_node.children[0].symbol
                # Find the function's symbol table
                for table in symbol_tables[1:]:  # Skip global table
                    if table.name == func_name:
                        semantic_preStep(child, table)
                        break
                else:
                    semantic_preStep(child, current_function_table)
            else:
                semantic_preStep(child, current_function_table)
        else:
            semantic_preStep(child, current_function_table)

def find_id_or_num(node):
    """Traverse expression tree to find ID or NUM node"""
    if not node or not node.children:
        return None
    
    if node.symbol == TokenType.ID or node.symbol == TokenType.NUM:
        return node
    
    # Try each child
    for child in node.children:
        result = find_id_or_num(child)
        if result:
            return result
    return None

def has_return_statement(node):
    """Check if a compound statement contains a return statement"""
    if not node:
        return False
        
    if node.symbol == PT.return_stmt:
        return True
        
    for child in node.children:
        if has_return_statement(child):
            return True
            
    return False

def check_return_statements(node, current_function_table):
    """Check return statement compatibility with function type"""
    if not current_function_table:
        return  # Skip if not in a function

    # Get function's declared return type
    func_name = current_function_table.name
    func_info = None
    for elem in symbol_tables[0].elements:
        if elem.symbol.symbol == func_name and elem.type == "function":
            func_info = elem
            break
    
    if not func_info:
        return  # Skip if function info not found

    return_type = func_info.returnE

    # If this is a return statement
    if node.symbol == PT.return_stmt:
        # Look for return value in return_stmt_p
        return_expr = None
        for child in node.children:
            if child.symbol == PT.return_stmt_p:
                if child.children:
                    for c in child.children:
                        if c.symbol == PT.expr:
                            return_expr = c
                            break
        
        if return_type == "void":
            if return_expr:
                print(f"Error: Void function '{func_name}' cannot return a value on line {node.line}")
        else:
            if not return_expr:
                print(f"Error: Non-void function '{func_name}' must return a value on line {node.line}")
            else:
                # Get the type of the returned expression
                expr_node = find_id_or_num(return_expr)
                if expr_node:
                    if expr_node.symbol == TokenType.ID:
                        # Variable return
                        var_name = expr_node.children[0].symbol
                        var_type, var_is_array = get_variable_info(var_name, current_function_table)
                        
                        if var_type is None:
                            print(f"Error: Undefined variable '{var_name}' in return statement on line {node.line}")
                        elif var_type != return_type:
                            print(f"Error: Function '{func_name}' returns {return_type} but got {var_type} on line {node.line}")
                        elif var_is_array:
                            print(f"Error: Cannot return array '{var_name}' from function '{func_name}' on line {node.line}")
                    
                    elif expr_node.symbol == TokenType.NUM:
                        # Number literal return
                        if return_type != "int":
                            print(f"Error: Function '{func_name}' returns {return_type} but got int literal on line {node.line}")

    # Check if we're at the end of a function definition
    elif node.symbol == PT.compound_stmt and node.parent and node.parent.symbol == PT.dec_p:
        if return_type != "void" and not has_return_statement(node):
            print(f"Error: Non-void function '{func_name}' must have a return statement")

def check_arithmetic_operations(node, current_function_table):
    """Check type compatibility in arithmetic expressions"""
    # Check additive expressions (+ -)
    if node.symbol == PT.additive_expr_p:
        # Look for operator in addop node
        addop_node = get_node(node, [PT.addop])
        if addop_node and addop_node.children:
            operator = addop_node.children[0].symbol
            if operator in ['+', '-']:
                # Get left operand from parent's term
                left_operand = get_node(node.parent, [PT.term])
                # Get right operand
                right_operand = get_node(node, [PT.term])
                
                if left_operand and right_operand:
                    check_operand_compatibility(left_operand, right_operand, operator, node.line, current_function_table)

    # Check multiplicative expressions (* /)
    elif node.symbol == PT.term_p:
        # Look for operator in mulop node
        mulop_node = get_node(node, [PT.mulop])
        if mulop_node and mulop_node.children:
            operator = mulop_node.children[0].symbol
            if operator in ['*', '/']:
                # Get left operand from parent's factor
                left_operand = get_node(node.parent, [PT.factor])
                # Get right operand
                right_operand = get_node(node, [PT.factor])
                
                if left_operand and right_operand:
                    check_operand_compatibility(left_operand, right_operand, operator, node.line, current_function_table)

def check_operand_compatibility(left_node, right_node, operator, line, current_function_table):
    """Helper function to check if two operands are compatible for arithmetic operations"""
    left_info = get_operand_info(left_node, current_function_table)
    right_info = get_operand_info(right_node, current_function_table)
    
    if not left_info or not right_info:
        return  # Error already reported in get_operand_info
        
    left_type, left_is_array, left_name = left_info
    right_type, right_is_array, right_name = right_info
    
    # Check for array operands
    if left_is_array:
        print(f"Error: Cannot use array '{left_name}' in arithmetic operation '{operator}' on line {line}")
        return
    if right_is_array:
        print(f"Error: Cannot use array '{right_name}' in arithmetic operation '{operator}' on line {line}")
        return
        
    # Check for void operands
    if left_type == "void":
        print(f"Error: Cannot use void value in arithmetic operation '{operator}' on line {line}")
        return
    if right_type == "void":
        print(f"Error: Cannot use void value in arithmetic operation '{operator}' on line {line}")
        return
        
    # Check type compatibility
    if left_type != right_type:
        print(f"Error: Type mismatch in arithmetic operation '{operator}' between {left_type} and {right_type} on line {line}")

def get_operand_info(node, current_function_table):
    """Helper function to get type information about an operand"""
    # If we get a term node, use its factor child
    if node.symbol == PT.term:
        factor_node = get_node(node, [PT.factor])
        if factor_node:
            return get_operand_info(factor_node, current_function_table)
    
    # Find the actual value node (ID or NUM)
    id_node = get_node(node, [TokenType.ID])
    num_node = get_node(node, [TokenType.NUM])
    
    if id_node and id_node.children:
        # Variable operand
        var_name = id_node.children[0].symbol
        
        # Check if it's a function call
        if get_node(node, [PT.factor_p, "("]):
            # Find function return type
            func_type = None
            for elem in symbol_tables[0].elements:
                if elem.symbol.symbol == var_name and elem.type == "function":
                    func_type = elem.returnE
                    break
            return func_type, False, var_name
            
        # Regular variable
        var_type, var_is_array = get_variable_info(var_name, current_function_table)
        
        if var_type is None:
            print(f"Error: Undefined variable '{var_name}' used in arithmetic expression")
            return None
            
        # Check if array is being used with indexing
        var_p = get_node(node, [PT.factor_p, PT.var_p])
        
        if var_is_array:
            # If it's an array, check for indexing
            if var_p and var_p.children:
                # Check if var_p has the array indexing structure: [ expr ]
                has_indexing = False
                if len(var_p.children) >= 3:
                    if var_p.children[0].symbol == "[" and var_p.children[2].symbol == "]":
                        expr_node = var_p.children[1]
                        if expr_node.symbol == PT.expr:
                            has_indexing = True
                
                if has_indexing:
                    # Array is properly indexed, treat it as a regular int
                    return var_type, False, f"{var_name}[...]"
            # Array without indexing
            return var_type, True, var_name
            
        return var_type, var_is_array, var_name
        
    elif num_node and num_node.children:
        # Number literal operand
        return "int", False, str(num_node.children[0].symbol)
        
    return None

def check_boolean_conditions(node, current_function_table):
    """Check if conditions in if/while statements are valid"""
    # Check selection (if) and iteration (while) statement conditions
    if node.symbol in [PT.selection_stmt, PT.iteration_stmt]:
        # Get the condition expression (both have the same structure: '(' expr ')')
        condition = get_node(node, [PT.expr])
        if condition:
            check_condition_validity(condition, node.line, current_function_table)

def check_condition_validity(node, line, current_function_table):
    """Check if a condition expression is valid"""
    # Check simple expression (left side of relop)
    simple_expr = get_node(node, [PT.simple_expr])
    if not simple_expr:
        return
    
    # Get operand info for left side
    left_additive_expr = get_node(simple_expr, [PT.additive_expr])
    if left_additive_expr:
        left_term = get_node(left_additive_expr, [PT.term])
        if left_term:
            left_info = get_operand_info(left_term, current_function_table)
            if left_info:
                left_type, left_is_array, left_name = left_info
                # Check for invalid types in condition
                if left_is_array:
                    print(f"Error: Cannot use array '{left_name}' in condition on line {line}")
                    return
                if left_type == "void":
                    print(f"Error: Cannot use void value in condition on line {line}")
                    return
    
    # Check if there's a relational operation
    simple_expr_p = get_node(simple_expr, [PT.simple_expr_p])
    if simple_expr_p and simple_expr_p.children:
        # Look for relop
        relop = get_node(simple_expr_p, [PT.relop])
        if relop and relop.children:
            operator = relop.children[0].symbol
            # Get right operand (additive expression)
            right_additive_expr = get_node(simple_expr_p, [PT.additive_expr])
            if right_additive_expr:
                right_term = get_node(right_additive_expr, [PT.term])
                if right_term:
                    right_info = get_operand_info(right_term, current_function_table)
                    if right_info:
                        right_type, right_is_array, right_name = right_info
                        # Check for invalid types in right operand
                        if right_is_array:
                            print(f"Error: Cannot use array '{right_name}' in condition on line {line}")
                            return
                        if right_type == "void":
                            print(f"Error: Cannot use void value in condition on line {line}")
                            return
                        # Check type compatibility for relational operation
                        if left_info and right_info and left_type != right_type:
                            print(f"Error: Type mismatch in condition using operator '{operator}' between {left_type} and {right_type} on line {line}")
                            return

def check_assignment_compatibility(node, current_function_table):
    """Check type compatibility in assignments"""
    pass

def check_variable_declarations(node, current_function_table):
    """Check for multiple declarations and initialization issues"""
    pass

# tree_root =  Abstract Syntax Tree
# Se llama a la funcion tabla(tree) para obtener la tabla de simbolos
# Usando reglas lógicas de inferencia para implementar la semántica de C‐
def semantica(tree_root, imprime = True):
    """
    Main semantic analysis function.
    Returns True if no type errors found, False otherwise.
    """
    # Build symbol tables
    symbol_tables = tabla(tree_root[0], imprime)

    print("\nSemantic Check\n" + "-"*50)

    semantic_preStep(tree_root[0])
    

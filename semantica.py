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

from Parser import *

def globales(prog, pos, long, line_ = 0, symbol_tables_ = []):
    global programa, posicion, progLong, line, symbol_tables
    programa = prog
    posicion = pos
    progLong = long
    line = line_
    symbol_tables = symbol_tables_
    globalesParser(programa, posicion, progLong)


# Elemento de una declaracion -------------------------------------------------------------------
class DecElement:
    def __init__(self, symbol, type, arr=None):
        self.symbol = symbol
        self.type = type
        self.arr = arr

    def __str__(self):
        # Only print the first type (e.g., "int"), ignore "array"
        main_type = self.type[0] if isinstance(self.type, list) and self.type else self.type
        arr_str = ""
        if self.arr == 0:
            arr_str = "[]"
        elif self.arr:
            arr_str = "[" + self.arr + "]"
        return f"{main_type} {self.symbol}{arr_str}"        

# Elemento de la tabla de simbolos -------------------------------------------------------------------
class TableElement:
    def __init__(self, symbol:DecElement, type=None, line=None, param=None, size=None, returnE=None):
        self.symbol = symbol
        self.line = line
        self.type = type
        self.param = param
        self.size = size
        self.returnE = returnE

    def printName(symb : DecElement):
        # Only print the first type (e.g., "int"), ignore "array"
        arr_str = ""
        if symb.arr == 0:
            arr_str = "[]"
        elif symb.arr:
            arr_str = "[" + symb.arr + "]"
        return f"{symb.symbol}{arr_str}"


    def __str__(self):
        def fmt(val):
            if isinstance(val, list):
                # Now each param is [DecElement, element_form], print only the DecElement
                return ", ".join(str(p[0]) if isinstance(p, list) and len(p) > 0 else str(p) for p in val)
            if isinstance(val, DecElement):
                return str(val)
            return "----" if val is None else str(val)
        return (f"{fmt(self.symbol):<10} | {fmt(self.type):<12} | {fmt(self.line):<5} | "
                f"{fmt(self.param):<30} | {fmt(self.size):<5} | {fmt(self.returnE):<10}")

# Tabla de simbolos ----------------------------------------------------------------------------------
class SymbolTable:
    def __init__(self, name="Global"):
        self.name = name
        self.elements = []  # List of TableElement objects

    # def get_symbol(self, symbol):
    #     for elem in self.elements:
    #         if elem.symbol == symbol:
    #             return elem
    #     return None

    def __str__(self):
        output = f"\nBlock {self.name}:\n"
        output += f"{'Symbol':<10} | {'Type':<12} | {'Line':<5} | {'Parameters':<30} | {'Size':<5} | {'Return':<10}\n"
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
    func_type, a = is_function(node)
    if arr_type or arr_type == 0:
        type = "array"

    elif func_type:
        type = "function"
    else:
        type = "variable"

    return DecElement(matchValue, matchType), type  

def getFuncitondEnd(node):
    return get_node(node, [PT.dec_p, PT.compound_stmt, "}"])            

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
    print(f"Tryinggggggggggggggg ARAYYYYYYYYYYYYY")

    func_arr = get_node(node, [PT.param_p, "["])
    alone_arr = get_node(node, [PT.dec_p, "["])

    if func_arr:
        print(f"I've fouund and ARRAYYYYYYY: {0}")
        return 0

    elif alone_arr:
        my_node = get_node(node, [PT.dec_p, TokenType.NUM])
        print(f"I've fouund and ARRAYYYYYYY: {my_node.children[0].symbol}")
        return my_node.children[0].symbol
    
    return None

# --------------------------------------------------------------------------------------------------------------

def pre_order(node, declaration = False, new_table = None, endTableElement = None):
    nextChildren = node

    if node is None:
        return

    if declaration == False and node.symbol == PT.dec:
        print(f"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA: {node.symbol}")
        declaration = True

        nodeDec, node_Form =  get_VarParam_info(node)

        new_table = SymbolTable(nodeDec.symbol)

        func, func_params = is_function(node)
        if func:
            new_table.elements.append(TableElement(nodeDec, node_Form, None, func_params, None, None))
            print(new_table)
            
            # Stop iterating over the function declaration, and continue to its <compund statement>
            endTableElement = getFuncitondEnd(node)
            match = get_node(node, [PT.dec_p, PT.compound_stmt])
            if match:
                nextChildren = match

            print(f"BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB: {node.symbol}")
            for element in func_params:
                print(element)
                new_table.elements.append(TableElement(element[0], 
                                                       element[1], None, None, None, None))


    if declaration:
        if node == endTableElement:
            symbol_tables.append(new_table)
            print(f"YES: {node.symbol}")
        
        else:
            if node.symbol == PT.dec:
                print(f"FOUNDDDDDDDDDDDDDDD NEWWWWWWWWWWW: {node.symbol}")


            print(f"YES: {node.symbol}")

    else:
        print(f"NOT: {node.symbol}")
        pass

    
    # Traverse children
    for child in nextChildren.children:
        pre_order(child, declaration, new_table, endTableElement)

    if not node.children:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


# --------------------------------------------------------------------------------------------------------------
# tree_root =  Abstract Syntax Tree
# La salida genera una tabla o tablas de símbolos, una por cada bloque
def tabla(tree_root, imprime=True):
    global symbol_tables

    pre_order(tree_root[0])
    
    if imprime:
        print("\nSymbol Tables:")
        for table in symbol_tables:
            print(table)

    return symbol_tables



# --------------------------------------------------------------------------------------------------------------
# tree_root =  Abstract Syntax Tree
# Se llama a la funcion tabla(tree) para obtener la tabla de simbolos
# Usando reglas lógicas de inferencia para implementar la semántica de C‐
def semantica(tree_root, imprime = True):
    """
    Main semantic analysis function.
    Returns True if no type errors found, False otherwise.
    """
    # Build symbol tables
    symbol_tables = tabla(tree_root, imprime)
    
    # print("\nChequeo de tipos\n" + "-"*50)

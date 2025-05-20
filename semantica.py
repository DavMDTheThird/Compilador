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


# Elemento de la tabla de simbolos -------------------------------------------------------------------
class TableElement:
    def __init__(self, symbol, type_=None, line=None, param=None, size=None, return_=None):
        self.symbol = symbol
        self.line = line
        self.type = type_
        self.param = param
        self.size = size
        self.return_ = return_

    def __str__(self):
        def fmt(val):
            if isinstance(val, list):
                # Format parameters as "type name"
                return ", ".join(f"{t} {n}" for t, n in val)
            return "----" if val is None else str(val)
        return (f"{fmt(self.symbol):<10} | {fmt(self.type):<8} | {fmt(self.line):<5} | "
                f"{fmt(self.param):<30} | {fmt(self.size):<5} | {fmt(self.return_):<10}")

# Tabla de simbolos ----------------------------------------------------------------------------------
class SymbolTable:
    def __init__(self, name="Global"):
        self.name = name
        self.elements = []  # List of TableElement objects

    def add_symbol(self, symbol, line=None, type_=None, param=None, size=None, return_=None):
        elem = TableElement(symbol, line, type_, param, size, return_)
        self.elements.append(elem)

    # def get_symbol(self, symbol):
    #     for elem in self.elements:
    #         if elem.symbol == symbol:
    #             return elem
    #     return None

    def __str__(self):
        output = f"\nBlock {self.name}:\n"
        output += f"{'Symbol':<10} | {'Type':<8} | {'Line':<5} | {'Parameters':<30} | {'Size':<5} | {'Return':<10}\n"
        output += "-" * 100 + "\n"
        for elem in self.elements:
            output += str(elem) + "\n"
        return output

# def debug_print(node):
#     match = next((x for x in node.children if x.symbol == PT.type_specifier), None)
#     # #print(f"UNUNUNUNUNUNUNUNUNUNUNUNUNUNNUN:", end=" ")
#     for child in node.children[:-1]:
#         #print(f"{child.symbol}", end=", ")
#     #print(f"{node.children[-1].symbol}")


def get_VarParam_info(node):
    type = None
    value = None

    match = next((x for x in node.children if x.symbol == PT.type_specifier), None)
    # Esta recursion le agrega seguridad de que no le vaya a llegar un nodo sin hijos
    if match and match.children:
        type = match.children[0].symbol

    match = next((x for x in node.children if x.symbol == TokenType.ID), None)
    if match and match.children:
        value = match.children[0].symbol

    return type, value


def is_function(node):
    param_lst = []

    match = next((x for x in node.children if x.symbol == PT.dec_p), None)
    # Si la declaracion es una funcion:
    if next((x for x in match.children if x.symbol == "("), None):
        # Los parametros de la funcion:
        match = next((x for x in match.children if x.symbol == PT.params), None)
        if match:

            match = next((x for x in match.children if x.symbol == PT.param_list), None)
            if match:

                param = next((x for x in match.children if x.symbol == PT.param), None)
                if param:
                    param_type, param_val = get_VarParam_info(param)
                    param_lst.append([param_type, param_val])

                # Itera por todas las N cantidad de parametros
                match = next((x for x in match.children if x.symbol == PT.param_list_p), None)
                while match:

                    param = next((x for x in match.children if x.symbol == PT.param), None)
                    if param:
                        param_type, param_val = get_VarParam_info(param)
                        param_lst.append([param_type, param_val])

                    match = next((x for x in match.children if x.symbol == PT.param_list_p), None)

                return True, param_lst
            else:
                return True, param_lst    
    else:
        return False, param_lst


def pre_order(node, declaration = False, new_table = None, endTableElement = None):

    if node is None:
        return

    if declaration == False and node.symbol == PT.dec:

        new_table = SymbolTable()

        declaration = True
        #print(f"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA: {node.symbol}")

        node_type, node_val =  get_VarParam_info(node)
        a, b = is_function(node)
        if a:
            new_table.elements.append(TableElement(node_val, node_type, None, b, None, node_type))
            #print(new_table)
            # #print(f"I've found a function with {len(b)} parameters: ")
            # if b:
            #     for i in b:
            #         #print(i)
            test = next((x for x in node.children if x.symbol == PT.dec_p), None)
            # debug_print(test)
            test2 = next((x for x in test.children if x.symbol == PT.compound_stmt), None)
            # debug_print(test2)
            test3 = next((x for x in test2.children if x.symbol == "}"), None)
            #print(f"FOUNDDDDDDDDDDDDDDDDDDDDDDDDD_____: {test3.symbol}")
            endTableElement = test3


    if declaration:
        if node == endTableElement:
            #print(f"MATCHHHHHHHHHHHHHHHHHHHHHHHH_____: {node.symbol}")
            symbol_tables.append(new_table)
        # else:
            #print(f"YES: {node.symbol}")

    else:
        #print(f"NOT: {node.symbol}")
        pass

    
    # Traverse children
    for child in node.children:
        pre_order(child, declaration, new_table, endTableElement)

    # if not node.children:
    #     #print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


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
    
    # #print("\nChequeo de tipos\n" + "-"*50)

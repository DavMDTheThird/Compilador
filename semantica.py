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

def globales(prog, pos, long, line_ = 0, symbol_tables_ = [{}]):
    global programa, posicion, progLong, line, symbol_tables
    programa = prog
    posicion = pos
    progLong = long
    line = line_
    symbol_tables = symbol_tables_
    globalesParser(programa, posicion, progLong)


# Elemento de la tabla de simbolos -------------------------------------------------------------------
class TableElement:
    def __init__(self, symbol, line=None, type_=None, param=None, size=None, return_=None):
        self.symbol = symbol
        self.line = line
        self.type = type_
        self.param = param
        self.size = size
        self.return_ = return_

    def __str__(self):
        return (f"{self.symbol:<15} | {str(self.type):<10} | {str(self.line):<5} | "
                f"{str(self.param):<10} | {str(self.size):<5} | {str(self.return_):<10}")

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
        output += f"{'Symbol':<15} | {'Type':<10} | {'Line':<5} | {'Param':<10} | {'Size':<5} | {'Return':<10}\n"
        output += "-" * 70 + "\n"
        for elem in self.symbols:
            output += str(elem) + "\n"
        return output

def get_name_var(node):
    name = None
    type = None

    # match = next((x for x in node.children if x.symbol == PT.type_specifier), None)
    print(f"zzzzzzzzzzzzzzz:", end=" ")
    for child in node.children[:-1]:
        print(f"{child.symbol}", end=", ")
    print(f"{node.children[-1].symbol}")


def get_params(node):
    param_type = None
    param_value = None

    match = next((x for x in node.children if x.symbol == PT.type_specifier), None)
    # Esta recursion le agrega seguridad de que no le vaya a llegar un nodo sin hijos
    if match and match.children:
        if match.children[0].children:
            param_type = match.children[0].children[0]

    match = next((x for x in node.children if x.symbol == TokenType.ID), None)
    if match and match.children:
        param_value = match.children[0]

    return param_type, param_value


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
                    param_lst.append([get_params(param)])

                # Itera por todas las N cantidad de parametros
                match = next((x for x in match.children if x.symbol == PT.param_list_p), None)
                while match:

                    param = next((x for x in match.children if x.symbol == PT.param), None)
                    if param:
                        param_lst.append([get_params(param)])

                    match = next((x for x in match.children if x.symbol == PT.param_list_p), None)

                return True, param_lst
            else:
                return True, param_lst    
    else:
        return False, param_lst


def pre_order(node, declaration = False, state = TokenType.UNDECLARED):

    if node is None:
        return
    
    if declaration == False and node.symbol == PT.dec:

        table = SymbolTable()

        declaration = True
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

        a, b = get_name_var()
        a, b = is_function(node)
        if a:
            print(f"I've found a function with {len(b)} parameters: ")
            table.elements.append(TableElement())
            if b:
                for i in b:
                    print(i)

    if declaration:





        print(f"YES: {node.symbol}")

        if node.symbol == PT.dec_list:

            declaration = False

    else:
        print(f"NOT: {node.symbol}")
        pass

    
    # Traverse children
    for child in node.children:
        pre_order(child, declaration, state)


# --------------------------------------------------------------------------------------------------------------
# tree_root =  Abstract Syntax Tree
# La salida genera una tabla o tablas de símbolos, una por cada bloque
def tabla(tree_root, imprime=True):
    global symbol_tables

    pre_order(tree_root[0])

    print(symbol_tables)
    
    if imprime:
        print("\nSymbol Tables:")
        for i, table in enumerate(symbol_tables):
            block_name = "Block Global" if i == 0 else f"Block {i}"
            print(f"\n{block_name}:")
            print(f"{'Symbol':<15} | {'Type':<10} | {'Lines'}")
            print("-" * 45)
            for symbol, (symbol_type, lines) in table.items():
                type_str = symbol_type if symbol_type else "Unknown"
                print(f"{symbol:<15} | {type_str:<10} | {', '.join(map(str, lines))}")

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
    
    print("\nChequeo de tipos\n" + "-"*50)
    
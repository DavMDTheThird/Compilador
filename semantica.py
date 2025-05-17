print("Hola Mundo! Esto es la Semantica de David Medina Domínguez (A01783155)\n")

"""
Autor:
    David Medina Domínguez
    Matricula: A01783155
Fecha:
    12/05/2025
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

def is_function(node, declaration = False, state = TokenType.UNDECLARED):

    match = next((x for x in node.children if x.symbol == PT.dec_p), None)

    if next((x for x in match.children if x.symbol == "("), None):
        match = next((x for x in match.children if x.symbol == PT.params), None)
        if match:
            match = next((x for x in match.children if x.symbol == PT.param_list), None)
            if match:
                print(f"BBBBBBBBBBB:", end=" ")
                for child in match.children[:-1]:
                    print(f"{child.symbol}", end=", ")
                print(f"{match.children[-1].symbol}")
        return True
    
    else:
        return False



def pre_order(node, declaration = False, state = TokenType.UNDECLARED):
    global symbol_tables

    if node is None:
        return
    
    if declaration == False and node.symbol == PT.dec:
        declaration = True
        symbol_tables.append({})
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

        is_function(node, declaration, state)

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
# Tree =  Abstract Syntax Tree
# La salida genera una tabla o tablas de símbolos, una por cada bloque
def tabla(tree_root, imprime=True):
    global symbol_tables

    pre_order(tree_root[0])

    print(symbol_tables)

    # # Make the global sybols table of functions
    # for it in symbol_tables[1:]:
    #     if not next(iter(it)) in symbol_tables[0]:
    #         symbol_tables[0][next(iter(it))] = ["Function", [it[next(iter(it))][1][0]]]
    


    # print(symbol_tables)

    # if imprime:
    #     print("\nSymbol Tables:")
    #     for i, table in enumerate(symbol_tables):
    #         block_name = "Block Global" if i == 0 else f"Block {i}"
    #         print(f"\n{block_name}:")
    #         print(f"{'Symbol':<15} | {'Type':<10} | {'Lines'}")
    #         print("-" * 45)
    #         for symbol, (symbol_type, lines) in table.items():
    #             type_str = symbol_type if symbol_type else "Unknown"
    #             print(f"{symbol:<15} | {type_str:<10} | {', '.join(map(str, lines))}")

    return symbol_tables



# --------------------------------------------------------------------------------------------------------------
# Tree =  Abstract Syntax Tree
# Se llama a la funcion tabla(tree) para obtener la tabla de simbolos
# Usando reglas lógicas de inferencia para implementar la semántica de C‐
def semantica(tree, imprime = True):
    """
    Main semantic analysis function.
    Returns True if no type errors found, False otherwise.
    """
    # Build symbol tables
    symbol_tables = tabla(tree, imprime)
    
    print("\nChequeo de tipos\n" + "-"*50)
    




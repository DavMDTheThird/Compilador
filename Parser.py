"""
Autores:
    - David Medina Domínguez
        Matricula: A01783155
    - Juan Pablo Cruz Rodríguez
        Matricula: A01783208

Objetivo:
    Creación de un parser basico para el lenguaje de C-

Instrucciones:
    1. Contentan una función llamada parser(imprime = true), la cual, recibe una bandera booleana imprime , 
    con valor por defecto True, y regresa el Árbol Sintáctico Abstracto (AST) o un mensaje de error.
        a. Deberá declarar las variables globales que requiera para que funcione su lexer.

        b. Mediante esas variables podrá manejar el archivo de texto conteniendo un programa en C- que se 
            desea analizar.
        
        c.Si la bandera imprime es true, la función deberá imprimir al final, el AST generado, simplemente con 
            indentación por nodo, es decir, los hijos de un nodo indentados con respecto a su papá.

    2. La función parser(imprime) deberá manejar las siguientes variables globales: 
        * posicion: contiene la posición del siguiente carácter del string que se debe analizar. Deberá poder modificarla en su funcionamiento.
        * progLong: contiene la logitud del programa. Sólo la leerá cuando la requiera.
        * programa: contiene el string del programa completo. Sólo la leerá cuando lo requiera.


    3. Utilice un algoritmo Top-Down. Su función, cuando necesite el siguiente token, llamará a su función 
    getToken, que implementó en su lexer.
"""

from lexer import *
from parsingTable import *

global dev
dev = False

# Funciones requisito: ---------------------------------------------------------------------------------------
def globalesParser(prog, pos, long):
    global posicion, progLong, programa
    posicion = pos
    progLong = long
    programa = prog
    globalesLexer(programa, posicion, progLong)



# Clase del AST: ------------------------------------------------------------------------------------------
class ASTNode:
    def __init__(self, symbol, line_, children=None, parent_=None):
        self.symbol = symbol  # PT Enum or terminal (string)
        self.line = line_ 
        self.children = children if children else []
        self.parent = parent_

        for child in self.children:
            child.parent = self

    def __repr__(self, level=0):
        ret = "  " * level + repr(self.symbol) + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret
    
def print_ast1(node, level=0):
    indent = "  " * level

    if isinstance(node.symbol, PT):
        pass
        print(f"{indent}{level}.{node.symbol.name}")
    else:
        level += 1
        indent = "  " * level
        print(f"{indent}{node.symbol}")
    for child in node.children:
        print_ast1(child, level+1)


def print_ast2(node, imprime, level=0):
    indent = "  " * level
    
    if isinstance(node.symbol, PT):
        if node.symbol != PT.lambda_pass:
            print(f"{indent}{node.symbol.name}")
    else:
        print(f"{indent}{node.symbol}")

    for child in node.children:
        print_ast2(child, level+1)

    return 


def get_order(node):
    parsing_order = []
    
    if isinstance(node.symbol, PT):
        if node.symbol != PT.lambda_pass:
            parsing_order.append(node.symbol.name)
    else:
        parsing_order.append(node.symbol)

    for child in node.children:
        parsing_order.extend(get_order(child))  # Extend the list with child nodes' parsing_order

    return parsing_order


def printStack(stack):
    print("--Stack: ", end="")
    for i in stack:
        print(i, end=", ")
    print("")


# Funcion base obligatoria, regresa una de estas opciones:
#   1. El Árbol Sintáctico Abstracto o
#   2. Un mensaje de ERROR
def parser(imprime=True):
    global now_token, now_token_str, stack, line
    now_token, now_token_str, line = getToken(False)

    error = False
    stack = [PT.program]
    ast_stack = []
    root_node = ASTNode(PT.program, line)
    ast_stack.append(root_node)


    while(not(error) and now_token != TokenType.ENDFILE):
        # Omit all type of comments
        if(now_token == TokenType.COMMENT):
            pass
        # Parse!!!
        else:
            # Parse through until a match is found 
            while not(error):

                if dev: print(f"Checking: {stack[-1]} == {now_token_str}")

                if stack[-1] == PT.lambda_pass:

                    if dev: printStack(stack)
                    
                    stack.pop()
                    ast_stack.pop()
                elif(stack[-1] == now_token_str or now_token == stack[-1]):

                    if dev: print(f"MATCH with: {now_token_str}")
                    
                    stack.pop()
                    ast_node = ast_stack.pop()
                    ast_node.children.append(ASTNode(now_token_str, line, None, ast_node))
                    
                    if dev: printStack(stack)
                    
                    break
                else:
                    if now_token == TokenType.ERROR:
                        print(f"Invalid token detected on line : '{now_token_str}', expected token: '{stack[-1]}'")
                        break

                    if dev: printStack(stack)
                    
                    pop = stack.pop()
                    ast_node = ast_stack.pop()
                    elements = parsingTable[get_row(pop)][get_column(now_token, now_token_str)]

                    child_nodes = [ASTNode(e, line, None, ast_node) for e in elements]
                    ast_node.children.extend(child_nodes)

                    for element, child in zip(reversed(elements), reversed(child_nodes)):
                        stack.append(element)
                        ast_stack.append(child)


        # Parse the next token
        now_token, now_token_str, line = getToken(False)
        
        if dev: print(f"[{line}]{now_token},{now_token_str}")

        if now_token == TokenType.ENDFILE:
            print(f"The program parsed correctly")

            if imprime:
                print_ast1(root_node, imprime)

            parsing_order = get_order(root_node)

            if dev: 
                for i in parsing_order:
                    print(i)

    return root_node, parsing_order if not error else "Syntax Error"
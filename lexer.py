print("Hola Mundo! Esto es el Lexer de David Medina Domínguez (A01783155)")

"""
Autor:
    David Medina Domínguez
    Matricula: A01783155
Fecha:
    9/04/2025
Objetivo:
    Creación de un lexer basico para el lenguaje de C-

Instrucciones:
    1. Hacer un programa en python, llamado lexer.py, que contenga una función llamada getToken(imprime = True), y
        regresa el siguiente token que encuentre en el string de entrada o un mensaje de error.
    2. Utilice la implementación de variable estado o la de tabla. Recuerde que la implementación con variable 
        estado es más eficiente.
    3. Genere un archivo llamado globalTypes.py, por separado, que contenga todas los tipos de variables que se 
        manejarán en su proyecto: Que se encuentre en el mismo path que todo lo demás:
        - class TokenType(Enum): la cual contendrá todos los tokens que se requieran (con sus valores) y en particular
        deberá contener el token ENDFILE (TokenType.ENDFILE), para que se puede probar sin problemas (ver “prueba del
        programa”).
    
    Tokens examples:
        (ID, “contador”)
        (EQUAL, “=”)
        (ID, “contador”)
        (PLUS, “+”)
        (ERROR, “”)

"""

from globalTypes import *

#region Funciones requisito: -----------------------------------------------------------------------------------------
def globalesLexer(prog, pos, long, line_ = 0):
    global posicion, progLong, programa, line
    posicion = pos
    progLong = long
    programa = prog
    line = line_
#endregion


def acceptToken_clear(imprimir, token, tokenString):
    if imprimir:
        print(f"({line}: {token.name}, \"{tokenString}\")")
    tokenStringTemp = tokenString
    tokenString = ""
    tokenTemp = token
    token = TokenType.UNDECLARED
    return tokenTemp, tokenStringTemp, line


def printError(tokenString, token):
    print(f"(Error, \"{tokenString}\")")
    if token == TokenType.NUM:
        print(f"Error on line: {line}, in the creation of a NUMBER")


#region Retorno de valores: 'token, tokenString = getToken(true)'
def getToken(imprime = True):
    global posicion, progLong, programa, line
    token = TokenType.UNDECLARED
    tokenString = ""

    # Recorrer caracter por caracter
    while True:
        # print(f"posicion: {posicion}, token: {token.name}, ch: {programa[posicion]}")
        if token == TokenType.UNDECLARED:
            if programa[posicion] == "/" and posicion < progLong - 1:
                if programa[posicion+1] == "*":
                    token = TokenType.COMMENT
                else:
                    token = TokenType.OPS
            elif programa[posicion] in TokenType.ID.value[0] + TokenType.ID.value[1]:
                token = TokenType.ID

            elif programa[posicion] in TokenType.NUM.value:
                token = TokenType.NUM

            elif programa[posicion] in TokenType.OPS.value:
                token = TokenType.OPS

            elif programa[posicion] in TokenType.COMP.value + TokenType.ASG.value and posicion < progLong - 1:
                if programa[posicion+1] == "=":
                    token = TokenType.COMP
                else:
                    tokenString += programa[posicion]
                    token = TokenType.ASG
                
            elif programa[posicion] in TokenType.PUN_SEP.value:
                tokenString += programa[posicion]
                token = TokenType.PUN_SEP
                        
            elif programa[posicion] == TokenType.ENDFILE.value:
                tokenString += programa[posicion]
                token = TokenType.ENDFILE
            
            # A blank space, new line or tab is found: SKIP
            elif programa[posicion] in TokenType.UNDECLARED.value:
                if programa[posicion] == '\n':
                    line += 1
                posicion += 1           

            else:
                return TokenType.ERROR, tokenString, line

        else:
            # Store everything that is within the comment
            if token == TokenType.COMMENT:
                if(posicion >= progLong):
                    printError(tokenString)
                    return TokenType.ERROR, tokenString, line

                tokenString += programa[posicion]
                if programa[posicion] == "/" and programa[posicion-1] == "*":
                    posicion += 1 
                    return acceptToken_clear(imprime, token, tokenString)
                
            # If an ID is detected
            elif token == TokenType.ID:
                if programa[posicion] in TokenType.ID.value[0] + TokenType.ID.value[1] + TokenType.NUM.value:
                    tokenString += programa[posicion]
                else:
                    if tokenString in TokenType.RESERVED.value:
                        token = TokenType.RESERVED
                    return acceptToken_clear(imprime, token, tokenString)
                
            # If a Number is detected
            elif token == TokenType.NUM:
                if programa[posicion] in TokenType.NUM.value:
                    tokenString += programa[posicion]
                # Blank space or a SEPARATOR
                elif programa[posicion] in TokenType.UNDECLARED.value + TokenType.PUN_SEP.value:
                    return acceptToken_clear(imprime, token, tokenString)
                else:
                    printError(tokenString, token)
                    return TokenType.ERROR, tokenString, line

            # If an Operator is detected
            elif token == TokenType.OPS:
                tokenString += programa[posicion]
                posicion += 1
                return acceptToken_clear(imprime, token, tokenString)
            
            elif token == TokenType.COMP:
                if programa[posicion] in TokenType.COMP.value + TokenType.ASG.value:
                    tokenString += programa[posicion]
                else:
                    posicion += 1
                    return acceptToken_clear(imprime, token, tokenString)
            

            elif token == TokenType.PUN_SEP:
                posicion += 1
                return acceptToken_clear(imprime, token, tokenString)
            

            elif token == TokenType.ASG:
                posicion += 1
                return acceptToken_clear(imprime, token, tokenString)

            if(programa[posicion] == "$"):
                token = TokenType.ENDFILE
                tokenString = programa[posicion]
                return acceptToken_clear(imprime, token, tokenString)
                
            posicion += 1

    return token, tokenString, line
#endregion
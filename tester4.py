from globalTypes import *
from lexer import *

f = open('sample.c-', 'r')
programa = f.read()         # lee todo el archivo a compilar
progLong = len(programa)    # longitud original del programa
programa = programa + '$'   # agregar un caracter $ que represente EOF
posicion = 0                # posición del caracter actual del string

imp = True

# función para pasar los valores iniciales de las variables globales
globalesLexer(programa, posicion, progLong)
token, tokenString, line = getToken(imp)

while (token != TokenType.ENDFILE):
    token, tokenString, line = getToken(imp)
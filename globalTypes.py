"""
Tokens:
    Palabras RESERVADAS:
        else, if, int, return, void, while, if-else
        posiblemente: input(), output()

    SIMBOLOS:
        + - * / < <= > >= == != = ; , ( ) [ ] { } /* */

    ID:
        letra letra*
    letra = a|..|z|A|..|Z
    
    NUM:
        digito digito*
    digito = 0|..|9

    espacios en blanco = ' ', '\n', '\t'

    COMENTARIO (en cualquier lugar donde pueda estar un espacio en blanco):
        /* ... */ (puede ocupar más de una linea)
        
        
Tokens examples:
    (ID, “contador”)
    (EQUAL, “=”)
    (PLUS, “+”)
    (ERROR, “”)
"""

from enum import Enum, auto
import string

class TokenType(Enum):
    UNDECLARED = [" ", "\n", "\t"]
    COMMENT = "/*"
    ID = [string.ascii_letters, "_"]
    RESERVED = ["else", "if", "int", "return", "void", "while", "if-else"]
    NUM = "0123456789"
    OPS = ["+", "-", "*", "/"]
    COMP = ["<", "<=", ">", ">=", "==", "!="]
    PUN_SEP = [";", ",", "(", ")", "{", "}", "[", "]"]
    ASG = ["="]
    ENDFILE = "$"
    ERROR = ""

    def __str__(self):
        return self.name



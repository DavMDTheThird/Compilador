#Creamos funcion principal del generador del codigo

def codeGen(node, fileName, printAST):
    """
    Genera el código intermedio a partir del árbol de sintáxis abstracta (AST) y lo guarda en un archivo.
    """
    # Abre el archivo de salida para escribir el código intermedio
    with open(fileName + '.tny', 'w') as f:
        # Escribe la cabecera del código intermedio
        f.write(";; Código Intermedio\n")
        f.write(";; Generado por el compilador\n")
        f.write(";; Autor: Tu Nombre\n")
        f.write(";; Fecha: Fecha Actual\n")
        f.write("\n")
        
        # Genera el código intermedio a partir del AST
        generateCode(node, f)


def generateCode(node, f):
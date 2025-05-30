# Manual del Usuario: Compilador del Lenguaje C-

## ✨ Introducción

Este manual está diseñado para explicar detalladamente el uso de un compilador para el lenguaje **C- (C-minus)**, incluyendo el funcionamiento interno del proceso de compilación. El lenguaje C- es un subconjunto muy restringido del lenguaje de programación C, utilizado principalmente para fines educativos.

El compilador desarrollado para este lenguaje genera **código en TM (Tiny Machine)**, un lenguaje intermedio ficticio que representa instrucciones simples de máquina. Este tipo de código permite comprender mejor el proceso de traducción desde un lenguaje de alto nivel hasta instrucciones ejecutables.

### 🔧 Por qué se seleccionó TM (Tiny Machine)?

El lenguaje TM fue seleccionado por las siguientes razones:

- **Simplicidad**: TM define un conjunto reducido de instrucciones (cargar, almacenar, sumar, comparar, saltar, etc.), lo cual lo hace ideal para el aprendizaje.
- **Enfoque educativo**: Es un lenguaje de destino clásico en cursos de compiladores, propuesto por Kenneth Louden en su libro "Compiler Construction: Principles and Practice".
- **Fácil de simular**: Permite crear un simulador en Python para ejecutar el código sin depender de una arquitectura de hardware real.
- **Transparencia**: Cada instrucción generada puede rastrearse fácilmente hasta su origen en el programa fuente, lo que permite una depuración y análisis detallado.

---

## 📚 El Lenguaje C-

El lenguaje **C-** (pronunciado "C minus") es un lenguaje imperativo de propósito general, pero reducido. Las características clave incluyen:

- **Tipos soportados**: `int`, `void` (para funciones sin valor de retorno).
- **Estructuras de control**: `if`, `if-else`, `while`.
- **Funciones**: Soporta definición de funciones con parámetros y llamadas.
- **Variables**: Variables locales y globales; arreglos unidimensionales.
- **Entrada/Salida**: Funciones `input()` y `output()`.
- **Estructura**: Un programa C- consiste en una secuencia de declaraciones de funciones y variables, siendo obligatoria la función `main()` como punto de entrada.

Ejemplo de programa en C-:

```c
int x;
void main() {
    x = input();
    if (x > 0) {
        output(x);
    } else {
        output(0);
    }
}
````

El compilador sigue una arquitectura clásica dividida en varias fases:

## 1. Análisis Léxico (Lexer)

Entrada: Archivo de texto fuente (.c-).

Salida: Flujo de tokens.

Esta fase convierte la secuencia de caracteres del archivo fuente en tokens: unidades significativas como palabras clave (int, if), identificadores (x, main), literales (123), operadores (+, -, ==) y puntuación (;, (, )).

Se usa un analizador basado en expresiones regulares que reconoce patrones, por ejemplo:

```c
int|void|if|else|while|return
[a-zA-Z_][a-zA-Z_0-9]*
[0-9]+
\+|\-|\*|/|==|<=|>=|!=
```

Errores léxicos se detectan cuando aparece un símbolo no reconocido.

## 2. Análisis Sintáctico (Parser)

Entrada: Flujo de tokens.

Salida: Árbol de Sintaxis Abstracta (AST).

El parser utiliza una gramática (por ejemplo en forma EBNF) para verificar si los tokens siguen la estructura del lenguaje. Genera un AST que representa la jerarquía sintáctica del programa.

Errores comunes: falta de punto y coma, llaves desbalanceadas, uso incorrecto de paréntesis.

## 3. Análisis Semántico

Entrada: AST.

Salida: AST validado + Tabla de símbolos.

En esta fase se validan:

Declaración de variables antes de su uso.

Tipos de expresiones y retorno de funciones.

Uso correcto de funciones y parámetros.

Se construye una tabla de símbolos para rastrear identificadores, tipos y ubicaciones. Se implementa con una pila de scopes para manejar bloques anidados.

Errores comunes: uso de variables no declaradas, retorno incorrecto, conflicto de nombres.

## 4. Generación de Código (TM)

Entrada: AST validado.

Salida: Archivo .tm con instrucciones de máquina.

Se recorre el AST y se traduce cada nodo en instrucciones TM:

Asignaciones: traducidas a LD, ST, ADD, etc.

Condicionales y bucles: traducidos con JMP, JZ, JNZ.

Funciones: generan código con manejo de pila y retorno.

El código generado puede ejecutarse con un simulador TM escrito en Python.

## 📝 Ejemplo Práctico Completo

Paso 1: Crear el archivo fuente

Guardar el siguiente código como ejemplo.c-:

```C
//Generador de codigo
python3 test1.py 
```

Para los demas partes del codigo se ejecuta la siguiente linea

```C
//lEXER
python3 test2.py
//PARSER
python3 test3.py
//SEMANTICA
python3 test4.py
```

# 📊 Conclusión

El compilador C- es una herramienta educativa poderosa que permite comprender todas las fases de la compilación:

La transformación desde texto a tokens.

La validación estructural y semántica del programa.

La generación de código de máquina abstracta.

El uso de TM como lenguaje destino facilita la comprensión, simulación y depuración de programas. A través de ejemplos como este, es posible dominar los principios de la construcción de compiladores de una forma clara y progresiva.

## 💡 Importancia de los compiladores en los lenguajes de programación

Los compiladores son componentes fundamentales del ecosistema de programación. Permiten traducir el código fuente de un lenguaje de alto nivel, legible por humanos, a un formato ejecutable por máquinas. Sin compiladores, los programas escritos en lenguajes modernos como C, Java o Python no podrían ser interpretados ni ejecutados por los sistemas operativos ni el hardware. Además:

Optimización del rendimiento: los compiladores generan código eficiente que aprovecha mejor los recursos del sistema.

Abstracción del hardware: permiten escribir software portable e independiente de la arquitectura específica.

Verificación temprana: ayudan a detectar errores de sintaxis y semántica antes de la ejecución.

En resumen, los compiladores son el puente que conecta el pensamiento humano con el funcionamiento computacional, y son esenciales para el desarrollo de cualquier software moderno.

**Nota**: La documentacion del compilador y su respectivas partes se encuentran en la carpeta de Documentacion Compilador
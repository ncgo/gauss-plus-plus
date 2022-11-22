# ERRORES
# Definición de errores de compilación y ejecución.
#
# GAUSS++
# Nadia Corina Garcia Orozco A01242428
# Noviembre, 2022
import sys

# ERROR DUPLICADO
# Aparece cuando se redeclara una función o variable ya registrada en el Directorio de Procedimientos o su respectiva Tabla de Variables.
# ENTRADAS: elemento -> tipo de elemento (funcion o variable), string
#           nombre -> nombre del elemento (nombre de la funcion o variable), string
def errorDuplicado(elemento, nombre):
    message = "🚨ERROR DE COMPILACIÓN.\n🚨El elemento" + " " + str(elemento) + " " + str(nombre) + " ya ha sido declarado."
    sys.exit(message)

# ERROR NO EXISTE
# Aparece cuando se trata de utilizar una función o variable que no ha sido registrada en el Directorio de Procedimientos o su respectiva Tabla de Variables.
# ENTRADAS: elemento -> tipo de elemento (funcion o variable), string
#           nombre -> nombre del elemento (nombre de la funcion o variable), string
def errorNoExiste(elemento, nombre):
    message = "🚨ERROR DE COMPILACIÓN.\n🚨El elemento" + " " + str(elemento) + " " + str(nombre) + " no existe."
    sys.exit(message)

# ERROR TYPE MISMATCH
# Aparece cuando se trata de aplicar una operación de dos operandos con dos tipos incompatibles.
# ENTRADAS: tipo1 -> tipo 1 del elemento, string
#           tipo2 -> tipo 2 del elemento, string
#           operator -> operador con el que se trata de hacer la operacion, string
def errorTypeMismatch(tipo1, tipo2, operator):
    message = "🚨ERROR DE COMPILACIÓN.\n🚨Type mismatch. Los tipos " + str(tipo1) + " y " + str(tipo2) + " no son compatibles para la operacion " + str(operator)
    sys.exit(message)

# ERROR COND TYPE MISMATCH
# Aparece cuando se hace una condición con un valor diferente de booleano.
# ENTRADAS: tipo1 -> tipo recibido, string
def errorCondTypeMismatch(tipo1):
    message = "🚨ERROR DE COMPILACIÓN.\n🚨Type mismatch. Se esperaba un valor booleano y se recibió un valor de tipo " + str(tipo1)
    sys.exit(message)

# ERROR PARAM TYPE MISMATCH
# Aparece cuando se llama una función con parámetros diferentes a los previamente definidos.
# ENTRADAS: tipoDado -> tipo del elemento recibido, string
#           tipoEsperado -> tipo del elemento esperado, string
#           funcion -> nombre de la funcion, string
def errorParamTypeMismatch(tipoDado, tipoEsperado, funcion):
    message = "🚨ERROR DE COMPILACIÓN.\n🚨Type mismatch. Se ha dado un parametro de tipo " + str(tipoDado) + " cuando se esperaba un valor de tipo " + str(tipoEsperado) + " en la función " + str(funcion) + "."
    sys.exit(message)

# ERROR NUM PARAMS
# Aparece cuando se llama una función con un número diferente de parámetros diferentes a los previamente definidos.
# ENTRADAS: numDado -> numero de parametros recibidos, entero
#           numEsperado -> numero de parametros esperados, entero
#           funcion -> nombre de la funcion, string
def errorNumParams(numDado, numEsperado, funcion): 
    message = "🚨ERROR DE COMPILACIÓN.\n🚨Type mismatch. Se han dado " + str(numDado) + " parametros cuando se esperaban " + str(numEsperado) + " parametros en la función " + str(funcion) + "."
    sys.exit(message)

# ERROR RETURN VOID
# Aparece cuando una función void tiene un estatuto de retorno.
# ENTRADAS: funcion -> nombre de la funcion, string
def errorReturnVoid(funcion):
    message = "🚨ERROR DE COMPILACIÓN.\n🚨 La funcion " + str(funcion) + " es de tipo void. No puede tener un valor de retorno."
    sys.exit(message)

# ERROR TYPE MISMATCH
# Aparece cuando se trata de utilizar el valor de retorno de una función void.
# ENTRADAS: tipoDado -> tipo del elemento regresado por la funcion, string
#           tipoEsperado -> tipo del elemento esperado, string
#           funcion -> nombre de la funcion, string
def errorTypeMismatchReturn(tipoDado, tipoEsperado, funcion):
    message = "🚨ERROR DE COMPILACIÓN.\n🚨Type mismatch. Se esperaba regresar un valor " + str(tipoEsperado) + " y se ha regresado un valor de tipo " + str(tipoDado) + " para la funcion " + str(funcion)
    sys.exit(message)

# ERROR ID NOT ARRAY
# Aparece cuando se trata de hacer un acceso de arreglo a una variable que no fue declarada como arreglo
# ENTRADAS:  id -> nombre de la variable
def erroIDNotArray(id):
    message = "🚨ERROR DE COMPILACIÓN.\n🚨 La variable " + str(id) + " no fue declarada como un arreglo."
    sys.exit(message)

# ERROR FILE NOT FOUND
# Aparece cuando se trata de ejecutar el programa sin haber antes llevado a cabo la compilacion
# ENTRADAS: file -> archivo que no pudo ser abierto
def errorFileNotFound(file):
    message = "🚨ERROR DE EJECUCIÓN.\n🚨 File not found. El archivo de la " + file + " no ha sido generado o encontrado."
    sys.exit(message)

# ERROR DIV ZERO
# Aparece cuando se trata de hcaer una division enre 0
def errorDivZero():
    message = "🚨ERROR DE EJECUCIÓN.\n🚨 División entre 0. El denominador de esta división es 0."
    sys.exit(message)

# ERROR LIMITS
# Aparece cuando el indice de un arreglo esta fuera de limites
# ENTRADAS: id -> indice que se trata de accesar
def errorLimits(id):
    message = "🚨ERROR DE EJECUCIÓN.\n🚨 Error de limites. La casilla " + id + " no existe."
    sys.exit(message)
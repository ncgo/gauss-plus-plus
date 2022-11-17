import sys

def errorDuplicado(elemento, nombre):
    message = "🚨ERROR\n🚨El elemento" + " " + elemento + " " + nombre + " ya ha sido declarado."
    sys.exit(message)

def errorNoExiste(elemento, nombre):
    message = "🚨ERROR\n🚨El elemento" + " " + elemento + " " + nombre + " " + "no existe."
    sys.exit(message)

def errorTypeMismatch(tipo1, tipo2, operator):
    message = "🚨ERROR\n🚨Type mismatch. Los tipos " + tipo1 + " y " + tipo2 + "no son compatibles para la operacion " + operator
    sys.exit(message)

def errorCondTypeMismatch(tipo1):
    message = "🚨ERROR\n🚨Type mismatch. Se esperaba un valor booleano y se recibió un valor de tipo " + tipo1
    sys.exit(message)

def errorParamTypeMismatch(tipoDado, tipoEsperado, funcion):
    message = "🚨ERROR\n🚨Type mismatch. Se ha dado un parametro de tipo " + tipoDado + " cuando se esperaba un valor de tipo " + tipoEsperado + " en la función " + funcion + "."
    sys.exit(message)

def errorNumParams(numDado, numEsperado, funcion): 
    message = "🚨ERROR\n🚨Type mismatch. Se han dado " + str(numDado) + " parametros cuando se esperaban " + str(numEsperado) + " parametros en la función " + funcion + "."
    sys.exit(message)
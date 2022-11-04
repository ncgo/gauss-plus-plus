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
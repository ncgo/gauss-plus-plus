
# DIR
import errores as errores

# DIRECTORIO DE PROCEDIMIENTOS
# Apoyo para la semántica básica de variables
# Guardará las funciones y/o procedimientos 
class DirProcedimientos():
    def __init__(self):
        self.dirProcedimientos = {}
    
    # ADD PROC
    # Agrega un procedimiento al Directorio de Procedimientos
    # revisando que no exista previamente 
    def addProc(self, proc):
        if proc.nombre in self.dirProcedimientos.keys():
            return errores.errorDuplicado("procedimiento", proc.nombre)
        else:
            self.dirProcedimientos[proc.nombre] = proc

    def searchProc(self, proc):
        if proc in self.dirProcedimientos.keys():
            return self.dirProcedimientos[proc]
        else:
            return errores.errorNoExiste("procedimiento", proc)

    def printDir(self):
        for key, value in self.dirProcedimientos.items() :
            print (key, value)
            self.dirProcedimientos[key].printProcedimiento()

# TABLA DE VARIABLES
# Apoyo para la semántica básica de variables
# Guardará las variables 
class TablaVariables():
    def __init__(self):
        self.tablaVariables = {}
        self.sizeTabla = 0

    # ADD VAR
    def addVar(self, var):
        if var.nombre in self.tablaVariables.keys():
            return errores.errorDuplicado("variable", var)
        else:
            self.tablaVariables[var.nombre] = var
            self.sizeTabla += 1

    def searchVar(self, varNombre):
        if varNombre in self.tablaVariables.keys():
            return self.tablaVariables[varNombre]
        else:
            # return errores.errorNoExiste("variable", varNombre)
            return 0

    def printTablaVariables(self):
        for key, value in self.tablaVariables.items() :
            print (key, value)
            self.tablaVariables[key].printVar()

# PROCEDIMIENTO
# Clase auxiliar que contiene los datos relevantes de un procedimiento
# a ser insertado en el Directorio de Procedimientos
class Procedimiento():
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo
        self.tablaVariables = TablaVariables()
        self.parameterTable = []
        self.numParams = 0
        self.numVars = 0
        self.numTemps = 0
        self.quadruple = 0

    def printProcedimiento(self):
        print(self.nombre, self.tipo, self.tablaVariables.printTablaVariables())

    def addParam(self, type):
        self.parameterTable.append(type)
        self.numParams += 1
    
    def addStartQuadruple(self, num):
        self.quadruple = num

    def addNumVars(self):
        self.numVars = self.tablaVariables.sizeTabla

    def addTemps(self, numTemps):
        self.numTemps = numTemps
        
# VARIABLE
# Clase auxiliar que contiene los datos relevantes de una variable
# a ser insertada en la Tabla de Variables
class Variable():
    def __init__(self, nombre, tipo, valor = None):
        self.nombre = nombre
        self.tipo = tipo
        self.valor = valor
        self.isArray = False
        self.nodosArreglo = [NodoArreglo()]

    def printVar(self):
        print("{nombre:", self.nombre, "tipo:", self.tipo, "valor:", self.valor)

class NodoArreglo():
    def __init__(self, dim = 1, r = 1):
        self.dim = dim
        self.r = r
        self.li = 0
        self.ls = 0

class Cuadruplo():
    def __init__(self, numero, operator, left_operand, right_operand, result):
        self.numero = numero
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.result = result
    
    def printCuadruplo(self):
        return(str(self.operator) + ', ' + str(self.left_operand) + ', ' + str(self.right_operand) + ', ' + str(self.result))

    def fillCuadruplo(self, fill):
        self.result = fill
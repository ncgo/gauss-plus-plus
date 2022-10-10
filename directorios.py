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
        if proc in self.dirProcedimientos:
            return errores.errorDuplicado("procedimiento", proc)
        else:
            self.dirProcedimientos.push(proc)

# TABLA DE VARIABLES
# Apoyo para la semántica básica de variables
# Guardará las variables 
class TablaVariables():
    def __init__(self):
        self.tablaVariables = {}

    # ADD VAR
    def addVar(self, var):
        if var in self.tablaVariables:
            return errores.errorDuplicado("variable", var)
        else:
            self.tablaVariables.push(var)

# PROCEDIMIENTO
# Clase auxiliar que contiene los datos relevantes de un procedimiento
# a ser insertado en el Directorio de Procedimientos
class Procedimiento():
    def __init__(self):
        self.nombre = ""
        self.tipo = ""
        self.tablaVariables = {}

# VARIABLE
# Clase auxiliar que contiene los datos relevantes de una variable
# a ser insertada en la Tabla de Variables
class Variable():
    def __init__(self, nombre, tipo, valor):
        self.nombre = nombre
        self.tipo = tipo
        self.valor = valor



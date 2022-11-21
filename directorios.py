# DIRECTORIOS
# Clases auxiliares para compilación.
#
# GAUSS++
# Nadia Corina Garcia Orozco A01242428
# Noviembre, 2022
import errores as errores

# DIRECTORIO DE PROCEDIMIENTOS
# Apoyo para la semántica básica de variables
# Guardará las funciones y/o procedimientos 
class DirProcedimientos():
    def __init__(self):
        self.dirProcedimientos = {} # Directorio de Procedimientos, directorio
    
    # ADD PROC
    # Agrega un procedimiento al Directorio de Procedimientos
    # revisando que no exista previamente 
    # ENTRADAS: proc -> objeto Procedimiento a agregar
    def addProc(self, proc):
        if proc.nombre in self.dirProcedimientos.keys():
            return errores.errorDuplicado("procedimiento", proc.nombre)
        else:
            self.dirProcedimientos[proc.nombre] = proc

    # SEARCH PROC
    # Funcion que busca la existencia de un procedimiento en el Directorio de Procedimientos
    # ENTRADAS: proc -> nombre del procedimiento a buscar
    # SALIDAS:  en caso de encontrarlo, regresa el objeto procedimiento
    #           en caso de no hacerlo, retorna error y se termina la ejecucion
    def searchProc(self, proc):
        if proc in self.dirProcedimientos.keys():
            return self.dirProcedimientos[proc]
        else:
            return errores.errorNoExiste("procedimiento", proc)

    # PRINT DIR
    # Funcion que imprime los elementos del Directorio de Procedimientos
    def printDir(self):
        for key, value in self.dirProcedimientos.items() :
            print (key, value)
            self.dirProcedimientos[key].printProcedimiento()

# TABLA DE VARIABLES
# Apoyo para la semántica básica de variables
# Guardará las variables 
class TablaVariables():
    def __init__(self):
        self.tablaVariables = {}    # Tabla de Variables, directorio
        self.sizeTabla = 0          # Tamaño de la tabla, número de variables guardadas, entero

    # ADD VAR
    # Agrega un a Variable a la Tabla de Variables
    # revisando que no exista previamente
    # ENTRADAS: var -> objeto variable a agregar
    def addVar(self, var):
        # Si ya existe, retorna error
        if var.nombre in self.tablaVariables.keys():
            return errores.errorDuplicado("variable", var)
        else:
            # Si no existe, se agrega a la Tabla 
            self.tablaVariables[var.nombre] = var
            # Se incrementa el tamaño de la tabla
            self.sizeTabla += 1

    # SEARCH VAR
    # Funcion que busca la existencia de una variable en la Tabla de Variables
    # ENTRADAS: varNombre -> nombre de la variable a buscar
    # SALIDAS:  en caso de encontrarla, regresa el objeto variable
    #           en caso de no hacerlo, retorna 0
    def searchVar(self, varNombre):
        # Si se encuentra
        if varNombre in self.tablaVariables.keys():
            return self.tablaVariables[varNombre]
        else:
            # Si no
            return 0

    # PRINT TABLA VARIABLES
    # Funcion que imprime los elementos de la Tabla de Variables
    def printTablaVariables(self):
        for key, value in self.tablaVariables.items() :
            print (key, value)
            self.tablaVariables[key].printVar()

# PROCEDIMIENTO
# Clase auxiliar que contiene los datos relevantes de un procedimiento
# a ser insertado en el Directorio de Procedimientos
class Procedimiento():
    def __init__(self, nombre, tipo):
        self.nombre = nombre                    # Nombre del procedimiento, string
        self.tipo = tipo                        # Tipo del procedimiento, string
        self.tablaVariables = TablaVariables()  # Tabla de variables, objeto de tipo TablaVariables
        self.parameterTable = []                # Tabla de parametros, lista de tipos
        self.numParams = 0                      # Numero de parametros, entero
        self.numVars = 0                        # Numero de variables, entero
        self.numTemps = 0                       # Numero de temporales, entero
        self.quadruple = 0                      # Numero de cuadruplo, entero

    # PRINT PROCEDIMIENTO
    # Funcion que imprime los atributos del procedimiento
    def printProcedimiento(self):
        print(self.nombre, self.tipo, self.tablaVariables.printTablaVariables())

    # ADD PARAM
    # Funcion que agrega el tipo de los parametros de un procedimiento a la Tabla de Parametros
    # ENTRADAS: type -> tipo del parametro
    def addParam(self, type):
        self.parameterTable.append(type)
        # Aumenta la cantidad de parametros para cuando se llame la ERA
        self.numParams += 1
    
    # ADD START QUADRUPLE
    # Funcion que indica el numero de inicio del cuadruplo de la funcion
    # Para ser llamado cuando se invoque la funcion con GOSUB
    # ENTRADAS: num -> entero que representa el numero de cuadruplo
    def addStartQuadruple(self, num):
        self.quadruple = num

    # ADD NUM VARS
    # Funcion que registra el numero de variables utilizadas en la funcion
    def addNumVars(self):
        self.numVars = self.tablaVariables.sizeTabla

    # ADD TEMPS
    # Funcion que registra el numero de temporales generadas en la funcion
    # ENTRADAS: numTemps -> entero que representa el numero de temporales generados
    def addTemps(self, numTemps):
        self.numTemps = numTemps
        
# VARIABLE
# Clase auxiliar que contiene los datos relevantes de una variable
# a ser insertada en la Tabla de Variables
class Variable():
    def __init__(self, nombre, tipo, valor = None):
        self.nombre = nombre                # Nombre de la variable, string
        self.tipo = tipo                    # Tipo de la variable, string
        self.valor = valor                  # Valor de la variable, depende
        self.isArray = False                # determina si la variable es el identificador de un arreglo, bool
        self.nodosArreglo = []              # Lista de los nodos de las dimensiones de un arreglo
        self.virtualAddress = 0             # Direccion virtual, entero

    # PRINT VAR
    # Funcion que imprime los atributos de una variable
    def printVar(self):
        print("{nombre:", self.nombre, "tipo:", self.tipo, "valor:", self.valor)

# NODO ARREGLO
# Clase que representa los nodos de las dimensiones de un arreglo
# para auxiliar en la indexación de los elementos y su acceso
class NodoArreglo():
    def __init__(self, dim = 1, r = 1):
        self.dim = dim  # Numero de dimension 
        self.r = r      # R 
        self.li = 0     # Limite inferior. Gauss++ indexa desde 0.
        self.ls = 0     # Limite superior
        self.m = 1      # M

# CUADRUPLO
# Clase que representa un cuadruplo
class Cuadruplo():
    def __init__(self, numero, operator, left_operand, right_operand, result):
        self.numero = numero                # Numero de cuadruplo, entero
        self.operator = operator            # Operador de la operacion
        self.left_operand = left_operand    # Operando izquierdo
        self.right_operand = right_operand  # Operando derecho
        self.result = result                # Resultado de la operacion
    
    # PRINT CUADRUPLO
    # Funcion que imprime los elementos de un cuadruplo
    def printCuadruplo(self):
        return(str(self.operator) + ', ' + str(self.left_operand) + ', ' + str(self.right_operand) + ', ' + str(self.result))

    # FILL CUADRUPLO
    # Funcion que rellena el resultado de un cuadruplo en especifico
    # ENTRADAS: fill -> valor a rellenar el resultado
    def fillCuadruplo(self, fill):
        self.result = fill

class TablaConstantes():
    def __init__(self):
        self.tablaConstantes = []
    
    def addCte(self, cte):
        self.tablaConstantes.append(cte)

    # CREATE CTE TABLE FILE
    # Funcion auxiliar que genera el archivo de la tabla de constantes
    def createCteTable(self):
        f = open("ctetable", "w")
        for x in self.tablaConstantes:
            f.write(x.cteFormat() + '\n')
        f.close()

    

class Constante():
    def __init__(self, valor, tipo, virtualAddress):
        self.valor = valor
        self.tipo = tipo
        self.virtualAddress = virtualAddress

    def cteFormat(self):
        return (str(self.virtualAddress) + '@' + str(self.valor))
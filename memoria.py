# ADMINISTRACION DE MEMORIA
# Clases auxiliares para el manejo de memoria en compilacion y ejecucion de un programa Gauss++
#
# GAUSS++
# Nadia Corina Garcia Orozco A01242428
# Noviembre, 2022

# CLASE MEMORIA LOCAL
# Clase auxiliar que ayuda a manejar la memoria local de cada instancia de una funcion
class MemoriaLocal():
    def __init__(self):
        self.memoria = MapaDeMemoria()  
        self.memLocalGauss = [None] * 1000  # Arreglo vacio de memoria de variables generales de Gauss locales
        self.varsInt = [None] * 1000        # Arreglo vacio de memoria de variables enteras locales
        self.varsFloat = [None] * 1000      # Arreglo vacio de memoria de variables flotantes locales
        self.varsString = [None] * 1000     # Arreglo vacio de memoria de variables strings locales
        self.varsBool = [None] * 1000       # Arreglo vacio de memoria de variables booleanas locales
        self.tempsInt = [None] * 1000       # Arreglo vacio de memoria de temporales enteros locales
        self.tempsFloat = [None] * 1000     # Arreglo vacio de memoria de temporales flotantes locales
        self.tempsString = [None] * 1000    # Arreglo vacio de memoria de temporales strings locales
        self.tempsBool = [None] * 1000      # Arreglo vacio de memoria de temporales booleanos locales
        self.tempsPointer = [None] * 1000   # Arreglo vacio de memoria de temporales pointer locales

    # INDEX
    # Funcion auxiliar que indexa valores en la memoria local
    def index(self, dir, result):
        # Variables locales del programa Gauss
        if dir >= self.memoria.varLocalesGauss and dir < self.memoria.varLocalesInt:
            self.memLocalGauss[dir - self.memoria.varLocalesGauss] = result
        # Variables locales tipadas de tipo entero  
        elif dir >= self.memoria.varLocalesInt and dir < self.memoria.varLocalesFloat:
            self.varsInt[dir - self.memoria.varLocalesInt] = result
        # Variables locales tipadas de tipo flotante 
        elif dir >= self.memoria.varLocalesFloat and dir < self.memoria.varLocalesString:
            self.varsFloat[dir - self.memoria.varLocalesFloat] = result
        # Variables locales tipadas de tipo string 
        elif dir >= self.memoria.varLocalesString and dir < self.memoria.varLocalesBool:
            self.varsString[dir - self.memoria.varLocalesString] = result
        # Variables locales tipadas de tipo booleano  
        elif dir >= self.memoria.varLocalesBool and dir < (self.memoria.varLocalesBool + 2000):
            self.varsBool[dir - self.memoria.varLocalesBool] = result
        # Temporales locales tipados de tipo entero
        elif dir >= self.memoria.tempsInt and dir < self.memoria.tempsFloat:
            self.tempsInt[dir - self.memoria.tempsInt] = result
        # Temporales locales tipados de tipo flotante
        elif dir >= self.memoria.tempsFloat and dir < self.memoria.tempsString:
            self.tempsFloat[dir - self.memoria.tempsFloat] = result
        # Temporales locales tipados de tipo string
        elif dir >= self.memoria.tempsString and dir < self.memoria.tempsBool:
            self.tempsString[dir - self.memoria.tempsString] = result
        # Temporales locales tipados de tipo bool
        elif dir >= self.memoria.tempsBool and dir < self.memoria.tempsPointers:
            self.tempsBool[dir - self.memoria.tempsBool] = result
        # Temporales locales tipados de tipo pointer
        elif dir >= self.memoria.tempsPointers and dir < (self.memoria.tempsPointers + 2000):
            self.tempsPointer[dir - self.memoria.tempsPointers] = result

    # VALUE
    # Funcion auxiliar que retorna el valor de una variable o temporal en la memoria local 
    def value(self, dir):
        # Variables generales del programa Gauss en la memoria local
        if dir >= self.memoria.varLocalesGauss and dir < self.memoria.varLocalesInt:
            return self.memLocalGauss[dir - self.memoria.varLocalesGauss]
        # Variables locales tipadas de tipo entero
        elif dir >= self.memoria.varLocalesInt and dir < self.memoria.varLocalesFloat:
            return self.varsInt[dir - self.memoria.varLocalesInt]
        # Variables locales tipadas de tipo flotante
        elif dir >= self.memoria.varLocalesFloat and dir < self.memoria.varLocalesString:
            return self.varsFloat[dir - self.memoria.varLocalesFloat]
        # Variables locales tipadas de tipo string
        elif dir >= self.memoria.varLocalesString and dir < self.memoria.varLocalesBool:
            return self.varsString[dir - self.memoria.varLocalesString]
        # Variables locales tipadas de tipo booleano
        elif dir >= self.memoria.varLocalesBool and dir < (self.memoria.varLocalesBool + 2000):
            return self.varsBool[dir - self.memoria.varLocalesBool]
        # Temporales locales tipados de tipo entero
        elif dir >= self.memoria.tempsInt and dir < self.memoria.tempsFloat:
            return self.tempsInt[dir - self.memoria.tempsInt]
        # Temporales locales tipados de tipo flotante
        elif dir >= self.memoria.tempsFloat and dir < self.memoria.tempsString:
            return self.tempsFloat[dir - self.memoria.tempsFloat]
        # Temporales locales tipados de tipo string
        elif dir >= self.memoria.tempsString and dir < self.memoria.tempsBool:
            return self.tempsString[dir - self.memoria.tempsString]
        # Temporales locales tipados de tipo booleano
        elif dir >= self.memoria.tempsBool and dir < self.memoria.tempsPointers:
            return self.tempsBool[dir - self.memoria.tempsBool]
        # Temporales locales tipados de tipo pointer
        elif dir >= self.memoria.tempsPointers and dir < (self.memoria.tempsPointers + 2000):
            return self.tempsPointer[dir - self.memoria.tempsPointers]

# MAPA DE MEMORIA
# Manejo de direcciones virtuales para el proceso de compilacion 
class MapaDeMemoria():
    def __init__(self):
        # VARIABLES PROPIAS DEL PROGRAMA
        self.varsGauss = 0
        # VARIABLES GLOBALES
        self.varGlobalesInt = 1000
        self.varGlobalesFloat = 3000
        self.varGlobalesString = 5000
        self.varGlobalesBool = 7000
        # TEMPORALES GLOBALES
        self.tempsGlobalesInt = 10000
        self.tempsGlobalesFloat = 12000
        self.tempsGlobalesString = 14000
        self.tempsGlobalesBool = 16000
        self.tempsGlobalesPointers = 18000
        # VARIABLES LOCALES
        self.varLocalesGauss = 20000
        self.varLocalesInt = 21000
        self.varLocalesFloat = 23000
        self.varLocalesString = 25000
        self.varLocalesBool = 27000
        # TEMPORALES LOCALES
        self.tempsInt = 30000
        self.tempsFloat = 32000
        self.tempsString = 34000
        self.tempsBool = 36000
        self.tempsPointers = 38000
        # CONSTANTES
        self.ctesInt = 40000
        self.ctesFloat = 42000
        self.ctesString = 44000
        self.ctesBool = 46000
    
    # AVAIL NEXT
    # Funcion auxiliar que regresa el siguiente temporal 
    # ENTRADAS: type -> tipo del temporal necesitado, string
    # SALIDAS: temporal apropiado de acuerdo al tipo
    def availNext(self, type):
        # temporales enteros
        if (type == "int"):
            res = self.tempsInt
            # Se incrementa en uno para dejar listo para el siguiente temporal
            self.tempsInt += 1

        # temporales flotantes
        elif (type == "float"):
            res = self.tempsFloat
            # Se incrementa en uno para dejar listo para el siguiente temporal
            self.tempsFloat += 1

        # temporales string
        elif (type == "string"):
            res = self.tempsString
            # Se incrementa en uno para dejar listo para el siguiente temporal
            self.tempsString += 1

        # temporales bool
        elif (type == "bool"):
            res = self.tempsBool
            # Se incrementa en uno para dejar listo para el siguiente temporal
            self.tempsBool += 1

        # temporales pointer
        elif (type == "pointer"):
            res = self.tempsPointers
            # Se incrementa en uno para dejar listo para el siguiente temporal
            self.tempsPointers += 1

        return res

    # VIRTUAL ADDRESS
    # Funcion que retorna la direccion virtual apropiada de acuerdo al tipo
    # ENTRADAS: type -> tipo de la variable, string
    #           g -> booleano que indica si la variable es local o global
    # SALIDAS: direccion apropaiada de acuerdo al tipo y contexto
    def virtualAddress(self, type, g = False):
        # variables enteras locales
        if (type == "int" and g == False):
            res = self.varLocalesInt
            # Se incrementa en uno para dejar listo para la siguiente variable
            self.varLocalesInt += 1

        # variables enteras globales
        elif (type == "int" and g == True):
            res = self.varGlobalesInt
            # Se incrementa en uno para dejar listo para la siguiente variable
            self.varGlobalesInt += 1

        # variables locales flotantes
        elif (type == "float" and g == False):
            res = self.varLocalesFloat
            # Se incrementa en uno para dejar listo para la siguiente variable
            self.varLocalesFloat += 1

        # variables flotantes globales
        elif (type == "float" and g == True):
            res = self.varGlobalesFloat
            # Se incrementa en uno para dejar listo para la siguiente variable
            self.varGlobalesFloat += 1

        # variables string locales
        elif (type == "string" and g == False):
            res = self.varLocalesString
            # Se incrementa en uno para dejar listo para la siguiente variable
            self.varLocalesString += 1

        # variables string globales
        elif (type == "string" and g == True):
            res = self.varGlobalesString
            # Se incrementa en uno para dejar listo para la siguiente variable
            self.varGlobalesString += 1

        # variables booleanas locales
        elif (type == "bool" and g == False):
            res = self.varLocalesBool
            # Se incrementa en uno para dejar listo para la siguiente variable
            self.varLocalesBool += 1

        # variables booleanas globales
        elif (type == "bool" and g == True):
            res = self.varGlobalesBool
            # Se incrementa en uno para dejar listo para la siguiente variable
            self.varGlobalesBool += 1

        # variables generales de gauss (globales)
        elif (type == "lista" or type == "categorias"):
            res = self.varsGauss
            # Se incrementa en uno para dejar listo para la siguiente variable
            self.varsGauss += 1

        # variables generales de gauss (locales)
        elif (type == "respuesta" or type == "opciones"):
            res = self.varLocalesGauss
            # Se incrementa en uno para dejar listo para la siguiente variable
            self.varLocalesGauss += 1
            
        return res

    # ADDRES CTE
    # Funcion que retorna la direccion virtual apropiada de acuerdo al tipo de una constante
    # ENTRADAS: type -> tipo de la constante, string
    # SALIDAS: direccion apropiada de acuerdo al tipo
    def addressCte(self, type):
        # Constantes enteras
        if (type == "int"):
            res = self.ctesInt
            # Se incrementa en uno para dejar listo para la siguiente constante
            self.ctesInt += 1

        # Constantes flotantes
        elif (type == "float" ):
            res = self.ctesFloat
            # Se incrementa en uno para dejar listo para la siguiente constante
            self.ctesFloat += 1

        # constantes string
        elif (type == "string"):
            res = self.ctesString
            # Se incrementa en uno para dejar listo para la siguiente constante
            self.ctesString += 1

        # Constantes booleanas
        elif (type == "bool"):
            res = self.ctesBool
            # Se incrementa en uno para dejar listo para la siguiente constante
            self.ctesBool += 1
            
        return res

    # UPDATE BY ARRAY
    # Funcion que actualiza la siguiente direccion virtual cuando se declara un arreglo de acuerdo de acuerdo al tipo
    # ENTRADAS: type -> tipo de la variable, string
    #           R -> cantidad a aumentar (numero de elementos del arreglo), entero
    #           g -> booleano que indica si la variable es local o global
    def updateByArray(self, type, R, g = False):
        # Direcciones de variables enteras locales
        if (type == "int" and g == False):
            self.varLocalesInt += R - 1
        # Direcciones de variables enteras globales
        elif (type == "int" and g == True):
            self.varGlobalesInt += R - 1
        # Direcciones de variables flotantes locales
        elif (type == "float" and g == False):
            self.varLocalesFloat += R - 1
        # Direcciones de variables flotantes globales
        elif (type == "float" and g == True):
            self.varGlobalesFloat += R - 1
        # Direcciones de variables string locales
        elif (type == "string" and g == False):
            self.varLocalesString += R - 1
        # Direcciones de variables string globales
        elif (type == "string" and g == True):
            self.varGlobalesString += R - 1
        # Direcciones de variables booleanas locales
        elif (type == "bool" and g == False):
            self.varLocalesBool += R - 1
        # Direcciones de variables booleanas globales
        elif (type == "bool" and g == True):
            self.varGlobalesBool += R - 1
        # Direcciones de variables generales de Gauss locales
        elif (type == "respuesta" or type == "opciones"):
            self.varLocalesGauss += R - 1 
        # Direcciones de variables generales de Gauss gloables
        elif (type == "categorias" or type == "lista"):
            self.varsGauss += R - 1 
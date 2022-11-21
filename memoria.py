# MAPA DE MEMORIA
# Manejo de direcciones virtuales para el proceso de compilacion
#
# GAUSS++
# Nadia Corina Garcia Orozco A01242428
# Noviembre, 2022

class MemoriaLocal():
    def __init__(self):
        self.memoria = MapaDeMemoria()
        self.varsInt = [None] * 1000
        self.varsFloat = [None] * 1000
        self.varsString = [None] * 1000
        self.varsBool = [None] * 1000
        self.tempsInt = [None] * 1000
        self.tempsFloat = [None] * 1000
        self.tempsString = [None] * 1000
        self.tempsBool = [None] * 1000
        self.tempsPointer = [None] * 1000

    def index(self, dir, result):
        if dir >= self.memoria.varLocalesGauss and dir < self.memoria.varLocalesInt:
            self.varsInt[dir - self.memoria.varLocalesGauss] = result
        elif dir >= self.memoria.varLocalesInt and dir < self.memoria.varLocalesFloat:
            self.varsInt[dir - self.memoria.varLocalesInt] = result
        elif dir >= self.memoria.varLocalesFloat and dir < self.memoria.varLocalesString:
            self.varsFloat[dir - self.memoria.varLocalesFloat] = result
        elif dir >= self.memoria.varLocalesString and dir < self.memoria.varLocalesBool:
            self.varsString[dir - self.memoria.varLocalesString] = result
        elif dir >= self.memoria.varLocalesBool and dir < (self.memoria.varLocalesBool + 2000):
            self.varsBool[dir - self.memoria.varLocalesBool] = result
        elif dir >= self.memoria.tempsInt and dir < self.memoria.tempsFloat:
            self.tempsInt[dir - self.memoria.tempsInt] = result
        elif dir >= self.memoria.tempsFloat and dir < self.memoria.tempsString:
            self.tempsFloat[dir - self.memoria.tempsFloat] = result
        elif dir >= self.memoria.tempsString and dir < self.memoria.tempsBool:
            self.tempsString[dir - self.memoria.tempsString] = result
        elif dir >= self.memoria.tempsBool and dir < self.memoria.tempsPointers:
            self.tempsBool[dir - self.memoria.tempsBool] = result
        elif dir >= self.memoria.tempsPointers and dir < (self.memoria.tempsPointers + 2000):
            self.tempsPointer[dir - self.memoria.tempsPointers] = result

    def value(self, dir):
        if dir >= self.memoria.varLocalesGauss and dir < self.memoria.varLocalesInt:
            return self.varsInt[dir - self.memoria.varLocalesGauss]
        elif dir >= self.memoria.varLocalesInt and dir < self.memoria.varLocalesFloat:
            return self.varsInt[dir - self.memoria.varLocalesInt]
        elif dir >= self.memoria.varLocalesFloat and dir < self.memoria.varLocalesString:
            return self.varsFloat[dir - self.memoria.varLocalesFloat]
        elif dir >= self.memoria.varLocalesString and dir < self.memoria.varLocalesBool:
            return self.varsString[dir - self.memoria.varLocalesString]
        elif dir >= self.memoria.varLocalesBool and dir < (self.memoria.varLocalesBool + 2000):
            return self.varsBool[dir - self.memoria.varLocalesBool]
        elif dir >= self.memoria.tempsInt and dir < self.memoria.tempsFloat:
            return self.tempsInt[dir - self.memoria.tempsInt]
        elif dir >= self.memoria.tempsFloat and dir < self.memoria.tempsString:
            return self.tempsFloat[dir - self.memoria.tempsFloat]
        elif dir >= self.memoria.tempsString and dir < self.memoria.tempsBool:
            return self.tempsString[dir - self.memoria.tempsString]
        elif dir >= self.memoria.tempsBool and dir < self.memoria.tempsPointers:
            return self.tempsBool[dir - self.memoria.tempsBool]
        elif dir >= self.memoria.tempsPointers and dir < (self.memoria.tempsPointers + 2000):
            return self.tempsPointer[dir - self.memoria.tempsPointers]

    

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
        if (type == "int"):
            res = self.tempsInt
            self.tempsInt += 1

        elif (type == "float"):
            res = self.tempsFloat
            self.tempsFloat += 1

        elif (type == "string"):
            res = self.tempsString
            self.tempsString += 1

        elif (type == "bool"):
            res = self.tempsBool
            self.tempsBool += 1

        elif (type == "pointer"):
            res = self.tempsPointers
            self.tempsPointers += 1

        return res

    # VIRTUAL ADDRESS
    # Funcion que retorna la direccion virtual apropiada de acuerdo al tipo
    # ENTRADAS: type -> tipo de la variable, string
    #           g -> booleano que indica si la variable es local o global
    # SALIDAS: direccion apropaiada de acuerdo al tipo y contexto
    def virtualAddress(self, type, g = False):
        if (type == "int" and g == False):
            res = self.varLocalesInt
            self.varLocalesInt += 1

        elif (type == "int" and g == True):
            res = self.varGlobalesInt
            self.varGlobalesInt += 1

        elif (type == "float" and g == False):
            res = self.varLocalesFloat
            self.varLocalesFloat += 1

        elif (type == "float" and g == True):
            res = self.varGlobalesFloat
            self.varGlobalesFloat += 1

        elif (type == "string" and g == False):
            res = self.varLocalesString
            self.varLocalesString += 1

        elif (type == "string" and g == True):
            res = self.varGlobalesString
            self.varGlobalesString += 1

        elif (type == "bool" and g == False):
            res = self.varLocalesBool
            self.varLocalesBool += 1

        elif (type == "bool" and g == True):
            res = self.varGlobalesBool
            self.varGlobalesBool += 1

        elif (type == "lista" or type == "categorias"):
            res = self.varsGauss
            self.varsGauss += 1

        elif (type == "respuesta" or type == "opciones"):
            res = self.varLocalesGauss
            self.varLocalesGauss += 1
            
        return res

    def addressCte(self, type):
        if (type == "int"):
            res = self.ctesInt
            self.ctesInt += 1

        elif (type == "float" ):
            res = self.ctesFloat
            self.ctesFloat += 1

        elif (type == "string"):
            res = self.ctesString
            self.ctesString += 1

        elif (type == "bool"):
            res = self.ctesBool
            self.ctesBool += 1
            
        return res

    def updateByArray(self, type, R, g = False):
        if (type == "int" and g == False):
            self.varLocalesInt += R - 1
        elif (type == "int" and g == True):
            self.varGlobalesInt += R - 1
        elif (type == "float" and g == False):
            self.varLocalesFloat += R - 1
        elif (type == "float" and g == True):
            self.varGlobalesFloat += R - 1
        elif (type == "string" and g == False):
            self.varLocalesString += R - 1
        elif (type == "string" and g == True):
            self.varGlobalesString += R - 1
        elif (type == "bool" and g == False):
            self.varLocalesBool += R - 1
        elif (type == "bool" and g == True):
            self.varGlobalesBool += R - 1
        elif (type == "respuesta" or type == "opciones" or type == "categorias" or type == "lista"):
            self.varsGauss += R - 1 
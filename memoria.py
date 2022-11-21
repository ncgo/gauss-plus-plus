# MAPA DE MEMORIA
# Manejo de direcciones virtuales para el proceso de compilacion
#
# GAUSS++
# Nadia Corina Garcia Orozco A01242428
# Noviembre, 2022

class MemoriaLocal():
    def __init__(self):
        self.varsInt = []
        self.varsFloat = []
        self.varsString = []
        self.varsBool = []

class MapaDeMemoria():
    def __init__(self):
        # VARIABLES PROPIAS DEL PROGRAMA
        self.varsGauss = 0
        # VARIABLES GLOBALES
        self.varGlobalesInt = 1000
        self.varGlobalesFloat = 3000
        self.varGlobalesString = 5000
        self.varGlobalesBool = 7000
        # VARIABLES LOCALES
        self.varLocalesInt = 10000
        self.varLocalesFloat = 12000
        self.varLocalesString = 14000
        self.varLocalesBool = 16000
        # TEMPORALES
        self.tempsInt = 20000
        self.tempsFloat = 22000
        self.tempsString = 24000
        self.tempsBool = 26000
        self.tempsPointers = 28000
        # CONSTANTES
        self.ctesInt = 30000
        self.ctesFloat = 32000
        self.ctesString = 34000
        self.cteBool = 36000
    
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

        elif (type == "respuesta" or type == "opciones" or type == "lista" or type == "categorias"):
            res = self.varsGauss
            self.varsGauss += 1
            
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
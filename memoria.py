# MAPA DE MEMORIA
# Manejo de direcciones virtuales para el proceso de compilacion
#
# GAUSS++
# Nadia Corina Garcia Orozco A01242428
# Noviembre, 2022

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
            self.tempsInt += 1
            return 'tI' + str(self.tempsInt)
        elif (type == "float"):
            self.tempsFloat += 1
            return 'tF' + str(self.tempsFloat)
        elif (type == "string"):
            self.tempsString += 1
            return 'tS' + str(self.tempsString)
        elif (type == "bool"):
            self.tempsBool += 1
            return 'tB' + str(self.tempsBool)
        elif (type == "pointer"):
            self.tempsPointers += 1
            return 'tP' + str(self.tempsPointers)

    # VIRTUAL ADDRESS
    # Funcion que retorna la direccion virtual apropiada de acuerdo al tipo
    # ENTRADAS: type -> tipo de la variable, string
    #           g -> booleano que indica si la variable es local o global
    # SALIDAS: direccion apropaiada de acuerdo al tipo y contexto
    def virtualAddress(self, type, g = False):
        if (type == "int" and g == False):
            self.varLocalesInt += 1
            return self.varLocalesInt
        elif (type == "int" and g == True):
            self.varGlobalesInt += 1
            return self.varGlobalesInt
        elif (type == "float" and g == False):
            self.varLocalesFloat += 1
            return self.varLocalesFloat
        elif (type == "float" and g == True):
            self.varGlobalesFloat += 1
            return self.varGlobalesFloat
        elif (type == "string" and g == False):
            self.varLocalesString += 1
            return self.varLocalesString
        elif (type == "string" and g == True):
            self.varGlobalesString += 1
            return self.varGlobalesString
        elif (type == "bool" and g == False):
            self.varLocalesBool += 1
            return self.varLocalesBool
        elif (type == "bool" and g == True):
            self.varGlobalesBool += 1
            return self.varGlobalesBool
        elif (type == "respuesta" or type == "opciones"):
            self.varsGauss += 1
            return self.varsGauss

    def updateByArray(self, type, R, g = False):
        if (type == "int" and g == False):
            self.varLocalesInt += R
        elif (type == "int" and g == True):
            self.varGlobalesInt += R
        elif (type == "float" and g == False):
            self.varLocalesFloat += R
        elif (type == "float" and g == True):
            self.varGlobalesFloat += R
        elif (type == "string" and g == False):
            self.varLocalesString += R
        elif (type == "string" and g == True):
            self.varGlobalesString += R
        elif (type == "bool" and g == False):
            self.varLocalesBool += R
        elif (type == "bool" and g == True):
            self.varGlobalesBool += R
        elif (type == "respuesta" or type == "opciones" or type == "categorias" or type == "lista"):
            self.varsGauss += R
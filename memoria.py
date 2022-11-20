class MapaDeMemoria():
    def __init__(self):
        self.varsGauss = 0
        self.varGlobalesInt = 1000
        self.varGlobalesFloat = 3000
        self.varGlobalesString = 5000
        self.varGlobalesBool = 7000
        self.varLocalesInt = 10000
        self.varLocalesFloat = 12000
        self.varLocalesString = 14000
        self.varLocalesBool = 15000
        self.tempsInt = 20000
        self.tempsFloat = 22000
        self.tempsString = 24000
        self.tempsBool = 26000
        self.tempsPointers = 28000
        self.ctesInt = 30000
        self.ctesFloat = 32000
        self.ctesString = 34000
        self.cteBool = 36000
    
    # Avail Next
    # Funcion auxiliar que regresa el siguiente temporal 
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

        
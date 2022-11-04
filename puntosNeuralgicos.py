from lark import Visitor
import directorios
import errores

class PuntosNeuralgicos(Visitor):
    def __init__(self):
        self.directorioProcedimientos = None
        self.pilaProcedimientos = []
        self.pilaTipos = []
    # Registro de proceso programa en Directorio de Procedimientos
    def program(self, tree):
        self.directorioProcedimientos = directorios.DirProcedimientos()
        startProc = directorios.Procedimiento(tree.children[1].value, "program")
        self.directorioProcedimientos.addProc(startProc)
        self.pilaProcedimientos.append(tree.children[1].value)
    
    # Registro de proceso modulo en Directorio de Procedimientos
    def modulo(self, tree):
        tipoMod = tree.children[0].children[0].value
        nombreMod = tree.children[1].value
        modProc = directorios.Procedimiento(nombreMod, tipoMod)
        self.directorioProcedimientos.addProc(modProc)
        self.pilaProcedimientos.append(nombreMod)

    # Registro de proceso problema en Directorio de Procedimientos
    def problema(self, tree):
        tipoProb = tree.children[0].value
        nombreProb = tree.children[1].value
        problemaProc = directorios.Procedimiento(nombreProb, tipoProb)
        self.directorioProcedimientos.addProc(problemaProc)
        self.pilaProcedimientos.append(nombreProb)

    # Registro de proceso genera en Directorio de Procedimientos
    def genera(self, tree):
        generaProc = directorios.Procedimiento(tree.children[0].value, tree.children[0].value)
        self.directorioProcedimientos.addProc(generaProc)
        self.pilaProcedimientos.append(tree.children[0].value)

    # Registro de proceso main en Directorio de Procedimientos
    def main(self, tree):
        mainProc = directorios.Procedimiento(tree.children[0].value, tree.children[0].value)
        self.directorioProcedimientos.addProc(mainProc)
        self.pilaProcedimientos.append(tree.children[0].value)
        

    def info(self, tree):
        tablaVarsInfo = directorios.TablaVariables()
        organizacion = directorios.Variable(tree.children[0].value, "string", tree.children[2].value)
        etapa = directorios.Variable(tree.children[3].value, "string", tree.children[5].value)
        categorias = directorios.Variable(tree.children[6].value, "arr", tree.children[6].value)
        tablaVarsInfo.addVar(organizacion)
        tablaVarsInfo.addVar(etapa)
        tablaVarsInfo.addVar(categorias)

    def np_vars(self, tree):
        # Cada que se crea un proceso, se crea su taba de variables
        procActual = self.directorioProcedimientos.searchProc(self.pilaProcedimientos[-1])
        tipoVar = tree.children[0].children[0]
        self.pilaTipos.append(tipoVar)
        var = directorios.Variable(tree.children[1], tipoVar)
        procActual.tablaVariables.addVar(var)


    def end(self, tree):
        # self.directorioProcedimientos.printDir()
        print(self.pilaProcedimientos)
        print("fin")

    
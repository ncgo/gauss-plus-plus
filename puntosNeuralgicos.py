from lark import Visitor
import directorios

directorioProcedimientos = directorios.DirProcedimientos()
pilaProcedimientos = []

class PuntosNeuralgicos(Visitor):
    # Registro de proceso programa en Directorio de Procedimientos
    def program(self, tree):
        startProc = directorios.Procedimiento(tree.children[1].value, "program")
        directorioProcedimientos.addProc(startProc)
    
    # Registro de proceso modulo en Directorio de Procedimientos
    def modulo(self, tree):
        tipoMod = tree.children[0].children[0].value
        nombreMod = tree.children[1].value
        modProc = directorios.Procedimiento(nombreMod, tipoMod)
        directorioProcedimientos.addProc(modProc)

    # Registro de proceso problema en Directorio de Procedimientos
    def problema(self, tree):
        tipoProb = tree.children[0].value
        nombreProb = tree.children[1].value
        problemaProc = directorios.Procedimiento(nombreProb, tipoProb)
        directorioProcedimientos.addProc(problemaProc)

    # Registro de proceso genera en Directorio de Procedimientos
    def genera(self, tree):
        generaProc = directorios.Procedimiento(tree.children[0].value, tree.children[0].value)
        directorioProcedimientos.addProc(generaProc)

    # Registro de proceso main en Directorio de Procedimientos
    def main(self, tree):
        mainProc = directorios.Procedimiento(tree.children[0].value, tree.children[0].value)
        directorioProcedimientos.addProc(mainProc)

    def info(self, tree):
        tablaVarsInfo = directorios.TablaVariables()
        organizacion = directorios.Variable(tree.children[0].value, "string", tree.children[2].value)
        etapa = directorios.Variable(tree.children[3].value, "string", tree.children[5].value)
        categorias = directorios.Variable(tree.children[6].value, "arr", tree.children[6].value)
        tablaVarsInfo.addVar(organizacion)
        tablaVarsInfo.addVar(etapa)
        tablaVarsInfo.addVar(categorias)

    def vars(self, tree):
        tablaVars = directorios.TablaVariables()
        print(tree)

    def end(self, tree):
        # directorioProcedimientos.printDir()
        print("fin")

    
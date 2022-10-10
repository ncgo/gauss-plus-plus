from lark import Visitor
import directorios

directorioProcedimientos = directorios.DirProcedimientos()

class PuntosNeuralgicos(Visitor):
    def program(self, tree):
        startProc = directorios.Procedimiento(tree.children[1].value, "program")
        directorioProcedimientos.addProc(startProc)
    
    def modulo(self, tree):
        tipoMod = tree.children[0].children[0].value
        nombreMod = tree.children[1].value
        modProc = directorios.Procedimiento(nombreMod, tipoMod)
        directorioProcedimientos.addProc(modProc)

    def problema(self, tree):
        tipoProb = tree.children[0].value
        nombreProb = tree.children[1].value
        problemaProc = directorios.Procedimiento(nombreProb, tipoProb)
        directorioProcedimientos.addProc(problemaProc)

    def genera(self, tree):
        generaProc = directorios.Procedimiento(tree.children[0].value, tree.children[0].value)
        directorioProcedimientos.addProc(generaProc)

    def main(self, tree):
        mainProc = directorios.Procedimiento(tree.children[0].value, tree.children[0].value)
        directorioProcedimientos.addProc(mainProc)

    def end(self, tree):
        directorioProcedimientos.printDir()
        print("holaaaa")
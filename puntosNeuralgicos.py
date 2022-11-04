from lark import Visitor
import directorios
import cubo_semantico
import errores

class PuntosNeuralgicos(Visitor):
    def __init__(self):
        self.directorioProcedimientos = None
        self.pilaProcedimientos = []
        self.pilaTipos = []
        self.pOper = []
        self.pilaO = []
        self.temp = 0
        self.procActual = None
        self.cuadruplos = []
        self.numCuadruplos = 0

    def availNext(self):
        self.temp += 1
        return 't' + str(self.temp)

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
        self.procActual = problemaProc

    # Registro de proceso genera en Directorio de Procedimientos
    def genera(self, tree):
        generaProc = directorios.Procedimiento(tree.children[0].value, tree.children[0].value)
        self.directorioProcedimientos.addProc(generaProc)
        self.pilaProcedimientos.append(tree.children[0].value)
        self.procActual = generaProc

    # Registro de proceso main en Directorio de Procedimientos
    def main(self, tree):
        mainProc = directorios.Procedimiento(tree.children[0].value, tree.children[0].value)
        self.directorioProcedimientos.addProc(mainProc)
        self.pilaProcedimientos.append(tree.children[0].value)
        self.procActual = mainProc
        
    # Registro de variables generales del programa
    def info(self, tree):
        tablaVarsInfo = directorios.TablaVariables()
        organizacion = directorios.Variable(tree.children[0].value, "string", tree.children[2].value)
        etapa = directorios.Variable(tree.children[3].value, "string", tree.children[5].value)
        categorias = directorios.Variable(tree.children[6].value, "arr", tree.children[6].value)
        tablaVarsInfo.addVar(organizacion)
        tablaVarsInfo.addVar(etapa)
        tablaVarsInfo.addVar(categorias)
        procActual = self.directorioProcedimientos.searchProc(self.pilaProcedimientos[-1])
        procActual.tablaVariables = tablaVarsInfo

    # Punto neuralgico de adicion de variables
    def np_vars(self, tree):
        # Cada que se crea un proceso, se crea su taba de variables
        procActual = self.directorioProcedimientos.searchProc(self.pilaProcedimientos[-1])
        tipoVar = tree.children[0].children[0]
        self.pilaTipos.append(tipoVar)
        var = directorios.Variable(tree.children[1], tipoVar)
        procActual.tablaVariables.addVar(var)

    def np_endfunc(self, tree):
        print(self.pilaProcedimientos)
        proc = self.directorioProcedimientos.searchProc(self.pilaProcedimientos.pop())
        del proc.tablaVariables
        self.procActual = self.pilaProcedimientos[-1]

    def fact1(self, tree):
        self.pilaO.append(tree.children[0].children[0].value)
        self.pilaTipos.append(tree.children[0].children[0].type)
       
    def fact2(self, tree):
        procActual = self.procActual
        id = tree.children[0].value
        var = procActual.tablaVariables.searchVar(id)
        self.pilaO.append(id)
        self.pilaTipos.append(var.tipo)

    # Agrega * o / a la pila de Operadores
    def ter1(self, tree):
        self.pOper.append(tree.children[0].value)
    
    # Agrega + o - a la pila de Operadores
    def exp1(self, tree):
        print(tree.children[0].value)
        self.pOper.append(tree.children[0].value)

    def exp(self, tree):
        print(tree)

    # Punto neuralgico que crea los cuadruplos de suma y resta 
    def np_exp(self, tree):
        print("entro")
        if(self.pOper):
            if (self.pOper[-1] == '+' or self.pOper[-1] == '-'):
                right_operand = self.pilaO.pop()
                right_operand_type = self.pilaTipos.pop()
                left_operand = self.pilaO.pop()
                left_operand_type = self.pilaTipos.pop()
                operator = self.pOper.pop()
                # ⭐️ Revisa cubo semantico
                result_type = 1
                if (result_type != 0):
                    result = self.availNext()
                    quad = directorios.Cuadruplo(self.numCuadruplos, operator, left_operand, right_operand, result)
                    self.cuadruplos.append(quad)
                    self.pilaO.append(result)
                    self.pilaTipos.append(result_type)
                    self.numCuadruplos += 1
                else:
                    errores.errorTypeMismatch(left_operand_type, right_operand_type, operator)

    # Punto neuralgico que crea los cuadruplos de multiplicaicon y divison
    def np_exp(self, tree):
        if(self.pOper):
            if ((self.pOper[-1] == '*' or self.pOper[-1] == '/')):
                right_operand = self.pilaO.pop()
                right_operand_type = self.pilaTipos.pop()
                left_operand = self.pilaO.pop()
                left_operand_type = self.pilaTipos.pop()
                operator = self.pOper.pop()
                # ⭐️ Revisa cubo semantico
                result_type = 1
                if (result_type != 0):
                    result = self.availNext()
                    quad = directorios.Cuadruplo(self.numCuadruplos, operator, left_operand, right_operand, result)
                    self.cuadruplos.append(quad)
                    self.pilaO.append(result)
                    self.pilaTipos.append(result_type)
                    self.numCuadruplos += 1
                else:
                    errores.errorTypeMismatch(left_operand_type, right_operand_type, operator)

    # Punto neuralgico que marca el fin del programa
    def np_end(self, tree):
        # self.directorioProcedimientos.printDir()
        del self.directorioProcedimientos
        print(self.pilaProcedimientos)
        print(self.cuadruplos)
        for x in self.cuadruplos:
            x.printCuadruplo()
        print("fin")
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
        self.pilaSaltos = []
        self.temp = 0
        self.procActual = None
        self.cuadruplos = []
        self.quadCounter = 0

    def availNext(self):
        self.temp += 1
        return 't' + str(self.temp)

    def newQuad(self):
        self.quadCounter += 1
        return self.quadCounter

    # Registro de proceso programa en Directorio de Procedimientos
    def program(self, tree):
        # Se crea el directorio de Procedimientos
        self.directorioProcedimientos = directorios.DirProcedimientos()
        nombre = tree.children[1].value
        startProc = directorios.Procedimiento(nombre, "program")
        # Se agrega el procedimiento programa al Directorio de Procedimientos
        self.directorioProcedimientos.addProc(startProc)
        # Se agrega el procedimiento a la Pila de Procedimientos para mantener el contexto
        self.pilaProcedimientos.append(nombre)
        self.procActual = startProc
        # Se crea el cuádruplo de goto main a ser llenado posteriormente
        quad = directorios.Cuadruplo(self.newQuad(), "goto", "", "", "")
        self.cuadruplos.append(quad)
        # Se agrega el número de cuádruplo para llenar posteriormente
        self.pilaSaltos.append(self.quadCounter)

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
        tablaVarsInfo.addVar(organizacion)
        quadOrg = directorios.Cuadruplo(self.newQuad(), "=", tree.children[2].value, '', tree.children[0].value)
        
        etapa = directorios.Variable(tree.children[3].value, "string", tree.children[5].value)
        tablaVarsInfo.addVar(etapa)
        quadEtapa = directorios.Cuadruplo(self.newQuad(), "=", tree.children[5].value, '', tree.children[3].value)
        
        categorias = directorios.Variable(tree.children[6].value, "arr", tree.children[6].value)
        quadCategorias = directorios.Cuadruplo(self.newQuad(), "=", tree.children[6].value, '', tree.children[6].value)
        tablaVarsInfo.addVar(categorias)
        
        procActual = self.directorioProcedimientos.searchProc(self.pilaProcedimientos[-1])
        procActual.tablaVariables = tablaVarsInfo

        self.cuadruplos.extend([quadOrg, quadEtapa, quadCategorias])

    # Punto neuralgico de adicion de variables
    def np_vars(self, tree):
        # Cada que se crea un proceso, se crea su taba de variables
        procActual = self.directorioProcedimientos.searchProc(self.pilaProcedimientos[-1])
        tipoVar = tree.children[0].children[0].value
        nombreVar = tree.children[1].value
        self.pilaTipos.append(tipoVar)
        var = directorios.Variable(nombreVar, tipoVar)
        procActual.tablaVariables.addVar(var)
        self.pilaO.append(nombreVar)

    def vars1(self, tree):
        if (tree.children[0] == '='):
            self.pOper.append('=')
        else:
            if (self.pilaO):
                self.pilaO.pop()

    def vars2(self, tree): 
        if(tree.children[0] == ','):
            procActual = self.directorioProcedimientos.searchProc(self.pilaProcedimientos[-1])
            tipoVar = self.pilaTipos[-1]
            nombreVar = tree.children[1].value
            var = directorios.Variable(nombreVar, tipoVar)
            procActual.tablaVariables.addVar(var)
            self.pilaO.append(nombreVar)
    
    def np_fin_vars(self, tree):
        procActual = self.directorioProcedimientos.searchProc(self.pilaProcedimientos[-1])
        # print("Tabla Variables de Gen")
        # procActual.tablaVariables.printTablaVariables()
        #print("PilaO", self.pilaO)
        #print("POper", self.pOper)
        self.pilaTipos.pop()

    def np_endfunc(self, tree):
        proc = self.directorioProcedimientos.searchProc(self.pilaProcedimientos.pop())
        del proc.tablaVariables
        self.procActual = self.pilaProcedimientos[-1]
        quad = directorios.Cuadruplo(self.newQuad(), 'endfunc', '', '', '')
        self.cuadruplos.append(quad)

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
        self.pOper.append(tree.children[0].value)

    # Punto neuralgico que crea los cuadruplos de suma y resta 
    def np_exp(self, tree):
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
                    quad = directorios.Cuadruplo(self.newQuad(), operator, left_operand, right_operand, result)
                    self.cuadruplos.append(quad)
                    self.pilaO.append(result)
                    self.pilaTipos.append(result_type)
                else:
                    errores.errorTypeMismatch(left_operand_type, right_operand_type, operator)

    # Punto neuralgico que crea los cuadruplos de multiplicaicon y divison
    def np_termino(self, tree):
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
                    quad = directorios.Cuadruplo(self.newQuad(), operator, left_operand, right_operand, result)
                    self.cuadruplos.append(quad)
                    self.pilaO.append(result)
                    self.pilaTipos.append(result_type)
                else:
                    errores.errorTypeMismatch(left_operand_type, right_operand_type, operator)

    def modids1(self, tree):
        procActual = self.directorioProcedimientos.searchProc(self.pilaProcedimientos[-1])
        tipo = tree.children[0].children[0].value
        id = tree.children[1].value
        var = directorios.Variable(id, tipo)
        procActual.tablaVariables.addVar(var)

    def np_vars_mod(self, tree):
        procActual = self.directorioProcedimientos.searchProc(self.pilaProcedimientos[-1])
        procActual.np_mod(self.quadCounter)

    # Punto neuralgico que marca el fin del programa
    def np_end(self, tree):
        # self.directorioProcedimientos.printDir()
        del self.directorioProcedimientos
        # print(self.pilaProcedimientos)
        # print(self.cuadruplos)
        for x in self.cuadruplos:
            x.printCuadruplo()
        print("fin")
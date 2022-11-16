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

    # Regresa el siguiente temporal 
    def availNext(self):
        self.temp += 1
        return 't' + str(self.temp)

    # Regresa el número del siguiente cuádruplo
    def newQuad(self):
        self.quadCounter += 1
        return self.quadCounter

    def currProc(self):
        return self.directorioProcedimientos.searchProc(self.pilaProcedimientos[-1])

    def searchVar(self, id):
        if (self.currProc().tablaVariables.searchVar(id) != 0):
            return self.currProc().tablaVariables.searchVar(id)
        else:
            if (self.directorioProcedimientos.searchProc(self.pilaProcedimientos[0]).tablaVariables.searchVar(id) != 0):
                return self.directorioProcedimientos.searchProc(self.pilaProcedimientos[0]).tablaVariables.searchVar(id)
            else:
                return errores.errorNoExiste("variable", id)

    # NP PROGRAM
    # Punto neuralgico de registro de proceso programa en Directorio de Procedimientos
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

    # NP MODULO
    # Punto neuralgico de registro de proceso modulo en Directorio de Procedimientos
    def modulo(self, tree):
        tipoMod = tree.children[0].children[0].value
        nombreMod = tree.children[1].value
        modProc = directorios.Procedimiento(nombreMod, tipoMod)
        # Se agrega el modulo al Directorio de Procedimientos
        self.directorioProcedimientos.addProc(modProc)
        # Se agrega el modulo a la Pila de Procedimientos para mantener el contexto
        self.pilaProcedimientos.append(nombreMod)
        self.procActual = modProc

    # NP MODIDS1
    # Punto neuralgico que procesa los parametros
    def modids1(self, tree):
        tipo = tree.children[0].children[0].value
        id = tree.children[1].value
        var = directorios.Variable(id, tipo)
        # Se agrega el parametro como variable local a la Tabla de Variables
        self.currProc().tablaVariables.addVar(var)
        # Se agrega el tipo a la Tabla de Parametros del procedimiento para generar la firma de la funcion 
        # Esta funcion calcula el numero de parametros definidos para calcular el tamaño del workspace para ejecucion
        self.currProc().addParam(tipo)

    # NP MOD
    # Punto neuralgico que agrega al Procedimiento el cuadruplo donde inicia el modulo
    def np_mod(self, tree):
        self.currProc().addStartQuadruple(self.quadCounter)

    # NP VARS MOD
    # Punto neuralgico que agrega el numero de variables locales en la Tabla de Variables al procedimiento 
    def np_vars_mod(self, tree):
        self.currProc().addNumVars()

    # NP END FUNC
    # Punto neuralgico que se encarga de terminar el procedimiento
    def np_endfunc(self, tree):
        proc = self.directorioProcedimientos.searchProc(self.pilaProcedimientos.pop())
        # Se elimina la tabla de Variables
        del proc.tablaVariables
        # Se cambia el contexto actual
        self.procActual = self.pilaProcedimientos[-1]
        # Se genera el cuadruplo para finalizar la funcion
        quad = directorios.Cuadruplo(self.newQuad(), 'endfunc', '', '', '')
        self.cuadruplos.append(quad)
        # Se inserta al Directorio de Procedimientos el numero de variables temporales utilizadas
        proc.addTemps(self.temp)
        # Se reinicia el contador de temporales
        self.temp = 0

    # NP PROBLEMA
    # Registro de proceso problema en Directorio de Procedimientos
    def problema(self, tree):
        tipoProb = tree.children[0].value
        nombreProb = tree.children[1].value
        problemaProc = directorios.Procedimiento(nombreProb, tipoProb)
        # Se agrega el problema al Directorio de Procedimientos
        self.directorioProcedimientos.addProc(problemaProc)
        # Se agrega el problema a la Pila de Procedimientos
        self.pilaProcedimientos.append(nombreProb)
        self.procActual = problemaProc

    # NP PARAM PROB
    # Punto neuralgico que procesa el parametro de un problema
    def np_param_prob(self, tree):
        id = tree.children[0].value
        op = tree.children[1].value
        res = tree.children[2].value
        var = directorios.Variable(id, "string", res)
        # Se agrega el parametro como variable local a la Tabla de Variables
        self.currProc().tablaVariables.addVar(var)
        # Se genera el cuadruplo de asignacion del parametro
        quad = directorios.Cuadruplo(self.newQuad(), op, res, "", id)
        self.cuadruplos.append(quad)

    # NP GENERA
    # Registro de proceso genera en Directorio de Procedimientos
    def genera(self, tree):
        genera = tree.children[0].value
        generaProc = directorios.Procedimiento(genera, genera)
        # Se agrega el procedimiento genera al Directorio de Procedimientos
        self.directorioProcedimientos.addProc(generaProc)
        # Se agrega el procedimiento genera a la Pila de Procedimientos para mantener el contexto
        self.pilaProcedimientos.append(tree.children[0].value)
        self.procActual = generaProc

    # NP PARAM GENERA
    # Registra los parametros de la funcion genera
    def np_param_genera(self, tree):
        varOrientacion = directorios.Variable(tree.children[0].value, "string")
        varCategoria = directorios.Variable(tree.children[2].value, "string")
        varProblemas = directorios.Variable(tree.children[4].value, "arr")
        varNombreArchivo = directorios.Variable(tree.children[5].value, "string")
        # Se agregan los parametros como variables a la Tabla de Variables del programa
        self.currProc().tablaVariables.addVar(varOrientacion)
        self.currProc().tablaVariables.addVar(varCategoria)
        self.currProc().tablaVariables.addVar(varProblemas)
        self.currProc().tablaVariables.addVar(varNombreArchivo)

    # NP MAIN
    # Registro de proceso main en Directorio de Procedimientos
    def main(self, tree):
        mainProc = directorios.Procedimiento(tree.children[0].value, tree.children[0].value)
        # Se agrega el procedimiento main al Directorio de Procedimientos
        self.directorioProcedimientos.addProc(mainProc)
        # Se agrega el procedimiento main a la Pila de Procedimientos
        self.pilaProcedimientos.append(tree.children[0].value)
        self.procActual = mainProc
        
    # NP INFO    
    # Registro de variables generales del programa
    def info(self, tree):
        # Registro de variable organizacion
        organizacion = directorios.Variable(tree.children[0].value, "string", tree.children[2].value)
        self.currProc().tablaVariables.addVar(organizacion)
        quadOrg = directorios.Cuadruplo(self.newQuad(), "=", tree.children[2].value, '', tree.children[0].value)
        
        # Registro de variable etapa
        etapa = directorios.Variable(tree.children[3].value, "string", tree.children[5].value)
        self.currProc().tablaVariables.addVar(etapa)
        quadEtapa = directorios.Cuadruplo(self.newQuad(), "=", tree.children[5].value, '', tree.children[3].value)
        
        # Registro de variable categorias
        categorias = directorios.Variable(tree.children[6].value, "arr", tree.children[6].value)
        quadCategorias = directorios.Cuadruplo(self.newQuad(), "=", tree.children[6].value, '', tree.children[6].value)
        self.currProc().tablaVariables.addVar(categorias)

        # Se agregan los cuadruplos a la lista de cuadruplos
        self.cuadruplos.extend([quadOrg, quadEtapa, quadCategorias])

    # NP VARS
    # Punto neuralgico de adicion de variables
    def np_vars(self, tree):
        # Cada que se crea un proceso, se crea su taba de variables
        tipoVar = tree.children[0].children[0].value
        nombreVar = tree.children[1].value
        # Se agrega el tipo de la variable a la pila de variables
        self.pilaTipos.append(tipoVar)
        var = directorios.Variable(nombreVar, tipoVar)
        # Se registra la variable en la Tabla de Variables
        self.currProc().tablaVariables.addVar(var)
        self.pilaO.append(nombreVar)

    # NP VARS 1
    # Punto neuralgico que prepara la asignacion de valores a una variable
    def vars1(self, tree):
        if (tree.children[0] == '='):
            self.pOper.append('=')
        else:
            # Si no se realizara una asignacion, se elimina el operando
            if (self.pilaO):
                self.pilaO.pop()

    # NP VARS 2
    # Punto neuralgico que registra las demas variables declaradas en la misma linea
    def vars2(self, tree): 
        if(tree.children[0] == ','):
            tipoVar = self.pilaTipos[-1]
            nombreVar = tree.children[1].value
            var = directorios.Variable(nombreVar, tipoVar)
            # Se registra la variable en la Tabla de Variables
            self.currProc().tablaVariables.addVar(var)
            self.pilaO.append(nombreVar)
    
    # NP FIN VARS
    # Punto neuralgico que elimina el tipo guardado de la declaracion al terminarse esta y proseguir a la siguiente
    def np_fin_vars(self, tree):
        self.pilaTipos.pop()

    # NP ASIG VARS
    # Punto neuralgico que asigna los valores de las variables
    def np_asig_vars(self, tree):
        if(self.pOper[-1] == '='):
            resultado = self.pilaO.pop()
            resultado_type = self.pilaTipos.pop()
            id = self.pilaO.pop()
            id_operand_type = self.pilaTipos[-1]
            operator = self.pOper.pop()
            # ⭐️  Revisa cubo semantico
            result_type = 1
            if (result_type != 0):
                quad = directorios.Cuadruplo(self.newQuad(), operator, resultado, "", id)
                self.cuadruplos.append(quad)
            else:
                errores.errorTypeMismatch(resultado, id, operator)

    # NP FACT1
    # Punto neuralgico que agrega a la pila de operandos un factor
    def fact1(self, tree):
        if(tree.children[0].children[0].type == "ID"):
            id = tree.children[0].children[0].value
            var = self.currProc().tablaVariables.searchVar(id)
            self.pilaO.append(id)
            self.pilaTipos.append(var.tipo)
        else:
            self.pilaO.append(tree.children[0].children[0].value)
            self.pilaTipos.append(tree.children[0].children[0].type)

        #print(self.pilaO)
        #print(self.pilaTipos)

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
    
    def asignacion(self, tree):
        id = tree.children[0].value
        var = self.searchVar(id)
        self.pilaO.append(id)
        self.pilaTipos.append(var.tipo)

    def asig2(self, tree):
        self.pOper.append("=")

    def np_asig(self, tree):
        if(self.pOper[-1] == '='):
            resultado = self.pilaO.pop()
            resultado_type = self.pilaTipos.pop()
            id = self.pilaO.pop()
            id_operand_type = self.pilaTipos[-1]
            operator = self.pOper.pop()
            # ⭐️  Revisa cubo semantico
            result_type = 1
            if (result_type != 0):
                quad = directorios.Cuadruplo(self.newQuad(), operator, resultado, "", id)
                self.cuadruplos.append(quad)
            else:
                errores.errorTypeMismatch(resultado, id, operator)

    # Punto neuralgico que marca el fin del programa
    def np_end(self, tree):
        # self.directorioProcedimientos.printDir()
        del self.directorioProcedimientos
        # print(self.pilaProcedimientos)
        # print(self.cuadruplos)
        for x in self.cuadruplos:
            x.printCuadruplo()
        print("fin")
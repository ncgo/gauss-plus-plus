# PUNTOS NEURALGICOS
# Acciones semánticas y de generación de código
#
# GAUSS++
# Nadia Corina Garcia Orozco A01242428
# Noviembre, 2022

from lark import Visitor

import directorios
import errores
import memoria
from cubo_semantico import cuboSemantico


class PuntosNeuralgicos(Visitor):
    def __init__(self):
        self.directorioProcedimientos = None    # Directorio de procedimientos 
        self.pilaProcedimientos = []            # Pila que almacena el orden de los procedimentos para el manejo de contexto
        self.pilaTipos = []                     # Pila que guarda los tipos de los operandos
        self.pOper = []                         # Pila que guarda los operadores
        self.pilaO = []                         # Pila que guarda los operandos 
        self.pilaSaltos = []                    # Pila que guarda el numero del cuadruplo con saltos pendientes
        self.temp = 0           
        self.procActual = None          
        self.cuadruplos = []                    # Lista de cuadruplos generados
        self.quadCounter = 0                    # Contador de cuadruplos
        self.k = 0                              # Auxiliar para el registro de parametros
        self.memoria = memoria.MapaDeMemoria()  # Memoria
        self.pilaDim = []                       # Pila que auxilia con el acceso a arreglos
        self.tablaConstantes = None
        self.returns = 0
        self.pReturns = []
        self.r = 1
    # CREATE OBJ FILE
    # Funcion auxiliar que genera el archivo de codigo objeto con lso cuadruplso generados por el programa a ser ejecutado por la maquina virtual
    def createObjFile(self):
        f = open("obj", "w")
        for x in self.cuadruplos:
            f.write(x.printCuadruplo() + '\n')
        f.close()

    # NEW QUAD
    # Funcion auxiliar que regresa el número del siguiente cuádruplo
    def newQuad(self):
        self.quadCounter += 1
        return self.quadCounter

    # CURR PROC
    # Funcion auxiliar que regresa el proceso actual para manejo de contextos
    def currProc(self):
        return self.directorioProcedimientos.searchProc(self.pilaProcedimientos[-1])

    # SEARCH VAR
    # Funcion auxiliar que busca la variable en el contextoa actual y en el contexto global
    def searchVar(self, id):
        # Busca la variable en el contexto actual
        if (self.currProc().tablaVariables.searchVar(id) != 0):
            return self.currProc().tablaVariables.searchVar(id)
        
        else:
            # Busca la variable en el contexto global
            if (self.directorioProcedimientos.searchProc(self.pilaProcedimientos[0]).tablaVariables.searchVar(id) != 0):
                return self.directorioProcedimientos.searchProc(self.pilaProcedimientos[0]).tablaVariables.searchVar(id)
            
            else:
                return errores.errorNoExiste("variable", id)
    
    # FILL QUAD
    # Funcion auziliar para rellenar los cuadruplos pertinentes
    def fillQuad(self, quadToFill, filler):
        self.cuadruplos[quadToFill-1].fillCuadruplo(filler)

    # NORMALIZE TYPE
    # Funcion auxiliar que regresa el tipo correcto para constantes
    def normalizeType(self, type):
        if type == "CTEINT":
            return "int"
        elif type == "CTEFLOAT":
            return "float"
        elif type == "CTEBOOL":
            return "bool"
        elif type == "CTESTRING":
            return "string"
        else:
            return "string"

    # PROGRAM
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
        # Se crea el cuádruplo de regsitro de programa
        quad = directorios.Cuadruplo(self.newQuad(), "PROGRAM", "", "", nombre)
        self.cuadruplos.append(quad)
        # Se crea la tabla de Constantes
        self.tablaConstantes = directorios.TablaConstantes()

    # NP MAIN
    # Punto neuralgico que llama la funcion de main despues de procesar las variables globales
    def np_main(self, tree):
        # Se crea el cuádruplo de goto main a ser llenado posteriormente
        quad = directorios.Cuadruplo(self.newQuad(), "GOTO", "", "", "")
        self.cuadruplos.append(quad)
        # Se agrega el número de cuádruplo para llenar posteriormente
        self.pilaSaltos.append(self.quadCounter)

    # MODULO
    # Punto neuralgico de registro de proceso modulo en Directorio de Procedimientos
    def modulo(self, tree):
        self.memoria.restart()
        tipoMod = tree.children[0].children[0].value
        nombreMod = tree.children[1].value
        modProc = directorios.Procedimiento(nombreMod, tipoMod)
        # Se agrega el modulo al Directorio de Procedimientos
        self.directorioProcedimientos.addProc(modProc)
        # Se agrega el modulo a la Pila de Procedimientos para mantener el contexto
        self.pilaProcedimientos.append(nombreMod)

    # MODIDS1
    # Punto neuralgico que procesa los parametros
    def modids1(self, tree):
        tipo = tree.children[0].children[0].value
        id = tree.children[1].value
        var = directorios.Variable(id, tipo)
        var.virtualAddress = self.memoria.virtualAddress(tipo)
        # Se agrega el parametro como variable local a la Tabla de Variables
        self.currProc().tablaVariables.addVar(var)
        # Se agrega el tipo a la Tabla de Parametros del procedimiento para generar la firma de la funcion 
        # Esta funcion calcula el numero de parametros definidos para calcular el tamaño del workspace para ejecucion
        self.currProc().addParam(tipo)

    # NP MOD
    # Punto neuralgico que agrega al Procedimiento el cuadruplo donde inicia el modulo
    def np_mod(self, tree):
        self.currProc().addStartQuadruple(self.quadCounter + 1)

    # NP VARS MOD
    # Punto neuralgico que agrega el numero de variables locales en la Tabla de Variables al procedimiento 
    def np_vars_mod(self, tree):
        self.currProc().addNumVars()

    # NP RETURN
    # Punto neuralgico que agrega la instruccion return a la pila de operadores
    def np_return(self, tree):
        # Revisa si no es void y si aplica el return
        if (self.currProc().tipo != "void"):
            self.pOper.append("return")
        else:
            # La funcion es de tipo void y no puede regresar valores
            errores.errorReturnVoid(self.currProc().nombre)

    # NP RETURN1
    # Punto neuralgico que genera el cuadruplo de return
    def np_return1(self, tree):
        self.createObjFile()
        if(self.pOper[-1] == 'return'):
            retorno = self.pilaO.pop()
            retorno_type = self.pilaTipos.pop()
            operator = self.pOper.pop()
            funcion_type = self.currProc().tipo
            # Se revisa que el tipo de retorno corresponda con el tipo de funcion
            if (retorno_type == funcion_type):
                # Se genera el cuadruplo RETURN
                quad = directorios.Cuadruplo(self.newQuad(), "RETURN", "", "", retorno)
                self.cuadruplos.append(quad)
                # Se genera el cuadruplo GOTO que cortará la ejecución de una función al tener un return
                quad = directorios.Cuadruplo(self.newQuad(), "GOTO", "", "", "FILL")
                self.cuadruplos.append(quad)
                # Se agrega el cuadruplo a la pila de retornos para ser rellenada posteriormente
                self.pReturns.append(self.quadCounter)
                # Se incrementa el numero de retornos
                self.returns += 1
            else:
                # No corresponde el tipo de retorno con el tipo de funcion
                errores.errorTypeMismatchReturn(retorno_type, funcion_type, self.currProc().nombre)

    # NP END FUNC
    # Punto neuralgico que se encarga de terminar el procedimiento
    def np_endfunc(self, tree):
        proc = self.directorioProcedimientos.searchProc(self.pilaProcedimientos.pop())
        # Se elimina la tabla de Variables
        del proc.tablaVariables
        # Se cambia el contexto actual
        self.procActual = self.pilaProcedimientos[-1]
        # Se genera el cuadruplo para finalizar la funcion
        quad = directorios.Cuadruplo(self.newQuad(), 'ENDFUNC', '', '', proc.nombre)
        self.cuadruplos.append(quad)
        # Mientras hayan retornos pendientes
        while (self.returns >= 1):
            # Se rellenan los cuadruplos de GOTO generados por los retornos
            self.fillQuad(self.pReturns.pop(), self.quadCounter - 1)
            # Se decrementa la cantidad de retornos faltantes
            self.returns -= 1
        # Se inserta al Directorio de Procedimientos el numero de variables temporales utilizadas
        proc.addTemps(self.temp)
        # Se reinicia el contador de temporales
        self.temp = 0

    # PROBLEMA
    # Registro de proceso problema en Directorio de Procedimientos
    def problema(self, tree):
        tipoProb = tree.children[0].value
        nombreProb = tree.children[1].value
        problemaProc = directorios.Procedimiento(nombreProb, tipoProb)
        # Se agrega el problema al Directorio de Procedimientos
        self.directorioProcedimientos.addProc(problemaProc)
        # Se agrega el problema a la Pila de Procedimientos
        self.pilaProcedimientos.append(nombreProb)

    # NP PARAM PROB
    # Punto neuralgico que procesa el parametro de un problema
    def np_param_prob(self, tree):
        id = tree.children[0].value
        res = tree.children[2].value

        # Se registra la constante en la tabla de constantes
        cte = directorios.Constante(tree.children[2].value, "string", self.memoria.addressCte("string"))
        self.tablaConstantes.addCte(cte)

        var = directorios.Variable(id, "string", res)
        var.virtualAddress = self.memoria.virtualAddress("string")
        # Se agrega el parametro como variable local a la Tabla de Variables
        self.currProc().tablaVariables.addVar(var)
        # Se genera el cuadruplo de asignacion del parametro
        quad = directorios.Cuadruplo(self.newQuad(), "AREA", cte.virtualAddress, "", var.virtualAddress)
        self.cuadruplos.append(quad)

    # GENERA
    # Registro de proceso genera en Directorio de Procedimientos
    def genera(self, tree):
        try:
            tree.children[0].value
        except:
            next
        else:
            genera = tree.children[0].value
            generaProc = directorios.Procedimiento(genera, genera)
            # Se agrega el procedimiento genera al Directorio de Procedimientos
            self.directorioProcedimientos.addProc(generaProc)
            # Se agrega el procedimiento genera a la Pila de Procedimientos para mantener el contexto
            self.pilaProcedimientos.append(tree.children[0].value)
            generaProc.addStartQuadruple(self.quadCounter + 1)

    # NP PARAM GENERA
    # Registra los parametros de la funcion genera
    def np_param_genera(self, tree):
        varOrientacion = directorios.Variable(tree.children[0].value, "string")
        varOrientacion.virtualAddress = self.memoria.virtualAddress("string")
        varCategoria = directorios.Variable(tree.children[2].value, "string")
        varCategoria.virtualAddress = self.memoria.virtualAddress("string")
        varProblemas = directorios.Variable(tree.children[4].value, "lista")
        varProblemas.virtualAddress = self.memoria.virtualAddress("lista")
        varProblemas.isArray = True
        varNombreArchivo = directorios.Variable(tree.children[5].value, "string")
        varNombreArchivo.virtualAddress = self.memoria.virtualAddress("string")
        # Se agregan los parametros como variables a la Tabla de Variables del programa
        self.currProc().tablaVariables.addVar(varOrientacion)
        self.currProc().addParam("string")
        self.currProc().tablaVariables.addVar(varCategoria)
        self.currProc().addParam("string")
        self.currProc().tablaVariables.addVar(varProblemas)
        self.currProc().addParam("lista")
        self.currProc().tablaVariables.addVar(varNombreArchivo)
        self.currProc().addParam("string")

    # HEADER
    # Punto neuralgico que registra el primer valor del Header
    def header(self, tree):
        organizacion = tree.children[2].children[0].value
        if tree.children[2].children[0].type == "ID":
            var = self.searchVar(organizacion)
            quad = directorios.Cuadruplo(self.newQuad(), "GENERA", "HEADER", 0, var.virtualAddress)
        else:
            quad = directorios.Cuadruplo(self.newQuad(), "GENERA", "HEADER", 0, organizacion)
        self.cuadruplos.append(quad)

    # FECHA
    # Punto neuralgico que registra el segundo valor del header
    def fecha(self, tree):
        fecha = tree.children[0].children[0].value
        if tree.children[0].children[0].type == "ID" and fecha != "fecha":
            var = self.searchVar(fecha)
            quad = directorios.Cuadruplo(self.newQuad(), "GENERA", "HEADER", 1, var.virtualAddress)
        else:
            quad = directorios.Cuadruplo(self.newQuad(), "GENERA", "HEADER", 1, fecha)
        self.cuadruplos.append(quad)

    # ETAPA
    # Punto neuralgico que registra el tercer valor del header
    def etapa(self, tree):
        etapa = tree.children[0].children[0].value
        if tree.children[0].children[0].type == "ID":
            var = self.searchVar(etapa)
            quad = directorios.Cuadruplo(self.newQuad(), "GENERA", "HEADER", 2, var.virtualAddress)
        else:
            quad = directorios.Cuadruplo(self.newQuad(), "GENERA", "HEADER", 2, etapa)
        self.cuadruplos.append(quad)

    # TITULO
    # Punto neuralgico que registra el valor del titulo
    def titulo(self, tree):
        titulo = tree.children[2].children[0].value
        if tree.children[2].children[0].type == "ID":
            var = self.searchVar(titulo)
            quad = directorios.Cuadruplo(self.newQuad(), "GENERA", "TITULO", 0, var.virtualAddress)
        else:
            # Se registra la constante en la tabla de constantes
            cte = directorios.Constante(titulo, "string", self.memoria.addressCte("string"))
            self.tablaConstantes.addCte(cte)
            quad = directorios.Cuadruplo(self.newQuad(), "GENERA", "TITULO", 0, cte.virtualAddress)
        self.cuadruplos.append(quad)

    # INSTRUCCIONES
    # Punto neuralgico que registra las instrucciones
    def instrucciones(self, tree):
        instrucciones = tree.children[2].children[0].value
        if tree.children[2].children[0].type == "ID":
            var = self.searchVar(instrucciones)
            quad = directorios.Cuadruplo(self.newQuad(), "GENERA", "INSTRUCCIONES", 0, var.virtualAddress)
        else:
            # Se registra la constante en la tabla de constantes
            cte = directorios.Constante(instrucciones, "string", self.memoria.addressCte("string"))
            self.tablaConstantes.addCte(cte)
            quad = directorios.Cuadruplo(self.newQuad(), "GENERA", "INSTRUCCIONES", 0, cte.virtualAddress)
        self.cuadruplos.append(quad)

    # PROBLEMAS INCLUIDOS
    # Punto neuralgico que registra los problemas incluidos
    def problemasincluidos(self, tree):
        problemas = tree.children[2].value
        var = self.currProc().tablaVariables.searchVar(problemas)
        # Se valida que la variable exista y que sea un arreglo
        if (var != 0 and var.isArray):
            problemas = directorios.Cuadruplo(self.newQuad(), "GENERA", "PROBLEMASINCLUIDOS", 0, var.virtualAddress)
            self.cuadruplos.append(problemas)
            # Registra si sera random el acomodo no
            randomV = directorios.Cuadruplo(self.newQuad(), "GENERA", "PROBLEMASINCLUIDOS", 1, tree.children[6].children[0].value)
            self.cuadruplos.append(randomV)
        else:
            errores.errorIDNotArray(problemas)

    # FOOTER
    # Punro neuralgico que registra el valor del footer
    def footer(self, tree):
        footer = tree.children[2].children[0].value
        if tree.children[2].children[0].type == "ID":
            var = self.searchVar(footer)
            quad = directorios.Cuadruplo(self.newQuad(), "GENERA", "FOOTER", 0, var.virtualAddress)
        else:
            quad = directorios.Cuadruplo(self.newQuad(), "GENERA", "FOOTER", 0, footer)
        self.cuadruplos.append(quad)

    # MAIN
    # Registro de proceso main en Directorio de Procedimientos
    def main(self, tree):
        quad = directorios.Cuadruplo(self.newQuad(), "MAIN", "", "", "")
        self.cuadruplos.append(quad)
        mainProc = directorios.Procedimiento(tree.children[0].value, tree.children[0].value)
        # Se agrega el procedimiento main al Directorio de Procedimientos
        self.directorioProcedimientos.addProc(mainProc)
        # Se agrega el procedimiento main a la Pila de Procedimientos
        self.pilaProcedimientos.append(tree.children[0].value)
        # Se rellena el cuadruplo inicial para indicar que aqui inicia la ejecucion del programa
        main = self.pilaSaltos.pop()
        self.fillQuad(main, self.quadCounter - 1)
        
    # INFO    
    # Registro de variables generales del programa
    def info(self, tree):
        try:
            tree.children[0].value
        except:
            next
        else:
            # Registro de variable organizacion
            organizacion = directorios.Variable(tree.children[0].value, "string")
            # Se registra la constante en la tabla de constantes
            cte = directorios.Constante(tree.children[2].value, "string", self.memoria.addressCte("string"))
            self.tablaConstantes.addCte(cte)
            organizacion.virtualAddress = self.memoria.virtualAddress("string", True)
            self.currProc().tablaVariables.addVar(organizacion)
            quadOrg = directorios.Cuadruplo(self.newQuad(), "INFO", cte.virtualAddress, '', organizacion.virtualAddress)
            
            # Registro de variable etapa
            etapa = directorios.Variable(tree.children[3].value, "string")
            # Se registra la constante en la tabla de constantes
            cte = directorios.Constante(tree.children[5].value, "string", self.memoria.addressCte("string"))
            self.tablaConstantes.addCte(cte)
            etapa.virtualAddress = self.memoria.virtualAddress("string", True)
            self.currProc().tablaVariables.addVar(etapa)
            quadEtapa = directorios.Cuadruplo(self.newQuad(), "INFO", cte.virtualAddress, '', etapa.virtualAddress)

            # Se agregan los cuadruplos a la lista de cuadruplos
            self.cuadruplos.extend([quadOrg, quadEtapa])

    # CATEGORIAS DEC
    # Punto neuralgico que registra la variable categorias en la Tabla de Variables
    def categoriasdec(self, tree):
        # Registro de variable categorias
        categorias = directorios.Variable(tree.children[0].value, "string")
        categorias.virtualAddress = self.memoria.virtualAddress("string", True)
        # Se declara que la variable categorias es un arreglo
        categorias.isArray = True
        self.currProc().tablaVariables.addVar(categorias)

    # CAT DEC
    # Punto neuralgico que registra el valor de la primer categoria
    def catdec(self, tree):
        var = self.searchVar("categorias")
        # Se registra la constante en la tabla de constantes
        cte = directorios.Constante(tree.children[0].value, "string", self.memoria.addressCte("string"))
        self.tablaConstantes.addCte(cte)
        quad = directorios.Cuadruplo(self.newQuad(), "INFO", cte.virtualAddress, self.k, var.virtualAddress)
        self.cuadruplos.append(quad)
        # Se incrementa el numero de categorias en 1
        self.k += 1
    
    # CAT DEC 1
    # Punto neuralgico que registra el valor del resto de las categorias
    def catdec1(self, tree):
        try:
            tree.children[1]
        except:
            next
        else:
            var = self.searchVar("categorias")
            # Se registra la constante en la tabla de constantes
            cte = directorios.Constante(tree.children[1].value, "string", self.memoria.addressCte("string"))
            self.tablaConstantes.addCte(cte)
            quad = directorios.Cuadruplo(self.newQuad(), "INFO", cte.virtualAddress, self.k, var.virtualAddress)
            self.cuadruplos.append(quad)
            # Se incrementa en 1 el numero de categorias
            self.k += 1

    # NP CAT DEC FIN
    # Punto neuralgico que da por finalizada la declaracion del arreglo categorias
    def np_catdecfin(self, tree):
        # Se suma la cantidad de categorias para las direcciones virtuales
        self.memoria.updateByArray("string", self.k, True)
        # Se reestablece k
        self.k = 0

    # NP VARS
    # Punto neuralgico de adicion de variables
    def np_vars(self, tree):
        try: tree.children[0].children[0].value
        except: next
        else:
            # Cada que se crea un proceso, se crea su taba de variables
            tipoVar = tree.children[0].children[0].value
            nombreVar = tree.children[1].value
            # Se agrega el tipo de la variable a la pila de variables
            self.pilaTipos.append(tipoVar)
            var = directorios.Variable(nombreVar, tipoVar)
            if (len(self.pilaProcedimientos) == 1):
                var.virtualAddress = self.memoria.virtualAddress(tipoVar, True)
            else:
                var.virtualAddress = self.memoria.virtualAddress(tipoVar)
            # Se registra la variable en la Tabla de Variables
            self.currProc().tablaVariables.addVar(var)
            self.pilaO.append(var.virtualAddress)

    # VARS 1
    # Punto neuralgico que prepara la asignacion de valores a una variable
    def vars1(self, tree):
        if (tree.children[0] == '='):
            self.pOper.append('=')
        else:
            # Si no se realizara una asignacion, se elimina el operando
            if (self.pilaO):
                self.pilaO.pop()

    # VARS 2
    # Punto neuralgico que registra las demas variables declaradas en la misma linea
    def vars2(self, tree): 
        try: tree.children[0]
        except: next
        else:
            if(tree.children[0] == ','):
                tipoVar = self.pilaTipos[-1]
                nombreVar = tree.children[1].value
                var = directorios.Variable(nombreVar, tipoVar)
                if (len(self.pilaProcedimientos) == 1):
                    var.virtualAddress = self.memoria.virtualAddress(tipoVar, True)
                else:
                    var.virtualAddress = self.memoria.virtualAddress(tipoVar)
                # Se registra la variable en la Tabla de Variables
                self.currProc().tablaVariables.addVar(var)
                self.pilaO.append(var.virtualAddress)
    
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
            result_type = cuboSemantico[operator][resultado_type][id_operand_type]
            if (result_type != "ERROR"):
                quad = directorios.Cuadruplo(self.newQuad(), operator, resultado, "", id)
                self.cuadruplos.append(quad)
            else:
                errores.errorTypeMismatch(resultado, id, operator)

    # FACTOR
    # Punto neuralgico que agrega un fondo falso a la pila de operadores cuando se presenta un paréntesis en una expresión
    def factor(self, tree):
        try: tree.children[0].value
        except: next
        else: 
            if (tree.children[0].value == '('):
                self.pOper.append('[')

    # NP FACTOR
    # Punto neuralgico que elimina el fondo falso cuando se cierra un paréntesis en una expresión
    def np_factor(self, tree):
        if (self.pOper[-1] == '['):
            self.pOper.pop()

    # FACT1
    # Punto neuralgico que agrega a la pila de operandos un factor
    def fact1(self, tree):
        try: tree.children[0].children[0].value
        except: 
            # Si se tiene una llamada a una funcion como un factor
            if (tree.children[0].children[0].data == "llamadafunc"):
                procNombre = tree.children[0].children[0].children[0].value
                proc = self.directorioProcedimientos.searchProc(procNombre)
                # Se agrega el nombre del procedimiento como variable local del procedimiento para guardar los valores de retorno
                var = directorios.Variable(procNombre, proc.tipo)
                self.pilaO.append(procNombre)
                self.pilaTipos.append(proc.tipo)
        else:
            # Si se tiene una constante como factor
            if (tree.children[0].data == "varcte"):
                # Si se tiene un ID como factor
                if(tree.children[0].children[0].type == "ID"):
                    id = tree.children[0].children[0].value
                    var = self.searchVar(id)
                    self.pilaO.append(var.virtualAddress)
                    self.pilaTipos.append(var.tipo)
                else:
                    # Se registra la constante en la tabla de constantes
                    cte = directorios.Constante(tree.children[0].children[0].value, self.normalizeType(tree.children[0].children[0].type), self.memoria.addressCte(self.normalizeType(tree.children[0].children[0].type)))
                    self.tablaConstantes.addCte(cte)
                    self.pilaO.append(cte.virtualAddress)
                    self.pilaTipos.append(cte.tipo)

    # LLAMADA AUX
    # Punto neuralgico que agrega un fondo falso a la pila de operadores cuando se empieza una llamada a una funcion
    def llamadaaux(self, tipo):
        self.pOper.append('[')

    # TER1
    # Agrega * o / a la pila de Operadores
    def ter1(self, tree):
        self.pOper.append(tree.children[0].value)
    
    # EXP1
    # Agrega + o - a la pila de Operadores
    def exp1(self, tree):
        self.pOper.append(tree.children[0].value)

    # NP EXP
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
                result_type = cuboSemantico[operator][right_operand_type][left_operand_type]
                if (result_type != "ERROR"):
                    result = self.memoria.availNext(result_type)
                    quad = directorios.Cuadruplo(self.newQuad(), operator, left_operand, right_operand, result)
                    self.cuadruplos.append(quad)
                    self.pilaO.append(result)
                    self.pilaTipos.append(result_type)
                else:
                    errores.errorTypeMismatch(left_operand_type, right_operand_type, operator)

    # NP TERMINO
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
                result_type = cuboSemantico[operator][right_operand_type][left_operand_type]
                if (result_type != "ERROR"):
                    result = self.memoria.availNext(result_type)
                    quad = directorios.Cuadruplo(self.newQuad(), operator, left_operand, right_operand, result)
                    self.cuadruplos.append(quad)
                    self.pilaO.append(result)
                    self.pilaTipos.append(result_type)
                else:
                    errores.errorTypeMismatch(left_operand_type, right_operand_type, operator)
    
    # ASIGNACION
    # Agrega la variable a ser asignada a la Pila de operandos y su tipo a la fila de tipos
    def asignacion(self, tree):
        try:
            id = tree.children[0].value
            # Verifica que la variable ya haya sido declarada
            var = self.searchVar(id)
            self.pilaO.append(var.virtualAddress)
            self.pilaTipos.append(var.tipo)
        except:
            next

    # ASIG2
    # Agrega el operador a la pila de operadores
    def asig2(self, tree):
        self.pOper.append("=")

    # ASIG
    # Genera el cuadruplo de asignacion
    def np_asig(self, tree):
        if(self.pOper[-1] == '='):
            resultado = self.pilaO.pop()
            resultado_type = self.pilaTipos.pop()
            id = self.pilaO.pop()
            id_operand_type = self.pilaTipos.pop()
            operator = self.pOper.pop()
            # ⭐️  Revisa cubo semantico
            result_type = cuboSemantico[operator][resultado_type][id_operand_type]
            if (result_type != "ERROR"):
                quad = directorios.Cuadruplo(self.newQuad(), operator, resultado, "", id)
                self.cuadruplos.append(quad)
            else:
                errores.errorTypeMismatch(resultado_type, id_operand_type, operator)

    # PRINT PROB
    # Punto neuralgico que agrega el simbolo de impresion de problema a la pila de operadores
    def printprob(self, tree):
        try:
            tree.children[0]
        except: 
            next
        else:
            self.pOper.append(tree.children[0].value)

    # PRINT PROB 1
    # Punto neuralgico que genera el cuadruplo de impresion de problema
    def printprob1(self, tree):
        try:
            tree.children[0].type
        except:
            next
        else:
            # Se registra la constante en la tabla de constantes
            cte = directorios.Constante(tree.children[0].value, "string", self.memoria.addressCte("string"))
            self.tablaConstantes.addCte(cte)
            self.pilaO.append(cte.virtualAddress)
            self.pilaTipos.append("string")
            if(self.pOper[-1] == '>>'):
                printp = self.pilaO.pop()
                printp_type = self.pilaTipos.pop()
                operator = self.pOper.pop()
                if (printp_type == "string"):
                    quad = directorios.Cuadruplo(self.newQuad(), "PRINTP", "", "", printp)
                    self.cuadruplos.append(quad)
                else:
                    errores.errorTypeMismatch(printp, "", operator)

    # PRINT EXPR
    # Punto neuralgico que genera el cuadruplo de expresion
    def printexpr(self, tree):
        # Se registra la constante en la tabla de constantes
        cte = directorios.Constante(tree.children[0].value, "string", self.memoria.addressCte("string"))
        self.tablaConstantes.addCte(cte)
        self.pOper.append(cte.virtualAddress)
        self.pilaO.append(tree.children[3].value)
        self.pilaTipos.append("string")
        if(self.pOper[-1] == '$'):
            expr = self.pilaO.pop()
            expr_type = self.pilaTipos.pop()
            operator = self.pOper.pop()
            if (expr_type == "string"):
                quad = directorios.Cuadruplo(self.newQuad(), "EXPR", "", "", expr)
                self.cuadruplos.append(quad)
            else:
                errores.errorTypeMismatch(expr, "", operator)

    # PRINT IMPORT 
    # Punto neuralgico que genera el cuadruplo de importar
    def printimport(self, tree):
        # Se registra la constante en la tabla de constantes
        cte = directorios.Constante(tree.children[0].value, "string", self.memoria.addressCte("string"))
        self.tablaConstantes.addCte(cte)
        self.pOper.append(cte.virtualAddress)
        self.pilaO.append(tree.children[3].value)
        self.pilaTipos.append("string")
        if(self.pOper[-1] == '$'):
            imp = self.pilaO.pop()
            imp_type = self.pilaTipos.pop()
            operator = self.pOper.pop()
            if (imp_type == "path"):
                quad = directorios.Cuadruplo(self.newQuad(), "IMPORT", "", "", imp)
                self.cuadruplos.append(quad)
            else:
                errores.errorTypeMismatch(imp, "", operator)

    # OPCIONES
    # Punto neuralgico que registra la variable opciones
    def opciones(self, tree):
        try:
            tree.children
        except:
            next
        else:
            # Registro de la variable opciones
            opciones = directorios.Variable(tree.children[0].value, "string")
            opciones.virtualAddress = self.memoria.virtualAddress("opciones")
            # Se declara que la variable opciones es un arreglo
            opciones.isArray = True
            self.currProc().tablaVariables.addVar(opciones)

    # OPCIONES DEC
    # Punto neuralgico que registra el primer valor de la variable opciones
    def opcionesdec(self, tree):
        var = self.searchVar("opciones")
        # Se registra la constante en la tabla de constantes
        cte = directorios.Constante(tree.children[0].children[0].value, self.normalizeType(tree.children[0].children[0].type), self.memoria.addressCte(self.normalizeType(tree.children[0].children[0].type)))
        self.tablaConstantes.addCte(cte)
        quad = directorios.Cuadruplo(self.newQuad(), "OPCIONES", cte.virtualAddress, self.k, var.virtualAddress)
        self.cuadruplos.append(quad)
        # Se incrementa el numero de opciones en 1
        self.k += 1

    # OPCIONES DEC 1
    # Punto neuralgico que registra los valroes del resto de las opciones
    def opcionesdec1(self, tree):
        try:
            tree.children[1].children[0].value
        except:
            next
        else:
            var = self.searchVar("opciones")
            # Se registra la constante en la tabla de constantes
            cte = directorios.Constante(tree.children[1].children[0].value, self.normalizeType(tree.children[1].children[0].type), self.memoria.addressCte(self.normalizeType(tree.children[1].children[0].type)))
            self.tablaConstantes.addCte(cte)
            quad = directorios.Cuadruplo(self.newQuad(), "OPCIONES", cte.virtualAddress, self.k, var.virtualAddress)
            self.cuadruplos.append(quad)
            # Se incrementa en 1 el numero de opciones
            self.k += 1

    # NP OPCIONES DEC FIN
    # Punto neuralgico que da por finalizada la declaracion de opciones
    def np_opcionesdecfin(self, tree):
        # Se suma la cantidad de opciones para las direcciones virtuales
        self.memoria.updateByArray("string", self.k)
        # Se reestablece k
        self.k = 0

    # RESPUESTA
    # Punto neuralgico que registra la respuesta de un problema
    def respuesta(self, tree):
        respuesta = tree.children[0].value
        # Se registra la constante en la tabla de constantes
        cte = directorios.Constante(tree.children[2].children[0].value, self.normalizeType(tree.children[2].children[0].type), self.memoria.addressCte(self.normalizeType(tree.children[2].children[0].type)))
        self.tablaConstantes.addCte(cte)
        var = directorios.Variable(respuesta, "respuesta")
        var.virtualAddress = self.memoria.virtualAddress(respuesta)
        self.currProc().tablaVariables.addVar(var)
        quad = directorios.Cuadruplo(self.newQuad(), "RESPUESTA", cte.virtualAddress, "", var.virtualAddress)
        self.cuadruplos.append(quad)

    # LISTA
    # Punto neuralgico que registra las variables de tipo listas
    def lista(self, tree):
        id = tree.children[0].value
        var = directorios.Variable(id, "lista")
        # Registro de la variable
        self.currProc().tablaVariables.addVar(var)
        var.virtualAddress = self.memoria.virtualAddress("lista", True)
        # Se declara que la variable es un arreglo
        var.isArray = True
        self.pilaO.append(id)

    # E LISTA
    # Punto neuralgico que registra el valor del primer elemento de la lista
    def elista(self, tree):
        problema = tree.children[0].value
        if self.directorioProcedimientos.searchProc(problema):
            var = self.searchVar(self.pilaO[-1])
            quad = directorios.Cuadruplo(self.newQuad(), "LISTA", tree.children[0].value, self.k, var.virtualAddress)
            self.cuadruplos.append(quad)
            # Se incrementa el numero de elementos en 1
            self.k += 1
        
    # E LISTA 1
    #P Punto neuralgico que registra el valor del resto de los elementos de la lista
    def elista1(self, tree):
        try:
            tree.children[1]
        except:
            next
        else:
            problema = tree.children[1].value
            if self.directorioProcedimientos.searchProc(problema):
                var = self.searchVar(self.pilaO[-1])
                quad = directorios.Cuadruplo(self.newQuad(), "LISTA", problema, self.k, var.virtualAddress)
                self.cuadruplos.append(quad)
                # Se incrementa el numero de elementos en 1
                self.k += 1
    
    # NP LISTA FIN
    # Punto neuralgico que da por finalizada la declaracion de la lista
    def np_listafin(self, tree):
        # Se suma la cantidad de elementos de la lista para las direcciones virtuales
        self.memoria.updateByArray("lista", self.k, True)
        # Se reestablece k
        self.k = 0
        self.pilaO.pop()

    # ESCRITURA
    # Punto neuralgico que agrega el operador de print a la pila de operadores
    def escritura(self, tree):
        operador = tree.children[0].value
        self.pOper.append(operador)

    # ESCR1
    # Punto neuralgico que genera el cuadruplo de impresion
    def escr1(self, tree):
        if(self.pOper[-1] == 'print'):
            expr = self.pilaO.pop()
            expr_type = self.pilaTipos.pop()
            operator = self.pOper.pop()
            quad = directorios.Cuadruplo(self.newQuad(), "PRINT", "", "", expr)
            self.cuadruplos.append(quad)
    
    # ESCR2
    # Punto neuralgico que vuelve a agregar el operador print a la pila de operadores cuando hay varios argumentos para la funcion
    def escr2(self, tree):
        self.pOper.append("print")

    # LECTURA
    # Punto neuralgico que maneja la lectura 
    def lectura(self, tree):
        id = tree.children[2].value
        if self.searchVar(id) != 0:
            var = self.searchVar(id)
            quad = directorios.Cuadruplo(self.newQuad(), "READ", "", "", var.virtualAddress)
            self.cuadruplos.append(quad)

    # NP COND
    # Punto neuralgico que revisa la condicion y genera el cuadruplo GOTOF
    def np_cond(self, tree):
        result = self.pilaO.pop()
        result_type = self.pilaTipos.pop()
        # Se revisa que la condicion sea de tipo booleano
        if (result_type != "bool"):
            # Error de mismatch de tipos
            errores.errorCondTypeMismatch(result_type)
        else:
            # Se crea el cuadruplo GOTOF y se agrega el numero de cuadruplo a la pila de saltos para ser llenado posteriormente
            quad = directorios.Cuadruplo(self.newQuad(), "GOTOF", result, "", "FILL")
            self.cuadruplos.append(quad)
            self.pilaSaltos.append(self.quadCounter)

    # EXPRESION1
    # Punto neuralgico que agrega los simbolos de comparacion a la pila de operadores
    def expresion1(self, tree):
        self.pOper.append(tree.children[0].value)

    # NP EXPRESION
    # Punto neuralgico que genera los cuadruplos de comparacion logica
    def np_expresion(self, tree):
        if ((self.pOper[-1] == '<' or self.pOper[-1] == '>' or self.pOper[-1] == '<=' or self.pOper[-1] == '>=' or self.pOper[-1] == '!=' or self.pOper[-1] == "and" or self.pOper[-1] == "or" or self.pOper[-1] == "==")):
            right_operand = self.pilaO.pop()
            right_operand_type = self.pilaTipos.pop()
            left_operand = self.pilaO.pop()
            left_operand_type = self.pilaTipos.pop()
            operator = self.pOper.pop()
            # ⭐️ Revisa cubo semantico
            result_type = cuboSemantico[operator][right_operand_type][left_operand_type]
            if (result_type != "ERROR"):
                if operator == "and":
                    operator = "AND"
                elif operator == "or":
                    operator = "OR"
                result = self.memoria.availNext(result_type)
                quad = directorios.Cuadruplo(self.newQuad(), operator, left_operand, right_operand, result)
                self.cuadruplos.append(quad)
                self.pilaO.append(result)
                self.pilaTipos.append("bool")
            else:
                errores.errorTypeMismatch(left_operand_type, right_operand_type, operator)

    # COND1
    # Punto neuralgico que rellena el cuadruplo de GOTO para expresiones con else 
    # y GOTOF para condiciones sin
    def cond1(self, tree):
        end = self.pilaSaltos.pop()
        self.fillQuad(end, self.quadCounter)

    # NP COND1
    def np_cond1(self, tree):
        end = self.pilaSaltos.pop()
        self.fillQuad(end, self.quadCounter)

    # NP ELSE
    # Punto neuralgico que genera el cuadruplo GOTO y rellena el GOTOF
    def np_else(self, tree):
        quad = directorios.Cuadruplo(self.newQuad(), "GOTO", "", "", "FILL")
        self.cuadruplos.append(quad)
        false = self.pilaSaltos.pop()
        self.pilaSaltos.append(self.quadCounter)
        self.fillQuad(false, self.quadCounter)

    # CICLO
    # Punto neuralgico que agrega la condicion a la pila de saltos para regresar en el estatuto while
    def ciclo(self, tree):
        self.pilaSaltos.append(self.quadCounter + 1)

    # NP CICLO
    # Punto neuralgico que revisa la condicion y genera el cuadruplo GOTOF
    def np_ciclo(self, tree):
        exp = self.pilaO.pop()
        exp_type = self.pilaTipos.pop()
        # Se revisa que la condicion sea de tipo booleano
        if (exp_type != "bool" and exp_type != "CTEBOOL"):
            # Error de mismatch de tipos
            errores.errorCondTypeMismatch(exp_type)
        else:
            # Se crea el cuadruplo GOTOF y se agrega el numero de cuadruplo a la pila de saltos para ser llenado posteriormente
            quad = directorios.Cuadruplo(self.newQuad(), "GOTOF", exp, "", "FILL")
            self.cuadruplos.append(quad)
            self.pilaSaltos.append(self.quadCounter)

    # NP CICLO END
    # Punto neuralgico que genera el cuadruplo para regresar a la condicion
    def np_ciclo_end(self, tree):
        end = self.pilaSaltos.pop()
        returnQuad = self.pilaSaltos.pop()
        # Genera cuadruplo para dar instruccion de regresar y volver a revisar la condicion
        quad = directorios.Cuadruplo(self.newQuad(), "GOTO","", "", returnQuad - 1)
        self.cuadruplos.append(quad)
        # Se llena el GOTOF
        self.fillQuad(end, self.quadCounter)

    # LLAMADA FUNC
    # Punto neuralgico que genera el cuadruplo de ERA para la llamada de una funcion
    def llamadafunc(self, tree):
        id = tree.children[0].value
        # Se verifica la existencia del procedimiento en el Directorio de Procedimientos
        proc = self.directorioProcedimientos.searchProc(id)
        # Se establece el proceso actual para auxiliar en la llamada
        self.procActual = proc
        # Se genera el cuadruplo ERA con los numeros correspondientes al numero de parametros, numero de variables, y numero de temporales
        quad = directorios.Cuadruplo(self.newQuad(), "ERA", proc.numParams, proc.numVars, proc.numTemps)
        self.cuadruplos.append(quad)
        # Se reestablece el numero k para la verificacion de parametros
        self.k = 0

    # NP RETURN LLAM
    #Punto neuralgico que genera el cuadruplo IGUAL para la asignacion de valor de una funcion con retorno
    def np_returnllam(self, tree):
        left_operand = self.pilaO.pop()
        tipo = self.pilaTipos.pop()
        # Se obtiene el siguiente temporal de acuerdo al tipo
        right_operand = self.memoria.availNext(tipo)
        self.pilaO.append(right_operand)
        self.pilaTipos.append(tipo)
        # Se genera el cuadruplo de aisgnacion
        quad = directorios.Cuadruplo(self.newQuad(), "IGUAL", left_operand, "", right_operand)
        self.cuadruplos.append(quad)

    # NP LLAM
    # Punto neuralgico que registra los parametros para una funcion
    def np_llam(self, tree):
        try:
            # Revisamos si es posible acceder al parametro numero k en la tabla de parametros de la funcion
            self.procActual.parameterTable[self.k]
        except:
            # Si la tabla de parametros no esta vacia, y se ocasiono un error, se han enviado mas parametros d elos declarados
            if len(self.procActual.parameterTable) > 0:
                errores.errorNumParams(self.k + 1, len(self.procActual.parameterTable), self.procActual.nombre)
        else:
            # Si no hay error, se prosigue con comparar los tipos entre los argumentos enviados y los parametros declarados
            argumento = self.pilaO.pop()
            argumento_type = self.pilaTipos.pop()
            parametro_type = self.procActual.parameterTable[self.k]
            if(argumento_type == parametro_type):
                # Si coinciden, se genera el cuadruplo de asignacion de parametro
                quad = directorios.Cuadruplo(self.newQuad(), "PARAMETER", argumento, "", "param" + str(self.k + 1))
                self.cuadruplos.append(quad)
            else:
                # Si no coinciden, hay error
                errores.errorParamTypeMismatch(argumento_type, parametro_type, self.procActual.nombre )
        # Se aumenta la cantidad de parametros
        self.k += 1

    # NP LLAM SUB
    # Al finalizar la declaracion de parametros se genera el cuadruplo GOSUB
    def np_llamsub(self, tree):
        # Se compara la cantidad de argumentos enviados con los parametros definidos
        if self.k == len(self.procActual.parameterTable):
            quad = directorios.Cuadruplo(self.newQuad(), "GOSUB", self.procActual.nombre, "" , self.procActual.quadruple - 1)
            self.cuadruplos.append(quad)
        else:
            # Si no coincide hay error
            errores.errorNumParams(self.k, len(self.procActual.parameterTable), self.procActual.nombre)
        # Se elimina el fondo falso 
        self.pOper.pop()
        # Se reestablece los valores de k y el procedimiento actual para una siguiente llamada de funcion
        self.k = 0
        self.procActual = None

    # ARR DEC
    # Punto neuralgico que maneja la declaracion de un arreglo
    def arrdec(self, tree):
        try:
            tree.children[0]
        except:
            next
        else:
            # NP 1
            # Se agrega el arreglo a la tabla de variables
            tipo = tree.children[0].children[0].value
            id = tree.children[1].value
            var = directorios.Variable(id, tipo)
            var.virtualAddress = self.memoria.virtualAddress(tipo)
            self.currProc().tablaVariables.addVar(var)
            self.pilaO.append(id)
            self.pilaTipos.append(tipo)
            # NP 2
            # Se establece que el ID es un arreglo
            var.isArray = True
            # NP 3
            # Se agrega un nuevo nodo para guardar información de las dimensiones
            node = directorios.NodoArreglo(1, 1)
            self.r = 1
            var = self.currProc().tablaVariables.searchVar(self.pilaO[-1])
            var.nodosArreglo.append(node)

    # ARR SIZE
    # Punto neuralgico que registra los limites superiores de las dimensiones y hace el calculo de R
    def arrsize(self, tree):
        var = self.currProc().tablaVariables.searchVar(self.pilaO[-1])
        # NP 4 y 5
        # Se guarda el limite superior
        var.nodosArreglo[-1].ls = tree.children[0].value
        # Se calcula R
        self.r = (int(var.nodosArreglo[-1].ls) + 1) * self.r
        var.nodosArreglo[-1].r = self.r

    # ARR DEC 1
    # Punto neuralgico que cambia de dimension y crea un nuevo nodo
    def arrdec1(self, tree):
        try: tree.children[0]
        except: next
        else:
            if(tree.children[0].value == '['):
                var = self.currProc().tablaVariables.searchVar(self.pilaO[-1])
                # NP 6
                dim = var.nodosArreglo[-1].dim + 1
                node = directorios.NodoArreglo(dim)
                # Se liga el nodo a la variable
                var.nodosArreglo.append(node)

    # ARR DEC FIN
    # Punto neuralgico que hace los calculos de las dimensiones al terminar la declaracion del arreglo
    def arrdecfin(self, tree):
        var = self.currProc().tablaVariables.searchVar(self.pilaO[-1])
        # NP 7
        aux = self.r
        # Empezando en 0 empezamos en el primer nodo de la lista
        for dim in range(len(var.nodosArreglo)):
            # Se repite para todos los nodos
            # Se guarda m en el nodo actual
            var.nodosArreglo[dim].m = int(self.r / (int(var.nodosArreglo[dim].ls) + 1))
            self.r = var.nodosArreglo[dim].m
            # no hay offset porque el limite inferior siempre sera 0
        # NP 8
        # Guarda la direccion virtual del id actual en la Tabla de Variables
        tipo = self.pilaTipos.pop()
        var.virtualAddress = self.memoria.virtualAddress(tipo)
        # Calcula la siguiente direccion virtual 
        self.memoria.updateByArray(tipo, aux)

    # ARR ACC
    # Punto neuralgico que maneja el acceso a un arreglo
    def arracc(self, tree):
        # NP 1
        id = tree.children[0].value
        var = self.searchVar(id)
        # NP 2
        # Se verifica que la variable sea un arreglo
        # y que tenga dimensiones
        if var.isArray == True:
            dim = 1
            self.pilaDim.append([id, dim])
            self.pOper.append("[")
        else:
            errores.erroIDNotArray(id)

    # ARR ACC
    # Punto neuralgico que registra los accesos
    def np_arracc(self, tree):
        id = self.pilaDim[0][0]
        var = self.searchVar(id)
        dim = self.pilaDim[0][1]
        nodo = var.nodosArreglo[dim - 1]

        # NP 3
        # Se rea el cuadruplo para verificar limites
        cteli = directorios.Constante(nodo.li, "int", self.memoria.addressCte("int"))
        ctels = directorios.Constante(nodo.ls, "int", self.memoria.addressCte("int"))
        self.tablaConstantes.addCte(cteli)
        self.tablaConstantes.addCte(ctels)
        quad = directorios.Cuadruplo(self.newQuad(), "VERIFY", nodo.li, nodo.ls, self.pilaO[-1] )
        self.cuadruplos.append(quad)
        try:
            var.nodosArreglo[dim - 1]
        except:
            next
        else:
            if nodo.dim < len(var.nodosArreglo):
                aux = self.pilaO.pop()
                tn = self.memoria.availNext("int")
                ctem = directorios.Constante(nodo.m, "int", self.memoria.addressCte("int"))
                self.tablaConstantes.addCte(ctem)
                quad = directorios.Cuadruplo(self.newQuad(), "*", aux, ctem.virtualAddress, tn)
                self.pilaO.append(tn)
                self.cuadruplos.append(quad)
            if dim > 1:
                aux2 = self.pilaO.pop()
                aux1 = self.pilaO.pop()
                tk = self.memoria.availNext("int")
                quad = directorios.Cuadruplo(self.newQuad(), "+", aux1, aux2, tk)
                self.pilaO.append(tk)
                self.cuadruplos.append(quad)

    # ARRACC1
    def arracc1(self, tree):
        try: tree.children[0]
        except: next
        else:
            if tree.children[0].value == '[':
                self.pilaDim[0][1] += 1
                dim = self.pilaDim[0][1]
                id = self.pilaDim[0][0]
                var = self.searchVar(id)
                nodo = var.nodosArreglo[dim - 1]
                
    # NP ARRACCFIN
    def np_arraccfin(self, tree):
        aux1 = self.pilaO.pop()
        id = self.pilaDim[0][0]
        var = self.searchVar(id)
        tn = self.memoria.availNext("pointer")
        cte = directorios.Constante(var.virtualAddress, "int", self.memoria.addressCte("int"))
        self.tablaConstantes.addCte(cte)
        quad = directorios.Cuadruplo(self.newQuad(), "+", aux1, cte.virtualAddress, tn)
        self.pilaO.append(('(' + str(tn) + ')'))
        self.cuadruplos.append(quad)
        self.pOper.pop()
        self.pilaDim.pop()
        

    # NP END
    # Punto neuralgico que marca el fin del programa
    def np_end(self, tree):
        # Se genera el cuadruplo de fin de programa que indica el final de la ejecucion
        quad = directorios.Cuadruplo(self.newQuad(), "ENDPROG", "", "", "")
        self.cuadruplos.append(quad)
        # Se elimina el directorio de Procedimientos
        del self.directorioProcedimientos
        # Se crea el archivo con el codigo intermedio generado
        self.createObjFile()
        self.tablaConstantes.createCteTable()
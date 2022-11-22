# MAQUINA VIRTUAL
# Proceso de ejecución
#
# GAUSS++
# Nadia Corina Garcia Orozco A01242428
# Noviembre, 2022
import errores
import memoria
import sys

# MAQUINA VIRTUAL
# Clase que maneja la ejecución con base al código intermedio
class MaquinaVirtual():
    def __init__(self):
        self.cuadruplos = []                        # Cuadruplos, lista de cuadruplos rescatados de la generacion de codigo intermedio
        self.ip = 0                                 # Instruction Pointer
        self.instancias = []                        # Arreglo de memorias locales generadas por las instancias de una funcion
        self.pilaProc = []
        self.memGlobalGauss = [None] * 1000         # Arreglo vacio de memoria de variables generales de Gauss globales
        self.varsGlobalesInt = [None] * 1000        # Arreglo vacio de variables enteras globales
        self.varsGlobalesFloat = [None] * 1000      # Arreglo vacio de variables flotantes globales
        self.varsGlobalesString = [None] * 1000     # Arreglo vacio de variables strings globales
        self.varsGlobalesBool = [None] * 1000       # Arreglo vacio de variables booleanas globales
        self.tempsGlobalesInt = [None] * 1000       # Arreglo vacio de temporales enteros globales
        self.tempsGlobalesFloat = [None] * 1000     # Arreglo vacio de temporales flotantes globales
        self.tempsGlobalesString = [None] * 1000    # Arreglo vacio de temporales strings globales
        self.tempsGlobalesBool = [None] * 1000      # Arreglo vacio de temporales booleanos globales
        self.tempsGlobalesPointers = [None] * 1000  # Arreglo vacio de temporales pointers globales
        self.memoria = memoria.MapaDeMemoria()      # Variable memoria auxiliar para el acceso de los limites de memoria 
        self.ctesInt = [None] * 1000                # Arreglo vacio de constantes enteras para el programa
        self.ctesFloat = [None] * 1000              # Arreglo vacio de constantes flotantes para el programa
        self.ctesString = [None] * 1000             # Arreglo vacio de constantes string para el programa
        self.ctesBool = [None] * 1000               # Arreglo vacio de constantes booleanas para el programa

    # INDEX
    # Funcion auxiliar que indexa los valores de las variables en la memoria global
    def index(self, dir, result):
        dir = int(dir)
        # Variables globales generales del programa Gauss 
        if dir >= self.memoria.varsGauss and dir < self.memoria.varGlobalesInt:
            self.memGlobalGauss[dir] = result
        # Variables globales tipadas de tipo entero
        elif dir >= self.memoria.varGlobalesInt and dir < self.memoria.varGlobalesFloat:
            self.varsGlobalesInt[dir - self.memoria.varGlobalesInt] = result
        # Variables globales tipadas de tipo flotante
        elif dir >= self.memoria.varGlobalesFloat and dir < self.memoria.varGlobalesString:
            self.varsGlobalesFloat[dir - self.memoria.varGlobalesFloat] = result
        # Variables globales tipadas de tipo string
        elif dir >= self.memoria.varGlobalesString and dir < self.memoria.varGlobalesBool:
            self.varsGlobalesString[dir - self.memoria.varGlobalesString] = result
        # Variables globales tipadas de tipo bool
        elif dir >= self.memoria.varGlobalesBool and dir < self.memoria.tempsGlobalesInt:
            self.varsGlobalesBool[dir - self.memoria.varGlobalesBool] = result
        # Temporales globales tipados de tipo entero 
        elif dir >= self.memoria.tempsGlobalesInt and dir < self.memoria.tempsGlobalesFloat:
            self.tempsGlobalesInt[dir - self.memoria.tempsGlobalesInt] = result
        # Temporales globales tipados de tipo flotante
        elif dir >= self.memoria.tempsGlobalesFloat and dir < self.memoria.tempsGlobalesString:
            self.tempsGlobalesFloat[dir - self.memoria.tempsGlobalesFloat] = result
        # Temporales globales tipados de tipo string
        elif dir >= self.memoria.tempsGlobalesString and dir < self.memoria.tempsGlobalesBool:
            self.tempsGlobalesString[dir - self.memoria.tempsGlobalesString] = result
        # Temporales globales tipados de tipo bool
        elif dir >= self.memoria.tempsGlobalesBool and dir < self.memoria.varLocalesInt:
            self.tempsGlobalesBool[dir - self.memoria.tempsGlobalesBool] = result
        # Si el valor es mayor, es una variable local y hay que indexar en su determinada instancia
        else:
            self.instancias[-1].index(dir, result)

    # VALUE
    # Funcion auxiliar que indexa los valores de las variables en la memoria global
    def getValue(self, dir):
        dir = int(dir)
        # Variables globales generales del programa Gauss 
        if dir >= self.memoria.varsGauss and dir < self.memoria.varGlobalesInt:
            return self.memGlobalGauss[dir] 
        # Variables globales tipadas de tipo entero
        elif dir >= self.memoria.varGlobalesInt and dir < self.memoria.varGlobalesFloat:
            return int(self.varsGlobalesInt[dir - self.memoria.varGlobalesInt])
        # Variables globales tipadas de tipo flotante
        elif dir >= self.memoria.varGlobalesFloat and dir < self.memoria.varGlobalesString:
            return float(self.varsGlobalesFloat[dir - self.memoria.varGlobalesFloat])
        # Variables globales tipadas de tipo string
        elif dir >= self.memoria.varGlobalesString and dir < self.memoria.varGlobalesBool:
            return self.varsGlobalesString[dir - self.memoria.varGlobalesString]
        # Variables globales tipadas de tipo bool
        elif dir >= self.memoria.varGlobalesBool and dir < self.memoria.tempsGlobalesInt:
            return self.varsGlobalesBool[dir - self.memoria.varGlobalesBool] 
        # Temporales globales tipados de tipo entero 
        elif dir >= self.memoria.tempsGlobalesInt and dir < self.memoria.tempsGlobalesFloat:
            return int(self.tempsGlobalesInt[dir - self.memoria.tempsGlobalesInt])
        # Temporales globales tipados de tipo flotante
        elif dir >= self.memoria.tempsGlobalesFloat and dir < self.memoria.tempsGlobalesString:
            return float(self.tempsGlobalesFloat[dir - self.memoria.tempsGlobalesFloat])
        # Temporales globales tipados de tipo string
        elif dir >= self.memoria.tempsGlobalesString and dir < self.memoria.tempsGlobalesBool:
            return self.tempsGlobalesString[dir - self.memoria.tempsGlobalesString]
        # Temporales globales tipados de tipo bool
        elif dir >= self.memoria.tempsGlobalesBool and dir < self.memoria.varLocalesInt:
            return self.tempsGlobalesBool[dir - self.memoria.tempsGlobalesBool]
        # Constantes de tipo entero
        elif dir >= self.memoria.ctesInt and dir < self.memoria.ctesFloat:
            return int(self.ctesInt[dir - self.memoria.ctesInt])
        # Constantes de tipo flotante
        elif dir >= self.memoria.ctesFloat and dir < self.memoria.ctesString:
            return float(self.ctesFloat[dir - self.memoria.ctesFloat])
        # Constantes de tipo string
        elif dir >= self.memoria.ctesString and dir < self.memoria.ctesBool:
            return self.ctesString[dir - self.memoria.ctesString]
        # Constantes de tipo bool
        elif dir >= self.memoria.ctesBool and dir < (self.memoria.ctesBool + 2000):
            return self.ctesBool[dir - self.memoria.ctesBool]
        # Si el valor es mayor, es una variable local y hay que indexar en su determinada instancia
        else:
            return self.instancias[-1].getValue(dir)
    
    # EJECUTAR
    # Funcion que maneja la ejecucion
    def ejecutar(self):
        # Se inicia la ejecución en el primer cuádruplo 
        op = self.cuadruplos[0][0]
        while op != "ENDPROG":
            # print(self.ip, op)
            left_operand = self.cuadruplos[self.ip][1]
            right_operand = self.cuadruplos[self.ip][2]
            result = self.cuadruplos[self.ip][3]

            # OPERACION PROGRAM
            # Indica que se ha iniciado la ejecucion del programa
            if op == "PROGRAM":
                print("Se inicia la ejecución del programa", result)
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION GOTO 
            # Cambia el Instruction Pointer al cuadruplo señalado
            elif op == "GOTO":
                self.ip = int(self.cuadruplos[self.ip][3])

            # OPERACION INFO
            # Registra las variables informativas para el preograma Gauss
            elif op == "INFO":
                # Indexa las variables de tipo arreglo en la memoria global
                if right_operand != "":
                    self.index(int(result) + int(right_operand), left_operand)
                    # self.memGlobalGauss[int(result) - 5000 + int(right_operand)] = left_operand
                # Indexa el resto de las variables en la memoria gloabl
                else:
                    self.index(int(result), left_operand)
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION = 
            elif op == "=":
                self.index(int(result), self.getValue(left_operand))
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION +
            elif op == "+":
                try: self.getValue(left_operand) + self.getValue(right_operand)
                except TypeError:
                    res = str(self.getValue(left_operand)).strip('"') + str(self.getValue(right_operand)).strip('"')
                else:
                    res = self.getValue(left_operand) + self.getValue(right_operand)
                self.index(result, res)
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION -
            elif op == "-":
                res = self.getValue(left_operand) - self.getValue(right_operand)
                self.index(result, res)
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION *
            elif op == "*":
                res = self.getValue(left_operand) * self.getValue(right_operand)
                self.index(result, res)
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION /
            elif op == "/":
                if self.getValue(right_operand) == 0 or self.getValue(right_operand) == 0.0:
                    return errores.errorDivZero()
                else:
                    res = self.getValue(left_operand) / self.getValue(right_operand)
                    self.index(result, res)
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION >
            elif op == ">":
                res = self.getValue(left_operand) > self.getValue(right_operand)
                self.index(result, res)
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION <
            elif op == "<":
                res = self.getValue(left_operand) < self.getValue(right_operand)
                self.index(result, res)
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION <=
            elif op == "<=":
                res = self.getValue(left_operand) <= self.getValue(right_operand)
                self.index(result, res)
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION >=
            elif op == ">=":
                res = self.getValue(left_operand) >= self.getValue(right_operand)
                self.index(result, res)
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION !=
            elif op == "!=":
                res = self.getValue(left_operand) != self.getValue(right_operand)
                self.index(result, res)
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION ==
            elif op == "==":
                res = self.getValue(left_operand) == self.getValue(right_operand)
                self.index(result, res)
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION and
            elif op == "AND":
                res = self.getValue(left_operand) and self.getValue(right_operand)
                self.index(result, res)
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION OR
            elif op == "OR":
                res = self.getValue(left_operand) or self.getValue(right_operand)
                self.index(result, res)
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION GOTOF
            elif op == "GOTOF":
                # Si la condicion evalua en Verdadero, se continua con el siguiente cuadruplo
                if (self.getValue(left_operand) == 'True' or self.getValue(left_operand) == True):
                    # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                    self.ip += 1
                # Si la condicion evalua en Falso se cambia el IP al cuadruplo especificado
                else:
                    self.ip = int(result)

            # OPERACION PRINT
            elif op == "PRINT" :
                print(self.getValue(result))
                self.ip += 1

            # OPERACION RETURN
            elif op == "RETURN":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION ENDFUNC
            elif op == "ENDFUNC":
                instancia = self.instancias.pop()
                del instancia
                # Se cambia el IP al cuadruplo en el que nos habiamos quedado y se incrementa en uno para pasar al siguiente 
                self.ip = (self.pilaProc.pop() + 1)

            # OPERACION VERIFY
            elif op == "VERIFY":
                if int(left_operand) >= 0 and int(right_operand) <= int(result):
                    # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                    self.ip += 1
                else:
                    errores.errorLimits(str(result))
            
            # OPERACION MAIN
            elif op == "MAIN":
                instancia = memoria.MemoriaLocal()
                self.instancias.append(instancia)
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION ERA
            elif op == "ERA":
                instancia = memoria.MemoriaLocal()
                self.instancias.append(instancia)
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION PARAMETER
            elif op == "PARAMETER":
                param = int(result.strip("param"))
                if int(left_operand) >= self.memoria.ctesInt:
                    self.index(self.tipoCte(left_operand) + param - 1, self.getValue(left_operand))
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION GOSUB
            elif op == "GOSUB":
                # Se guarda el cuadruplo actual
                self.pilaProc.append(self.ip)
                # Se cambia el IP al cuadruplo inicial de la funcion especificada
                self.ip = int(result)

            # OPERACION AREA
            elif op == "AREA":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION PRINTP
            elif op == "PRINTP":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1
            
            # OPERACION EXPR
            elif op == "EXPR":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION OPCIONES
            elif op == "OPCIONES":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION RESPUESTA
            elif op == "RESPUESTA":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION LISTA
            elif op == "LISTA":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION GENERA
            elif op == "GENERA":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION READ
            elif op == "READ":
                x = input()
                # Se indexa el valor leido en la memoria
                self.index(result, x)
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            else:
                message = "Operador no reconocido " + op
                sys.exit(message)

            # Cambiamos a la siguiente instruccion
            op = self.cuadruplos[self.ip][0]
    
    # CARGA CTES
    # Funcion auxiliar que carga el archivo de la Tabla de Constantes a la Maquina Virtual
    def cargaCtes(self, line):
        # Generamos el arreglo para ser accesado
        linea = line.strip('\n').split('@')
        # Direccion virtual de la constante
        dir = int(linea[0])
        # Se indexa la constante en su respectivo espacio de acuerdo a su tipo
        # Constantes de tipo entero
        if(dir >= self.memoria.ctesInt and dir < self.memoria.ctesFloat):
            self.ctesInt[dir - self.memoria.ctesInt] = int(linea[1].strip('"'))
        # Constantes de tipo flotante
        elif(dir >= self.memoria.ctesFloat and dir < self.memoria.ctesString):
            self.ctesFloat[dir - self.memoria.ctesFloat] = float(linea[1].strip('"'))
        # Constantes de tipo string
        elif(dir >= self.memoria.ctesString and dir < self.memoria.ctesBool):
            self.ctesString[dir - self.memoria.ctesString] = linea[1].strip('"')
        # Constantes de tipo bool
        elif(dir >= self.memoria.ctesBool and dir < (self.memoria.ctesBool + 1000)):
            if linea[1].strip('"') == 'True':
                self.ctesBool[dir - self.memoria.ctesBool] = True
            elif linea[1].strip('"') == 'False':
                self.ctesBool[dir - self.memoria.ctesBool] = False

    def tipoCte(self, dir):
        dir = int(dir)
        # Constantes de tipo entero
        if(dir >= self.memoria.ctesInt and dir < self.memoria.ctesFloat):
            return self.memoria.varLocalesInt
        # Constantes de tipo flotante
        elif(dir >= self.memoria.ctesFloat and dir < self.memoria.ctesString):
            return self.memoria.varLocalesFloat
        # Constantes de tipo string
        elif(dir >= self.memoria.ctesString and dir < self.memoria.ctesBool):
            return self.memoria.varLocalesString
        # Constantes de tipo bool
        elif(dir >= self.memoria.ctesBool and dir < (self.memoria.ctesBool + 1000)):
            return self.memoria.varLocalesBool
# MAIN
# Punto de entrada a la maquina virtual
def main():
    # Se trata de abrir el archivo con el codigo intermedio generado
    try:
        fp = open("obj", 'r', encoding='latin-1')
        fp.close()
    except FileNotFoundError:
        errores.errorFileNotFound("Codigo intermedio")

    # Se verifica que se pueda abrir el archivo de la tabla de constantes
    try:
        fCte = open("ctetable", 'r', encoding='latin-1')
        fCte.close()
    except FileNotFoundError:
        errores.errorFileNotFound("Tabla de Constantes")

    with open('obj', 'r', encoding='latin-1') as fp:
        # Se crea una instancia de la maquina virtual
        maquinaVirtual = MaquinaVirtual()
        # Se lee la primer linea del archivo
        line = fp.readline()
        # Se itera el archivo hasta que se llegue al final (EOF)
        while line != '':
            # Se cargan los cuadruplos a la maquina virtual
            maquinaVirtual.cuadruplos.append(line.strip('\n').split(', '))
            line = fp.readline()  

        with open('ctetable', 'r', encoding='utf-8') as fCte:
            # Se lee la primer linea del archivo
            line = fCte.readline()
            # Se itera el archivo hasta que se llegue al final (EOF)
            while line != '':
                # Se cargan las constantes a la maquina virtual
                maquinaVirtual.cargaCtes(line)
                line = fCte.readline()  
        # Se lleva a cabo el proceso de ejecucion  
        maquinaVirtual.ejecutar()
    
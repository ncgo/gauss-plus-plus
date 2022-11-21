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
        self.cuadruplos = []    # Cuadruplos, lista de cuadruplos rescatados de la generacion de codigo intermedio
        self.ip = 0             # Instruction Pointer
        self.instancias = []
        self.memGlobalGauss = [None] * 1000
        self.varsGlobalesInt = [None] * 1000
        self.varsGlobalesFloat = [None] * 1000
        self.varsGlobalesString = [None] * 1000
        self.varsGlobalesBool = [None] * 1000
        self.tempsGlobalesInt = [None] * 1000
        self.tempsGlobalesFloat = [None] * 1000
        self.tempsGlobalesString = [None] * 1000
        self.tempsGlobalesBool = [None] * 1000
        self.tempsGlobalesPointers = [None] * 1000
        self.memoria = memoria.MapaDeMemoria()
        self.ctesInt = [None] * 1000
        self.ctesFloat = [None] * 1000
        self.ctesString = [None] * 1000
        self.ctesBool = [None] * 1000

    def index(self, dir, result):
        if dir >= self.memoria.varsGauss and dir < self.memoria.varGlobalesInt:
            self.memGlobalGauss[dir] = result
        elif dir >= self.memoria.varGlobalesInt and dir < self.memoria.varGlobalesFloat:
            self.varsGlobalesInt[dir - self.memoria.varGlobalesInt] = result
        elif dir >= self.memoria.varGlobalesFloat and dir < self.memoria.varGlobalesString:
            self.varsGlobalesFloat[dir - self.memoria.varGlobalesFloat] = result
        elif dir >= self.memoria.varGlobalesString and dir < self.memoria.varGlobalesBool:
            self.varsGlobalesString[dir - self.memoria.varGlobalesString] = result
        elif dir >= self.memoria.varGlobalesBool and dir < self.memoria.tempsGlobalesInt:
            self.varsGlobalesBool[dir - self.memoria.varGlobalesBool] = result
        elif dir >= self.memoria.tempsGlobalesInt and dir < self.memoria.tempsGlobalesFloat:
            self.tempsGlobalesInt[dir - self.memoria.tempsGlobalesInt] = result
        elif dir >= self.memoria.tempsGlobalesFloat and dir < self.memoria.tempsGlobalesString:
            self.tempsGlobalesFloat[dir - self.memoria.tempsGlobalesFloat] = result
        elif dir >= self.memoria.tempsGlobalesString and dir < self.memoria.tempsGlobalesBool:
            self.tempsGlobalesString[dir - self.memoria.tempsGlobalesString] = result
        elif dir >= self.memoria.tempsGlobalesBool and dir < self.memoria.varLocalesInt:
            self.tempsGlobalesBool[dir - self.memoria.tempsGlobalesBool] = result
        else:
            self.instancias[-1].index(dir, result)
    
    # EJECUTAR
    # Funcion que maneja la ejecucion
    def ejecutar(self):
        # Se inicia la ejecución en el primer cuádruplo 
        op = self.cuadruplos[0][0]
        while op != "ENDPROG":
            left_operand = self.cuadruplos[self.ip][1]
            right_operand = self.cuadruplos[self.ip][2]
            result = self.cuadruplos[self.ip][3]

            print(op, self.ip, left_operand, right_operand, result)
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
                self.index(int(result), left_operand)
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION +
            elif op == "+":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION -
            elif op == "-":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION *
            elif op == "*":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION /
            elif op == "/":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION >
            elif op == ">":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION <
            elif op == "<":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION <=
            elif op == "<=":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION >=
            elif op == ">=":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION !=
            elif op == "!=":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION ==
            elif op == "==":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION GOTOF
            elif op == "GOTOF":
                if (True):
                    self.ip = int(result)
                else:
                    # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                    self.ip += 1

            # OPERACION PRINT
            elif op == "PRINT":
                print(result)
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION RETURN
            elif op == "RETURN":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION ENDFUNC
            elif op == "ENDFUNC":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION VERIFY
            elif op == "VERIFY":
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
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            # OPERACION GOSUB
            elif op == "GOSUB":
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
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
                # Se incrementa el IP en uno para pasar al siguiente cuadruplo
                self.ip += 1

            else:
                sys.exit(op)

            op = self.cuadruplos[self.ip][0]
    
    def cargaCtes(self, line):
        linea = line.strip('\n').split('@')
        dir = int(linea[0])
        if(dir >= self.memoria.ctesInt and dir < self.memoria.ctesFloat):
            self.ctesInt[dir - self.memoria.ctesInt] = int(linea[1].strip('"'))
        elif(dir >= self.memoria.ctesFloat and dir < self.memoria.ctesString):
            self.ctesFloat[dir - self.memoria.ctesFloat] = float(linea[1].strip('"'))
        elif(dir >= self.memoria.ctesString and dir < self.memoria.ctesBool):
            self.ctesString[dir - self.memoria.ctesString] = linea[1]
        elif(dir >= self.memoria.ctesBool and dir < (self.memoria.ctesBool + 1000)):
            self.ctesBool[dir - self.memoria.ctesBool] = linea[1].strip('"')
        

# MAIN
def main():
    try:
        fp = open("ctetable", 'r', encoding='latin-1')
        fp.close()
    except FileNotFoundError:
        errores.errorFileNotFound()

    # Se trata de abrir el archivo con el codigo intermedio generado
    try:
        fCte = open("obj", 'r', encoding='latin-1')
        fCte.close()
    except FileNotFoundError:
        errores.errorFileNotFound()

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
                # Se cargan los cuadruplos a la maquina virtual
                maquinaVirtual.cargaCtes(line)
                line = fCte.readline()  
        print(maquinaVirtual.ctesInt[0:10])
        print(maquinaVirtual.ctesFloat[0:10])
        print(maquinaVirtual.ctesString[0:30])
        print(maquinaVirtual.ctesBool[0:10])
        # Se lleva a cabo el proceso de ejecucion  
        # maquinaVirtual.ejecutar()
    
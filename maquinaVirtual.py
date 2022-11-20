# MAQUINA VIRTUAL
# Proceso de ejecución
#
# GAUSS++
# Nadia Corina Garcia Orozco A01242428
# Noviembre, 2022
import errores

# MAQUINA VIRTUAL
# Clase que maneja la ejecución con base al código intermedio
class MaquinaVirtual():
    def __init__(self):
        self.cuadruplos = []    # Cuadruplos, lista de cuadruplos rescatados de la generacion de codigo intermedio
        self.ip = 0             # Instruction Pointer

    # EJECUTAR
    # Funcion que maneja la ejecucion
    def ejecutar(self):
        # Se inicia la ejecución en el primer cuádruplo 
        op = self.cuadruplos[0][0]
        while op != "ENDPROG":
            if op == "PROGRAM":
                self.ip += 1
            elif op == "GOTO":
                self.ip = int(self.cuadruplos[self.ip][3])
            elif op == "INFO":
                self.ip += 1
            elif op == "=":
                self.ip += 1
            elif op == "+":
                self.ip += 1
            elif op == "-":
                self.ip += 1
            elif op == "*":
                self.ip += 1
            elif op == "/":
                self.ip += 1
            else:
                op = "ENDPROG"
                self.ip = 52

            op = self.cuadruplos[self.ip][0]

# MAIN
def main():
    # Se trata de abrir el archivo con el codigo intermedio generado
    try:
        fp = open("obj", 'r', encoding='latin-1')
        fp.close()
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
        # Se lleva a cabo el proceso de ejecucion  
        maquinaVirtual.ejecutar()
    
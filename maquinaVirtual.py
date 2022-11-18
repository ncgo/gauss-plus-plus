class MaquinaVirtual():
    def __init__(self):
        self.cuadruplos = []
        self.ip = 0

    def ejecutar(self):
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


def main():
    try:
        fp = open("obj", 'r', encoding='utf-8')
        fp.close()
    except FileNotFoundError:
        print("Archivo no encontrado")

    with open('obj', 'r', encoding='latin-1') as fp:
        maquinaVirtual = MaquinaVirtual()
        # Read the first line
        line = fp.readline()
        # Iterate the file till it reached the EOF
        while line != '':
            maquinaVirtual.cuadruplos.append(line.strip('\n').split(', '))
            line = fp.readline()    
        maquinaVirtual.ejecutar()
    
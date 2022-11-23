# GAUSS++
# Nadia Corina Garcia Orozco A01242428
# Noviembre, 2022

from lark import Lark, Visitor
import puntosNeuralgicos
import maquinaVirtual
import errores
import os

def loadCode():
    res = []
    for path in os.listdir("./code"):
        if os.path.isfile(os.path.join("./code", path)):
            name = path.split(".gauss")
            res.append(name[0])
    print("Archivos de codigo disponibles", res)
            
# Se genera el parser de la gramática
parser = Lark(open("grammar", 'r').read())
loadCode()
#x = input("Escoje el codigo a ejecutar: ")
x = 'factorial_recusivo'
# Se parsea el código recibido
try: open("code/" + x + ".gauss",'r')
except:
    errores.errorCodeNotFound(x)
else:
    tree = parser.parse(open("code/" + x + ".gauss",'r').read())
# Se escanea el aárbol y se ejecutan las acciones semánticas pertinentes
# Se genera el código intermedio
puntosNeuralgicos.PuntosNeuralgicos().visit_topdown(tree)
# El código intermedio es ejecutado por la máquina virtual
maquinaVirtual.main()
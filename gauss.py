# GAUSS++
# Nadia Corina Garcia Orozco A01242428
# Noviembre, 2022

from lark import Lark, Visitor
import puntosNeuralgicos
import maquinaVirtual

# Se genera el parser de la gramática
parser = Lark(open("grammar", 'r').read())
# Se parsea el código recibido
tree = parser.parse(open("code/test1",'r').read())
# Se escanea el aárbol y se ejecutan las acciones semánticas pertinentes
# Se genera el código intermedio
puntosNeuralgicos.PuntosNeuralgicos().visit_topdown(tree)
# El código intermedio es ejecutado por la máquina virtual
maquinaVirtual.main()

from lark import Lark, Visitor
import puntosNeuralgicos
import maquinaVirtual
parser = Lark(open("grammar", 'r').read())
tree = parser.parse(open("code/test1",'r').read())
puntosNeuralgicos.PuntosNeuralgicos().visit_topdown(tree)
maquinaVirtual.main()

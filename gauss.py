from lark import Lark, Visitor
import puntosNeuralgicos
parser = Lark(open("grammar", 'r').read())
tree = parser.parse(open("code/test1",'r').read())
print(tree)
puntosNeuralgicos.PuntosNeuralgicos().visit_topdown(tree)



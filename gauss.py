from lark import Lark, Visitor
parser = Lark(open("grammar", 'r').read())
parser.parse(open("code/test1",'r').read())

class PuntosNeuralgicos(Visitor):
    def program(self, tree):
        print("inicio")
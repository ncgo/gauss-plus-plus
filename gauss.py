from lark import Lark
parser = Lark(open("grammar", 'r').read())

print(parser.parse(open("test1",'r').read()))


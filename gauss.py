from lark import Lark
parser = Lark(open("grammar", 'r').read())

parser.parse(open("sample",'r').read())
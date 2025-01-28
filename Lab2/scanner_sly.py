import sys
from sly import Lexer


class Scanner(Lexer):
    literals = {'+', '-', '*', '/', "=", ";", ":", ",", "(", ")", "'", "{", "}", "[", "]"}

    tokens = [
        # Matrix binary operators
        DOTPLUS, DOTMINUS, DOTTIMES, DOTDIVIDE,
        # Assign operators
        PLUSASSIGN, MINUSASSIGN, TIMESASSIGN, DIVIDEASSIGN,
        # Relation operators
        LT, GT, LE, GE, NE, EQ,
        # Keywords
        IF, ELSE, FOR, WHILE,
        BREAK, CONTINUE, RETURN,
        EYE, ZEROS, ONES,
        PRINT,
        # IDs, numbers and string
        ID, INT, FLOAT, STRING  
    ]

    ignore = ' \t'

    @_(r'#.*')
    def ignore_comment(self, t):
        pass

    DOTPLUS = r'\.\+'
    DOTMINUS = r'\.-'
    DOTTIMES = r'\.\*'
    DOTDIVIDE = r'\./'
    PLUSASSIGN = r'\+='
    MINUSASSIGN = r'-='
    TIMESASSIGN = r'\*='
    DIVIDEASSIGN = r'/='
    LE = r'<='
    GE = r'>='
    NE = r'!='
    EQ = r'=='
    LT = r'<'
    GT = r'>'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    ID['if'] = IF
    ID['else'] = ELSE
    ID['for'] = FOR
    ID['while'] = WHILE
    ID['BREAK'] = BREAK
    ID['CONTINUE'] = CONTINUE
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID['return'] = RETURN
    ID['eye'] = EYE
    ID['zeros'] = ZEROS
    ID['ones'] = ONES
    ID['print'] = PRINT


    FLOAT = r'(([0-9]+\.[0-9]*)|(\.[0-9]+))([eE][-+]?[0-9]+)?|\d+([eE][-+]?[0-9]+)'
    INT = r'\d+'
    STRING = r'\".*?\"'
   
    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f'Incorrect sign: {t.value[0]} in line: {self.lineno}')
        self.index += 1
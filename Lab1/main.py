import sys
from sly import Lexer


class Scanner(Lexer):
    literals = {
        '+', '-', '*', '/',
        "=", ";", ":", ",",
        "(", ")", "{", "}",
        "[", "]", "'"
    }

    ignore = ' \t'
    ignore_comment = r'\#.*'

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
        UMINUS,
        # IDs, numbers and string
        ID, FLOATNUM, INTNUM, STRING
    ]

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

    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def ID(self, t):
        t.value = str(t.value)
        return t

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE
    ID['for'] = FOR
    ID['while'] = WHILE
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID['return'] = RETURN
    ID['eye'] = EYE
    ID['zeros'] = ZEROS
    ID['ones'] = ONES
    ID['print'] = PRINT

    # FLOAT = r'(([0-9]+\.[0-9]*)|(\.[0-9]+))([eE][-+]?[0-9]+)?|\d+([eE][-+]?[0-9]+)'
    # INTNUM = r'\d+'
    # STRING = r'\".*?\"'

    @_(r'\".*?\"')
    def STRING(self, t):
        t.value = str(t.value)
        t.value = t.value[1:-1].replace('\\"', '"')
        return t


    @_(r'(([0-9]+\.[0-9]*)|(\.[0-9]+))([eE][-+]?[0-9]+)?|\d+([eE][-+]?[0-9]+)')
    def FLOATNUM(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INTNUM(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f'Incorrect sign: {t.value[0]} in line: {self.lineno}')
        self.index += 1


if __name__ == "__main__":
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "testing_strings_and_keywords.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()

    for tok in lexer.tokenize(text):
        print(tok)

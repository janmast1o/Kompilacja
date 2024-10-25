import sys
from sly import Lexer


class Scanner(Lexer):

    tokens = {
        LE, GE, LT, GT, NE, EQ, # compare operators
        ASSIGN, PLUSASSIGN, MINUSASSIGN, TIMESASSIGN, DIVIDEASSIGN, # assign operators
        DOTPLUS, DOTMINUS, DOTTIMES, DOTDIVIDE, # dot operators
        RANGE, TRANSPOSE, COMMA, SEMICOLON, # other
        ID, # ids
        IF, ELSE, FOR, WHILE, BREAK, CONTINUE, RETURN, EYE, ZEROS, ONES, PRINT, TRUE, FALSE, IN, FUNCTION,  # keywords
        FLOAT, INT, STRING,  # explicit value declarations
    }

    literals = {'+', '-', '*', '/', '(', ')', '{', '}', '[', ']'}

    # Ignored
    ignore = ' \t'
    ignore_comment = r'\#.*'

    # compare operators
    LE = r'<='
    GE = r'>='
    LT = r'<'
    GT = r'>'
    NE = r'!='
    EQ = r'=='

    # assign operators
    ASSIGN = r'='
    PLUSASSIGN = r'\+='
    MINUSASSIGN = r'-='
    TIMESASSIGN = r'\*='
    DIVIDEASSIGN = r'/='

    # dot operators
    DOTPLUS = r'\.\+'
    DOTMINUS = r'\.-'
    DOTTIMES = r'\.\*'
    DOTDIVIDE = r'\./'

    # other
    RANGE = r':'
    TRANSPOSE = r'\''
    COMMA = r','
    SEMICOLON = r';'

    # ids and keywords
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
    ID['true'] = TRUE
    ID['false'] = FALSE
    ID['in'] = IN
    ID['function'] = FUNCTION

    # explicit value declarations
    FLOAT = r'(([0-9]+\.[0-9]*)|(\.[0-9]+))([eE][-+]?[0-9]+)?|\d+([eE][-+]?[0-9]+)'
    INT = r'\d+'
    STRING = r'\".*?\"'

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "testing_numeric_types.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()

    for tok in lexer.tokenize(text):
        print(tok)


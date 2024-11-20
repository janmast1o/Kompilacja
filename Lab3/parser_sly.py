from sly import Parser
from scanner_sly import Scanner
import AST
from TreePrinter import *


class Mparser(Parser):
    tokens = Scanner.tokens
    debugfile = 'parser.out'

    precedence = (
        ('nonassoc', IFX),
        ('nonassoc', ELSE),
        ('nonassoc', LE, GE, EQ, NE, LT, GT),
        ('left', '+', '-', DOTPLUS, DOTMINUS),
        ('left', '*', '/', DOTTIMES, DOTDIVIDE),
        ('nonassoc', "'"),
        ('right', UMINUS)
    )

    @_('instructions instruction',
       'instruction')
    def instructions(self, p):
        if len(p) == 1:
            return AST.InstructionsNode([p[0]])
        return AST.InstructionsNode(p[0].instructions + [p[1]])

    @_('"{" instructions "}"',
   'if_instruction',
   'while_instruction',
   'for_instruction',
   'assign_expression',
   'print_instruction',
   'BREAK ";"',
   'CONTINUE ";"',
   'RETURN expression ";"')
    def instruction(self, p):
        if len(p) == 1:
            return p[0]
        elif p[0] == 'BREAK':
            return AST.BreakInstruction()
        elif p[0] == 'CONTINUE':
            return AST.ContinueInstruction()
        elif p[0] == 'RETURN':
            return AST.ReturnInstruction(p[1])
        elif len(p) == 3:
            return p[1]


    @_('IF "(" relation_expression ")" instruction ELSE instruction',
   'IF "(" relation_expression ")" instruction %prec IFX')
    def if_instruction(self, p):
        if len(p) == 7:
            return AST.IfElseNode(p[2], p[4], p[6])
        else:
            return AST.IfElseNode(p[2], p[4], None)


    @_('WHILE "(" relation_expression ")" instruction')
    def while_instruction(self, p):
        return AST.WhileNode(p.relation_expression, p.instruction)

    @_('FOR ID "=" id_int ":" id_int instruction')
    def for_instruction(self, p):
        return AST.ForNode(p.ID, p.id_int0, p.id_int1, p.instruction)

    @_('ID',
    'INTNUM')
    def id_int(self, p):
        try:
            if (p.INTNUM):
                return AST.IntNum(p[0])
        except:
            pass
        try:
            if (p.ID):
                return AST.IDNode(p[0])
        except:
            pass


    @_('PRINT value ";"')
    def print_instruction(self, p):
        return AST.PrintNode(p[1])

    @_('INTNUM',
       'FLOATNUM',
       'ID',
       'STRING')
    def value(self, p):
        try:
            if (p.INTNUM or p.INTNUM == 0):
                return AST.IntNum(p[0])
        except:
            pass
        try:
            if (p.FLOATNUM or p.FLOATNUM == 0.0):
                return AST.FloatNum(p[0])
        except:
            pass
        try:
            if (p.ID):
                return AST.IDNode(p[0])
        except:
            pass
        try:
            if (p.STRING):
                return AST.Variable(p[0])
        except:
            pass

        return None

    @_("unary_minus")
    def expression(self, p):
        return p[0]
    
    @_('"-" expression %prec UMINUS')
    def unary_minus(self, p):
        return AST.UnaryMinusNode(p[1])
    
    @_('"[" vectors "]"')
    def expression(self, p):
        return AST.MatrixNode(p[1])

    @_('value',
       'assign_expression',
       'relation_expression',
       'matrix_functions',
       'matrix_ref',
       'UMINUS expression',
       '"(" expression ")"',
       'expression "\'"')
    def expression(self, p):
        if len(p) == 1:
            return AST.ExpressionNode(p[0])

        try:
            if (p.UMINUS):
                return AST.UnaryMinusNode(p[1])
        except:
            pass

        if p[1] == "'":
            return AST.TransposeNode(p[0])

        return AST.ExpressionNode(p[1])

    @_('expression "+" expression',
       'expression "-" expression',
       'expression "*" expression',
       'expression "/" expression')
    def expression(self, p):
        return AST.BinExpr(p[1], p[0], p[2])

    @_('expression DOTPLUS expression',
       'expression DOTMINUS expression',
       'expression DOTTIMES expression',
       'expression DOTDIVIDE expression')
    def expression(self, p):
        return AST.BinExpr(p[1], p[0], p[2])

    @_('id_ref "=" expression ";"',
       'id_ref PLUSASSIGN expression ";"',
       'id_ref MINUSASSIGN expression ";"',
       'id_ref TIMESASSIGN expression ";"',
       'id_ref DIVIDEASSIGN expression ";"',)
    def assign_expression(self, p):
        return AST.AssignExpression(p[0], p[1], p[2])
    

    @_('ID "[" list_of_ints "]"')
    def matrix_ref(self, p):
        return AST.MatrixRefNode(p[0], p[2])
    
    @_('ID',
       'matrix_ref')
    def id_ref(self, p):
        try:
            if (p.matrix_ref):
                return p[0]
        except:
            pass

        return AST.IDRefNode(p[0])

    @_('expression LT expression',
       'expression GT expression',
       'expression LE expression',
       'expression GE expression',
       'expression EQ expression',
       'expression NE expression',)
    def relation_expression(self, p):
        return AST.RelationExpression(p[1], p[0], p[2])

    @_('ZEROS "(" INTNUM ")"',
       'ONES "(" INTNUM ")"',
       'EYE "(" INTNUM ")"')
    def matrix_functions(self, p):
        function = p[0]

        if function == 'zeros':
            return AST.ZerosNode(function, p[2])
        elif function == 'ones':
            return AST.OnesNode(function, p[2])
        elif function == 'eye':
            return AST.EyeNode(function, p[2])


    @_('"[" list_of_ints "]"',
       'vectors "," "[" list_of_ints "]"')
    def vectors(self, p):
        if len(p) == 3:
            return AST.VectorsNode([p[1]])

        return AST.VectorsNode(p[0].values+[p[3]])

    @_('INTNUM',
       'list_of_ints "," INTNUM')
    def list_of_ints(self, p):
        if len(p) == 1:
            return AST.ListOfIntsNode([p[0]])
        else:
            return AST.ListOfIntsNode(p[0].values + [p[2]])


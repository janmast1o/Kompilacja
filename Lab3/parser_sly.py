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
   'full_line_expression',
   'print_instruction',
   'BREAK ";"',
   'CONTINUE ";"',
   'RETURN right_hand_side_expression ";"')
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


    @_('PRINT printables ";"')
    def print_instruction(self, p):
        return AST.PrintableNode([p[1]])

    @_('printables "," value',
       'value')
    def printables(self, p):
        if len(p) == 3:
            return AST.ListOfPrintablesNode(p[0].values + [p[2]])
        else:
            return AST.ListOfPrintablesNode([p[0]])


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

    @_('right_hand_side_expression',
       'assign_expression',
       'left_hand_side_expression',
       '"(" full_line_expression ")"')
    def full_line_expression(self, p):
        if len(p) > 1:
            return AST.ExpressionNode(p[1])
        else:
            return AST.ExpressionNode(p[0])

    @_('relation_expression',
       '"(" right_hand_side_expression ")"',
       'matrix_functions',
       'value',
       'right_hand_side_expression "\'"')
    def right_hand_side_expression(self, p):
        if len(p) == 1:
            return AST.ExpressionNode(p[0])
        elif p[1] == "'":
            return AST.TransposeNode(p[0])

        return AST.ExpressionNode(p[1])

    @_('right_hand_side_expression "+" right_hand_side_expression',
       'right_hand_side_expression "-" right_hand_side_expression',
       'right_hand_side_expression "*" right_hand_side_expression',
       'right_hand_side_expression "/" right_hand_side_expression',
       'right_hand_side_expression DOTPLUS right_hand_side_expression',
       'right_hand_side_expression DOTMINUS right_hand_side_expression',
       'right_hand_side_expression DOTTIMES right_hand_side_expression',
       'right_hand_side_expression DOTDIVIDE right_hand_side_expression')
    def right_hand_side_expression(self, p):
        return AST.BinExpr(p[1], p[0], p[2])

    @_('"[" vectors "]"')
    def right_hand_side_expression(self, p):
        return AST.MatrixNode(p[1])

    @_('"[" list_of_elems "]"',
       '"[" "]"')
    def right_hand_side_expression(self, p):
        if len(p) == 2:
            return AST.EmptyNode()
        return AST.VectorsNode([p[1]])

    @_('matrix_ref')
    def right_hand_side_expression(self, p):
        return p[0]

    @_('left_hand_side_expression "=" right_hand_side_expression ";"',
       'left_hand_side_expression PLUSASSIGN right_hand_side_expression ";"',
       'left_hand_side_expression MINUSASSIGN right_hand_side_expression ";"',
       'left_hand_side_expression TIMESASSIGN right_hand_side_expression ";"',
       'left_hand_side_expression DIVIDEASSIGN right_hand_side_expression ";"')
    def assign_expression(self, p):
        return AST.AssignExpression(p[0], p[1], p[2])

    @_('ID "[" list_of_ints "]"')
    def matrix_ref(self, p):
        return AST.MatrixRefNode(p[0], p[2])
    
    @_('ID',
       'matrix_ref')
    def left_hand_side_expression(self, p):
        try:
            if (p.matrix_ref):
                return p[0]
        except:
            pass

        return AST.IDRefNode(p[0])

    @_('right_hand_side_expression LT right_hand_side_expression',
       'right_hand_side_expression GT right_hand_side_expression',
       'right_hand_side_expression LE right_hand_side_expression',
       'right_hand_side_expression GE right_hand_side_expression',
       'right_hand_side_expression EQ right_hand_side_expression',
       'right_hand_side_expression NE right_hand_side_expression',)
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

    @_('"[" list_of_elems "]"',
       'vectors "," "[" list_of_elems "]"',
       '"[" "]"')
    def vectors(self, p):
        if len(p) == 3:
            return AST.VectorsNode([p[1]])
        elif len(p) == 5:
            return AST.VectorsNode(p[0].values+[p[3]])
        return AST.EmptyNode()

    @_('vectors "," "[" "]" ')
    def vectors(self, p):
        return AST.VectorsNode(p[0].values + [AST.EmptyNode()])


    @_('value',
       'list_of_elems "," value')
    def list_of_elems(self, p):
        if len(p) == 1:
            return AST.ListOfElemsNode([p[0]])
        else:
            return AST.ListOfElemsNode(p[0].values + [p[2]])

    @_('INTNUM',
       'list_of_ints "," INTNUM')
    def list_of_ints(self, p):
        if len(p) == 1:
            return AST.ListOfElemsNode([p[0]])
        else:
            return AST.ListOfElemsNode(p[0].values + [p[2]])


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
        ('right', UMINUS),
    )

    @_('instructions instruction',
       'instruction')
    def instructions(self, p):
        if len(p) == 1:
            return AST.InstructionsNode([p[0]])
        return AST.InstructionsNode(p[0].instructions + [p[1]])

    @_('if_instruction',
    'while_instruction',
    'for_instruction',
    'full_line_instruction',
    'print_instruction')
    def instruction(self, p):
        return p[0]
    
    @_('"{" instructions "}"')
    def instruction(self, p):
        return p[1]

    @_('BREAK ";"')
    def instruction(self, p):
        return AST.BreakInstruction()

    @_('CONTINUE ";"')
    def instruction(self, p):
        return AST.ContinueInstruction()

    @_('RETURN right_hand_side_expression ";"')
    def instruction(self, p):
        return AST.ReturnInstruction(p[1])

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

    @_('INTNUM')
    def id_int(self, p):
        return AST.IntNum(p[0])

    @_('ID')
    def id_int(self, p):
        return AST.IDNode(p[0])

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

    @_('INTNUM')
    def value(self, p):
        return AST.IntNum(p[0])

    @_('FLOATNUM')
    def value(self, p):
        return AST.FloatNum(p[0])

    @_('ID')
    def value(self, p):
        return AST.IDNode(p[0])

    @_('STRING')
    def value(self, p):
        return AST.String(p[0])

    @_("unary")
    def right_hand_side_expression(self, p):
        return p[0]
    
    @_('"-" right_hand_side_expression %prec UMINUS')
    def unary(self, p):
        return AST.UnaryMinusNode(p[1])
    
    @_('assign_instruction',
       '"(" full_line_instruction ")"')
    def full_line_instruction(self, p):
        if len(p) > 1:
            return AST.ExpressionNode(p[1])
        else:
            return AST.ExpressionNode(p[0])

    # @_('relation_expression',
    #    '"(" right_hand_side_expression ")"',
    #    'matrix_functions',
    #    'value',
    #    'right_hand_side_expression "\'"')
    # def right_hand_side_expression(self, p):
    #     if len(p) == 1:
    #         return AST.ExpressionNode(p[0])
    #     elif p[1] == "'":
    #         return AST.TransposeNode(p[0])
    #
    #     return AST.ExpressionNode(p[1])

    @_('relation_expression',
       '"(" right_hand_side_expression ")"',
       'matrix_functions',
       'value',
       'matrix_ref',
       'matrix "\'"')
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

    @_('matrix_ref "=" right_hand_side_expression ";"',
       'matrix_ref PLUSASSIGN right_hand_side_expression ";"',
       'matrix_ref MINUSASSIGN right_hand_side_expression ";"',
       'matrix_ref TIMESASSIGN right_hand_side_expression ";"',
       'matrix_ref DIVIDEASSIGN right_hand_side_expression ";"')
    def assign_instruction(self, p):
        return AST.AssignInstruction(p[0], p[1], p[2])
    

    @_('ID "=" right_hand_side_expression ";"',
       'ID PLUSASSIGN right_hand_side_expression ";"',
       'ID MINUSASSIGN right_hand_side_expression ";"',
       'ID TIMESASSIGN right_hand_side_expression ";"',
       'ID DIVIDEASSIGN right_hand_side_expression ";"')
    def assign_instruction(self, p):
        return AST.AssignInstruction(AST.IDNode(p[0]), p[1], p[2])
    
    @_('ID "[" id_ints "]"')
    def matrix_ref(self, p):
        return AST.Variable(AST.IDNode(p[0]), p[2])

    @_('id_ints "," id_int')
    def id_ints(self, p):
        return p[0] + [p[2]]

    @_('id_int')
    def id_ints(self, p):
        return [p[0]]

    @_('matrix_ref')
    def printables(self, p):
        return AST.ListOfPrintablesNode([p[0]])
    
    @_('right_hand_side_expression LT right_hand_side_expression',
       'right_hand_side_expression GT right_hand_side_expression',
       'right_hand_side_expression LE right_hand_side_expression',
       'right_hand_side_expression GE right_hand_side_expression',
       'right_hand_side_expression EQ right_hand_side_expression',
       'right_hand_side_expression NE right_hand_side_expression',)
    def relation_expression(self, p):
        return AST.RelationExpression(p[1], p[0], p[2])

    @_('ZEROS "(" id_int ")"')
    def matrix_functions(self, p):
        return AST.ZerosNode('zeros', p[2])
    
    @_('ZEROS "(" id_int "," id_int ")"')
    def matrix_functions(self, p):
        return AST.ZerosNode('zeros', p[2], p[4])

    @_('ONES "(" id_int ")"')
    def matrix_functions(self, p):
        return AST.OnesNode('ones', p[2])
    
    @_('ONES "(" id_int "," id_int ")"')
    def matrix_functions(self, p):
        return AST.OnesNode('ones', p[2], p[4])

    @_('EYE "(" id_int ")"')
    def matrix_functions(self, p):
        return AST.EyeNode('eye', p[2])
    
    @_('EYE "(" id_int "," id_int ")"')
    def matrix_functions(self, p):
        return AST.EyeNode('eye', p[2], p[4])

    @_('vector',
       'matrix')
    def right_hand_side_expression(self, p):
        return p[0]

    # @_('matrix')
    # def right_hand_side_expression(self, p):
    #     return p[0]

    @_('"[" variables "]"')
    def vector(self, p):
        return AST.VectorNode(p[1])

    @_('"[" vectors "]"')
    def matrix(self, p):
        return AST.MatrixNode(p[1])

    @_('vectors "," vector',
       'vector')
    def vectors(self, p):
        return p[0] + [p[2]] if len(p) == 3 else [p[0]]
    
    @_('"[" "]"')
    def vector(self, p):
        return AST.VectorNode([])

    @_('variables "," value',
       'value')
    def variables(self, p):
        return p[0] + [p[2]] if len(p) == 3 else [p[0]]

class Node(object):
    pass


class InstructionsNode(Node):
    def __init__(self, instructions):
        self.instructions = instructions


# class EmptyNode(Node):
#     def __init__(self):
#         self.value = "EMPTY"


class BreakInstruction(Node):
    pass


class ContinueInstruction(Node):
    pass


class ReturnInstruction(Node):
    def __init__(self, expr):
        self.expr = expr


class IntNum(Node):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class FloatNum(Node):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class String(Node):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)


class IDNode(Node):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class ForNode:
    def __init__(self, variable, start, end, body):
        self.variable = variable
        self.start = start
        self.end = end
        self.body = body


class IfElseNode:
    def __init__(self, condition, if_body, else_body=None):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body


class AssignInstruction(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Variable(Node):
    def __init__(self, name, index):
        self.name = name
        self.index = index

    # def __str__(self):
    #     return f"{self.name}{self.index}"


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class RelationExpression(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class MatrixFuncNode(Node):
    def __init__(self, func_name, arg_x, arg_y=None):
        self.func_name = func_name
        self.arg_x = arg_x
        self.arg_y = arg_y if arg_y is not None else arg_x


class ZerosNode(MatrixFuncNode):
    pass


class OnesNode(MatrixFuncNode):
    pass


class EyeNode(MatrixFuncNode):
    pass


class IDRefNode(Node):
    def __init__(self, value):
        self.value = value


class PrintableNode(Node):
    def __init__(self, printable):
        self.printable = printable


class ListOfPrintablesNode(Node):
    def __init__(self, printables_list):
        self.printables_list = printables_list


class ExpressionNode(Node):
    def __init__(self, expr):
        self.expr = expr


class UnaryMinusNode(Node):
    def __init__(self, expr):
        self.expr = expr


class TransposeNode(Node):
    def __init__(self, expr):
        self.expr = expr


class VectorNode(Node):
    def __init__(self, values):
        self.values = values


class MatrixNode(Node):
    def __init__(self, vectors):
        self.vectors = vectors


class Error(Node):
    def __init__(self):
        pass


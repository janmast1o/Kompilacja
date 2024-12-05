#!/usr/bin/python
from collections import defaultdict
import AST
from SymbolTable import SymbolTable, Symbol, VariableSymbol, Additional

dict_of_types = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: "")))

dict_of_types["+"]["int"]["int"] = "int"
dict_of_types["+"]["int"]["float"] = "float"
dict_of_types["+"]["float"]["int"] = "float"
dict_of_types["+"]["float"]["float"] = "float"
dict_of_types["+"]["str"]["str"] = "str"
dict_of_types["+"]["vector"]["vector"] = "vector"
dict_of_types["+"]["matrix"]["matrix"] = "matrix"

dict_of_types["-"]["int"]["int"] = "int"
dict_of_types["-"]["int"]["float"] = "float"
dict_of_types["-"]["float"]["int"] = "float"
dict_of_types["-"]["float"]["float"] = "float"
dict_of_types["-"]["str"]["str"] = "str"
dict_of_types["-"]["vector"]["vector"] = "vector"
dict_of_types["-"]["matrix"]["matrix"] = "matrix"

dict_of_types["*"]["int"]["int"] = "int"
dict_of_types["*"]["int"]["float"] = "float"
dict_of_types["*"]["float"]["int"] = "float"
dict_of_types["*"]["float"]["float"] = "float"
dict_of_types["*"]["str"]["str"] = "str"
dict_of_types["*"]["str"]["int"] = "str"
dict_of_types["*"]["int"]["str"] = "str"
# dict_of_types["*"]["vector"]["vector"] = "vector"
dict_of_types["*"]["matrix"]["matrix"] = "matrix"

dict_of_types["/"]["int"]["int"] = "int"
dict_of_types["/"]["int"]["float"] = "float"
dict_of_types["/"]["float"]["int"] = "float"
dict_of_types["/"]["float"]["float"] = "float"
# dict_of_types["/"]["vector"]["vector"] = "vector"


dict_of_types[">"]["int"]["int"] = "bool"
dict_of_types[">"]["int"]["float"] = "bool"
dict_of_types[">"]["float"]["int"] = "bool"
dict_of_types[">"]["float"]["float"] = "bool"

dict_of_types["<"]["int"]["int"] = "bool"
dict_of_types["<"]["int"]["float"] = "bool"
dict_of_types["<"]["float"]["int"] = "bool"
dict_of_types["<"]["float"]["float"] = "bool"

dict_of_types[">="]["int"]["int"] = "bool"
dict_of_types[">="]["int"]["float"] = "bool"
dict_of_types[">="]["float"]["int"] = "bool"
dict_of_types[">="]["float"]["float"] = "bool"

dict_of_types["<="]["int"]["int"] = "bool"
dict_of_types["<="]["int"]["float"] = "bool"
dict_of_types["<="]["float"]["int"] = "bool"
dict_of_types["<="]["float"]["float"] = "bool"

dict_of_types["=="]["int"]["int"] = "bool"
dict_of_types["=="]["int"]["float"] = "bool"
dict_of_types["=="]["float"]["int"] = "bool"
dict_of_types["=="]["float"]["float"] = "bool"

dict_of_types["!="]["int"]["int"] = "bool"
dict_of_types["!="]["int"]["float"] = "bool"
dict_of_types["!="]["float"]["int"] = "bool"
dict_of_types["!="]["float"]["float"] = "bool"

dict_of_types[".+"]["vector"]["vector"] = "vector"
dict_of_types[".-"]["vector"]["vector"] = "vector"
dict_of_types[".*"]["vector"]["vector"] = "vector"
dict_of_types["./"]["vector"]["vector"] = "vector"
dict_of_types[".+"]["matrix"]["matrix"] = "matrix"
dict_of_types[".-"]["matrix"]["matrix"] = "matrix"
dict_of_types[".*"]["matrix"]["matrix"] = "matrix"
dict_of_types["./"]["matrix"]["matrix"] = "matrix"

dict_of_types["+="]["int"]["int"] = "int"
dict_of_types["+="]["int"]["float"] = "float"
dict_of_types["+="]["float"]["int"] = "float"
dict_of_types["+="]["float"]["float"] = "float"
dict_of_types["+="]["str"]["str"] = "str"
# dict_of_types["+="]["vector"]["vector"] = "vector"
# dict_of_types["+="]["matrix"]["matrix"] = "matrix"

dict_of_types["-="]["int"]["int"] = "int"
dict_of_types["-="]["int"]["float"] = "float"
dict_of_types["-="]["float"]["int"] = "float"
dict_of_types["-="]["float"]["float"] = "float"
dict_of_types["-="]["str"]["str"] = "str"
# dict_of_types["-="]["vector"]["vector"] = "vector"
# dict_of_types["-="]["matrix"]["matrix"] = "matrix"

dict_of_types["*="]["int"]["int"] = "int"
dict_of_types["*="]["int"]["float"] = "float"
dict_of_types["*="]["float"]["int"] = "float"
dict_of_types["*="]["float"]["float"] = "float"
dict_of_types["*="]["str"]["str"] = "str"
# dict_of_types["*="]["vector"]["vector"] = "vector"
# dict_of_types["*="]["matrix"]["matrix"] = "matrix"

dict_of_types["/="]["int"]["int"] = "int"
dict_of_types["/="]["int"]["float"] = "float"
dict_of_types["/="]["float"]["int"] = "float"
dict_of_types["/="]["float"]["float"] = "float"
# dict_of_types["/="]["vector"]["vector"] = "vector"
# dict_of_types["/="]["matrix"]["matrix"] = "matrix"


type_negotiation_dict = defaultdict(lambda: defaultdict(lambda: ""))

type_negotiation_dict["any"]["int"] = "int"
type_negotiation_dict["any"]["float"] = "float"
type_negotiation_dict["any"]["bool"] = "bool"
type_negotiation_dict["any"]["str"] = "str"

type_negotiation_dict["int"]["int"] = "int"
type_negotiation_dict["int"]["float"] = "int"
type_negotiation_dict["int"]["bool"] = "int"

type_negotiation_dict["float"]["float"] = "float"
type_negotiation_dict["float"]["int"] = "float"
type_negotiation_dict["float"]["bool"] = "float"

type_negotiation_dict["bool"]["int"] = "int"
type_negotiation_dict["bool"]["bool"] = "bool"
type_negotiation_dict["bool"]["float"] = "float"

type_negotiation_dict["str"]["str"] = "str"


def negotiate_type(current_type, type_of_new_elem):
    return type_negotiation_dict[current_type][type_of_new_elem]


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.current_symbol_table = SymbolTable()


    def visit_InstructionsNode(self, node: AST.InstructionsNode):
        for instruction in node.instructions:
            self.visit(instruction)

        return None, None


    def visit_BreakInstruction(self, node: AST.BreakInstruction):
        if self.current_symbol_table.st_name != "loop_body":
            raise Exception(f"Break instruction can only occur inside a loop")

        return None, None


    def visit_ContinueInstruction(self, node: AST.ContinueInstruction):
        if self.current_symbol_table.st_name != "loop_body":
            raise Exception(f"Continue instruction can only occur inside a loop")

        return None, None


    def visit_ReturnInstruction(self, node: AST.ReturnInstruction): # ?
        return None, None


    def visit_IntNum(self, node: AST.IntNum):
        return "int", None


    def visit_FloatNum(self, node: AST.FloatNum):
        return "float", None


    def visit_String(self, node: AST.String):
        return "str", None


    def visit_IDNode(self, node: AST.IDNode):
        symbol = self.current_symbol_table.get(node.value)
        if symbol is None:
            raise Exception(f"Attempting to refer to {node.value}, which is"
                            f"uninitialized")

        return symbol.symbol_type, symbol.additional


    def visit_WhileNode(self, node: AST.WhileNode):
        condition_type, _ = self.visit(node.condition)
        if condition_type != "bool":
            raise Exception(f"The condition must of type bool, not {condition_type}")

        self.current_symbol_table = self.current_symbol_table.pushScope("loop_body")
        self.visit(node.body)
        self.current_symbol_table = self.current_symbol_table.popScope()

        return None, None


    def visit_ForNode(self, node: AST.ForNode):
        self.current_symbol_table = self.current_symbol_table.pushScope("loop_body")
        var = node.variable.value
        self.current_symbol_table.put(var, "int")
        self.current_symbol_table = self.current_symbol_table.popScope()

        return None, None


    def visit_IfElseNode(self, node: AST.IfElseNode):
        condition_type, _ = self.visit(node.condition)
        if condition_type != "bool":
            raise Exception(f"The condition must of type bool, not {condition_type}")

        self.current_symbol_table = self.current_symbol_table.pushScope("if_body")
        self.visit(node.if_body)
        self.current_symbol_table = self.current_symbol_table.popScope()

        self.current_symbol_table = self.current_symbol_table.pushScope("else_body")
        self.visit(node.else_body)
        self.current_symbol_table = self.current_symbol_table.popScope()

        return None, None


    def visit_AssignInstruction(self, node: AST.AssignInstruction):
        op = node.operator
        left_side = node.left
        right_side = node.right
        right_side_type, right_side_add = self.visit(right_side)
        if op == "=":
            if isinstance(left_side, AST.IDNode):
                symbol = VariableSymbol(left_side.value, right_side_type, right_side_add)
                self.current_symbol_table.put(left_side.value, symbol)

            elif isinstance(left_side, AST.Variable):
                left_side_id = left_side.name
                left_side_index = left_side.index
                symbol = self.current_symbol_table.get(left_side_id.value)
                if symbol is None:
                    raise Exception(f"Attempting to subscript an uninitialized variable: "
                                    f"{left_side_id.value}")
                elif symbol.symbol_type != "vector" and symbol.symbol_type != "matrix":
                    raise Exception(f"Cannot subscript a variable of type: {symbol.symbol_type}")

                if len(left_side_index) != len(symbol.additional.size):
                    raise Exception("Dims mismatch")

                # add checking array bounds

                if right_side_type == "vector" or right_side == "matrix":
                    raise Exception(f"Attempting to insert an array into {left_side_id},"
                                    f"arrays of more than dwo dims are not allowed")

                negotiated_type = negotiate_type(symbol.additional.stored_type, right_side_type)
                if negotiated_type == "":
                    raise Exception(f"Attempting to enter data of type {negotiated_type},"
                                    f"which is invalid for array {left_side_id}, which so far"
                                    f"has stored {symbol.additional.stored_type}")
                else:
                    symbol.additional.stored_type = negotiated_type

        else:
            if isinstance(left_side, AST.IDNode):
                symbol = self.current_symbol_table.get(left_side.value)
                if symbol is None:
                    raise Exception(f"Attempting to alter a variable {left_side.value}"
                                    f"with operator: {op}")

                negotiated_type = negotiate_type(symbol.symbol_type, right_side_type)
                if negotiated_type == "":
                    raise Exception(f"Type mismatch when applying operator: {op}"
                                    f"to variable: {left_side.value}")

            elif isinstance(left_side, AST.Variable):
                left_side_id = left_side.name
                left_side_index = left_side.index
                symbol = self.current_symbol_table.get(left_side_id.value)
                if symbol is None:
                    raise Exception(f"Attempting to subscript an uninitialized variable: "
                                    f"{left_side_id.value}")
                elif symbol.symbol_type != "vector" and symbol.symbol_type != "matrix":
                    raise Exception(f"Cannot subscript a variable of type: {symbol.symbol_type}")

                if len(left_side_index) != len(symbol.additional.size):
                    raise Exception("Dims mismatch")

                # add checking array bounds

                if right_side_type == "vector" or right_side == "matrix":
                    raise Exception(f"Attempting to insert an array into {left_side_id},"
                                    f"arrays of more than dwo dims are not allowed")

                negotiated_type = negotiate_type(symbol.additional.stored_type, right_side_type)
                if negotiated_type == "":
                    raise Exception(f"Attempting to enter data of type {negotiated_type},"
                                    f"which is invalid for array {left_side_id}, which so far"
                                    f"has stored {symbol.additional.stored_type}")
                else:
                    symbol.additional.stored_type = negotiated_type

        return None, None


    def visit_Variable(self, node: AST.Variable):
        node_id = node.name
        node_id_type = self.visit(node_id)
        if node_id_type != "matrix" and node_id_type != "vector":
            raise Exception(f"{node_id_type} is not subscriptable, only matrix and vector are")

        symbol = self.current_symbol_table.get(node_id.value)
        if symbol is None:
            raise Exception(f"Attempting to access an uninitialized variable: {node_id.value}")

        return symbol.symbol_type, symbol.additional


    def visit_BinaryExpr(self, node: AST.BinExpr):
        left_side = node.left
        op = node.op
        right_side = node.right

        left_side_type, left_side_add = self.visit(left_side)
        right_side_type, right_side_add = self.visit(right_side)

        result_type = dict_of_types[op][left_side_type][right_side_type]
        if result_type == "":
            raise Exception(f"Cannot apply operator {op} to "
                            f"{left_side_type} (left) and "
                            f"{right_side_type} (right)")

        # change when introducing checking dims and mat mul
        return result_type, left_side_add


    def visit_RelationExpr(self, node: AST.RelationExpression):
        left_side = node.left
        op = node.op
        right_side = node.right

        result_type = dict_of_types[op][left_side][right_side]
        if result_type != "bool":
            raise Exception("Condition should be asserted as bool"
                            f"bu {left_side} {op} {right_side} "
                            f"is asserted as {result_type}")

        return "bool", None


    def visit_MatrixFuncNode(self, node: AST.MatrixFuncNode):
        arg_type, _ = self.visit(node.arg)
        if arg_type != "int":
            raise Exception("Matrix functions must be initialized with int,"
                            f"not {arg_type}")

        # size set temporarily, need to change it
        return "matrix", Additional((1,1), "float")


    def visit_ZerosNode(self, node: AST.ZerosNode):
        return self.visit_MatrixFuncNode(node)


    def visit_OnesNode(self, node: AST.OnesNode):
        return self.visit_MatrixFuncNode(node)


    def visit_EyeNode(self, node: AST.EyeNode):
        return self.visit_MatrixFuncNode(node)


    def visit_PrintableNode(self, node: AST.PrintableNode):
        return None, None


    def visit_ListOfPrintableNodes(self, node: AST.ListOfPrintablesNode):
        return None, None


    def visit_ExpressionNode(self, node: AST.ExpressionNode):
        return self.visit(node.expr)


    def visit_UnaryMinusNode(self, node: AST.UnaryMinusNode):
        expr_type, _ = self.visit(node.expr)
        if expr_type != "int" and expr_type != "float":
            raise Exception("Can only apply unary minus on int and float,"
                            f" cannot apply it on {expr_type}")

        return expr_type, None


    def visit_TransposeNode(self, node: AST.TransposeNode):
        expr_type, _ = self.visit(node.expr)
        if expr_type != "matrix":
            raise Exception("Can only apply transpose on matrix,"
                            f" cannot apply it on {expr_type}")

        return expr_type, None


    def visit_VectorNode(self, node: AST.VectorNode):








        



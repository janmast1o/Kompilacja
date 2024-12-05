#!/usr/bin/python
from collections import defaultdict
import AST
from SymbolTable import SymbolTable, Symbol, VariableSymbol

dict_of_types = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: "")))

dict_of_types["+"]["int"]["int"] = "int"
dict_of_types["+"]["int"]["float"] = "float"
dict_of_types["+"]["float"]["int"] = "float"
dict_of_types["+"]["float"]["float"] = "float"
dict_of_types["+"]["str"]["str"] = "str"
dict_of_types["+"]["vector"]["vector"] = "vector"

dict_of_types["-"]["int"]["int"] = "int"
dict_of_types["-"]["int"]["float"] = "float"
dict_of_types["-"]["float"]["int"] = "float"
dict_of_types["-"]["float"]["float"] = "float"
dict_of_types["-"]["str"]["str"] = "str"
dict_of_types["-"]["vector"]["vector"] = "vector"

dict_of_types["*"]["int"]["int"] = "int"
dict_of_types["*"]["int"]["float"] = "float"
dict_of_types["*"]["float"]["int"] = "float"
dict_of_types["*"]["float"]["float"] = "float"
dict_of_types["*"]["str"]["str"] = "str"
dict_of_types["*"]["str"]["int"] = "str"
dict_of_types["*"]["int"]["str"] = "str"
dict_of_types["*"]["vector"]["vector"] = "vector"

dict_of_types["/"]["int"]["int"] = "int"
dict_of_types["/"]["int"]["float"] = "float"
dict_of_types["/"]["float"]["int"] = "float"
dict_of_types["/"]["float"]["float"] = "float"
dict_of_types["/"]["vector"]["vector"] = "vector"


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

dict_of_types["+="]["int"]["int"] = "int"
dict_of_types["+="]["int"]["float"] = "float"
dict_of_types["+="]["float"]["int"] = "float"
dict_of_types["+="]["float"]["float"] = "float"
dict_of_types["+="]["str"]["str"] = "str"
dict_of_types["+="]["vector"]["vector"] = "vector"

dict_of_types["-="]["int"]["int"] = "int"
dict_of_types["-="]["int"]["float"] = "float"
dict_of_types["-="]["float"]["int"] = "float"
dict_of_types["-="]["float"]["float"] = "float"
dict_of_types["-="]["str"]["str"] = "str"
dict_of_types["-="]["vector"]["vector"] = "vector"

dict_of_types["*="]["int"]["int"] = "int"
dict_of_types["*="]["int"]["float"] = "float"
dict_of_types["*="]["float"]["int"] = "float"
dict_of_types["*="]["float"]["float"] = "float"
dict_of_types["*="]["str"]["str"] = "str"
dict_of_types["*="]["vector"]["vector"] = "vector"

dict_of_types["/="]["int"]["int"] = "int"
dict_of_types["/="]["int"]["float"] = "float"
dict_of_types["/="]["float"]["int"] = "float"
dict_of_types["/="]["float"]["float"] = "float"
dict_of_types["/="]["vector"]["vector"] = "vector"



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

    # simpler version of generic_visit, not so general
    #def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)



class TypeChecker(NodeVisitor):
    def __init__(self):
        self.current_symbol_table = SymbolTable()


    def visit_InstructionsNode(self, node):
        for instruction in node.instructions:
            self.visit(instruction)


    def visit_returnInstruction(self, node): # ??? 
        ...        


    def visit_BinExpr(self, node):
        # alternative usage,
        # requires definition of accept method in class Node
        # type1 = node.left.accept(self)
        # type2 = node.right.accept(self)
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        result_type = dict[op][type1][type2]
        if result_type == "":
            raise Exception(f"Cannot apply operator {op} to types {type1}, {type2}")

        return result_type


    def visit_RelationExpression(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op
        result_type = dict[op][type1][type2]
        if result_type == "":
            raise Exception(f"Cannot apply operator {op} to types {type1}, {type2}")

        return result_type
    

    def visit_WhileNode(self, node):
        condition_type = self.visit(node.condition)
        if condition_type != "bool":
            raise Exception(f"There must be a bool expression in while condition, not {condition_type}")
        
        self.current_symbol_table = self.current_symbol_table.pushScope("loop body")
        self.visit(node.body)


    def visit_ForNode(self, node):
        start_type = self.visit(node.start)
        end_type = self.visit(node.end)
        if start_type != "int":
            raise Exception(f"Start in for loop condition must be of type int, not: {start_type}")
        elif end_type != "int":
            raise Exception(f"End in for loop condition must be of type int, not: {start_type}")

        self.current_symbol_table = self.current_symbol_table.pushScope("loop body")
        self.current_symbol_table.put(node.variable, VariableSymbol(node.variable, "int"))
        self.visit(node.body)


    def visit_BreakInstruction(self, node):  
        if not self.current_symbol_table.st_name == "loop body":
            raise Exception("Cannot run break outside of loop")
        self.current_symbol_table = self.current_symbol_table.popScope()


    def visit_ContinueInstruction(self, node):
        if not self.current_symbol_table.st_name == "loop body":
            raise Exception("Cannot run break outside of loop")  


    def visit_IfElseNode(self, node):
        condition_type = self.visit(node.condition)
        if not condition_type == "bool":
            raise Exception(f"There must be a bool expression in the if condition, not {condition_type}")      

        self.current_symbol_table = self.current_symbol_table.pushScope("if body")
        self.visit(node.if_body)
        self.current_symbol_table = self.current_symbol_table.popScope()

        self.current_symbol_table = self.current_symbol_table.pushScope("else body")
        self.visit(node.else_body)
        self.current_symbol_table = self.current_symbol_table.pop()


    def visit_IntNum(self, node):
        return "int"


    def visit_FloatNum(self, node):
        return "float"


    def visit_String(self, node):
        return "str"


    def visit_IDNode(self, node):
        symbol = self.current_symbol_table.get(node.value)
        if symbol is None:
            raise Exception(f"Cannot resolve reference to: {node.name}")
        
        return symbol.symbol_type


    def visit_Variable(self, node):
        pass
        



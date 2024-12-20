from on_when import *
import AST
import SymbolTable
from Memory import Memory,MemoryStack
from enum import Enum
from collections import defaultdict
import numpy as np


def perform_multiplication(x, y):
    if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
        return x @ y
    elif isinstance(x, np.ndarray) or isinstance(y, np.ndarray):
        raise Exception(f"Invalid types in multiplication")
    else:
        return x*y
    

def perform_dot_multiplication(x, y):
    if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
        return np.multiply(x, y)
    elif isinstance(x, np.ndarray) or isinstance(y, np.ndarray):
        raise Exception(f"Invalid types in multiplication")
    else:
        return x*y   


def perform_dot_divide(x, y):
    if isinstance(x, np.ndarray) and isinstance(y, np.ndarray):
        return np.divide(x, y)
    elif isinstance(x, np.ndarray) or isinstance(y, np.ndarray):
        raise Exception(f"Invalid types in multiplication")
    else:
        return x/y   
     

op_dict = {}
op_dict["+"] = lambda x, y: x+y
op_dict["-"] = lambda x, y: x-y
op_dict["*"] = perform_multiplication
op_dict["/"] = lambda x, y: x/y
op_dict[".+"] = lambda x, y: x+y
op_dict[".-"] = lambda x, y: x-y
op_dict[".*"] = perform_dot_multiplication
op_dict["./"] = perform_dot_divide
op_dict["=="] = lambda x, y: x == y 
op_dict["!="] = lambda x, y: x != y 
op_dict[">="] = lambda x, y: x >= y 
op_dict["<="] = lambda x, y: x <= y 
op_dict["<"] = lambda x, y: x < y 
op_dict[">"] = lambda x, y: x > y 


def apply_operator(op, x, y):
    if op not in op_dict:
        raise Exception("Invalid operator")
    else:
        return op_dict[op](x,y)
    

assign_op_to_op_dict = {"+=" : "+", "-=" : "-", "*=" : "*", "/=" : "/"}
def apply_assign_operator(op, x, y):
    if op not in assign_op_to_op_dict:
        raise Exception("Invalid assign operator")
    else:
        return op_dict[assign_op_to_op_dict[op]](x,y)
    

class SpecialCaseInstruction(Enum):
    BREAK_INS = 1,
    CONTINUE_INS = 2,
    RETURN_INS = 3


class Interpreter:
    def __init__(self):
        self.current_memory_stack: MemoryStack = MemoryStack(name="global")


    @on('node')
    def visit(self, node):
        ...


    @when(AST.InstructionsNode)
    def visit(self, node: AST.InstructionsNode):
        for instruction in node.instructions:
            # print(instruction)
            visited_res = self.visit(instruction)
            if visited_res == SpecialCaseInstruction.BREAK_INS:
                return SpecialCaseInstruction.BREAK_INS
            elif visited_res == SpecialCaseInstruction.CONTINUE_INS:
                return SpecialCaseInstruction.CONTINUE_INS
            elif visited_res == SpecialCaseInstruction.RETURN_INS:
                return         


    @when(AST.BreakInstruction)
    def visit(self, node: AST.BreakInstruction):
        if self.current_memory_stack.mem_stack_name != "loop_body":
            raise Exception(f"Break exception can only occur inside loop body")
        
        return SpecialCaseInstruction.BREAK_INS 
            
    
    @when(AST.ContinueInstruction)
    def visit(self, node: AST.ContinueInstruction):
        if self.current_memory_stack.mem_stack_name != "loop_body":
            raise Exception(f"Continue instruction can only occur inside loop body")
        
        return SpecialCaseInstruction.CONTINUE_INS


    @when(AST.ReturnInstruction)
    def visit(self, node: AST.ReturnInstruction):
        return SpecialCaseInstruction.RETURN_INS  


    @when(AST.IntNum)
    def visit(self, node: AST.IntNum):
        read_value = int(node.value)
        return read_value 
    
    
    @when(AST.FloatNum)
    def visit(self, node: AST.FloatNum):
        read_value = float(node.value)
        return read_value
    

    @when(AST.String)
    def visit(self, node: AST.String):
        read_value = str(node.name)
        return read_value 
    

    @when(AST.IDNode)
    def visit(self, node: AST.IDNode):
        read_value = self.current_memory_stack.get(node.value)
        # print(self.current_memory_stack.current_memory.memory_map)
        if read_value is None:
            raise Exception(f"Attempting to refer to uninitialized variable: {node.value}")
        
        return read_value 
    

    @when(AST.WhileNode)
    def visit(self, node: AST.WhileNode):
        returned_value = None
        self.current_memory_stack = self.current_memory_stack.push_scope(name="loop_body")
        while self.visit(node.condition):
            returned_value = self.visit(node.body)
            if returned_value == SpecialCaseInstruction.BREAK_INS: # handling return better
                break

        self.current_memory_stack = self.current_memory_stack.pop_scope()    


    @when(AST.ForNode)
    def visit(self, node: AST.ForNode):
        start_value = self.visit(node.start)
        end_value = self.visit(node.end)
        self.current_memory_stack = self.current_memory_stack.push_scope(name="loop_body")
        self.current_memory_stack.put(node.variable.value, start_value)
        while self.current_memory_stack.get(node.variable.value) <= end_value:
            returned_value = self.visit(node.body)
            if returned_value == SpecialCaseInstruction.BREAK_INS: # handling return better
                break 
            self.current_memory_stack.put(
                node.variable.value, 
                self.current_memory_stack.get(node.variable.value)+1
            )

        self.current_memory_stack = self.current_memory_stack.pop_scope()


    @when(AST.IfElseNode)
    def visit(self, node: AST.IfElseNode):
        # self.current_memory_stack = self.current_memory_stack.push_scope("if_body")
        if self.visit(node.condition):
            self.visit(node.if_body)
        elif node.else_body is not None:
            self.visit(node.else_body)
        # self.current_memory_stack = self.current_memory_stack.pop_scope()    


    @when(AST.AssignInstruction)
    def visit(self, node: AST.AssignInstruction):
        right_value = self.visit(node.right)

        if right_value is None:
            raise Exception(f"Implementation error")
        op = node.operator
        if op == "=":            
            if isinstance(node.left, AST.IDNode):
                self.current_memory_stack.put(node.left.value, right_value, override=True)
                # print(type(node.left.value))
                # print(node.left.value, right_value)
            elif isinstance(node.left, AST.Variable):
                # print(type(node.left.name))
                matrix_name = node.left.name.value
                corresponding_matrix = self.current_memory_stack.get(matrix_name)
                m, n = corresponding_matrix.shape[0], corresponding_matrix.shape[1]
                i, j = self.visit(node.left.index[0]), self.visit(node.left.index[1])
                if (not (0 <= i < m)) or (not(0 <= j < n)):
                    raise Exception(f"Matrix bounds breached during subscription {i}, {j} is invalid for matrix of size: {m}, {n}")
                else:
                    corresponding_matrix[i,j] = right_value
        else:
            if isinstance(node.left, AST.IDNode):
                left_value = self.current_memory_stack.get(node.left.value)
                self.current_memory_stack.put(node.left.value, apply_assign_operator(op, left_value, right_value))
            elif isinstance(node.left, AST.Variable):
                matrix_name = node.left.name
                corresponding_matrix = self.current_memory_stack.get(matrix_name)
                m, n = corresponding_matrix.shape[0], corresponding_matrix.shape[1]
                i, j = self.visit(node.left.index[0]), self.visit(node.left.index[1])
                if (not (0 <= i < m)) or (not (0 <= j < n)):
                    raise Exception(f"Matrix bounds breached during subscription {i}, {j} is invalid for matrix of size: {m}, {n}")
                else:
                    residing_value = corresponding_matrix[i,j]
                    corresponding_matrix[i,j] = apply_assign_operator(op, residing_value, right_value)


    @when(AST.Variable)
    def visit(self, node: AST.Variable):
        corresponding_matrix = self.current_memory_stack.get(node.name.value)
        if corresponding_matrix is None:
            raise Exception(f"Variable under name: {node.name.value} is unitialized")

        m, n = corresponding_matrix.shape[0], corresponding_matrix.shape[1]
        i, j = self.visit(node.index[0]), self.visit(node.index[1]) 
        if (not (0 <= i < m)) or (not (0 <= j < n)):
            raise Exception(f"Matrix bounds breached during subscription {i}, {j} is invalid for matrix of size: {m}, {n}")
        else:
            # print(corresponding_matrix[i,j])
            return corresponding_matrix[i,j]


    @when(AST.BinExpr)
    def visit(self, node: AST.BinExpr):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        return apply_operator(node.op, left_value, right_value)


    @when(AST.RelationExpression)
    def visit(self, node: AST.RelationExpression):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)
        return apply_operator(node.op, left_value, right_value)      


    @when(AST.MatrixFuncNode)
    def visit(self, node: AST.MatrixFuncNode):
        if self.visit(node.arg_x) <= 0 or self.visit(node.arg_y) <= 0:
            raise Exception("Invalid matrix func call args")

        created_matrix = None
        if node.func_name == 'zeros':
            created_matrix = np.zeros((self.visit(node.arg_x), self.visit(node.arg_y)))
        elif node.func_name == 'ones':
            created_matrix = np.ones((self.visit(node.arg_x), self.visit(node.arg_y)))
        elif node.func_name == 'eye':
            created_matrix = np.eye(self.visit(node.arg_x), self.visit(node.arg_y))

        return created_matrix


    @when(AST.ZerosNode)
    def visit(self, node: AST.ZerosNode):
        if self.visit(node.arg_x) <= 0 or self.visit(node.arg_y) <= 0:
            raise Exception("Invalid matrix func call args")
        return np.zeros((self.visit(node.arg_x), self.visit(node.arg_y)))


    @when(AST.OnesNode)
    def visit(self, node: AST.OnesNode):
        if self.visit(node.arg_x) <= 0 or self.visit(node.arg_y) <= 0:
            raise Exception("Invalid matrix func call args")
        return np.ones((self.visit(node.arg_x), self.visit(node.arg_y)))


    @when(AST.EyeNode)
    def visit(self, node: AST.EyeNode):
        if self.visit(node.arg_x) <= 0 or self.visit(node.arg_y) <= 0:
            raise Exception("Invalid matrix func call args")
        return np.eye(self.visit(node.arg_x), self.visit(node.arg_y))


    @when(AST.IDRefNode)    
    def visit(self, node: AST.IDRefNode):
        ...


    @when(AST.PrintableNode)
    def visit(self, node: AST.PrintableNode):
        self.visit(node.printable)


    @when(AST.ListOfPrintablesNode)
    def visit(self, node: AST.ListOfPrintablesNode):
        for value in node.printables_list:
            print(self.visit(value), end="  ")
        print()


    @when(AST.ExpressionNode)
    def visit(self, node: AST.ExpressionNode):
        return self.visit(node.expr)


    @when(AST.UnaryMinusNode)
    def visit(self, node: AST.UnaryMinusNode):
        return -self.visit(node.expr)                


    @when(AST.TransposeNode)
    def visit(self, node: AST.TransposeNode):
        # print(np.transpose(self.visit(node.expr)))
        return np.transpose(self.visit(node.expr))


    @when(AST.VectorNode)
    def visit(self, node: AST.VectorNode):
        read_vector = [None for _ in range (0,len(node.values))]
        for i in range(0,len(node.values)):
            value = node.values[i]
            read_vector[i] = self.visit(value)

        return np.array(read_vector)


    @when(AST.MatrixNode)
    def visit(self, node: AST.MatrixNode):
        read_matrix = []
        read_matrix_cols = None
        for v in node.vectors:
            vector = (self.visit(v)).tolist()
            vec_length = len(vector)
            if read_matrix_cols is None:
                read_matrix_cols = vec_length
            elif read_matrix_cols != vec_length:
                raise Exception("Invalid matrix shape - matrices must always be rectangular")    
            read_matrix.append(vector)

        return np.array(read_matrix) 


    @when(AST.Error)
    def visit(self, node: AST.Error):
        raise Exception(f"Error occured")       



    
                                  



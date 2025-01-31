from __future__ import print_function
import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.InstructionsNode)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            instruction.printTree(indent)

    @addToClass(AST.EmptyNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}EMPTY VECTOR")

    @addToClass(AST.AssignInstruction)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}{self.operator}")
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.RelationExpression)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}{self.op}")
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.IDRefNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}{self.value}")

    @addToClass(AST.ExpressionNode)
    def printTree(self, indent=0):
        self.expr.printTree(indent)

    @addToClass(AST.ZerosNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}ZEROS")
        print(f"{'|  ' * (indent + 1)}{self.arg}")

    @addToClass(AST.OnesNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}ONES")
        print(f"{'|  ' * (indent + 1)}{self.arg}")

    @addToClass(AST.EyeNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}EYE")
        print(f"{'|  ' * (indent + 1)}{self.arg}")

    @addToClass(AST.VectorNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}VECTOR")
        for value in self.values:
            value.printTree(indent + 1)

    @addToClass(AST.PrintableNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}PRINT")
        for value in self.values:
            value.printTree(indent)

    @addToClass(AST.ListOfPrintablesNode)
    def printTree(self, indent=0):
        # for value in self.values:
        #     print(f"{'|  ' * (indent + 1)}{value}")

        for value in self.values:
            value.printTree(indent+1)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        if self.index is not None:
            print(f"{'|  ' * indent}REF")
            self.name.printTree(indent+1)
            for e in self.index:
                e.printTree(indent+1)
        
    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}{self.value}")
        
    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}{self.value}")
        
    @addToClass(AST.UnaryMinusNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}-", end="")
        self.expr.printTree()
        
    @addToClass(AST.IDNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}{self.value}")

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}{self.name}")

    @addToClass(AST.TransposeNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}TRANSPOSE")
        self.expr.printTree(indent + 1)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}{self.op}")
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.ForNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}FOR")
        print(f"{'|  ' * (indent + 1)}{self.variable}")
        print(f"{'|  ' * (indent + 1)}RANGE")
        self.start.printTree(indent + 2)
        self.end.printTree(indent + 2)
        self.body.printTree(indent + 1)
        
    @addToClass(AST.WhileNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}WHILE")
        self.condition.printTree(indent+1)
        self.body.printTree(indent + 1)

    @addToClass(AST.IfElseNode)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}IF")
        self.condition.printTree(indent+1)
        print(f"{'|  ' * indent}THEN")
        self.if_body.printTree(indent + 1)

        if(self.else_body == None):
            return
        
        print(f"{'|  ' * indent}ELSE")
        self.else_body.printTree(indent + 1)

    @addToClass(AST.ReturnInstruction)
    def printTree(self, indent=0):
        print(f"{'|  ' * indent}RETURN")
        self.expr.printTree(indent+1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass    
        # fill in the body



#!/usr/bin/python
from collections import defaultdict
import AST

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

    def visit_BinExpr(self, node):
                                          # alternative usage,
                                          # requires definition of accept method in class Node
        type1 = self.visit(node.left)     # type1 = node.left.accept(self) 
        type2 = self.visit(node.right)    # type2 = node.right.accept(self)
        op    = node.op
        # ... 
        #
 

    def visit_Variable(self, node):
        pass
        



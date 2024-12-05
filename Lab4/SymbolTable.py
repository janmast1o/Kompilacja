#!/usr/bin/python
class Symbol:
    pass

class VariableSymbol(Symbol):

    def __init__(self, name, symbol_type):
        super().__init__()
        self.name = name
        self.symbol_type = symbol_type

    def __str__(self):
        return f"Variable: {self.name}, of type: {self.symbol_type}"


class SymbolTable(object):

    def __init__(self, st_parent = None, st_name = "global_scope"): # parent scope and symbol table name
        self.st_name = st_name
        self.st_parent = st_parent
        self.symbols = {}

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        if name in self.symbols:
            raise Exception(f"There already is a variable of name: {name} in scope {self.st_name}")
        else:
            self.symbols[name] = symbol

    def get(self, name): # get variable symbol or fundef from <name> entry
        if name in self.symbols:
            return self.symbols[name]
        elif self.st_parent is None:
            return None
        else:
            return self.st_parent.get(name)

    def getParentScope(self):
        return self.st_parent

    def pushScope(self, name=None):
        return SymbolTable(st_parent=self, st_name=name)

    def popScope(self):
        return self.st_parent

    def print_all_symbols(self):
        print(f"All symbols in {self.st_name}, whose parent is {self.st_parent}:")
        for key, val in self.symbols:
            print(f"{key}: {val}")

    def __str__(self):
        return f"{self.st_name}"



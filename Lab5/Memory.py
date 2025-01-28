class Memory:
    def __init__(self):
        self.memory_map = {}


    def has_key(self, name):
        return name in self.memory_map


    def put(self, name, value):
        self.memory_map[name] = value 


    def get(self, name):
        if self.has_key(name):
            return self.memory_map[name]

        return None


class MemoryStack:
    def __init__(self, parent = None, name = "global"):
        self.parent : MemoryStack = parent
        self.current_memory : Memory = Memory()
        self.mem_stack_name : str = name


    def get(self, name):
        # print(name)
        # print(type(name))
        # print(self.current_memory.memory_map)
        # print(self.current_memory.has_key(name))
        if self.current_memory.has_key(name):
            return self.current_memory.get(name)
        elif self.parent is not None:
            return self.parent.get(name)
        else:
            return None 
        

    def update_in_parent_scopes(self, name, value):
        if self.current_memory.has_key(name):
            self.current_memory.put(name, value)
            return True
        elif self.parent is not None:
            return self.parent.update_in_parent_scopes(name, value)
        else:
            return False      


    def put(self, name, value, override=True):
        if self.parent is not None and self.update_in_parent_scopes(name, value):
            return 
        if self.current_memory.has_key(name):
            if override:
                self.current_memory.put(name, value)
            else:
                print(f"Interpretor error: name {name} already in current memory scope, mark insertion as override insertion")

        else:
            self.current_memory.put(name, value)


    def push_scope(self, name):
        return MemoryStack(parent=self, name=name)     


    def pop_scope(self):
        return self.parent               
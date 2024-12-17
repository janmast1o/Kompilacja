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
    def __init__(self, parent = None, initial_stack_name = "global"):
        self.parent : MemoryStack = parent
        self.current_memory : Memory = Memory()
        self.mem_stack_name : str = initial_stack_name


    def get(self, name):
        if self.current_memory.has_key(name):
            return self.current_memory.get(name)
        elif self.parent is not None:
            return self.parent.get(name)
        else:
            return None 


    def put(self, name, value, override=True):
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
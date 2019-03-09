class SymbolTable():
    def __init__(self):
        self.table = dict()
        self.global_list = []
        self.parent = None
        self.extra = dict()

    def look_up(self, name):
        return (name in self.table)

    def insert(self, name, value, key = "type"):
        if not self.look_up(name):
            self.table[name] = dict([(key, value)])
            self.global_list += [name]

    def update(self, name, value, key):
        if not self.look_up(name):
            raise KeyError("Symbol " + str(name) + " does not exist.")
        else:
            self.table[name][key] = value

    def get_info(self, name):
        return self.table.get(name, None)

    def set_parent(self, parent):
        sef.parent = parent;

    def add_extra(self, value, key):
        self.extra[key] = value

class SymbolTable():
    def __init__(self):
        self.table = dict()                 # Dict of Dict (keeps key-value pairs for each item of dict)
        self.global_list = []               # Keeps track of all item's keys in the current table
        self.parent = None                  # A scope maybe a subscope some other scope, thus there maybe a parent
        self.extra = dict()                 # Any extra values required in the table goes here

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
        self.parent = parent;

    def add_extra(self, value, key):
        self.extra[key] = value

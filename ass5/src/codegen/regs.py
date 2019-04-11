class Register:
    def __init__(self, name):
        self.name = name
        self.temp = None
        self.location = None

    def save(self, temp, location = None):
        self.temp = temp
        if location != None:
            self.location = location

    def saver(self, reg):
        self.temp = reg.temp
        self.location = reg.location

    def printr(self):
        print(self.temp, self.location)
    
    def wb(self):
        if self.location != None:
            return ["movl " + self.name + ", " + self.location]
        else:
            assert (False), "Should not be here: " + self.temp

    def free(self):
        self.temp = None
        self.location = None

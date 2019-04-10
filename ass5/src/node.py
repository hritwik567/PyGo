class Node:
    def __init__(self):
        self.id_list = []       # For identifier
        self.code = []          # For 3AC
        self.type_list = []     # For types (like int etc.)
        self.place_list = []    # For temporary variables
        self.extra = {}         # Extra info in special cases like return type

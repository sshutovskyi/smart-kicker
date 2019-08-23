class Player:
    def __init__(self, id, name, key):
        self.id = id
        self.name = name
        self.key = key
    def __eq__(self, other):
        return self.id == other.id

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Building:
    def __init__(self, id, name, position):
        self.id = id
        self.name = name
        self.position = position

    def get_position(self):
        return self.position
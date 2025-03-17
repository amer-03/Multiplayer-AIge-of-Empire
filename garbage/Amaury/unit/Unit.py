class Unit:
    id_counter = 0

    def __init__(self, x, y, symbol):
        self.id = Unit.id_counter
        Unit.id_counter += 1
        self.x = x
        self.y = y
        self.symbol = symbol

    def get_symbol(self):
        return self.symbol
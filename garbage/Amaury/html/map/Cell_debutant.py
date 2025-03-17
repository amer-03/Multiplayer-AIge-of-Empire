# from vector import Vector

# class Cell:

#     def __init__ (self):
#         self.v = Vector()
#         self.e = Vector()
#         self.occupied = False
#         self.entity = None

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.unit = None  # Unité présente dans la cellule
        self.building = None  # Bâtiment dans la cellule

    def is_empty(self):
        return self.unit is None and self.building is None

    def add_unit(self, unit):
        """Ajoute une unité à cette cellule."""
        self.unit = unit

    def add_building(self, building):
        """Ajoute un bâtiment à cette cellule."""
        self.building = building

    def get_display_char(self):
        """Retourne le caractère pour afficher la cellule."""
        if self.building:
            return 'B'  # Affiche 'B' si un bâtiment est présent
        elif self.unit:
            return 'U'  # Affiche 'U' si une unité est présente
        else:
            return ' '  # Affiche un espace si la cellule est vide ' 

    def remove_unit(self):
        self.unit = None

    def remove_buildings(self):
        self.building = None

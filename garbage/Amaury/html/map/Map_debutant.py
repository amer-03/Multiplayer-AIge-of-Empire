from map.Cell_debutant import Cell

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y) for x in range(width)] for y in range(height)]
        self.units = []
        self.buildings = []

    def add_building(self, building):
        """Ajoute un bâtiment à la carte."""
        self.buildings.append(building)

    def get_unit_by_id(self, unit_id):
        for unit in self.units:
            if unit.id == unit_id:
                return unit
        return None

    def move_unit(self, unit, x, y):
        """Déplace une unité sur la carte si possible."""
        if 0 <= x < self.width and 0 <= y < self.height:
            old_cell = self.grid[unit.y][unit.x]
            new_cell = self.grid[y][x]
            if new_cell.is_empty():
                old_cell.remove_unit()
                new_cell.add_unit(unit)
                unit.x, unit.y = x, y
                return True
        return False
    
# from entity import Entity
# from cell import Cell
# from vector import Vector


# class Map:
#     n = 120
#     m = 120

#     def __init__ (self, n ,m):
#         self.m = m
#         self.n = n

#     def generate_map(self):
#         for i in range (self.n):
#             for j in range (self.m):
#                 self.tab[i][j] = Cell()

#     def add_entity(entity):
#         if(self.tab[entity.position[0]][entity.position[1]].occupied == True):
#             return 0
#         else:
#             self.tab[entity.position[0]][entity.position[1]].entity = entity 
#             return 1

#     def show_map(self):
#         for i in range (self.n):
#             for j in range (self.m):
#                 if(self.tab[i][j].occupied == True):
#                     print(f"{cell.entity.representation}", end=" ")
#                 else:
#                     print(" ")

#     def remove_entity(entity):
#         if(self.tab[entity.position[0]][entity.position[1]].occupied == True):
#             self.tab[entity.position[0]][entity.position[1]].entity = None
#             return 1
#         else:
#             return 0

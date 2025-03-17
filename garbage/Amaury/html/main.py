# main.py
# passer par des dictionnaires
# Importer les classes nécessaires
from map.Map_debutant import Map
from map.Cell_debutant import Cell
from unit.Unit import Unit
from unit.Buildings import Building  # Importer la classe Building
from unit.Buildings import Position
import random

def generate_html_file(buildings, units):
    with open("test_html_2.py", "r") as template_file:
        html_content = template_file.read()
    
    building_list_html = ""
    for building in buildings:
        building_list_html+=f"""<li class="building" > {building.get_position()}"""
    

    unit_list_html = ""
    for i, unit in enumerate(units, start=1):
        unit_list_html += f'<li class="unit">Villager {i} : {unit.get_x()}, {unit.get_y()}</li>'
    # unit_list_html = ""
    # for unit in units:
    #     unit_list_html+=f'<li class="unit" > {unit.get_x()}, {unit.get_y()}'
    
    # Replace the placeholder in the template with the actual building list
    html_content = html_content.replace("{{BUILDINGS}}", building_list_html)
    html_content = html_content.replace("{{UNITS}}", unit_list_html)

    # Write the modified HTML content to a new file
    with open("game_map.html", "w") as output_file:
        output_file.write(html_content)

class Game:
    def __init__(self):
        self.map = Map(width=10, height=10)  # Créer une carte de 10x10 par défaut
        self.running = True

    def display_map(self):
        """Affiche la carte avec les entités et bâtiments."""
        for row in self.map.grid:
            print(" ".join(cell.get_display_char() for cell in row))

    def process_command(self, command):
        """Analyse et exécute une commande utilisateur."""
        parts = command.split()
        if len(parts) == 0:
            return

        action = parts[0].lower()
        if action == "move" and len(parts) == 4:
            self.move_unit(int(parts[1]), int(parts[2]), int(parts[3]))
        elif action == "quit":
            self.running = False
        else:
            print("Commande inconnue.")

    def move_unit(self, unit_id, x, y):
        """Déplace une unité sur la carte."""
        unit = self.map.get_unit_by_id(unit_id)
        if unit:
            success = self.map.move_unit(unit, x, y)
            if success:
                print(f"L'unité {unit_id} a été déplacée.")
            else:
                print("Déplacement impossible.")
        else:
            print("Unité introuvable.")

    def run(self):
        """Boucle principale du jeu."""
        print("Bienvenue dans Age of Empire en Terminal !")
        while self.running:
            self.display_map()
            command = input("Entrez une commande : ")
            self.process_command(command)

if __name__ == "__main__":
    game = Game()

    random.seed()
    # Ajouter quelques unités
    # x_pos_1 = random.randint(0, 9)
    # y_pos_1 = random.randint(0, 9)
    # x_pos_2 = random.randint(0, 9)
    # y_pos_2 = random.randint(0, 9)
    unit1 = Unit(5, 6, "U1")
    unit2 = Unit(4, 3, "U2")
    game.map.units.append(unit1)
    game.map.grid[5][6].add_unit(unit1)  # Ajout de l'unité à la cellule
    game.map.units.append(unit2)
    game.map.grid[4][3].add_unit(unit2)  # Ajout de l'unité à la cellule

    # Ajouter quelques bâtiments
    position1 = Position(2, 2)  # Position (3, 3)
    building1 = Building(1, "Town Center", position1)  # Utilisation d'un objet Position
    position2 = Position(4,4)
    building2 = Building(2, "Barracks", position2)  # Position (4, 4)
    game.map.buildings.append(building1)
    game.map.grid[2][2].add_building(building1)  # Ajouter le bâtiment à la cellule
    game.map.buildings.append(building2)
    game.map.grid[4][4].add_building(building2)  # Ajouter le bâtiment à la cellule

    buildings = [building1,building2]
    units = [unit1,unit2]
    generate_html_file(buildings, units)
    # Lancer le jeu
    game.run()

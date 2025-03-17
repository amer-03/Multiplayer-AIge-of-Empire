import pygame
import sys
import json

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
TILE_SIZE = 50
MAP_WIDTH, MAP_HEIGHT = 10, 6  # 10x6 tuiles
SCREEN_WIDTH, SCREEN_HEIGHT = TILE_SIZE * MAP_WIDTH, TILE_SIZE * MAP_HEIGHT

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Save and Load Generic Objects")

# Couleurs
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Remplir le fond
screen.fill(WHITE)
pygame.display.flip()

# Fichier de sauvegarde
SAVE_FILE = "objects_save.json"

# Liste des objets (chaque objet est un dictionnaire)
objects = []

# Fonction pour ajouter un objet générique
def add_object(x, y):
    """Ajoute un objet générique à la liste et le dessine."""
    obj = {
        "x": x,
        "y": y,
        "type": "generic",  # Type d'objet
        "attributes": {"example_attr": "value"}  # Attributs d'exemple
    }
    objects.append(obj)
    draw_object(obj)  # Dessiner l'objet
    pygame.display.flip()

# Fonction pour dessiner un objet
def draw_object(obj):
    """Dessine un objet sur l'écran."""
    x, y = obj["x"], obj["y"]
    pygame.draw.circle(screen, BLUE, (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 3)

# Fonction pour sauvegarder les objets
def save_objects(filename):
    """Sauvegarde les objets dans un fichier JSON."""
    try:
        with open(filename, "w") as file:
            json.dump(objects, file)
        print(f"Objets sauvegardés dans {filename} !")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

# Fonction pour charger les objets
def load_objects(filename):
    """Charge les objets depuis un fichier JSON et les redessine."""
    global objects
    try:
        with open(filename, "r") as file:
            objects = json.load(file)
        print(f"Objets chargés depuis {filename} !")
        redraw_objects()
    except FileNotFoundError:
        print("Aucun fichier de sauvegarde trouvé.")
    except Exception as e:
        print(f"Erreur lors du chargement : {e}")

# Fonction pour redessiner tous les objets
def redraw_objects():
    """Efface l'écran et redessine tous les objets."""
    screen.fill(WHITE)  # Réinitialiser l'écran
    for obj in objects:
        draw_object(obj)
    pygame.display.flip()

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Ajouter un objet avec un clic gauche
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
            x, y = event.pos[0] // TILE_SIZE, event.pos[1] // TILE_SIZE
            print(f"Ajout d'un objet aux coordonnées : ({x}, {y})")
            add_object(x, y)

        # Sauvegarder les objets avec la touche "S"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            save_objects(SAVE_FILE)

        # Charger les objets avec la touche "L"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
            load_objects(SAVE_FILE)

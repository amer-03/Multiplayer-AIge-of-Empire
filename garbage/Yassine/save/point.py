import pygame
import sys
import json

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 600, 400

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Save and Load Points")

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Remplir le fond
screen.fill(WHITE)
pygame.display.flip()

# Liste pour stocker les points
points = []

# Fichier de sauvegarde
SAVE_FILE = "points.json"

# Fonction pour ajouter un point
def add_point(x, y):
    """Ajoute un point à la liste et le dessine sur l'écran."""
    points.append({"x": x, "y": y})  # Ajouter le point à la liste
    pygame.draw.circle(screen, RED, (x, y), 10)  # Dessiner un cercle rouge
    pygame.display.flip()  # Mettre à jour l'affichage

# Fonction pour sauvegarder les points dans un fichier JSON
def save_points(filename):
    """Sauvegarde les points dans un fichier JSON."""
    try:
        with open(filename, "w") as file:
            json.dump(points, file)
        print(f"Points sauvegardés dans {filename} !")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

# Fonction pour charger les points depuis un fichier JSON
def load_points(filename):
    """Charge les points depuis un fichier JSON et les redessine."""
    global points
    try:
        with open(filename, "r") as file:
            points = json.load(file)
        print(f"Points chargés depuis {filename} !")
        redraw_points()  # Redessiner tous les points
    except FileNotFoundError:
        print("Aucun fichier de sauvegarde trouvé.")
    except Exception as e:
        print(f"Erreur lors du chargement : {e}")

# Fonction pour redessiner tous les points
def redraw_points():
    """Efface l'écran et redessine tous les points."""
    screen.fill(WHITE)  # Effacer tout l'écran
    for point in points:
        x, y = point["x"], point["y"]
        pygame.draw.circle(screen, RED, (x, y), 10)  # Redessiner chaque point
    pygame.display.flip()

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Ajouter un point au clic gauche
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
            x, y = event.pos  # Coordonnées du clic
            print(f"Clic détecté aux coordonnées : ({x}, {y})")
            add_point(x, y)

        # Sauvegarder les points avec la touche "S"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            save_points(SAVE_FILE)

        # Charger les points avec la touche "L"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
            load_points(SAVE_FILE)

import pygame
import numpy as np

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
window_width, window_height = 800, 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Polygone inscrit dans une ellipse")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Paramètres initiaux
n = 6  # Nombre de sommets
largeur = 300
longueur = 200

# Fonction pour générer les sommets du polygone
def generer_polygone(n, largeur, longueur, centre_x, centre_y):
    a = largeur / 2  # Demi-grand axe
    b = longueur / 2  # Demi-petit axe
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    points = [
        (centre_x + a * np.cos(angle), centre_y + b * np.sin(angle))
        for angle in angles
    ]
    return points

# Boucle principale
running = True
clock = pygame.time.Clock()

while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # Augmenter le nombre de sommets
                n += 1
            elif event.key == pygame.K_DOWN and n > 3:  # Diminuer le nombre de sommets
                n -= 1
            elif event.key == pygame.K_RIGHT:  # Augmenter la largeur
                largeur += 10
            elif event.key == pygame.K_LEFT and largeur > 20:  # Diminuer la largeur
                largeur -= 10
            elif event.key == pygame.K_w:  # Augmenter la longueur
                longueur += 10
            elif event.key == pygame.K_s and longueur > 20:  # Diminuer la longueur
                longueur -= 10

    # Vérification pour empêcher un polygone invalide
    if n < 3:
        n = 3

    # Coordonnées du centre de l'ellipse
    centre_x, centre_y = window_width // 2, window_height // 2

    # Génération des sommets du polygone
    polygone_points = generer_polygone(n, largeur, longueur, centre_x, centre_y)

    # Dessin
    screen.fill(WHITE)  # Efface l'écran
    pygame.draw.rect(
        screen, BLACK, 
        (centre_x - largeur // 2, centre_y - longueur // 2, largeur, longueur), 2
    )  # Rectangle
    pygame.draw.polygon(screen, BLUE, polygone_points, 2)  # Polygone
    for point in polygone_points:
        pygame.draw.circle(screen, RED, (int(point[0]), int(point[1])), 5)  # Sommets

    # Affichage des instructions
    font = pygame.font.Font(None, 24)
    instructions = [
        f"Nombre de sommets: {n} (Flèches Haut/Bas pour modifier)",
        f"Largeur: {largeur} (Flèches Droite/Gauche pour modifier)",
        f"Longueur: {longueur} (Touches W/S pour modifier)",
        "Appuyez sur [ESC] pour quitter",
    ]
    for i, text in enumerate(instructions):
        label = font.render(text, True, BLACK)
        screen.blit(label, (10, 10 + i * 20))

    # Mise à jour de l'écran
    pygame.display.flip()
    clock.tick(30)

# Quitter Pygame
pygame.quit()

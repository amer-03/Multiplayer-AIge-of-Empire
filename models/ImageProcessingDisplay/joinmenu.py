import pygame
from GLOBAL_VAR import *
from ImageProcessingDisplay.imagemethods import adjust_sprite

class JoinMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(MEDIEVALSHARP, 28)

        # Rectangle noir central pour afficher les joueurs disponibles
        rect_width, rect_height = 400, 200
        self.players_rect = pygame.Rect(
            (screen.get_width() - rect_width) // 2,
            (screen.get_height() - rect_height) // 2,
            rect_width,
            rect_height
        )

        # Bouton "Join" sous le rectangle des joueurs
        self.join_button = pygame.Rect(
            screen.get_width() // 2 - 75,
            self.players_rect.bottom + 20,
            150,
            50
        )

    def draw(self):
        screen_width, screen_height = self.screen.get_size()

        # Affichage du fond
        self.screen.blit(adjust_sprite(START_IMG, screen_width, screen_height), (0, 0))

        # Rectangle noir pour les joueurs
        pygame.draw.rect(self.screen, (0, 0, 0), self.players_rect)

        # Texte d'en-tête du tableau (ID, IP)
        header_text = self.font.render("ID          IP", True, (255, 255, 255))
        self.screen.blit(header_text, (self.players_rect.x + 20, self.players_rect.y + 10))

        # Exemple d'un joueur connecté
        example_text = self.font.render("1       172.20.10.3", True, (255, 255, 255))
        self.screen.blit(example_text, (self.players_rect.x + 20, self.players_rect.y + 60))

        # Bouton "Join"
        pygame.draw.rect(self.screen, (128, 128, 128), self.join_button)
        join_text = self.font.render("Join", True, (255, 255, 255))
        join_text_rect = join_text.get_rect(center=self.join_button.center)
        self.screen.blit(join_text, join_text_rect)

    def handle_click(self, pos):
        if self.join_button.collidepoint(pos):
            print("Join button clicked!")
            return "join_clicked"
        return None

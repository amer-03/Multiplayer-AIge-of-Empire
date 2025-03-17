import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
UNIT_SIZE = 20
FPS = 60

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Define the Unit class
class Unit:
    def __init__(self, x, y, color, is_leader=False):
        self.x = x
        self.y = y
        self.color = color
        self.is_leader = is_leader
        self.path = []
        self.offset = (0, 0)  # For followers, their offset from the leader

    def set_path(self, path):
        self.path = path

    def move(self):
        if self.path:
            target = self.path[0]
            direction = (target[0] - self.x, target[1] - self.y)
            distance = math.hypot(direction[0], direction[1])
            if distance > 1:
                move_direction = (direction[0] / distance, direction[1] / distance)
                self.x += move_direction[0] * 2
                self.y += move_direction[1] * 2
            else:
                self.x, self.y = target
                self.path.pop(0)

    def update_follower_position(self, leader):
        # Followers maintain an offset from the leader
        self.x = leader.x + self.offset[0]
        self.y = leader.y + self.offset[1]

    def render(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), UNIT_SIZE)

# Setup the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Leader-Follower Movement")
clock = pygame.time.Clock()

# Create leader and followers
leader = Unit(100, 100, GREEN, is_leader=True)
followers = [Unit(120, 120, BLUE), Unit(140, 140, BLUE), Unit(160, 160, BLUE)]

# Set the formation offsets for followers (behind the leader in a line)
followers[0].offset = (-20, 0)  # First follower stays 20 pixels to the left of the leader
followers[1].offset = (0, 20)   # Second follower stays 20 pixels below the leader
followers[2].offset = (20, 0)   # Third follower stays 20 pixels to the right of the leader

# Example of a path to move the leader
leader.set_path([(200, 100), (200, 200), (400, 200)])

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the leader
    leader.move()

    # Update the followers' position based on leader's movement
    for follower in followers:
        follower.update_follower_position(leader)

    # Render the leader and followers
    leader.render(screen)
    for follower in followers:
        follower.render(screen)

    # Draw grid (optional for debugging)
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()

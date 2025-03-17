import heapq
import math
import time

from col import *



ONE_SEC = 1000

UNIT_IDLE = 0
UNIT_MOVING = 1
def is_almost(a, b, p=1e-7):
    return abs(a - b) < p

class PVector2:
    def __init__(self,_x,_y, _z = 0):
        global ID_GENERATOR

        self.x = _x #float
        self.y = _y #float
        self.z = _z # float
        self.representation = "V"

    def rotate_with_respect_to(self, theta, other):
        x = (self.x - other.x)*math.cos(theta) - (self.y - other.y) * math.sin(theta) + other.x
        y = (self.x - other.x)*math.sin(theta) + (self.y - other.y) * math.cos(theta) * other.y
        px_translated = self.x - other.x
        py_translated = self.y - other.y
        
        # Apply rotation using the 2D rotation matrix
        px_rot = px_translated * math.cos(theta) - py_translated * math.sin(theta)
        py_rot = px_translated * math.sin(theta) + py_translated * math.cos(theta)
        
        # Translate the point back
        px_rot += other.x
        py_rot += other.y
        
        self.x = px_rot
        self.y = py_rot
        
    def __add__(self,other_vector):
        return PVector2(self.x + other_vector.x,self.y + other_vector.y)

    def __mul__(self,const):
        return PVector2(self.x * const, self.y * const)

    def __rmul__(self,const):
        return PVector2(self.x * const, self.y * const)
    
    def __sub__(self,other_vector):
        return PVector2(self.x - other_vector.x,self.y - other_vector.y)

    def __eq__(self, other):
        return is_almost(self.x, other.x, 2) and is_almost(self.y, other.y, 2)
    
    def __lt__(self, other):
        return self.x <= other.x and self.y <= other.y 

    def __gt__(self, other):
        return self.x >= other.x and self.y >= other.y

    def abs_distance(self,other_vector):
        return math.sqrt((self.x - other_vector.x)**2 + (self.y - other_vector.y)**2)

    def alpha_angle(self, other_vector):
        delta_x = other_vector.x - self.x
        delta_y = other_vector.y - self.y
        return (math.atan2(delta_y, delta_x) + 2*math.pi)%(2*math.pi)    
    
    def __str__(self):
        return f"({self.x},{self.y},{self.z})"
padding = 20

class FormationNode:

    def __init__(self, position, direction):

        self.position = position
        self.direction = direction

        self.right = None
        self.left = None
        self.middle = None

        self.parent = None
        self.is_leader = False

        self.leader = None

    def link_to(self, parent, neighbor):

        self.parent = parent
        
        if parent.is_leader:
            self.leader = parent
        else:
            self.leader = parent.leader


        if neighbor == "right":
            
            parent.right = self

        elif neighbor == "left":
            parent.left = self
        elif neighbor == "middle":
            parent.middle = self
    
    def __repr__(self):
        return f"left{self.left}, right{self.right}, middle{self.middle}"
        

    
    
     
    
    def adjust_direction(self, amount):
        self.direction = (self.direction + amount + 2*math.pi) % (2*math.pi)
                

class Formation:
    
    def __init__(self, leader):
        self.leader = leader

    @classmethod
    def Create(cls, position, direction, depth):
        instance = cls.__new__(cls)
        leader = FormationNode(position, direction)
        leader.is_leader = True # make it the leader
        
        current_node = leader
        for wings_depth in range(depth, 0, -1):
            Formation.recursive_wings(current_node, wings_depth, neighbor="left")
            Formation.recursive_wings(current_node, wings_depth, neighbor="right")

            if wings_depth > 1:
                new_node = FormationNode(PVector2(current_node.position.x- padding*1.5, current_node.position.y ), current_node.direction)
                new_node.link_to(current_node, "middle")
                
                current_node = new_node
        
        instance.leader = leader

        return instance

    @staticmethod
    def recursive_wings(parent, wings_depth, neighbor):
        current_node = parent
        for _ in range(1, wings_depth + 1):
            new_node = FormationNode(
                PVector2(current_node.position.x - padding,
                         current_node.position.y - padding if neighbor == "left" else current_node.position.y + padding),
                current_node.direction
            )
            new_node.link_to(current_node, neighbor)
            current_node = new_node  # Move to the newly created node

    
    
    def update_formation_position(self):
        def update_position(node):

            if node != None:
                
                if node.is_leader == False:
                    parent = node.parent
                    node.direction = parent.direction
                    if parent.left == node:
                        node.position.x = parent.position.x - padding*math.cos(parent.direction)
                        node.position.y = parent.position.y - padding*math.sin(parent.direction)
                        
                    elif parent.right == node:
                        node.position.x = parent.position.x - padding*math.cos(parent.direction)
                        node.position.y = parent.position.y + padding*math.sin(parent.direction)
                    elif parent.middle == node:
                        node.position.x = parent.position.x - padding*math.cos(parent.direction)
                        node.position.y = parent.position.y 
        

        

import pygame

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Formation Visualization")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# FPS control
clock = pygame.time.Clock()

# Drawing function for FormationNode
def draw_node(screen, node, depth=0):
    if node is None:
        return
    
    # Draw current node
    pygame.draw.circle(screen, RED if node.is_leader else BLUE, (int(node.position.x), int(node.position.y)), 10)
    if node.parent:
        pygame.draw.line(screen, GREEN, (int(node.parent.position.x), int(node.parent.position.y)),
                         (int(node.position.x), int(node.position.y)), 2)
    
    # Draw left, right, and middle children recursively
    draw_node(screen, node.left, depth + 1)
    draw_node(screen, node.right, depth + 1)
    draw_node(screen, node.middle, depth + 1)

# Drawing function for the Formation
def draw_formation(screen, formation):
    screen.fill(WHITE)  # Clear the screen
    draw_node(screen, formation.leader)  # Draw nodes starting from the leader
    pygame.display.flip()  # Update the display

# Main Loop
def main():
    running = True
    last_time = pygame.time.get_ticks()

    # Create a formation
    leader_position = PVector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    formation = Formation.Create(leader_position, 0, depth=3)  # Adjust depth as needed

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if pygame.time.get_ticks() - last_time > 30:
            last_time =pygame.time.get_ticks()
            if keys[pygame.K_w]:
                formation.leader.adjust_direction(-math.radians(1))
                
            if keys[pygame.K_a]:
                formation.leader.adjust_direction(math.radians(1))
                
            if keys[pygame.K_s]:
                formation.leader.position.x += math.cos(formation.leader.direction)
                formation.leader.position.y += math.sin(formation.leader.direction)
        print(formation.leader.direction)
        # Draw formation
        draw_formation(screen, formation)

        clock.tick(60)  # Cap the frame rate to 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()

    
    
        
        





               
        
        
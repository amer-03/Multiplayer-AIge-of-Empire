import pickle

class A:
    def __init__(self, a):
        self.a = a 
        self.c = None
    def __repr__(self):
        return f" A:{self.a}" + (self.c.__repr__() if self.c is not None else "")
class B:
    def __init__(self, b):
        self.b = b
        self.c = None
    def __repr__(self):
        return f" B:{self.b}" + (self.c.__repr__() if self.c is not None else "")
class C:
    def __init__(self,c):
        self.c = c 
        self.obj = []
    def link(self, O):
        O.c = self
        self.obj.append(O)
    
    def __repr__(self):
        return f" C:{self.c}"


     

def save_object(file_name, obj):
        with open(file_name+".pkl", "wb") as outp:
            pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

def load_object(file_name):
    with open(file_name+".pkl", "rb") as inp:
        obj_outp =pickle.load(inp)

    return obj_outp
"""
_A = A(1)
_B = B(2)
_C = C(3)

_C.link(_A)
_C.link(_B)

save_object("Class", _C)
"""

"""
_C = load_object("Class")



_A = _C.obj[0]
_B = _C.obj[1]

_A.c.c = 10
print(_A)
print(_B)
"""

import pygame


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Create a building instance
T = 10

class build:

    def __init__(self, build_time):
        self.build_time = build_time
        self.build_progress = 0

        self.n = 0

    def b(self, dt):

        if self.n > 0:

            effective_time = (3*self.build_time * 1000)/(self.n + 2)

            progress = dt/effective_time
            
            self.build_progress += progress

            if self.build_progress >= 1:
                print("took ")
                print(pygame.time.get_ticks() - start)
                exit(0)
start = 0
# Game loop
b = build(T)
b.n = 3
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate delta time (in seconds)
    dt = clock.tick(60)
    b.b(dt)
    # Update the building progress
    

    # Draw the building and its progress
    screen.fill((0, 0, 0))  # Clear screen
   

    # Update the display
    pygame.display.flip()

pygame.quit()




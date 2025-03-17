

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

sep = 120

def Vcell(Y,X, d = 1):
    return  PVector2(sep/2 /d + sep*X/d, sep/2 /d + sep*Y/d)
class Entity:
    def __init__(self,Y,X,lm,sz, bs):
        self.Y = Y 
        self.X = X
        self.position =( Vcell((Y - sz + 1),(X - sz + 1)) + Vcell(Y,X))*(0.5)
        self.bs = bs/2 * (sep) 
        self.lm = lm
        self.sz = sz
        self.ShapeClass = None
    def track_cell(self):
        pass
    def collide_shape(self, shape):
        shape_self = self.ShapeClass(self.position.x, self.position.y, self.bs)

        return shape_self.collide_with(shape)

class Building(Entity):
    def __init__(self,Y,X,lm, bs = 4, sz= 2):
        
        super().__init__(Y,X,lm,sz, bs)
        self.ShapeClass = RoundedSquare
        self.bs = (sz/2.2 * (sep))
        
    def display(self, screen):
        half_side = self.bs
        self_shape = self.ShapeClass(self.position.x, self.position.y, self.bs)
        self_shape.draw(screen, (255,0,0))

class Unit(Entity):
    def __init__(self,Y,X, lm,bs = 1, sz = 1):
        super().__init__(Y,X,lm, sz, bs)
        self.ShapeClass = Circle
        self.bs = sep/4 /2
        self.last_time_moved = pygame.time.get_ticks()
        self.move_position = None
        self.path_to_position = None
        self.state = UNIT_IDLE
        self.direction = 0
        self.id = 0
        self.sz = 1
        self.speed = 0.5
        self.last_time_computed = pygame.time.get_ticks()

    def display(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), (int(self.position.x), int(self.position.y)), int(self.bs), 2)
        text_surface = Gfont.render(f"Y:{self.Y},X:{self.X}", True, (0,0,255))
        screen.blit(text_surface, (int(self.position.x - 18), int(self.position.y)))
    def track_cell(self):

        resX, resY = 0, 0
        smd = 1000
        for offsetY in range(-1,2):
            for offsetX in range(-1,2):
                currentY, currentX = self.Y + offsetY, self.X + offsetX
                currentD = self.position.abs_distance(Vcell(currentY, currentX))
                if currentD <smd:
                    smd = currentD
                    resY,resX = currentY, currentX
        uself = self.lm.remove_entity(self)
        self.Y, self.X = resY, resX

        self.lm.add_entity(self)

    def collided(self, entity, flags = 0):
        self_shape = self.ShapeClass(self.position.x, self.position.y, self.bs)
        ent_shape = entity.ShapeClass(entity.position.x, entity.position.y, entity.bs)
        alpha = self.position.alpha_angle(entity.position)
        op_alpha = alpha + math.pi
        Status = False
        
        """
        if isinstance(entity, Unit):
            if self_shape.collide_with(ent_shape):
                Status = True 
            if flags and Status:
                while self_shape.collide_with(ent_shape):
                    self.position.x += round(math.cos(op_alpha))
                    self.position.y += round(math.sin(op_alpha))
                    self_shape = self.ShapeClass(self.position.x, self.position.y, self.bs)
            if pygame.time.get_ticks() - self.last_time_computed > 1:
                self.last_time_computed = pygame.time.get_ticks()
                return Status
            return False
        else:
        """     
        if self_shape.collide_with(ent_shape):
            Status = True 
        if isinstance(entity, Unit):
            if pygame.time.get_ticks() - self.last_time_computed > 500:
                self.last_time_computed = pygame.time.get_ticks()
                if flags and Status:
                    while self_shape.collide_with(ent_shape):
                        self.position.x += round(math.cos(op_alpha))
                        self.position.y += round(math.sin(op_alpha))
                        self_shape = self.ShapeClass(self.position.x, self.position.y, self.bs)
                
                return Status
            else:
                return False
        if flags and Status:
            while self_shape.collide_with(ent_shape):
                self.position.x += round(math.cos(op_alpha))
                self.position.y += round(math.sin(op_alpha))
                self_shape = self.ShapeClass(self.position.x, self.position.y, self.bs)
        
        return Status
    def __repr__(self):
        return f"Unit id:{self.id}"
    def move_to_position(self,screen, _entity_optional_target = None):
        #self.check_and_set_path(_entity_optional_target)
        
        if self.state == UNIT_MOVING:
            if (self.check_collision_around()):
                self.check_and_set_path(_entity_optional_target)
            if (pygame.time.get_ticks() - self.last_time_moved > ONE_SEC*self.speed/60):
                
                self.last_time_moved = pygame.time.get_ticks()
                

                if self.path_to_position :
                    
                    amount_x = round(math.cos(self.direction))
                    amount_y = round(math.sin(self.direction))

                    print(f"amount_x: {amount_x}, amount_y:{amount_y}")
                    
                    
                    
                    
                    if self.path_to_position:
                        
                        # for debugging purposes
                        for i in range(len(self.path_to_position) - 1):
                            
                            (X1, Y1) = self.path_to_position[i] 
                            (X2, Y2) = self.path_to_position[i + 1] 
                            X1 -= 1
                            Y1 -= 1

                            X2 -= 1
                            Y2 -= 1
                            
                            cv1 = Vcell(Y1/3, X1/3)
                            cv2 = Vcell(Y2/3, X2/3)
                            # Draw a line between these two points
                            pygame.draw.line(screen, (46, 10, 0), (int(cv1.x), int(cv1.y)), (int(cv2.x),int(cv2.y)), 5)
                        

                        current_path_node_position = PVector2(self.path_to_position[0][0] * sep/CELL_DIVISION+ sep/2/CELL_DIVISION, self.path_to_position[0][1] * sep/CELL_DIVISION + sep/2/CELL_DIVISION)
                        self.direction = self.position.alpha_angle(current_path_node_position)
                        
                        self.position.x += amount_x
                        self.position.y += amount_y 

                        if self.position == current_path_node_position:
                            self.path_to_position = self.path_to_position[1:]
                else:
                    
                    self.check_and_set_path(_entity_optional_target)

            self.track_cell()

    def check_and_set_path(self, _entity_optional_target):
        start_X = math.floor(self.position.x/(sep/CELL_DIVISION))
        start_Y = math.floor(self.position.y/(sep/CELL_DIVISION))

        end_X = math.floor(self.move_position.x/(sep/CELL_DIVISION))
        end_Y = math.floor(self.move_position.y/(sep/CELL_DIVISION))
        self.path_to_position= A_STAR(start_X, start_Y ,end_X ,end_Y , self.lm,self, _entity_optional_target)
                
        if self.path_to_position != None:
            
            #pass
            if len(self.path_to_position):
                self.path_to_position = self.path_to_position[1:]
            
        else : 
            self.change_state(UNIT_IDLE)
    def changed_cell(self):
        topleft = PVector2(self.X*sep, self.Y*sep)
        bottomright = PVector2((self.X + 1)*sep, (self.Y + 1)*sep)

        return not(self.position < bottomright and self.position > topleft)
    
    def check_collision_around(self, _entity_optional_target = None): # this function is only made to se if we need to recalculate the path for the unit
        collided = False

        """
        for offsetY in [-1, 0, 1]:
            for offsetX in [-1, 0, 1]:

                currentY = self.Y + offsetY
                currentX = self.X + offsetX

                sset = self.lm.matrix.get((currentY, currentX), None)

                if sset:
                    for entity in sset:
                
                        if entity!= self and entity!= _entity_optional_target:

                            if self.collided(entity, flags= 1):
                                collided = True 
                                break             
                if (collided):
                    break
            if (collided):
                break
        """

        nextY = self.Y + round(math.sin(self.direction))
        nextX = self.X + round(math.cos(self.direction))

        for currentY, currentX in [(self.Y, self.X), (nextY, nextX)]:
            sset = self.lm.matrix.get((currentY, currentX), None)

            if sset:
                for entity in sset:
            
                    if entity!= self and entity!= _entity_optional_target:

                        if self.collided(entity, flags= 1):
                            collided = True 
                            break
        
        return collided


    def change_state(self, s):
        self.state = s

    def try_to_move(self, screen, _entity_optional_target = None):
        if _entity_optional_target:
            
            if self.collided(_entity_optional_target):
                
                if not(self.state == UNIT_IDLE):
                    self.change_state(UNIT_IDLE)
            else:
                
                if not(self.state == UNIT_MOVING):
                    self.change_state(UNIT_MOVING)
                    self.move_position = _entity_optional_target.position
                self.move_to_position(screen, _entity_optional_target)



def draw_square(screen, center, side_length, color, b = 1):
    
    half_side = side_length / 2
    top_left = (int(center[0] - half_side), int(center[1] - half_side))
    pygame.draw.rect(screen, color, (*top_left, side_length, side_length), b)
         

class Map:
    def __init__(self, Y, X):
        self.nY = Y
        self.nX = X
        self.matrix = {}

    def add_entity(self, entity):
        
        for Y_s in range(entity.Y, entity.Y - entity.sz, - 1):
            for X_s in range(entity.X, entity.X - entity.sz, - 1):
                
                s_sset = self.matrix.get((Y_s, X_s), None)

                if s_sset:
                    for s_entity in s_sset:
                        if isinstance(s_entity, Building):
                            return 0
                        
        for Y_s in range(entity.Y, entity.Y - entity.sz, - 1):
            for X_s in range(entity.X, entity.X - entity.sz, - 1):
                
                s_sset = self.matrix.get((Y_s, X_s), None)

                if not s_sset:
                    self.matrix[(Y_s, X_s)] = set()
                    s_sset = self.matrix.get((Y_s, X_s))
                
                s_sset.add(entity)

        return 1

    def remove_entity(self, entity):
        key = entity.Y, entity.X

        for Y_s in range(entity.Y, entity.Y - entity.sz, - 1):
            for X_s in range(entity.X, entity.X - entity.sz, - 1):
                
                s_sset = self.matrix.get((Y_s, X_s), None)

                if s_sset:
                    s_sset.discard(entity)
                if not s_sset:
                    self.matrix.pop((Y_s, X_s), None)
        return entity
        
    def update(self):
        for key in list(self.matrix.keys()):
            set = self.matrix.get(key,None)
            if set :
                for entity in set.copy():
                    entity.track_cell()
    
    def display(self,screen):
        for Y in range(0, self.nY):
            for X in range(0, self.nX):
                cv = Vcell(Y, X)
                sY,sX = Y*3,X*3
                for oY in range(3):
                    for oX in range(3):
                        tmpY,tmpX = sY + oY, sX + oX
                        ccv = Vcell(tmpY, tmpX,3)
                        draw_square(screen, (ccv.x, ccv.y), sep/3, (0, 0, 0))
                draw_square(screen, (cv.x, cv.y), sep, (220, 200, 120), 5)
        for sset in self.matrix.values():
            for entity in sset:
                entity.display(screen)



CELL_DIVISION = 3
class Node:
    def __init__(self, _X, _Y):
        self.X = _X
        self.Y = _Y
        self.G_cost = 0  # Cost from start node
        self.H_cost = 0  # Heuristic cost to target
        self.F_cost = 0  # Total cost
         
        self.previus = None
      

    def __lt__(self, other):
        return self.F_cost < other.F_cost or (self.F_cost == other.F_cost and self.H_cost < other.H_cost)

    def dist_to(self, other):
        return math.sqrt((other.X - self.X)**2 + (other.Y - self.Y)**2) * 10 

    def update_F_cost(self):
        self.F_cost = self.H_cost + self.G_cost

    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y

    def __str__(self):
        return f"({self.X},{self.Y}): G={self.G_cost} H={self.H_cost} F={self.F_cost}"

def arrounding_cells(startX, startY, the_moving_unit, _entity_optional_target, _map):
    def process_cell(currentY, currentX, ite_list):
        matY = currentY // CELL_DIVISION
        matX = currentX // CELL_DIVISION
        sset = _map.matrix.get((matY, matX), None)
        current_position = PVector2(currentX * (sep / CELL_DIVISION) + (sep / CELL_DIVISION) / 2,
                                    currentY * (sep / CELL_DIVISION) + (sep / CELL_DIVISION) / 2)
        current_shape = Square(current_position.x, current_position.y, sep / CELL_DIVISION / 2)
        current_C_cost = 0
        cell_walkable = True

        if sset:
            for entity in sset:
                if entity != the_moving_unit:
                    if entity.collide_shape(current_shape):
                        if entity == _entity_optional_target:
                            continue
                        elif isinstance(entity, Building):
                            s = entity.ShapeClass(entity.position.x, entity.position.y, entity.bs)
                            s.draw(screen, (255, 0, 23))
                            cell_walkable = False
                            break
                        else:
                            current_C_cost += 1

        if cell_walkable:
            ite_list.append(((currentY, currentX), current_C_cost))
            current_shape.draw(screen, (0, 255, 0))
        else:
            current_shape.draw(screen, (255, 0, 0))

    ite_list = []
    res = None

    if _entity_optional_target:
        top_Y = (_entity_optional_target.Y + 1) * CELL_DIVISION
        top_X = (_entity_optional_target.X + 1) * CELL_DIVISION
        sz = _entity_optional_target.sz

        bottom_Y = top_Y - sz * 3 - 1
        bottom_X = top_X - sz * 3 - 1

        # Top Boundary
        for Y in range(top_Y - 1, bottom_Y, -1):
            process_cell(Y, top_X, ite_list)

        # Right Boundary
        for X in range(top_X - 1, bottom_X, -1):
            process_cell(top_Y, X, ite_list)

        # Bottom Boundary
        for Y in range(bottom_Y + 1, top_Y):
            process_cell(Y, bottom_X, ite_list)

        # Left Boundary
        for X in range(bottom_X + 1, top_X):
            process_cell(bottom_Y, X, ite_list)

        if ite_list:
            res = sorted(
                ite_list,
                key=lambda item: (
                    item[1],  # Primary: crowd cost
                    math.sqrt((startX - item[0][1])**2 + (startY - item[0][0])**2)  # Secondary: distance
                )
            )[0][0]

    print(res)
    return res


def A_STAR(start_X, start_Y, end_X, end_Y, _map, the_moving_unit, _entity_optional_target = None):
    if not (0 <= start_X < _map.nX * CELL_DIVISION and 0 <= start_Y < _map.nY * CELL_DIVISION and 
            0 <= end_X < _map.nX * CELL_DIVISION and 0 <= end_Y < _map.nY * CELL_DIVISION):
        return None # Invalid start or end



    
    
    start_node = Node(start_X, start_Y)
    if _entity_optional_target:
        res = arrounding_cells(start_X, start_Y,the_moving_unit, _entity_optional_target, _map)
        if res == None:
            return res
        target_node = Node(res[1], res[0])
    else:
        target_node = Node(end_X, end_Y)

    start_node.H_cost = start_node.dist_to(target_node)
    start_node.update_F_cost()

    searching = []
    heapq.heappush(searching, (start_node.F_cost, start_node))

    discoverd = {}
    searched = set()

    
    collided_with_entity = False # these 3 variables are used in case we have an entity as target
    collision_node = None

    while searching:
        _, best_node = heapq.heappop(searching)
        
        # these conditions are have only sense when the target is an entity 
        # not a normal position path finding, but it doesnt affect 
        # the algo in the case of normal pathfinding

        ##found path !!###
        if best_node == target_node:
            # Reconstruct path
            path = []
            if _entity_optional_target:
                ent = []
                for offsetY in range(-1, 2):
                    for offsetX in range(-1, 2):
                        currentY = best_node.Y + offsetY
                        currentX = best_node.X + offsetX

                        matY = currentY // CELL_DIVISION
                        matX = currentX // CELL_DIVISION
                        sset = _map.matrix.get((matY, matX), None)

                        
                        if sset:
                            for entity in sset:
                                if entity == _entity_optional_target:
                                    ent.append((currentX, currentY))
                if len(ent) == 3:
                    path.append((ent[1][0], ent[1][1]))
                else:
                    path.append((ent[0][0],ent[0][1]))
            
            while best_node:
                path.append((best_node.X, best_node.Y))
                best_node = best_node.previus
            neighbor_position = PVector2(path[0][0] * (sep/CELL_DIVISION) + (sep/CELL_DIVISION)/2, path[0][1] * (sep/CELL_DIVISION) + (sep/CELL_DIVISION)/2)
            neighbor_shape = Square(neighbor_position.x, neighbor_position.y, sep/CELL_DIVISION/2)
            neighbor_shape.draw(screen, (255,52,1))
            
            path.reverse()
            print(path)
            return path
        ## end ##
        
        searched.add((best_node.X, best_node.Y))


        #for offsetY in [-1, 0, 1]:
        #    for offsetX in [-1, 0, 1]: # neighbors are the cells around
        for offsetY, offsetX in [(0, 1),(1,0),(-1,0),(0, -1)]:
            if collided_with_entity == False:
                neighbor_X = best_node.X + offsetX
                neighbor_Y = best_node.Y + offsetY

                neighbor_position = PVector2(neighbor_X * (sep/CELL_DIVISION) + (sep/CELL_DIVISION)/2, neighbor_Y * (sep/CELL_DIVISION) + (sep/CELL_DIVISION)/2)
                neighbor_shape = Square(neighbor_position.x, neighbor_position.y, sep/CELL_DIVISION/2)
                if (neighbor_X == best_node.X and neighbor_Y == best_node.Y ) or neighbor_X < 0 or neighbor_Y < 0 or neighbor_X >= _map.nX * CELL_DIVISION or neighbor_Y >= _map.nY * CELL_DIVISION: # not in bound
                    continue

                cell_walkable = True 

                #check if the current cellX and cellY contains entities 
                matY = neighbor_Y // CELL_DIVISION
                matX = neighbor_X // CELL_DIVISION
                mat_position = PVector2(matX * (sep) + (sep)/2, matY * (sep) + (sep)/2)
                
                text = FONT.render(f"Y:{matY},X:{matX}", True, (150,150,2))
                screen.blit(text, (int(mat_position.x) - 30, int(mat_position.y)))

                tt = Gfont.render(f"nY:{neighbor_Y},nX:{neighbor_X}", True, (0,150,190))
                screen.blit(tt, (int(neighbor_position.x - 18), int(neighbor_position.y)))
                
                
                sset = _map.matrix.get((matY, matX), None)

                current_C_cost = 0
                if sset:
                    for entity in sset:
                    
                        if entity != the_moving_unit:
                            if entity.collide_shape(neighbor_shape):
                                
                                

                                if isinstance(entity, Building):
                                    s = entity.ShapeClass(entity.position.x, entity.position.y, entity.bs)
                                    s.draw(screen, (255,0,23))
                                    cell_walkable = False
                                    break
                                else:
                                    current_C_cost += 10 # crowd cost 

                if not(cell_walkable):
                    neighbor_shape.draw(screen, (255, 0, 0))
                    continue
                neighbor_shape.draw(screen, (0, 255, 0))

                neighbor_node = discoverd.get((neighbor_Y, neighbor_X),None) 

                if neighbor_node is None: # we didnt discover this cell in the grid, so we create the node 
                    neighbor_node = Node(neighbor_X, neighbor_Y)
                    neighbor_node.G_cost = neighbor_node.dist_to(start_node) + current_C_cost
                    neighbor_node.H_cost = neighbor_node.dist_to(target_node)
                    neighbor_node.update_F_cost()
                    neighbor_node.previus = best_node

                    discoverd[(neighbor_Y, neighbor_X)] = neighbor_node # now it is discoverd and we need to explore it, push to the heap
                    heapq.heappush(searching, (neighbor_node.F_cost, neighbor_node)) # we push with respect to the F_cost, priority to the lowest F cost
                else:
                    current_G_cost = best_node.G_cost + best_node.dist_to(neighbor_node) + current_C_cost
                    if current_G_cost < neighbor_node.G_cost: # if it smaller, we found a path connected to this node, better than a previous one
                        neighbor_node.G_cost = current_G_cost # update its G cost
                        neighbor_node.update_F_cost()
                        neighbor_node.previus = best_node # connect the path
    return None # No path found



pygame.init()
screen_width, screen_height = 900, 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Draw Shapes")
FONT = pygame.font.Font(None, 36)
Gfont = pygame.font.Font(None, 13)
# Render the text

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
s = 7
mp = Map(s,s)
b = Building(2, 5,mp)
d = Building(5, 5, mp)
#mp.add_entity(d)
mp.add_entity(b)
dddv = Unit(0, 3, mp) # 6 4
dddv.id =0x3
l = []
import random
#"""
for i in range(5 * 3 * 4):
    Y, X = random.randint(0,s-1),random.randint(0,s-1)
    v = Unit(Y,X,mp)
    v.id = i+1
    while not(mp.add_entity(v)):
        Y, X = random.randint(0,s-1),random.randint(0,s-1)
        v.Y, v.X = Y, X
    l.append(v)


#"""
"""
row = s-1
line = 4
for i in range(row):
    for j in range(line):
        cv = Unit(i, j, mp)
        cv.id = i
        l.append(cv)

"""

print(mp.matrix)




# Game loop
clk = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousex, mousey = pygame.mouse.get_pos()
            boost = 30
    
            boost = 1
        
            a_Y, a_X = math.floor(mousey/sep), math.floor(mousex/sep)
            print(f"Y:{a_Y},X:{a_X}")
            dsl = Unit(a_Y, a_X, mp)
            dsl.id = 2
            dsl.position = PVector2(mousex, mousey)
            mp.add_entity(dsl)
            
    screen.fill((255, 255, 255))  # Clear screen with white background
    mp.display(screen)
    
    
    for v in l:
        v.try_to_move(screen, b)

    pygame.display.flip()  # Update the screen
    clk.tick(120)
pygame.quit()
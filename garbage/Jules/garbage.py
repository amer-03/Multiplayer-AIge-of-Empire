from entity import Entity
from cell import Cell
from vector import Vector



class Entity():
    def __init__(self, position, team, name, representation, SQ_size):
        self.position = position
        self.team = team
        self.name = name
        self.representation = representation
        self.SQ_size = SQ_size
        
    def is_alive(self):
        return self.hp>0


from ...entity import Entity
from ..projectile import PVector2
from ..projectile import Projectile
import time


class Unit(Entity):

    def __init(self, position, team, name, representation, SQ_size , hp, cost,training_time,speed,attack,range=1):
        super().__init(position, team, name, representation, SQ_size=1)
        self.hp = hp
        self.training_time=training_time
        self.attack=attack
        self.speed=speed
        self.cost=cost
        self.range=range
    
    def attacking(self,entity):
        lost_time_collect=time.time()
        vecteur_position=PVector2(self.position[0],self.position[1])
        vecteur_position_adverse =PVector2(entity.position[0],entity.position[1])
        while is_alive(entity) and abs_distance(vecteur_position_adverse) <=self.range:
            if time.time()-lost_time_collect==1:
                entity.hp-=self.attack
        if not is_alive(entity):
            map.remove_entity(entity)
        



1.archeryRange.py

from building import Building
from Unit import Archer

class archeryRange(Building):
    def __init__(self, position, team, name = "Archery Range", representation = "A", SQ_size = 3, hp = 500, cost = {"W" : 175}, build_time = 50, walkable = False, unit_spawn = None):
        super().__init__(position, team, name, representation, SQ_size, hp, cost, build_time, walkable)
        self.unit_spawn = unit_spawn
        

    def spawn_archers(self):
        if self.is_built:
            new_archer = Archer(self.position, self.team)
            return new_archer
        else:
            return None

    def spawn_archers():
        pass



2.barracks.py
from building import Building
from Unit.swordsman import Swordsman

class Barracks(Building):
    def __init__(self, position, team, name = "Barracks", representation = "B", SQ_size = 3, hp = 500, cost = {"W" : 175}, build_time = 50, walkable = False, unit_spawn = None):
        super().__init__(position, team, name, representation, SQ_size, hp, cost, build_time, walkable)
        self.unit_spawn = unit_spawn

    def spawn_swordsmen(self):
        
        if self.is_built:
            new_swordsman = Swordsman(self.position, self.team)
            return new_swordsman
        else:
            return None 


3.from entity import Entity
import time

class Building(Entity):
    def __init__(self, position, team, name, representation, SQ_size, hp, cost, build_time, walkable):

        super().__init__(position, team, name, representation, SQ_size)
        self.hp=hp
        self.cost=cost
        self.build_time=build_time
        self.walkable=walkable

        self.build_start_time = None  
        self.is_built = False
        self.population_increase = population_increase 

    
    def building_time(self, num_villagers):
        if num_villagers > 0:
            build_time = (3 * self.build_time) / (num_villagers + 2)
            return build_time
        else:
            return self.build_time

    def is_build(self, player_resources, num_villagers):
        if self.build_start_time is None:
            if player_resources['wood'] >= self.cost:
                player_resources['wood'] -= self.cost  
                self.build_start_time = time.time()  
                self.build_time = self.building_time(num_villagers)  
                print(f"{self.name} has started building with {num_villagers} villagers. Build time: {self.build_time:.2f} seconds")
            else:
                print(f"Not enough resources to build {self.name}.")
        else:
            elapsed_time = time.time() - self.build_start_time
            if elapsed_time >= self.build_time:
                self.is_built = True
                print(f"{self.name} has been completed!")
            else:
                remaining_time = self.build_time - elapsed_time
                print(f"{self.name} is under construction, remaining time: {remaining_time:.2f} seconds")

    def increase_population_limit(self, current_population_limit):
        if self.is_built:
            if self.name == "TownCentre" or self.name == "House":
                current_population_limit += self.population_increase  
                return current_population_limit 

4.camp
from building import Building

class Camp(Building):
    def __init__(self, position, team, name = "Camp", representation = "C", SQ_size = 2, hp = 200, cost = {"W" : 100}, build_time = 25, walkable = False, drop_point = True):
        super().__init__(position, team, name, representation, SQ_size, hp, cost, build_time, walkable)
        self.drop_point = drop_point


5.
from building import Building

class Farm(Building):
    def __init__(self, position, team, name = "Farm", representation = "F", SQ_size = 2, hp = 100, cost = {"W" : 60}, build_time = 10, walkable = True, inventory = {"F" : 0}, max_food = 300):
        super().__init__(position, team, name, representation, SQ_size, hp, cost, build_time, walkable)
        self.inventory = inventory
        self.max_food = max_food



6.house
from building import Building

class House(Building):

    def __init__(self, position, team, name = "House", representation = "H", SQ_size = 2, hp = 200, cost = {"W" : 25}, build_time = 25, walkable = False, population = 5):
        super().__init__(position, team, name, representation, SQ_size, hp, cost, build_time, walkable)
        self.population = population




7.keep
from building import Building

class Keep(Building):
    def __init__(self, position, team, name = "Keep", representation = "K", SQ_size = 1, hp = 800, cost = {"W" : 35, "G" : 125}, build_time = 80, walkable = False):
        super().__init__(position, team, name, representation, SQ_size, hp, cost, build_time, walkable)


8.Stable
from building import Building
from Unit import Horseman

class Stable(Building):
    def __init__(self, position, team, name = "Stable", representation = "S", SQ_size = 3, hp = 500, cost = {"W" : 175}, build_time = 50, walkable = False, unit_spawn = None):
        super().__init__(position, team, name, representation, SQ_size, hp, cost, build_time, walkable)
        self.unit_spawn = unit_spawn

    def spawn_horsemen(self):
        if self.is_built:
            new_horseman = Horseman(self.position, self.team) 
            return new_horseman
        else:
            return None


9.twoncenter
from building import Building
from Unit import Villager  

class TownCenter(Building):
    def __init__(self, position, team, name = "Town Center", representation = "T", SQ_size = 4, hp = 1000, cost = {"W" : 350}, build_time = 150, walkable = False, unit_spawn = None, drop_point = True, population_increase = 5):
        super().__init__(position, team, name, representation, SQ_size, hp, cost, build_time, walkable)
        self.unit_spawn = unit_spawn
        self.drop_point = drop_point
        self.population_increase = population_increase

    def spawn_villager(self):
        if self.is_built:
            new_villager = Villager(self.position, self.team) 
            return new_villager
        else:
            return None
        



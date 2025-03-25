class Habitat:
    def __init__(self, capacity):
        self.capacity = capacity  # Maximum units this habitat can hold
        self.current_population = 0


    def to_dict(self):
        return {
            "capacity":self.capacity,
            "current_population":self.current_population,
            '__class__':self.__class__.__name__
        }

    @classmethod
    def load(cls, from_dict):
        instance = cls.__new__(cls) # skip the constructor
        instance.capacity = from_dict['capacity']
        instance.current_population = from_dict['current_population']

        return instance

    def add_population(self):
        if self.current_population < self.capacity:
            self.current_population += 1
            return True
        return False
    def remove_population(self):
        if self.current_population > 0:
            self.current_population -= 1
            return True
        return False

    def available_space(self):
        return self.capacity - self.current_population

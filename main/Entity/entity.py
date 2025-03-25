from GLOBAL_VAR import *
from idgen import *
#from AITools.player import *
from shapely.geometry import Point, Polygon
import math
from shape import *
import ast
class Entity():
    def __init__(self, id_gen, cell_Y, cell_X, position, team, representation, sq_size = 1,id = None):
        self.cell_Y = cell_Y
        self.cell_X = cell_X
        self.position = position
        self.team = team
        self.representation = representation
        if id:
            self.id = id
        else:
            self.id = id_gen.give_ticket(team)
        self.sq_size = sq_size



        self.linked_map = None
        self.box_size = None
        self.hc = None # char not a class
        self.walkable = False

    def __repr__(self):
        return f"ent<{self.id},{self.representation},Y:{self.cell_Y},X:{self.cell_X},sz:{self.sq_size}>"

    def collide_with_shape(self, shape):
        Class = SHAPE_MAPPING.get(self.hc, None)

        shape_self = Class(self.position.x, self.position.y, self.box_size)

        return shape_self.collide_with(shape)

    def collide_with_entity(self, entity):

        Class = SHAPE_MAPPING.get(self.hc, None)
        shape_self = Class(self.position.x, self.position.y, self.box_size)

        entClass = SHAPE_MAPPING.get(entity.hc, None)
        ent_shape = entClass(entity.position.x, entity.position.y, entity.box_size)

        Status = False

        if shape_self.collide_with(ent_shape):
            Status = True
        # i wrote it like this on purpose incase there is some future update
        return Status

    def update(self, dt, camera = None, screen = None):
        return None

    def is_free(self):
        return True

    def to_json(self):
        attributes = self.__dict__.copy()

        if 'linked_map' in attributes:
            del attributes['linked_map'] # avoid saving the map
        attributes['__class__'] = self.__class__.__name__

        for key, value in list(attributes.items()):
            if hasattr(value, 'to_dict'):
                attributes[key] = value.to_dict() # special format for personal object
            elif hasattr(value, 'to_json'):
                attributes[key] = value.to_json() # special format for entit ( function itself )
            elif isinstance(value, dict):
                # Convert dict with non-string keys to a serializable format
                new_dict = {}
                for k, v in value.items():
                    if not isinstance(k, (str, int, float, bool)) or k is None:
                        # Convert non-string keys to string with a special format
                        new_key = f"__tuple__{str(k)}"
                    else:
                        new_key = k
                    new_dict[new_key] = v
                attributes[key] = new_dict
        return attributes

    @classmethod
    def load(cls, json):
        data = json.copy()

        for key, value in list(data.items()):
            if key != 'nonposition':
                if isinstance(value, dict): # check if it is a dict ( maybe an object that has been transformed to object )
                    new_dict = {}
                    for k, v in value.items():
                        if isinstance(k, str) and k.startswith("__tuple__"):
                            # Convert back to tuple
                            tuple_str = k[9:]  # Remove "__tuple__" prefix
                            # Safely evaluate the tuple string

                            tuple_key = ast.literal_eval(tuple_str)
                            new_dict[tuple_key] = v
                        else:
                            new_dict[k] = v

                    # If we made any conversions, replace the dict
                    if new_dict:
                        data[key] = new_dict
                    if '__class__' in value: # if __class__ in it then it is not

                        obj_class = JSON_MAPPING.get(value.pop('__class__', None)) # remove from the value the __class__ indicator, and put

                        if obj_class and hasattr(obj_class, 'load'): # recheck for the load method
                            data[key] = obj_class.load(value)


        instance = cls.__new__(cls) # skip the construtor

        for key, value in data.items():
            setattr(instance, key, value)

        instance.linked_map = None

        return instance

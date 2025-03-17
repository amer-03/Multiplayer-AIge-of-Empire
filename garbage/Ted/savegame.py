import json


class Savegame:
    def __init__(self, game_state, filename='savegame.json'):
        self.game_state = game_state
        self.filename = filename

    def save_game(self):
        data = {
            "map": self._save_map(),
            "entities": self._save_entities()
        }
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)
        print("Game saved successfully.")

    def load_game(self):
        with open(self.filename, 'r') as file:
            data = json.load(file)

        self._load_map(data["map"])
        self._load_entities(data["entities"])
        print("Game loaded successfully.")

    def _save_map(self):
        return {
            "nb_CellX": self.game_state.map.nb_CellX,
            "nb_CellY": self.game_state.map.nb_CellY
        }

    def _save_entities(self):
        entities = []
        for entity_id, entity in self.game_state.map.entity_id_dict.items():
            entity_data = {
                "id": entity.id,
                "type": type(entity).__name__,
                "x": entity.cell_X,
                "y": entity.cell_Y
            }
            # Ajouter l'HP uniquement si l'entité a cet attribut
            if hasattr(entity, 'hp'):
                entity_data["hp"] = entity.hp
            # Ajouter le stockage pour les ressources
            if hasattr(entity, 'storage'):
                entity_data["storage"] = entity.storage
            # Sauvegarder l'état des unités
            if isinstance(entity, Unit):
                entity_data["state"] = entity.state
                entity_data["direction"] = entity.direction
                entity_data["animation_frame"] = entity.animation_frame
                if entity.entity_target:
                    entity_data["target_id"] = entity.entity_target.id
            entities.append(entity_data)
        return entities

    def _load_map(self, map_data):
        self.game_state.map.nb_CellX = map_data["nb_CellX"]
        self.game_state.map.nb_CellY = map_data["nb_CellY"]

    def _load_entities(self, entities_data):
        for entity_data in entities_data:
            entity_type = entity_data["type"]
            x, y = entity_data["x"], entity_data["y"]
            
            if entity_type == "Archer":
                entity = Archer(y, x, PVector2(0, 0), 1)
                entity.hp = entity_data["hp"]
            elif entity_type == "Villager":
                entity = Villager(y, x, PVector2(0, 0), 2)
                entity.hp = entity_data["hp"]
            elif entity_type == "Gold":
                entity = Gold(y, x, PVector2(0, 0), 'g', entity_data["storage"])

            # Restaurer l'état des unités
            if isinstance(entity, Unit):
                entity.state = entity_data.get("state", UNIT_IDLE)
                entity.direction = entity_data.get("direction", 0)
                entity.animation_frame = entity_data.get("animation_frame", 0)
                target_id = entity_data.get("target_id")
                if target_id:
                    target = self.game_state.map.entity_id_dict.get(target_id)
                    if target:
                        entity.entity_target = target
                        entity.check_range_with_target = False
            self.game_state.map.add_entity(entity)
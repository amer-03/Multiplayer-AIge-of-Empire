import json

# Liste pour stocker les entités (chaque entité est un dictionnaire)
entities = []

# Fichier de sauvegarde
SAVE_FILE = "entities_save.json"

# Fonction pour ajouter une entité
def add_entity(id, name, entity_type, attributes):
    """Ajoute une entité à la liste."""
    entity = {
        "id": id,
        "name": name,
        "type": entity_type,
        "attributes": attributes
    }
    entities.append(entity)
    print(f"Entité ajoutée : {entity}")

# Fonction pour sauvegarder les entités
def save_entities(filename):
    """Sauvegarde les entités dans un fichier JSON."""
    try:
        with open(filename, "w") as file:
            json.dump(entities, file, indent=4)
        print(f"Entités sauvegardées dans {filename} !")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

# Fonction pour charger les entités
def load_entities(filename):
    """Charge les entités depuis un fichier JSON."""
    global entities
    try:
        with open(filename, "r") as file:
            entities = json.load(file)
        print(f"Entités chargées depuis {filename} :")
        for entity in entities:
            print(entity)
    except FileNotFoundError:
        print("Aucun fichier de sauvegarde trouvé.")
    except Exception as e:
        print(f"Erreur lors du chargement : {e}")

# Simulation d'ajout, de sauvegarde et de chargement d'entités
if __name__ == "__main__":
    # Ajouter des entités manuellement
    add_entity(1, "Hero", "Player", {"health": 100, "inventory": ["sword", "shield"]})
    add_entity(2, "Dragon", "Enemy", {"health": 300, "damage": 50})
    add_entity(3, "Potion", "Item", {"effect": "heal", "value": 50})

    # Sauvegarder les entités dans un fichier JSON
    save_entities(SAVE_FILE)

    # Charger les entités depuis le fichier JSON
    load_entities(SAVE_FILE)

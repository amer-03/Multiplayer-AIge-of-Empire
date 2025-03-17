from Entity.entity import Entity
from Entity.building import Building
from GameField.map import Map
from Player.player import Player
from decision_tree import tree  # Import the decision tree to use its structure.

class AIProfile:
    def __init__(self, strategy, aggressiveness=1.0, defense=1.0):
        """
        Initialize the AI profile with a specific strategy.
        :param strategy: Strategy type ('aggressive', 'defensive', 'balanced')
        :param aggressiveness: Aggressiveness level
        :param defense: Defense level
        """
        self.strategy = strategy
        self.aggressiveness = aggressiveness
        self.defense = defense

    def decide_action(self, context):
        """
        Decide the action to perform based on strategy and decision tree.
        :param context: Dictionary containing the current game state.
        :return: The chosen action as a string.
        """
        # Get the actions from the decision tree
        actions = tree.decide(context)

        # Call the appropriate strategy
        if self.strategy == "aggressive":
            return self._aggressive_strategy(actions, context)
        elif self.strategy == "defensive":
            return self._defensive_strategy(actions, context)
        elif self.strategy == "balanced":
            return self._balanced_strategy(actions, context)

    def _aggressive_strategy(self, actions, context):
        """
        Implement the aggressive strategy by prioritizing attacks and military training.
        """
        player = context['player']
        map = context['map']

        for action in actions:
            if action == "Attack the enemy!":
                # Attack the enemy with military units
                military_units = player.get_entities_by_class(['h', 'a', 's'])  # Get military units
                for unit_id in military_units:
                    unit = map.get_entity_by_id(unit_id)
                    unit.attack_entity(context['enemy_id'])  # Attack the enemy
                return "Executed attack strategy"

            if action == "Train military units!":
                # Train military units in training buildings
                training_buildings = context['buildings']['training']
                for building in training_buildings:
                    building['instance'].train_unit(player, context['current_time'], 'h')  # Train HorseMan
                return "Trained military units"

        # Default to gathering resources if no attack actions are possible
        return "Gather resources for further attacks"

    def _defensive_strategy(self, actions, context):
        """
        Implement the defensive strategy by focusing on repairs and defenses.
        """
        player = context['player']
        map = context['map']

        for action in actions:
            if action == "Defend the village!":
                # Defend the village by attacking enemies
                military_units = player.get_entities_by_class(['h', 'a', 's'])
                for unit_id in military_units:
                    unit = map.get_entity_by_id(unit_id)
                    unit.attack_entity(context['enemy_id'])  # Attack the enemy
                return "Executed defense strategy"

            if action == "Repair critical buildings!":
                # Repair damaged buildings
                buildings_to_repair = [
                    building for building in map.entity_matrix.values()
                    if isinstance(building, Building) and building.hp < building.max_hp
                ]
                for building in buildings_to_repair:
                    building.repair()  # Assuming a repair method exists in Building class
                return "Repaired critical buildings"

        # Default to building defensive structures
        return "Built defensive structures"

    def _balanced_strategy(self, actions, context):
        """
        Implement the balanced strategy by combining gathering, training, and attacks.
        """
        player = context['player']
        map = context['map']

        for action in actions:
            if action == "Gathering resources!":
                # Gather resources with villagers
                villagers = player.get_entities_by_class(['v'])
                for villager_id in villagers:
                    villager = map.get_entity_by_id(villager_id)
                    villager.collect_entity(context['resource_id'])  # Start collecting resources
                return "Gathered resources"

            if action == "Dropping off resources!":
                # Drop resources in storage buildings
                villagers = player.get_entities_by_class(['v'])
                for villager_id in villagers:
                    villager = map.get_entity_by_id(villager_id)
                    villager.drop_to_entity(context['drop_off_id'])  # Drop off resources
                return "Dropped off resources"

            if action == "Train military units!":
                # Train military units in training buildings
                training_buildings = context['buildings']['training']
                for building in training_buildings:
                    building['instance'].train_unit(player, context['current_time'], 'v')  # Train Villager
                return "Trained military units"

            if action == "Attack the enemy!":
                # Attack the enemy
                military_units = player.get_entities_by_class(['h', 'a', 's'])
                for unit_id in military_units:
                    unit = map.get_entity_by_id(unit_id)
                    unit.attack_entity(context['enemy_id'])  # Attack the enemy
                return "Executed attack strategy"

        # Default to gathering resources if no actions are possible
        return "Gathered resources for balanced strategy"

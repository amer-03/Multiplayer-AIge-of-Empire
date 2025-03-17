from GameField.map import Map
from ai_profiles import AIProfile
from Entity.entity import Entity
from Player.player import Player

class GameEventHandler:
    def __init__(self, map, players, ai_profiles):
        self.map = map
        self.players = players
        self.ai_profiles = ai_profiles

    def process_ai_decisions(self):
        for player_id, ai_profile in self.ai_profiles.items():
            context = self.get_context_for_player(player_id)
            actions = ai_profile.decide_action(context)
            print(f"Player {player_id} Actions: {actions}")

    def get_context_for_player(self, player_id):
        player = self.players[player_id]
        return {
            'under_attack': self.map.is_under_attack(player),
            'resources': player.resources,
            'military_units': len(player.get_entities_by_class(['h', 'a', 's'])),
            'military_units_details': {
                'archers': len(player.get_entities_by_class(['a'])),
                'infantry': len(player.get_entities_by_class(['s'])),
            },
            'enemy_visible': self.map.is_enemy_visible(player),
            'buildings': {
                'storage': player.has_building('storage'),
                'critical': player.get_critical_buildings(),
            },
            'enemy_distance': self.map.get_nearest_enemy_distance(player),
        }


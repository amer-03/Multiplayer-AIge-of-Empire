from jsonprocessor import *
class NetworkQueryFormatter:

    # All units
    @staticmethod
    def format_attack_entity(actor_id, target_id):
        """
        actor_id : unit performing the action
        build_target_id : enemy to attack

        initial call is unit.attack_entity(target_id)
        """

        return f"A/ae+{actor_id}:{target_id}" # ae :attack_entity easier and lighter to send in the packet

    # villager
    @staticmethod
    def format_villager_build_entity(actor_id, build_target_id): # we named it villager so that it is different from the player build_entity_function
        """
        actor_id : villager performing the action
        build_target_id : drop_target to collect

        initial call is villager.build_entity(build_target_id)
        """
        return f"A/vbe+{actor_id}:{build_target_id}" #vbe : villager_build_entity

    @staticmethod
    def format_drop_to_entity(actor_id, drop_target_id):
        """
        actor_id : villager performing the action
        drop_target_id : resource drop point

        initial call is villager.drop_to_entity(drop_target_id)
        """
        return f"A/dte+{actor_id}:{drop_target_id}" # dte : drop_to_entity

    @staticmethod
    def format_collect_entity(actor_id, resource_target_id):
        """
        actor_id : villager performing the action
        resource_target_id : resource to collect

        initial call is villager.collect_entity(resource_target_id)
        """
        return f"A/ce+{actor_id}:{resource_target_id}" # ce : collect_entity

    # traning building
    @staticmethod
    def format_train_unit(id_gen, actor_id, player_team, entity_repr):
        """
        actor_id : building performing the action
        player_id : team number of the player so we can get the player object from the map
        entity_repr : type of unit to train

        initial call is building.train_unit(player, entity_repr)
        """
        idticket = id_gen.team_tickets.get(player_team, None) - 1
        return f"A/tu+{idticket}:{actor_id}:{player_team}:{entity_repr}" # tu : train_unit

    # player
    @staticmethod
    def format_player_build_entity(id_gen, player_team, actors_id, representation = "", entity_id = None):

        """

        player_team : team number of the player so we can get the player object from the MAP
        actors_id : villagers id to perform the building
        representation : the type of the building, by default it is "" but why ?
        entity_id : when the representation is "" that means we want to continue the building of buildin that were being built, so give the id, and by default it is None means that we want to create a new one based on the representation

        initial call player.build_entity(villager_id_list, representation = "", entity_id = None)
        """

        idticket = id_gen.team_tickets.get(player_team, None) - 1 # - 1 cause the id has been used

        return f"A/pbe+{idticket}:{player_team}:{actors_id}:{representation}:{entity_id}" # pbe : player_build_entity

    @staticmethod
    def format_config_req():

        return f"R/config_req+{None}"

    @staticmethod
    def format_config_rep(seed, cellY, cellX, num_players, mode):

        """
        seed : map seed
        cellY : height of the map
        cellX : width of the map
        num_players : number of players
        mode : starting mode of the game

        """

        return f"R/config_resp+{seed}:{cellY}:{cellX}:{num_players}:{mode}"

    @staticmethod
    def format_create_entity_req(entity_id):
        """
        entity_id : the entity id we want to request its attr
        """
        return f"A/cerq+{entity_id}"

    @staticmethod
    def format_create_entity_rep(entity_json):
        """
        entity_json : dict of ONLY necessary attributes to create the entity ( NO CODE, key is the name of the attr ( can't be a method ) and the value int or str or list or dict)
        """
        return f"A/cerp+{JsonProcessor.to_string(entity_json)}"

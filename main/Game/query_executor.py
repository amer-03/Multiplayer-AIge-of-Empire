from GameField.map import *
from jsonprocessor import *
from network.QueryProcessing.networkqueryformatter import *
from network.QueryProcessing.networkqueryparser import *

import ast

class QueryExecutor:

    @staticmethod
    def exe_attack_entity(game_map, argsf, query_snd_queue, failed_queries, qfailed):

        args = argsf.split(":", 1) # 2 args

        actor_id = int(args[0]) # int actor_id
        target_id = int(args[1]) # int target_id

        sts = QueryExecutor.exe_verify_sync(game_map, [actor_id, target_id], query_snd_queue, qfailed)

        if not(sts):
            return sts

        game_map.get_entity_by_id(actor_id).attack_entity(target_id)

        return True



    @staticmethod
    def exe_verify_sync(game_map, actors_id, query_snd_queue, qfailed, build_action = False):

        print(f"=>verif !")
        status = True
        for aid in actors_id:
            if aid != None:
                entity = game_map.get_entity_by_id(aid)

                spawner = game_map.units_being_trained.get(aid, None)

                if spawner:
                    spawner.spawn_instantly()

                elif entity == None :
                    status = False

                    if not(qfailed): # if this is the first time it fails we send the request
                        query_snd_queue.append(NetworkQueryFormatter.format_create_entity_req(aid))

                elif isinstance(entity, Building) and not(build_action):

                    if entity.state == BUILDING_INPROGRESS:
                        print(f"+>instant")
                        entity.spawn_instantly()


        return status

    @staticmethod
    def exe_villager_build_entity(game_map, argsf, query_snd_queue, failed_queries, qfailed):

        args = argsf.split(":", 1) # 2 args

        actor_id = int(args[0]) # int actor_id
        build_target_id = int(args[1]) # int build_target_id

        sts = QueryExecutor.exe_verify_sync(game_map, [actor_id, build_target_id], query_snd_queue, qfailed, build_action = True)

        if not(sts):
            return sts

        game_map.get_entity_by_id(actor_id).build_entity(build_target_id)

        return True

    @staticmethod
    def exe_drop_to_entity(game_map, argsf, query_snd_queue, failed_queries, qfailed):

        args = argsf.split(":", 1) # 2 args

        actor_id = int(args[0]) # int actor_id
        drop_target_id = int(args[1]) # int drop_target_id

        sts = QueryExecutor.exe_verify_sync(game_map, [actor_id, drop_target_id], query_snd_queue, qfailed)

        if not(sts):
            return sts

        game_map.get_entity_by_id(actor_id).drop_to_entity(drop_target_id)


        return True

    @staticmethod
    def exe_collect_entity(game_map, argsf, query_snd_queue, failed_queries, qfailed):
        args = argsf.split(":", 1) # 2 args

        actor_id = int(args[0])

        resource_target_id = int(args[1])

        sts = QueryExecutor.exe_verify_sync(game_map, [actor_id, resource_target_id], query_snd_queue, qfailed)

        if not(sts):
            return sts

        game_map.get_entity_by_id(actor_id).collect_entity(resource_target_id)

        return True

    @staticmethod
    def exe_train_unit(game_map, argsf, query_snd_queue, failed_queries, qfailed):
        args = argsf.split(":", 2) # 3 args

        actor_id = int(args[0]) # int actor_id
        player_team = int(args[1]) # int player_team
        entity_repr = args[2] # char entity_rper

        sts = QueryExecutor.exe_verify_sync(game_map, [actor_id], query_snd_queue, qfailed)

        if not(sts):
            return sts

        game_map.get_entity_by_id(actor_id).train_unit(game_map.get_player_by_team(player_team), entity_repr)

        return True

    @staticmethod
    def exe_player_build_entity(game_map, argsf, query_snd_queue, failed_queries, qfailed):

        args = argsf.split(":", 3) # 4 args

        player_team = int(args[0]) # int player_team
        villager_id_list = ast.literal_eval(args[1]) # int[] villager id list
        _representation = args[2] # char represenation = ""
        _entity_id = ast.literal_eval(args[3]) # entity_id = None

        sts = QueryExecutor.exe_verify_sync(game_map, [_entity_id] + villager_id_list, query_snd_queue, qfailed, build_action = True)

        if not(sts):
            return sts

        game_map.get_player_by_team(player_team).build_entity(villager_id_list, representation = _representation, entity_id = _entity_id )

        return True

    def exe_create_entity_req(game_map, argsf, query_snd_queue, failed_queries, qfailed):
        entity_id = int(argsf) # one arg is the id of the object to send

        entity = game_map.get_entity_by_id(entity_id)
        print(entity)
        entity_json = entity.to_json()

        query = NetworkQueryFormatter.format_create_entity_rep(entity_json)

        return True

    def exe_create_entity_rep(game_map, argsf, query_snd_queue, failed_queries, qfailed):
        args = argsf # one arg is the string json
        json = JsonProcessor.to_json(args)

        cls = JSON_MAPPING.get(json.pop('__class__', None), None)

        obj = None

        if cls:
            obj = cls.load(json) # our personal load function

        exists = game_map.get_entity_by_id(obj.id)

        if exists:
            return True # dont add it

        game_map.add_entity(obj, from_json = True)

        return True

    _fct_map = {
            "ae": exe_attack_entity,
            "vbe": exe_villager_build_entity,
            "dte": exe_drop_to_entity,
            "ce": exe_collect_entity,
            "tu": exe_train_unit,
            "pbe": exe_player_build_entity,
            "cerq": exe_create_entity_req,
            "cerp": exe_create_entity_rep
        }

    @staticmethod
    def handle_query(game_map, query, query_snd_queue, failed_queries):
        status = None

        queryf = NetworkQueryParser.parse_query(query)

        if queryf["headerf"] == "A": # action type queries
            fct = QueryExecutor._fct_map.get(queryf["callf"], None)

            qfailed = (query in failed_queries)
            if fct != None:
                print(f"function :{queryf['callf']}")
                status = fct(game_map, queryf["argsf"], query_snd_queue, failed_queries, qfailed)

                if qfailed:
                    if status:
                        failed_queries.remove(query)

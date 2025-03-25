from GameField.map import *
from jsonprocessor import *
from network.QueryProcessing.networkqueryformatter import *
from network.QueryProcessing.networkqueryparser import *

import ast

class QueryExecutor:

    @staticmethod
    def exe_attack_entity(myteam, game_map, argsf, queue_snd_queue, failed_queries, qfailed):
        args = argsf.split(":", 1) # 2 args

        actor_id = int(args[0]) # int actor_id
        target_id = int(args[1]) # int target_id

        sts = QueryExecutor.exe_verify_sync(myteam, game_map, [actor_id, target_id], queue_snd_queue, qfailed)

        if not(sts):
            return sts

        game_map.get_entity_by_id(actor_id).attack_entity(target_id)

        return True



    @staticmethod
    def exe_verify_sync(myteam, game_map, actors_id, queue_snd_queue, qfailed, build_action = False):

        status = True
        for aid in actors_id:
            if aid != None:
                entity = game_map.get_entity_by_id(aid)

                spawner_id = game_map.units_being_trained.get(aid, None)

                spawner = game_map.get_entity_by_id(spawner_id)
                if spawner:
                    spawner.spawn_instantly()

                elif entity == None :
                    status = False

                    if not(qfailed): # if this is the first time it fails we send the request
                        queue_snd_queue.append(NetworkQueryFormatter.format_create_entity_req(aid))
                elif entity.netp == None:
                    status = False 
                    if not(qfailed):
                        queue_snd_queue.append(NetworkQueryFormatter.format_create_entity_req(aid))
                elif isinstance(entity, Building) and not(build_action):
                    if entity.state == BUILDING_INPROGRESS:
                        entity.spawn_instantly()


        return status

    @staticmethod
    def exe_villager_build_entity(myteam, game_map, argsf, queue_snd_queue, failed_queries, qfailed):

        args = argsf.split(":", 1) # 2 args

        actor_id = int(args[0]) # int actor_id
        build_target_id = int(args[1]) # int build_target_id

        sts = QueryExecutor.exe_verify_sync(myteam, game_map, [actor_id, build_target_id], queue_snd_queue, qfailed, build_action = True)

        if not(sts):
            return sts

        game_map.get_entity_by_id(actor_id).build_entity(build_target_id)

        return True

    @staticmethod
    def exe_drop_to_entity(myteam, game_map, argsf, queue_snd_queue, failed_queries, qfailed):

        args = argsf.split(":", 1) # 2 args

        actor_id = int(args[0]) # int actor_id
        drop_target_id = int(args[1]) # int drop_target_id

        sts = QueryExecutor.exe_verify_sync(myteam,game_map, [actor_id, drop_target_id], queue_snd_queue, qfailed)

        if not(sts):
            return sts

        game_map.get_entity_by_id(actor_id).drop_to_entity(drop_target_id)


        return True

    @staticmethod
    def exe_collect_entity(myteam, game_map, argsf, queue_snd_queue, failed_queries, qfailed):
        args = argsf.split(":", 1) # 2 args

        actor_id = int(args[0])

        resource_target_id = int(args[1])

        sts = QueryExecutor.exe_verify_sync(myteam,game_map, [actor_id, resource_target_id], queue_snd_queue, qfailed)

        if not(sts):
            return sts

        game_map.get_entity_by_id(actor_id).collect_entity(resource_target_id)

        return True

    @staticmethod
    def exe_train_unit(myteam, game_map, argsf, queue_snd_queue, failed_queries, qfailed):
        args = argsf.split(":", 3) # 4 args

        idticket = ast.literal_eval(args[0])
        actor_id = int(args[1]) # int actor_id
        player_team = int(args[2]) # int player_team
        entity_repr = args[3] # char entity_rper

        #if idticket != None:
        game_map.id_generator.team_tickets[player_team] = idticket # update the generator

        sts = QueryExecutor.exe_verify_sync(myteam,game_map, [actor_id], queue_snd_queue, qfailed)

        if not(sts):
            return sts

        game_map.get_entity_by_id(actor_id).train_unit(game_map.get_player_by_team(player_team), entity_repr)

        return True

    @staticmethod
    def exe_player_build_entity(myteam, game_map, argsf, queue_snd_queue, failed_queries, qfailed):

        args = argsf.split(":", 4) # 5 args

        idticket = ast.literal_eval(args[0])
        player_team = int(args[1]) # int player_team
        villager_id_list = ast.literal_eval(args[2]) # int[] villager id list
        _representation = args[3] # char represenation = ""
        _entity_id = ast.literal_eval(args[4]) # entity_id = None

        #if idticket != None:
        game_map.id_generator.team_tickets[player_team] = idticket # update the generator

        sts = QueryExecutor.exe_verify_sync(myteam,game_map, [_entity_id] + villager_id_list, queue_snd_queue, qfailed, build_action = True)

        if not(sts):
            return sts

        game_map.get_player_by_team(player_team).build_entity(villager_id_list, representation = _representation, entity_id = _entity_id )

        return True

    def exe_create_entity_req(myteam, game_map, argsf, queue_snd_queue, failed_queries, qfailed):
        entity_id = int(argsf) # one arg is the id of the object to send

        entity = game_map.get_entity_by_id(entity_id)

        if entity != None:

            if entity.netp == myteam:
                entity_json = entity.to_json()


                print(f"ENTITY TO SEND:{entity_json}")


                query = NetworkQueryFormatter.format_create_entity_rep(game_map.id_generator, entity.team, entity_json)
                queue_snd_queue.append(query)

        return True

    def exe_create_entity_rep(myteam, game_map, argsf, queue_snd_queue, failed_queries, qfailed):

        args = argsf.split(":", 2)# 3 args

        idticket = ast.literal_eval(args[0])
        player_team = int(args[1])

        game_map.id_generator.team_tickets[player_team] = idticket

        json = JsonProcessor.to_json(args[2])

        cls_name = json.pop('__class__', None)
        cls = JSON_MAPPING.get(cls_name, None)

        obj = None

        if cls:
            obj = cls.load(json) # our personal load function

        exists = game_map.get_entity_by_id(obj.id)

        player = game_map.get_player_by_team(obj.team)
        
        if exists:

            game_map.remove_entity(obj)

        else:

            print(f"ENTITY CREATED :{obj}")
            

            if isinstance(obj, Building):

                player.remove_resources(obj.cost)

        game_map.add_entity(obj, from_json = True)

        if isinstance(obj, Unit):
                

            player.add_population()
            player.current_population += 1

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
    def handle_query(myteam, game_map, query, queue_snd_queue, failed_queries, qfailed = False):
        status = None

        queryf = NetworkQueryParser.parse_query(query)

        if queryf["headerf"] == "A": # action type queries
            fct = QueryExecutor._fct_map.get(queryf["callf"], None)

            if fct != None:
                status = fct(myteam, game_map, queryf["argsf"], queue_snd_queue, failed_queries, qfailed)


                if status:
                    if qfailed:
                        failed_queries.remove(query)
                else:
                    if not qfailed:
                        failed_queries.add(query)

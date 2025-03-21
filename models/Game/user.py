from query_executor import *
from network.QueryProcessing.networkqueryparser import *

from collections import deque

class User:

    def __init__(self):
        self.communicator = None
        self.query_queue = deque()
        # run the c process here



        self.team = 1
        self.connected = False

    def add_query(self, query):

        self.query_queue.append(query)


    def get_query(self):

        if len(self.query_queue) > 0:

            return self.query_queue.popleft()

        return None

    def handle_all_queries(self, game_map):

        current_query = None

        while ((current_query := self.get_query()) != None):
            QueryExecutor.handle_query(game_map, NetworkQueryParser.parse_query(current_query))


    def update(self, dt, game_map):
        pass
        # packet_rcvd, addr = self.communicator.receive_packet()
        # if packet_rcvd != None:
            # self.add_query(packet_rcvd)

        # self.handle_all_queries(game_map)

        # packet_snd = game_map.get_player_by_team(self.team).think(dt)

        # if queryf != "":
            # self.communicator.send_packet(packet_snd)

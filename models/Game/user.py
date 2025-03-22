from Game.query_executor import *
#from network.QueryProcessing.networkqueryparser import *
# import comm here
from collections import deque

class User:

    def __init__(self):
        self.communicator = None
        self.query_rcv_queue = deque()
        self.query_snd_queue = deque()

        # run the c process here



        self.team = 1
        self.connected = False

    def add_query(self, query, flag):

        if flag == "r":
            self.query_rcv_queue.append(query)
        elif flag == "s":
            self.query_snd_queue.append(query)


    def get_query(self, flag):

        if flag == "r":
            if len(self.query_rcv_queue) > 0:

                return self.query_rcv_queue.popleft()

        elif flag == "s":
            if len(self.query_snd_queue) > 0:

                return self.query_snd_queue.popleft()

        return None

    def handle_all_rcv_queries(self, game_map):

        current_query = None

        while ((current_query := self.get_query("r")) != None):
            QueryExecutor.handle_query(game_map, NetworkQueryParser.parse_query(current_query))

    def handle_all_snd_queries(self):

        current_query = None

        while ((current_query := self.get_query("f")) != None):
            #self.communicator.send_packet(current_query)
            pass

    def update(self, dt, game_map):
        pass
        # packet_rcvd, addr = self.communicator.receive_packet()
        # if packet_rcvd != None:
            # self.add_query(packet_rcvd)

        # self.handle_all_rcv_queries(game_map)

        # game_map.get_player_by_team(self.team).think(dt, self.query_snd_queue)

        # self.handle_all_snd_queries()

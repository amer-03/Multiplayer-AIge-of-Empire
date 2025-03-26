
from Game.query_executor import *
from network.packettransport.python.CythonCommunicator import *
# import comm here

from collections import deque
import subprocess

class User:




    def __init__(self):
        self.communicator = CythonCommunicator(python_port=PYTHON_PORT, c_port=C_PORT)
        self.query_rcv_queue = deque()
        self.query_snd_queue = deque()
        self.failed_queries = set()

        # run the c process here
        script_dir = os.path.dirname(os.path.abspath(__file__))
        communicator_path = os.path.join(script_dir, "..", "network", "packettransport", "C", "communicator")
        #process = subprocess.Popen([communicator_path])
        print(f"Started communicator from: {communicator_path}")


        self.team = USER.id
        self.seed = 0xba5


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

        #print(f"failed queries: {self.failed_queries}")

        current_query = None

        for query in self.failed_queries.copy():
            QueryExecutor.handle_query(self.team, game_map, query, self.query_snd_queue, self.failed_queries, qfailed = True)

        while ((current_query := self.get_query("r")) != None):
            QueryExecutor.handle_query(self.team, game_map, current_query,self.query_snd_queue, self.failed_queries)

    def handle_all_snd_queries(self):

        current_query = None

        while ((current_query := self.get_query("s")) != None):
            self.communicator.send_packet(current_query)


    def update(self, dt, state):


        game_map = state.map 
        
        packet_rcvd, addr = self.communicator.receive_packet()
        if packet_rcvd != None and packet_rcvd[0] == "A":
            self.add_query(packet_rcvd, "r")
        elif packet_rcvd != None:
            self.handle_connection_queries(packet_rcvd, game_map)

        if self.connected:
            self.handle_all_rcv_queries(game_map)

            uplayer = game_map.get_player_by_team(self.team)

            if uplayer != None:
                uplayer.think(dt, self.query_snd_queue)

        self.handle_all_snd_queries()




    def handle_connection_queries(self, packet_rcvd, game_map):
        global ALL_PORT
        global HIDDEN_INFO
        queryf = NetworkQueryParser.parse_query(packet_rcvd)

        # D discovery response

        if queryf["headerf"] == "D":
            if self.connected: # in a game

                carte = 0  # normal then we se if we need to change it 

                if self.carte == "Carte Centrée":
                    carte = 1

                query = NetworkQueryFormatter.format_discover_response(game_map.seed, game_map.nb_CellX, game_map.nb_CellY, game_map.mode, carte,game_map.num_players)
                self.add_query(query, "s")

        elif queryf["headerf"] == "R":

            args = queryf["argsf"].split(":")

            seed = int(args[0]) # from python 
            cellX = int(args[1]) # from python 
            cellY = int(args[2]) # from python 
            mode = int(args[3]) # from python 
            carte = int(args[4]) # from python 
            player_num = int(args[5]) # from python 

            game_port = int(args[6]) # from c
            current_players = int(args[7]) # from  c

            ALL_PORT[port] = [cellX, cellY, mode, carte, player_num]
            HIDDEN_INFO[port] = [seed, current_players]
        # R bil table 

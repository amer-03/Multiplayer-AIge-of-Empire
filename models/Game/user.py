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

    def handle_all_queries(self):

        current_query = None

        while ((current_query := self.get_query()) != None):
            QueryExecutor.handle_query(NetworkQueryParser.parse_query(current_query))


    def update(self, game_map):

        # packet, addr = self.communicator.receive_packet()
        # if packet != None:
            # self.add_query(packet)

        self.handle_all_queries()

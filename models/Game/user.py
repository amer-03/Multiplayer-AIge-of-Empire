from query_executor import *
from network.QueryProcessing.networkqueryparser import *
from network.QueryProcessing.networkqueryformatter import *

from collections import deque

class User:

    def __init__(self):
        self.cython_comm = None
        self.query_queue = deque()

        self.team = 1
        self.connected = False


    def update(self, game_map):
        pass

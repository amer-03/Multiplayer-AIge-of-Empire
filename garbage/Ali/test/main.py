from collections import deque
import ast

class User:

    def __init__(self):
        self.cython_comm = None # communicator between the python and c to receive queries
        # run the c communicator

        self.query_queue = deque()

        self.team = None
        self.connected = False


    def add_query(self, query):

        self.query_queue.append(query)


    def get_query(self):

        if len(self.query_queue) > 0:

            return self.query_queue.popleft()

        return None


    def handle_queries(self):
        while ((cq := u.get_query()) != None):
            print(cq)

    def update(self):
        pass

u = User()
qn = 15
st = f"{1}:{[2,3,5]}:{''}:{None}"
print(st)

print(3 == ast.literal_eval(f"{int(3)}"))

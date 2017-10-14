"""
quiz2!

Use path finding algorithm to find your way through dark dungeon!

Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9

TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""
class PriorityN(object):
    """Node represents basic unit of graph"""
    def __init__(self, data, node):
        self.priority = data
        self.node  = node

    def __cmp__(self, other):
        if self.priority < other.priority:
            return -1
        elif self.priority == other.priority:
            return 0
        else:
            return 1

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority


import json
import codecs
from queue import *
import heapq


# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"

def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    body = {'id': room_id}
    return __json_request(GET_STATE_URL, body)

def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.

    You will be able to get the weight of edge between two rooms using this method
    """
    body = {'id': room_id, 'action': next_room_id}
    return __json_request(STATE_TRANSITION_URL, body)

def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    reader = codecs.getreader("utf-8")
    response = json.load(reader(urlopen(req, jsondataasbytes)))
    return response

if __name__ == "__main__":
    # Your code starts here
    empty_room = get_state('7f3dc077574c013d98b2de8f735058b4')
    print(empty_room)
    print('ekta')
    #delete giving start node id
    print(empty_room['id'])
    #print(empty_room['neighbors'])
    #print('shweta')
    dark_room = get_state('f1f131f647621a4be7c71292e79613f9')

    #for neig in empty_room['neighbors']:
    #    print(neig)

    #for neig in empty_room['neighbors']:
    #    print(neig['id'])
        #print(neig['effect'])

        #print(get_state(neig['id']))
    #print('ekta')
    print(transition_state(empty_room['id'], empty_room['neighbors'][0]['id']))

    q = Queue(maxsize=0)
    
    visited = []
    parent_dic = {}
    q.put(empty_room['id'])
    dis = []
    path_node = []
    
    while not(q.empty()):
        nei = []
       # print('empty room id', empty_room['id'])
        l = q.get()
        #print('lllllllllllll', l)
        #current_node = q.get()
        #print('current_node', l)
        
        
        current_node_state = get_state(l)
        #print('printing again', l)
        if l not in visited:
            #print('printing again', l)
            #getting the neighbors id
            for neig in current_node_state['neighbors']:
            #    print('printing again', l)
            #    print(neig['id'])
                nei.append(neig['id'])
            #traversing through the neighbor list
            for i in nei:
                q.put(i)
                if i not in dis:
                    parent_dic[i] = l
                dis.append(i)
            visited.append(l)
        
        if l == dark_room['id']:
            print('found')
            break

    #node1 = dark_room['id']
    #wei = 0
    #while True:
    #    if node1 in parent_dic:
    #        par = parent_dic[node1]
    #        wei = wei + int(par['effect'])
    #        node1 = par
    #    else:
    #        break
    print('found dark room', l == dark_room['id'])


    #DIJKSTRA
    heap1 = []
    neig = []
    visited = []
    predecessor_dic = {}
    distance_dic = {}
    heapq.heappush(heap1, PriorityN(0, empty_room['id']))
    distance_dic[initial_node] = 0
    path_node = []

    while heap1:
        c1 = heapq.heappop(heap1).node
        current_node_state = get_state(1)
        if c1 not in visited:   
            #neig = graph.neighbors(c1)
            #parsing neighbors of the current node
            for neig in current_node_state['neighbors']:
            #    print('printing again', l)
            #    print(neig['id'])
                nei.append(neig['id'])
            for n in neig:
                wei = graph.distance(c1, n)
                dist = wei + distance_dic[c1]
                if n in predecessor_dic:
                    dist_val = distance_dic[n]
                    #for changing the distance if found shorter distance
                    if dist < dist_val:
                        distance_dic[n] = dist
                        predecessor_dic[n] = c1 
                else:
                    predecessor_dic[n] = c1
                    distance_dic[n] = dist
                    heapq.heappush(heap1, PriorityN(dist, n))
            visited.append(c1)
        
        if c1 == dest_node:
            break
   
    #node1 = dest_node
    #while True:
    #    if node1 in predecessor_dic:
    #        par = predecessor_dic[node1]
    #        wei = graph.distance(par, node1)
    #        path_node.insert(0, g.Edge(par, node1, wei))
    #        node1 = par
    #    else:
    #        break
    
"""
quiz2!

Use path finding algorithm to find your way through dark dungeon!

Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9

TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""


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


class Node(object):
    """Node represents basic unit of graph"""
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'Node({})'.format(self.data)
    def __repr__(self):
        return 'Node({})'.format(self.data)

    def __eq__(self, other_node):
        return self.data == other_node.data
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.data)


class Edge(object):
    """Edge represents basic unit of graph connecting between two edges"""
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
    def __str__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)
    def __repr__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)

    def __eq__(self, other_node):
        return self.from_node == other_node.from_node and self.to_node == other_node.to_node and self.weight == other_node.weight
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.from_node, self.to_node, self.weight))


class AdjacencyList(object):
    """
    AdjacencyList is one of the graph representation which uses adjacency list to
    store nodes and edges
    """
    def __init__(self):
        # adjacencyList should be a dictonary of node to edges
        self.adjacency_list = {}

    def adjacent(self, node_1, node_2):
        if node_1 not in self.adjacency_list:
            return False

        for edge_val in self.adjacency_list[node_1]:
            if node_1 == edge_val.from_node and node_2 == edge_val.to_node:
                return True
        return False

    def neighbors(self, node):
        nei = []
        if node in self.adjacency_list:
            for edge_val in self.adjacency_list[node]:
                nei.append(edge_val.to_node)
        return nei

    def add_node(self, node):
        if node in self.adjacency_list:
            return False
        else:
            self.adjacency_list[node] = []
            return True

    def remove_node(self, node):
        if node not in self.adjacency_list:
            return False

        #To delete the node
        if node in self.adjacency_list:
            del self.adjacency_list[node]

        #Deleting the rest of edges linked to the node given
        for edge_val in self.adjacency_list.values():
            for edge in edge_val:
                if edge.to_node == node:
                    edge_val.remove(edge)
        return True

    def add_edge(self, edge):
        if edge.from_node not in self.adjacency_list:
            self.add_node(edge.from_node)

        if edge not in self.adjacency_list[edge.from_node]:
            self.adjacency_list[edge.from_node].append(edge)
            return True
        return False

    def remove_edge(self, edge):
        if edge in self.adjacency_list[edge.from_node]:
            self.adjacency_list[edge.from_node].remove(edge)
            return True
        return False

    def distance(self, node_1, node_2):
        if node_1 in self.adjacency_list:
            all_edges = self.adjacency_list[node_1]
            for edge1 in all_edges:
                if node_2 == edge1.to_node:
                    return edge1.weight
        return math.inf

def bfs(graph, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    sum1 = 0
    q = Queue(maxsize=0)
    neig = []
    visited = []
    parent_dic = {}
    q.put(initial_node)
    dis = []
    path_node = []

    while not(q.empty()):
        current_node = q.get()
        if current_node not in visited:
            neig = graph.neighbors(current_node)
            for i in neig:
                q.put(i)
                if i not in dis:
                    parent_dic[i] = current_node
                dis.append(i)
            visited.append(current_node)
        
        if current_node == dest_node:
            break
   
    node1 = dest_node
    
    while True:
        if node1 in parent_dic:
            par = parent_dic[node1]
            wei = graph.distance(par, node1)
            sum1 += wei
            path_node.insert(0, Edge(par, node1, wei))
            node1 = par
        else:
            break

    if path_node:
        print("Bfs_path: "+ str(path_node))
    else:
        print("Bfs_path: No Path Found!")

    print("total hp:", sum1)
 

def construct_graph(my_graph, list):

    queue = Queue(maxsize=0)
    queue.put(list['neighbors'][0]['id'])
    neigh = list['neighbors']
    add_q = set()
    add_q.add(list['id'])
    parent = list['id']

    while queue.qsize() > 0:
        for n in neigh:
            add_q.add(n['id'])
            weight = transition_state(parent, n['id'])
        
            if (n['id'] != '7f3dc077574c013d98b2de8f735058b4'):
                my_graph.add_edge(Edge(Node(parent),  Node(n['id']), weight['event']['effect']))
            if 'f1f131f647621a4be7c71292e79613f9' not in add_q:
                queue.put(n['id'])
        parent = queue.get()
        room = get_state(parent)
        neigh.clear()
        neigh = room['neighbors']
    
    return my_graph


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

def dijkstra_search(graph, initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    heap1 = []
    neig = []
    visited = []
    predecessor_dic = {}
    distance_dic = {}
    heapq.heappush(heap1, PriorityN(0, initial_node))
    distance_dic[initial_node] = 0
    path_node = []
    sum2 = 0
    print("entered dijkstra")

    while heap1:
        current_node = heapq.heappop(heap1).node
        #if current_node not in visited:   
        neig = graph.neighbors(current_node)
        #parsing neighbors of the current node
        for n in neig:
            if n not in visited:
                wei = graph.distance(current_node, n)
                dist = wei + distance_dic[current_node]
                if n not in predecessor_dic or dist > distance_dic[n]:
                    distance_dic[n] = dist
                    predecessor_dic[n] = current_node 
                    heapq.heappush(heap1, PriorityN(-(dist), n))
                        
        visited.append(current_node)
        
        if current_node == dest_node:
            break
   
    node1 = dest_node
    #print('before while')
    #print('node1',node1)
    #print('dic',predecessor_dic)
    sum2 = 0
    while True:
        if node1 in predecessor_dic:
            par = predecessor_dic[node1]
            wei = graph.distance(par, node1)
            sum2 += wei
            path_node.insert(0, Edge(par, node1, wei))
            node1 = par
        else:
            break

    
    if path_node:
        print("Dijkstra_path: " + str(path_node))
    else:
        print("Dijkstra_path: No Path Found!")

    print('Total hp:', sum2)

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
    #print(empty_room)

    graph = construct_graph(AdjacencyList(), empty_room)
    #bfs_path
    bfs(graph, Node('7f3dc077574c013d98b2de8f735058b4'), Node('f1f131f647621a4be7c71292e79613f9'))
    print()
    print()
    #dijkstra_path
    dijkstra_search(graph, Node('7f3dc077574c013d98b2de8f735058b4'), Node('f1f131f647621a4be7c71292e79613f9'))

    
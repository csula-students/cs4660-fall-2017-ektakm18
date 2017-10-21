"""
Searches module defines all different search algorithms
"""
from queue import *
from graph import graph  as g
import heapq

def bfs(graph, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
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
            path_node.insert(0, g.Edge(par, node1, wei))
            node1 = par
        else:
            break
    
    return path_node

def dfs(graph, initial_node, dest_node):
    """
    Depth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    stack = []
    neig = []
    visited = []
    parent_dic = {}
    stack.append(initial_node)
    path_node = []

    while (stack):
        current_node = stack.pop()
        if current_node not in visited:
            neig = graph.neighbors(current_node)
            neig.reverse()
            if neig:
                for i in neig:
                    stack.append(i)
                    parent_dic[i] = current_node
                visited.append(current_node)
        
        if current_node == dest_node:
            break
    
    node1 = dest_node
    while True:
        if node1 in parent_dic:
            par = parent_dic[node1]
            wei = graph.distance(par, node1)
            path_node.insert(0, g.Edge(par, node1, wei))
            node1 = par
        else:
            break
    
    return path_node


class PriorityN(object):

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

    while heap1:
        current_node = heapq.heappop(heap1).node
        if current_node not in visited:   
            neig = graph.neighbors(current_node)
            #parsing neighbors of the current node
            for n in neig:
                wei = graph.distance(current_node, n)
                dist = wei + distance_dic[current_node]
                if n in predecessor_dic:
                    dist_val = distance_dic[n]
                    #for changing the distance if found shorter distance
                    if dist < dist_val:
                        distance_dic[n] = dist
                        predecessor_dic[n] = current_node 
                else:
                    predecessor_dic[n] = current_node
                    distance_dic[n] = dist
                    heapq.heappush(heap1, PriorityN(dist, n))
            visited.append(current_node)
        
        if current_node == dest_node:
            break
   
    node1 = dest_node
    while True:
        if node1 in predecessor_dic:
            par = predecessor_dic[node1]
            wei = graph.distance(par, node1)
            path_node.insert(0, g.Edge(par, node1, wei))
            node1 = par
        else:
            break
    #print('dijk')
    return path_node

def heuristic(a, b):
   # Manhattan distance on a square grid
   return abs(a.x - b.x) + abs(a.y - b.y)

def a_star_search(graph, initial_node, dest_node):
    """
    A* Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    heap1 = []
    neig = []
    #visited = []
    predecessor_dic = {}
    distance_dic = {}
    
    heapq.heappush(heap1, PriorityN(0, initial_node))
    distance_dic[initial_node] = 0
    path_node = []
    #sum2 = 0
    #print("entered dijkstra")

    while heap1:
        current_node = heapq.heappop(heap1).node
        #if current_node not in visited:   
        neig = graph.neighbors(current_node)
        #parsing neighbors of the current node
        for n in neig:
            wei = graph.distance(current_node, n)
            dist = wei + distance_dic[current_node]
            if n not in distance_dic or dist < distance_dic[n]:
                distance_dic[n] = dist
                predecessor_dic[n] = current_node 
                total = dist + heuristic(current_node.data, n.data)
                heapq.heappush(heap1, PriorityN(total, n))
                        
        #visited.append(current_node)
        
        if current_node == dest_node:
            break

    node1 = dest_node
    #print('before while')
    #print('node1',node1)
    #print('dic',predecessor_dic)
    #sum2 = 0
    #print('parent', predecessor_dic)
    while True:
        if node1 in predecessor_dic:
            par = predecessor_dic[node1]
            wei = graph.distance(par, node1)
    #        sum2 += wei
            path_node.insert(0, g.Edge(par, node1, wei))
            node1 = par
        else:
            break
    
    #print('path_a', path_node)
    return path_node
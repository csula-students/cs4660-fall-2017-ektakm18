"""
utils package is for some quick utility methods

such as parsing
"""
from .graph import Edge
from .graph import Node

class Tile(object):
    """Node represents basic unit of graph"""
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def __str__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)
    def __repr__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y and self.symbol == other.symbol
        return False
    
    def __lt__(self, other):
        return self.x < other.x or self.y < other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self.x) + "," + str(self.y) + self.symbol)



def parse_grid_file(graph, file_path):
    """
    ParseGridFile parses the grid file implementation from the file path line
    by line and construct the nodes & edges to be added to graph

    Returns graph object
    """
    # TODO: read the filepaht line by line to construct nodes & edges

    # TODO: for each node/edge above, add it to graph

    grid = []
    tiles = {}

    #print('method')
    with open(file_path) as file:
        next(file)
    
        for line in file:
            line.strip().split("\n")
            grid.append([line[i:i + 2] for i in range(1, len(line[1:-1]), 2)])
 

    #print('before for')
    #ignoring the last line
    grid = grid[:-1]
 
    for i in range( len(grid) ):
        for j in range( len(grid[0]) ):
            tiles[ (j, i) ] = Tile(j, i, grid[i][j])
    
    #creating
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            
            current_node = Tile(j, i, grid[i][j])
            if current_node.symbol == "##":
                continue

            if (j + 1, i) in tiles:
                right = tiles[(j + 1, i)]

                if right.symbol != "##":
                    graph.add_edge(Edge (Node(current_node), Node(right), 1))

            if (j - 1, i) in tiles:
                
                left = tiles[(j - 1, i)]
                if left.symbol != "##":
                    graph.add_edge(Edge (Node(current_node), Node(left), 1))

            if (j, i + 1) in tiles:

                low = tiles[(j, i + 1)]
                if low.symbol != "##":
                    graph.add_edge(Edge (Node(current_node), Node(low), 1))

            if (j, i - 1) in tiles:
                up = tiles[(j, i - 1)]
                if up.symbol != "##":
                    graph.add_edge(Edge (Node(current_node), Node(up), 1))          
    
    #print('graph', graph)
    return graph


def convert_edge_to_grid_actions(edges):
    """
    Convert a list of edges to a string of actions in the grid base tile

    e.g. Edge(Node(Tile(1, 2), Tile(2, 2), 1)) => "S"
    """
    path = ""
    direct = { (0,0):"", (1,0):"W", (-1,0):"E", (0,1):"N", (0,-1):"S" }
    if edges:
        for edge1 in edges:
            tile1 = edge1.from_node.data
            tile2 = edge1.to_node.data
            path = path + direct[ (tile1.x - tile2.x) , (tile1.y - tile2.y) ]

    #print('path', path)
    return path
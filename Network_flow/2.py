class Node:
    def __init__(self, name):
        self.name = name
        self.neighbours = []
        self.visited = False
        self.is_start = False
        self.is_sink = False
        
class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.capacity = 1
        self.flow = 0
        self.visited = False

def max_flow(nodes, start):
    # Find a path from start to sink
    def find_path(node, path):
        if node.is_sink:
            return path
        for neighbour in node.neighbours:
            if neighbour.flow < neighbour.capacity and not neighbour.visited:
                neighbour.visited = True
                result = find_path(neighbour.end, path + [neighbour])
                if result:
                    return result
        return None
    
    # Increase the flow along the path
    def increase_flow(path):
        min_capacity = min(edge.capacity - edge.flow for edge in path)
        for edge in path:
            edge.flow += min_capacity
            edge.visited = False
    
    while True:
        path = find_path(start, [])
        if path is None:
            break
        increase_flow(path)
    
    return sum(edge.flow for edge in start.neighbours)

# Read the input
n, m = map(int, input().split())
nodes = {}
for i in range(n):
    nodes[i] = Node(i)

nodes[0].is_start = True
nodes[n-1].is_sink = True

for _ in range(m):
    i, j = map(int, input().split())
    i, j = i-1, j-1
    new_edge = Edge(nodes[i], nodes[j])
    nodes[i].neighbours.append(new_edge)

# Find the maximum flow
print(max_flow(nodes, nodes[0]))

# Find the path
def find_path(nodes, start):
    def find_path(node, path):
        if node.is_sink:
            return path
        for neighbour in node.neighbours:
            if neighbour.flow == 1 and not neighbour.visited:
                neighbour.visited = True
                result = find_path(neighbour.end, path + [neighbour])
                if result:
                    return result
        return None

    while True:
        path = find_path(start, [])
        if path is None:
            break
        if len(path) == 0 or not path[0].start.is_start or not path[-1].end.is_sink:
            break
        print(len(path)+1)
        node_in_path = []
        last_node = -1
        for edge in path:
            if edge.start.name != last_node:
                node_in_path.append(edge.start)
                last_node = edge.start.name
            if edge.end.name != last_node:
                node_in_path.append(edge.end)
                last_node = edge.end.name
        print(' '.join(str(node.name + 1) for node in node_in_path))

find_path(nodes, nodes[0])
class Node:
    def __init__(self, name):
        self.name = name
        self.is_source = False
        self.is_sink = False
        self.edge = []

class edge:
    def __init__(self, to, capacity):
        self.to = to
        self.capacity = capacity
        self.flow = 0

def read_input():
    n = int(input().strip())
    grid = []
    for _ in range(2 * n - 1):
        grid.append(list(input().strip()))
    return n, grid

def create_nodes(n, grid):
    source = Node('source')
    sink = Node('sink')
    source.is_source = True
    sink.is_sink = True
    
    # nodes = [[Node()] * n] * n
    nodes = [[Node((i,j)) for i in range(n)] for j in range(n)]
    
    for i in range(n):
        for j in range(n):
            is_left = (i + j) % 2 == 0
            i_grid = 2 * (i+1) - 1
            j_grid = 2 * (j+1) - 1
            
            count = 0
            count_out_of_range = 0
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if grid[i_grid + di][j_grid + dj] == '|' or grid[i_grid + di][j_grid + dj] == '-':
                    continue
                count += 1
                if 0 <= ni < n and 0 <= nj < n:
                    if is_left:
                        new_edge = edge(nodes[ni][nj], 1)
                        nodes[i][j].edge.append(new_edge)
                else:
                    count_out_of_range += 1

            if count_out_of_range > 0:
                if is_left:
                    new_edge = edge(sink, count_out_of_range)
                    nodes[i][j].edge.append(new_edge)
                else:
                    new_edge = edge(nodes[i][j], count_out_of_range)
                    source.edge.append(new_edge)
        
            if count - 1 > 0:
                if is_left:
                    new_edge = edge(nodes[i][j], count - 1)
                    source.edge.append(new_edge)
                else:
                    new_edge = edge(sink, count - 1)
                    nodes[i][j].edge.append(new_edge)
                
    return source, sink

def solve(source, sink):
    from collections import deque

    def bfs(source, sink):
        parent = {}
        visited = set()
        queue = deque([source])
        visited.add(source)

        while queue:
            current = queue.popleft()

            if current == sink:
                path = []
                while current in parent:
                    path.append(current)
                    current = parent[current]
                path.append(source)
                return path[::-1]

            for edge in current.edge:
                if edge.to not in visited and edge.capacity > edge.flow:
                    visited.add(edge.to)
                    parent[edge.to] = current
                    queue.append(edge.to)

        return None

    def edmonds_karp(source, sink):
        max_flow = 0

        while True:
            path = bfs(source, sink)
            if not path:
                break

            path_flow = float('inf')
            for i in range(len(path) - 1):
                current = path[i]
                next_node = path[i + 1]
                for edge in current.edge:
                    if edge.to == next_node:
                        path_flow = min(path_flow, edge.capacity - edge.flow)

            for i in range(len(path) - 1):
                current = path[i]
                next_node = path[i + 1]
                for edge in current.edge:
                    if edge.to == next_node:
                        edge.flow += path_flow
                        break

                for edge in next_node.edge:
                    if edge.to == current:
                        edge.flow -= path_flow
                        break

            max_flow += path_flow

        return max_flow

    # Example usage
    # Create nodes and add edges
    # Call edmonds_karp(source_node, sink_node)
    return edmonds_karp(source, sink)



n, grid = read_input()
source, sink = create_nodes(n-1, grid)
print(solve(source, sink))
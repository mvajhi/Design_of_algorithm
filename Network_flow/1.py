from collections import defaultdict, deque

def max_flow(capacity, source, sink):
    """
    Implements Edmonds-Karp algorithm to find the maximum flow.
    """
    n = len(capacity)
    flow = [[0] * n for _ in range(n)]
    total_flow = 0

    while True:
        parent = [-1] * n
        parent[source] = source
        queue = deque([source])
        while queue and parent[sink] == -1:
            u = queue.popleft()
            for v in range(n):
                if parent[v] == -1 and capacity[u][v] - flow[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
                    if v == sink:
                        break
        if parent[sink] == -1:
            break

        increment = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            increment = min(increment, capacity[u][v] - flow[u][v])
            v = u

        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += increment
            flow[v][u] -= increment
            v = u

        total_flow += increment

    return total_flow

def solve(n, grid):
    m = 2 * n - 1
    black_nodes = []
    white_nodes = []
    capacity = defaultdict(lambda: defaultdict(int))
    
    # Node indices
    def node_index(x, y):
        return x * m + y

    source = m * m
    sink = source + 1

    # Process grid and assign capacities
    for i in range(n):
        for j in range(n):
            x, y = 2 * i, 2 * j
            if (i + j) % 2 == 0:
                black_nodes.append((x, y))
                capacity[source][node_index(x, y)] = 3
            else:
                white_nodes.append((x, y))
                capacity[node_index(x, y)][sink] = 3

    # Add edges between adjacent nodes
    for i in range(0, m):
        for j in range(0, m):
            if grid[i][j] == '*':
                continue
            if i % 2 == 0 and j % 2 == 1 and grid[i][j] == '.':
                u = node_index(i, j - 1)
                v = node_index(i, j + 1)
                capacity[u][v] = 1
            if i % 2 == 1 and j % 2 == 0 and grid[i][j] == '.':
                u = node_index(i - 1, j)
                v = node_index(i + 1, j)
                capacity[u][v] = 1

    # Build adjacency matrix
    max_node = sink + 1
    adj_matrix = [[0] * max_node for _ in range(max_node)]
    for u in capacity:
        for v in capacity[u]:
            adj_matrix[u][v] = capacity[u][v]

    # Compute max flow
    return max_flow(adj_matrix, source, sink)

# Input and Output
n = int(input())
grid = [input().strip() for _ in range(2 * n - 1)]
print(solve(n, grid))

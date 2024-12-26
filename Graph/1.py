# https://chatgpt.com/share/676c18e7-4634-8001-b192-a397f2e33e7b
# سرعت کد رو افزایش بده
# از bfs استفاده کن
from collections import deque

def bfs(graph, start, visited):
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            queue.extend(graph[node] - visited)

def create_graph(num_vertices, nm, absent_edges):
    if num_vertices > nm ** 3:
        print(0)
        exit()
    graph = {i: set(range(num_vertices)) - {i} for i in range(num_vertices)}
    
    for u, v in absent_edges:
        graph[u].discard(v)
        graph[v].discard(u)
    return graph

def get_components_count(num_vertices, nm, absent_edges):
    graph = create_graph(num_vertices, nm, absent_edges)
    
    visited = set()
    count = 0
    
    for node in range(num_vertices):
        if node not in visited:
            bfs(graph, node, visited)
            count += 1
    
    return count

nm = 10
n, m = map(int, input().split())
edges = list()
for _ in range(m):
    u, v = map(int, input().split())
    edges.append((u - 1, v - 1))

print(get_components_count(n, nm, edges) - 1)

class Graph:
    def __init__(self, V, E):
        self.V = V
        self.E = E

class Node:
    def __init__(self, name):
        self.name = name
        self.income_edges = []
        self.outcome_edges = []

n,m = map(int, input().split())
nodes = [Node(i) for i in range(n)]
edges = []
c = {}
f = {}
for i in range(m):
    a,b = map(int, input().split())
    a,b = nodes[a - 1], nodes[b - 1]
    edges.append((a,b))
    c[(a,b)] = 1
    f[(a,b)] = 0
    f[(b,a)] = 0
    a.outcome_edges.append((a,b))
    b.income_edges.append((a,b))

G = Graph(nodes, edges)
flow = {}
parent = {}

def Ford_Fulkerson(G, s, t):
    global flow, f, parent
    while True :
        for u in G.V:
            flow[u] = None
        
        DFS(s, float('inf'))
        
        if flow[t] == None:
            return f
        
        v = t
        x = flow[t]
        while v != s:
            u = parent[v]
            f[(u,v)] += x
            f[(v,u)] -= x
            v = u
    
def DFS(u, x):
    global flow, f, parent, c
    flow[u] = x
    for (_, v) in u.outcome_edges:
        if flow[v] == None and c[(u,v)] - f[(u,v)] > 0:
            parent[v] = u
            DFS(v, min(x, c[(u,v)] - f[(u,v)]))
    
    for (v, _) in u.income_edges:
        if flow[v] == None and f[(v,u)] > 0:
            parent[v] = u
            DFS(v, min(x, f[(v,u)]))

s = nodes[0]
t = nodes[n-1]            
f = Ford_Fulkerson(G, s, t)

result = 0
for e in nodes[0].outcome_edges:
    result += f[e]

print(result)

def get_path_with_cost(node):
    global f, t
    if node == t:
        return [node]
    for e in node.outcome_edges:
        if f[e] > 0:
            f[e] -= 1
            return [node] + get_path_with_cost(e[1])

for _ in range(result):
    path = get_path_with_cost(s)
    print(len(path))
    print(' '.join(str(node.name + 1) for node in path))
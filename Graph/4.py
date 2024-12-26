class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1

def kruskal(n, edges, forced_edges=[]):
    uf = UnionFind(n)
    mst_weight = 0
    mst_edges = 0
    selected_edges = []  # لیست یال‌های انتخاب‌شده

    # Add forced edges first
    for u, v, w in forced_edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst_weight += w
            mst_edges += 1
            selected_edges.append((u, v, w))
        else:
            return float('inf'), []
            

    # Sort edges by weight

    # Add remaining edges
    for u, v, w in edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst_weight += w
            mst_edges += 1
            selected_edges.append((u, v, w))
            if mst_edges == n - 1:
                break

    # Check if we formed a valid MST
    if mst_edges == n - 1:
        return mst_weight, selected_edges  # بازگرداندن وزن و یال‌های انتخابی
    else:
        return float('inf'), []  # در صورت عدم امکان تشکیل MST

# Input parsing
n, m = map(int, input().split())
edges = []
for _ in range(m):
    u, v, w = map(int, input().split())
    edges.append((u - 1, v - 1, w))

# edges.sort(key=lambda x: x[2])

s_edge = sorted(edges, key=lambda x: x[2])

q = int(input())
queries = []
for _ in range(q):
    data = list(map(int, input().split()))
    k = data[0]
    queries.append([edges[i - 1] for i in data[1:]])

# Compute the MST weight of the original graph
base_mst_weight = kruskal(n, s_edge)

# Process each query
results = []
for query in queries:
    try:
        mst_weight = kruskal(n, s_edge, query)
        results.append("YES" if mst_weight[0] == base_mst_weight[0] else "NO")
    except:
        results.append("NO")

# Output results
print("\n".join(results))

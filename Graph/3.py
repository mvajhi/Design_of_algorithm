import sys
from collections import defaultdict, deque
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return False
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1
        return True

def kruskal(n, edges):
    dsu = DSU(n)
    mst = []
    mst_weight = 0
    edge_used = [False] * len(edges)
    for w, u, v, idx in edges:
        if dsu.union(u, v):
            mst.append((u, v, w, idx))
            mst_weight += w
            edge_used[idx] = True
    return mst, mst_weight, edge_used

def build_tree(n, mst):
    tree = [[] for _ in range(n)]
    for u, v, w, idx in mst:
        tree[u].append((v, w, idx))
        tree[v].append((u, w, idx))
    return tree

def bfs_max_weight(n, tree):
    max_weight = [[-1] * n for _ in range(n)]
    for src in range(n):
        visited = [False] * n
        q = deque([(src, -1, -1)])  # (node, parent, max_edge_weight)
        while q:
            node, parent, max_edge = q.popleft()
            visited[node] = True
            for neighbor, weight, _ in tree[node]:
                if neighbor != parent and not visited[neighbor]:
                    new_max_edge = max(max_edge, weight)
                    max_weight[src][neighbor] = new_max_edge
                    q.append((neighbor, node, new_max_edge))
    return max_weight

def solve():
    n, m = map(int, input().split())
    edges = []
    for i in range(m):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        edges.append((w, u, v, i))

    edges.sort()
    mst, mst_weight, edge_used = kruskal(n, edges)
    tree = build_tree(n, mst)
    max_weight = bfs_max_weight(n, tree)

    answers = ["none"] * m

    # بررسی یال‌های "at least one"
    for w, u, v, idx in edges:
        if w == max_weight[u][v]:
            answers[idx] = "at least one"

    # بررسی یال‌های "any"
    for w, u, v, idx in edges:
        if not edge_used[idx]:
            continue

        dsu_temp = DSU(n)
        temp_weight = 0
        for w2, u2, v2, idx2 in edges:
            if idx2 == idx:
                continue
            if dsu_temp.union(u2, v2):
                temp_weight += w2
        
        if dsu_temp.find(0) != dsu_temp.find(n - 1) or temp_weight > mst_weight:
            answers[idx] = "any"

    # هر یالی که در MST بود و "any" نشد را به "at least one" تغییر می‌دهیم
    for _, _, _, idx in mst:
        if answers[idx] != "any":
            answers[idx] = "at least one"

    print("\n".join(answers))

solve()
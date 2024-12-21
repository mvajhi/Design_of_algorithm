class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        
        return True

def find_mst(n, edges, must_include_edges=None):
    uf = UnionFind(n)
    mst_edges = []
    mst_weight = 0
    
    # First, include the must-include edges
    if must_include_edges:
        for idx in must_include_edges:
            edge = next((e for e in edges if e[3] == idx), None)
            if not edge:
                return None, None
            
            w, u, v, _ = edge
            if not uf.union(u, v):
                return None, None
            mst_edges.append(edge)
            mst_weight += w
    
    # Then add other edges to complete the MST
    for w, u, v, idx in sorted(edges):
        if len(mst_edges) == n - 1:
            break
        
        # Skip already included edges
        if must_include_edges and idx in must_include_edges:
            continue
        
        if uf.union(u, v):
            mst_edges.append((w, u, v, idx))
            mst_weight += w
    
    # Check if we have a complete MST
    return mst_edges if len(mst_edges) == n - 1 else None, mst_weight

def solve_banana_delivery():
    # Input reading
    n, m = map(int, input().split())
    
    # Store edges
    edges = []
    for i in range(1, m+1):
        u, v, w = map(int, input().split())
        edges.append((w, u-1, v-1, i))  # weight, island1, island2, edge_index
    
    # Number of requests
    q = int(input())
    
    # Process each request
    for _ in range(q):
        request = list(map(int, input().split()))
        k = request[0]  # number of requested edges
        requested_edges = set(request[1:])
        
        # Try to find an MST that includes all requested edges
        mst, _ = find_mst(n, edges, requested_edges)
        
        # Print YES if a valid MST can be formed, NO otherwise
        print('YES' if mst is not None else 'NO')

# Run the solution
solve_banana_delivery()
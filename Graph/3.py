n, m = map(int, input().split())

if n < 500:
    # https://chatgpt.com/c/676dc650-7990-8001-8ede-d1aa72850383
    # تبدیل به py
    #  https://chatgpt.com/share/67619d10-a894-8001-ac8a-2bbee1f9fd1a
    #  صورت سوال
    #  کدت درست نیست روی تست
    #  فقط یال های تویmst رو بررسی می کنی
    #  جواب های دوبخش قبلی رو باهم ادغام کن
    #  تبدیل کن به cpp
    class Edge:
        def __init__(self, u, v, w, idx):
            self.u = u
            self.v = v
            self.w = w
            self.idx = idx

        def __lt__(self, other):
            return self.w < other.w


    def init_dsu(n):
        global parent, rank_parent
        parent = list(range(n))
        rank_parent = [0] * n


    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]


    def union_sets(x, y):
        xr, yr = find(x), find(y)
        if xr == yr:
            return False
        if rank_parent[xr] < rank_parent[yr]:
            parent[xr] = yr
        elif rank_parent[xr] > rank_parent[yr]:
            parent[yr] = xr
        else:
            parent[yr] = xr
            rank_parent[xr] += 1
        return True


    def kruskal():
        init_dsu(n)
        edges.sort()
        mst_weight = 0
        for e in edges:
            if union_sets(e.u, e.v):
                mst_edges.append(e)
                mst_weight += e.w
                tree[e.u].append((e.v, e.w))
                tree[e.v].append((e.u, e.w))
        return mst_weight


    def dfs(u, parent, max_edge, max_weight, visited):
        visited[u] = True
        for v, w in tree[u]:
            if v != parent:
                max_weight[v] = max(max_edge, w)
                dfs(v, u, max_weight[v], max_weight, visited)


    def check_if_edge_critical(skip_idx, mst_weight):
        init_dsu(n)
        temp_weight = 0
        for e in edges:
            if e.idx != skip_idx and union_sets(e.u, e.v):
                temp_weight += e.w
        for i in range(1, n):
            if find(0) != find(i):
                return True  # گراف همبند نیست
        return temp_weight > mst_weight


    if __name__ == "__main__":
        import sys
        input = sys.stdin.read
        data = input().split()
        edges = []
        tree = [[] for _ in range(n)]
        idx = 0

        for i in range(m):
            u, v, w = map(int, data[idx:idx+3])
            edges.append(Edge(u - 1, v - 1, w, i))
            idx += 3

        mst_edges = []
        answers = ["none"] * m
        mst_weight = kruskal()

        for e in edges:
            max_weight = [-1] * n
            visited = [False] * n
            dfs(e.u, -1, -1, max_weight, visited)
            if e.w == max_weight[e.v]:
                answers[e.idx] = "at least one"

        for e in mst_edges:
            if check_if_edge_critical(e.idx, mst_weight):
                answers[e.idx] = "any"

        sys.stdout.write("\n".join(answers) + "\n")
        
else:
        # https://poe.com/s/jEeN9FXFlRVIEXViAhqV
    # صورت سوال
    '''
    برای این سوال ابتدا کروسکال بزن که یال های مورد استفاده به دست بیاد بعدش به ازای هر یال که توی mst نیست دو راس یال رو مسیرش رو توی mstبررسی کن
    به این صورت که سنگین ترین یال را تا اولین پدر مشترک پیدا کن اگر هم وزن بود یعنی میشه با اون عوضش کرد.
    در ابتدا همه یال ها رو none می گذاریم
    یال های mst را any می کنیم.
    اگر یالی خاصیت تعویض با یالی از mst را داشت هم یالmst هم آن یال را به at lest one تغییر می دهیم.

    باید اون یال ماکزییمم هم که lca میده رو at lest one کردش و ایندکسش رو می خواهیم
    همچنین اگر چندتا یال این ویژگی رو داشته باشن باید همه تغییر کنن
    '''

    from collections import defaultdict
    import sys

    class DSU:
        def __init__(self, n):
            self.parent = list(range(n))
            self.rank = [0] * n

        def find(self, x):
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]

        def union(self, x, y):
            xr = self.find(x)
            yr = self.find(y)
            if xr != yr:
                if self.rank[xr] < self.rank[yr]:
                    xr, yr = yr, xr
                self.parent[yr] = xr
                if self.rank[xr] == self.rank[yr]:
                    self.rank[xr] += 1

    def kruskal(n, edges):
        dsu = DSU(n)
        mst = []
        for w, u, v, idx in edges:
            if dsu.find(u) != dsu.find(v):
                dsu.union(u, v)
                mst.append((u, v, w, idx))
        return mst

    def dfs(u, parent, depth, max_edge, adj, par, mx, mx_idx, dep):
        dep[u] = depth
        par[u][0] = parent
        for v, w, idx in adj[u]:
            if v != parent:
                mx[v][0] = w
                mx_idx[v][0] = idx
                dfs(v, u, depth + 1, max_edge, adj, par, mx, mx_idx, dep)

    def prepare_lca(n, adj):
        LOG = 17  # Assuming n <= 10^5, log2(10^5) ~ 17
        par = [[-1] * LOG for _ in range(n)]
        mx = [[0] * LOG for _ in range(n)]
        mx_idx = [[-1] * LOG for _ in range(n)]
        dep = [0] * n

        # Run DFS to initialize parent and max_edge arrays
        dfs(0, -1, 0, 0, adj, par, mx, mx_idx, dep)

        # Precompute 2^j parents and max edges
        for j in range(1, LOG):
            for i in range(n):
                if par[i][j - 1] != -1:
                    par[i][j] = par[par[i][j - 1]][j - 1]
                    mx[i][j] = max(mx[i][j - 1], mx[par[i][j - 1]][j - 1])

                    # If the max edge comes from two different paths, prefer the one with the actual max weight
                    if mx[i][j - 1] > mx[par[i][j - 1]][j - 1]:
                        mx_idx[i][j] = mx_idx[i][j - 1]
                    else:
                        mx_idx[i][j] = mx_idx[par[i][j - 1]][j - 1]
        
        return par, mx, mx_idx, dep

    def lca(u, v, par, mx, mx_idx, dep):
        LOG = len(par[0])
        if dep[u] < dep[v]:
            u, v = v, u

        max_weight = 0
        max_edge_indices = []

        # Bring both nodes to the same depth
        for i in range(LOG - 1, -1, -1):
            if dep[u] - (1 << i) >= dep[v]:
                if mx[u][i] > max_weight:
                    max_weight = mx[u][i]
                    max_edge_indices = [mx_idx[u][i]]
                elif mx[u][i] == max_weight:
                    max_edge_indices.append(mx_idx[u][i])
                u = par[u][i]

        if u == v:
            return max_weight, max_edge_indices

        # Move both nodes upwards until their LCA is found
        for i in range(LOG - 1, -1, -1):
            if par[u][i] != par[v][i]:
                if mx[u][i] > max_weight:
                    max_weight = mx[u][i]
                    max_edge_indices = [mx_idx[u][i]]
                elif mx[u][i] == max_weight:
                    max_edge_indices.append(mx_idx[u][i])

                if mx[v][i] > max_weight:
                    max_weight = mx[v][i]
                    max_edge_indices = [mx_idx[v][i]]
                elif mx[v][i] == max_weight:
                    max_edge_indices.append(mx_idx[v][i])

                u = par[u][i]
                v = par[v][i]

        # Include the edge connecting to the LCA
        if mx[u][0] > max_weight:
            max_weight = mx[u][0]
            max_edge_indices = [mx_idx[u][0]]
        elif mx[u][0] == max_weight:
            max_edge_indices.append(mx_idx[u][0])

        if mx[v][0] > max_weight:
            max_weight = mx[v][0]
            max_edge_indices = [mx_idx[v][0]]
        elif mx[v][0] == max_weight:
            max_edge_indices.append(mx_idx[v][0])

        return max_weight, max_edge_indices

    def process_graph(n, edges):
        edges = sorted((w, u - 1, v - 1, i) for i, (u, v, w) in enumerate(edges))
        status = ["none"] * len(edges)

        # Step 1: Create MST using Kruskal
        mst_edges = kruskal(n, edges)
        mst_set = set((min(u, v), max(u, v)) for u, v, w, idx in mst_edges)

        for u, v, w, idx in mst_edges:
            status[idx] = "any"

        # Step 2: Build adjacency list for MST
        adj = defaultdict(list)
        for u, v, w, idx in mst_edges:
            adj[u].append((v, w, idx))
            adj[v].append((u, w, idx))

        # Step 3: Prepare LCA
        par, mx, mx_idx, dep = prepare_lca(n, adj)

        # Step 4: Process edges not in MST
        for w, u, v, idx in edges:
            if status[idx] == "none":
                max_weight, max_edge_indices = lca(u, v, par, mx, mx_idx, dep)
                if max_weight == w:
                    status[idx] = "at least one"
                    for edge_idx in max_edge_indices:
                        status[edge_idx] = "at least one"

        return status

    # Input reading
    edges = [tuple(map(int, input().split())) for _ in range(m)]

    # Process the graph and output the results
    result = process_graph(n, edges)
    print("\n".join(result))

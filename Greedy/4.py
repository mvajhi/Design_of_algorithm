
def dfs(tree, u, parent):
    if len(tree[u]["neighbor"]) == 1 and parent != -1:
        tree[u]["cost"] = tree[u]["h"]
        return u

    leafs = []
    for v in tree[u]["neighbor"]:
        if v == parent:
            continue
        leafs.append(dfs(tree, v, u))
        
    max_leaf = max(leafs, key=lambda x: tree[x]["cost"])
    
    if parent != -1:
        tree[max_leaf]["cost"] += max(0, tree[u]["h"] - tree[max_leaf]["cost"])
    else:
        tree[max_leaf]["cost"] += max(0, tree[u]["h"] - tree[max_leaf]["cost"])
        # Update the cost of 2 max leafs
        if len(leafs) == 1:
            tree[u]["cost"] = tree[u]["h"]
        else:
            leafs.sort(key=lambda x: tree[x]["cost"], reverse=True)
            tree[leafs[1]]["cost"] += max(0, tree[u]["h"] - tree[leafs[1]]["cost"])
        
    return max_leaf

def solve(n, heights, edges):
    # Construct the graph
    tree = {i: {"h" : heights[i], "neighbor" : [], "cost": 0} for i in range(n)}
    for u, v in edges:
        tree[u]["neighbor"].append(v)
        tree[v]["neighbor"].append(u)
        
    # argmax of heights
    max_height = max(heights)
    root = heights.index(max_height)
    
    # DFS to calculate the cost
    max_leaf = dfs(tree, root, -1)
    
    # sum of cost
    return sum(tree[i]["cost"] for i in range(n))
    

# Reading input
n = int(input().strip())
heights = list(map(int, input().strip().split()))

edges = []
for _ in range(n-1):
    u, v = map(int, input().strip().split())  # Reading each edge
    edges.append((u-1, v-1))  # Convert to 0-based index


# Solve and output result
print(solve(n, heights, edges))

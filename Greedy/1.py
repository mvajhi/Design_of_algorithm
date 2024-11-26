# https://poe.com/s/CTs44IJxDyDqizUpuPwv
# صورت سوال
import sys
sys.setrecursionlimit(1 << 25)

n = int(sys.stdin.readline())
h = list(map(int, sys.stdin.readline().split()))
tree = [[] for _ in range(n)]
for _ in range(n - 1):
    u, v = map(int, sys.stdin.readline().split())
    u -= 1
    v -= 1
    tree[u].append(v)
    tree[v].append(u)

total_planks = [0]

def dfs(u, parent):
    max_h = h[u]
    for v in tree[u]:
        if v != parent:
            child_h = dfs(v, u)
            max_h = max(max_h, child_h)
    if parent != -1:
        total_planks[0] += max_h - h[parent]
    return max_h

dfs(0, -1)
total_planks[0] += h[0]
print(total_planks[0])

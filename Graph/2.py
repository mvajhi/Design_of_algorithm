from collections import deque
import heapq

def minimum_roads_to_connect(n, m, grid):
    # Helper function to find all components using BFS
    def find_components():
        components = []
        visited = [[False] * m for _ in range(n)]

        for i in range(n):
            for j in range(m):
                if grid[i][j] in "123" and not visited[i][j]:
                    comp = []
                    queue = deque([(i, j)])
                    visited[i][j] = True

                    while queue:
                        x, y = queue.popleft()
                        comp.append((x, y))

                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny] and grid[nx][ny] in "123":
                                visited[nx][ny] = True
                                queue.append((nx, ny))

                    components.append(comp)
        return components

    # Calculate all edges (distances) between components using BFS from component borders
    def build_edges(components):
        edges = []
        tmp = {}
        for i, comp1 in enumerate(components):
            for x, y in comp1:
                visited = [[False] * m for _ in range(n)]
                queue = deque([(x, y, 0)])  # (current_x, current_y, distance)
                visited[x][y] = True

                while queue:
                    cx, cy, dist = queue.popleft()

                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny]:
                            visited[nx][ny] = True
                            if grid[nx][ny] == '.':
                                queue.append((nx, ny, dist + 1))
                            elif grid[nx][ny] in "123":
                                for j, comp2 in enumerate(components):
                                    if j != i and (nx, ny) in comp2:
                                        # edges.append((dist, i, j))
                                        if (min(i,j), max(i,j)) in tmp:
                                            tmp[(min(i,j), max(i,j))] = min(tmp[(min(i,j), max(i,j))], dist)
                                        else:
                                            tmp[(min(i,j), max(i,j))] = dist
                                        break
        return [(tmp[(i,j)], i, j) for i,j in tmp.keys()]

    # Find all components
    components = find_components()
    if len(components) < 2:
        return 0  # Already connected or no components

    # Build all possible edges between components with their distances
    edges = build_edges(components)

    # Use Kruskal's algorithm to find the minimum spanning tree (MST)
    edges.sort()
    parent = list(range(len(components)))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            parent[root_y] = root_x

    total_cost = 0
    used_edges = 0
    
    for dist, i, j in edges:
        if find(i) != find(j):
            union(i, j)
            total_cost += dist
            used_edges += 1
            if used_edges == len(components) - 1:
                break

    # Check if all components are connected
    connected_components = len(set(find(i) for i in range(len(components))))
    if connected_components > 1:
        return -1

    return total_cost

# Input reading
n, m = map(int, input().split())
grid = [input().strip() for _ in range(n)]

# Solve and output the result
print(minimum_roads_to_connect(n, m, grid))
# print(-1)

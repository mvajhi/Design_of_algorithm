# https://chatgpt.com/share/675fdb5f-f148-8001-aa8d-249b20b97b45
'''
یک گراف داریم
در ورودی خطر اول ابتدا تعداد راس ها و با یک فاصله تعداد یال ها را ورودی می دهیم و سپس در n خط بعد یال ها را ورودی می دهیم حال باید روی آن dfs یا bfs بزنیم و ببینیم می توان به همه راس ها رسید یا نه
'''
def is_connected_dfs(vertices, edges, graph):
    visited = [False] * (vertices + 1)

    def dfs_iterative(start):
        stack = [start]
        while stack:
            node = stack.pop()
            if not visited[node]:
                visited[node] = True
                for neighbor in graph[node]:
                    if not visited[neighbor]:
                        stack.append(neighbor)

    dfs_iterative(1)  # شروع DFS از راس 1

    # بررسی اینکه آیا همه رئوس بازدید شده‌اند یا خیر
    return all(visited[1:])

# ورودی گراف
n, m = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(m)]

# ساخت گراف به صورت لیست مجاورت
graph = {i: [] for i in range(1, n + 1)}
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)

# اجرای الگوریتم و چاپ نتیجه
if is_connected_dfs(n, m, graph):
    print(n - 1)
else:
    print(0)

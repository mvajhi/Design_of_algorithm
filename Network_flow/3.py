'''
از تابع حل نتورک فلو سوال ۱ استفاده کردم که جی پی تی داده بود

link: https://github.com/copilot/c/1a4cb0a4-ecce-45b5-91b5-66d841053099
backup link: https://drive.google.com/drive/folders/1rFMFBs0U46dVIMWdiY_cXRXKv4oPynD1?usp=sharing
class Node:
    def __init__(self, name):
        self.name = name
        self.is_source = False
        self.is_sink = False
        self.edge = []

class edge:
    def __init__(self, to, capacity):
        self.to = to
        self.capacity = capacity
        self.flow = 0

ساختمان داده بالا رو دارم می خوام 
شبکه جریان رو حل کنم. به عنوان ورودی source رو می دم.
با روش ادموند کارپ آن را حل کن و جریان ماکزیمم را برگردان

می خواهم فقط گره source رو بدم از طریق اون می تونی به باقی راس ها بررسی توی edge لیستی از یال ها هستش که از آن گره هستند به سمت گره to 

به جای ادموند کارپ از دینیچ استفاده کن
'''

class Node:
    def __init__(self, name):
        self.name = name
        self.edge = []
        self.is_full = True

class Edge:
    def __init__(self, to, capacity):
        self.to = to
        self.capacity = capacity
        self.flow = 0
        self.rev = None  

def add_edge(u, v, capacity):
    """
    این تابع بین دو گره u و v دو یال (اصلی و معکوس) اضافه می‌کند.
    """
    forward_edge = Edge(v, capacity)
    backward_edge = Edge(u, 0)  # یال معکوس با ظرفیت صفر
    # اتصال مراجع یال‌ها برای دسترسی به یکدیگر
    forward_edge.rev = backward_edge
    backward_edge.rev = forward_edge
    # قرار دادن یال‌ها در adjacency list
    u.edge.append(forward_edge)
    v.edge.append(backward_edge)
    
    return forward_edge


def solve_netflow(nodes, source, sink):
    from collections import deque
    def bfs_build_level_graph(nodes, source, sink, level):
        """
        در این BFS، گراف لایه‌ای (Level Graph) را می‌سازیم.
        در آرایه/دیکشنری level، برای هر گره لایه‌اش (عمق در گراف لایه‌ای) ذخیره می‌شود.
        اگر نتوانیم به گره مقصد برسیم، False برمی‌گرداند.
        """
        for node in nodes:
            level[node] = -1  # ابتدا تمام لایه‌ها را -1 قرار می‌دهیم.
        queue = deque()
        queue.append(source)
        level[source] = 0

        while queue:
            u = queue.popleft()
            for e in u.edge:
                # اگر هنوز بازدید نشده و ظرفیت باقیمانده مثبت دارد، برو به لایه بعد
                if level[e.to] < 0 and e.flow < e.capacity:
                    level[e.to] = level[u] + 1
                    queue.append(e.to)

        return level[sink] != -1

    def send_flow_dfs(u, flow, sink, level, start):
        """
        در این DFS، داخل گراف لایه‌ای تلاش می‌کنیم جریان را تا حد امکان ارسال کنیم.
        از 'start' برای جلوگیری از چرخیدن روی یال‌هایی که قبلاً بررسی شده‌اند استفاده می‌کنیم.
        """
        if u == sink:
            return flow

        while start[u] < len(u.edge):
            e = u.edge[start[u]]
            if level[e.to] == level[u] + 1 and e.flow < e.capacity:
                # ظرفیت باقیمانده را حساب می‌کنیم
                current_flow = e.capacity - e.flow
                min_flow = min(flow, current_flow)

                # تلاش برای ارسال جریان
                flow_sent = send_flow_dfs(e.to, min_flow, sink, level, start)
                if flow_sent > 0:
                    # به یال اصلی اضافه می‌کنیم
                    e.flow += flow_sent
                    # از یال معکوس کم می‌کنیم
                    e.rev.flow -= flow_sent
                    return flow_sent
            start[u] += 1

        return 0

    def dinic_max_flow(nodes, source, sink):
        """
        محاسبه جریان ماکزیمم با استفاده از الگوریتم دینیچ (Dinic).
        فرض بر این است که تنها یک گره به عنوان مبدأ (is_source=True)
        و تنها یک گره به عنوان مقصد (is_sink=True) داریم.
        """

        max_flow = 0
        level = {}

        # تا زمانی که می‌توانیم به گره مقصد برسیم، سطح‌بندی مجدد می‌کنیم و سپس با DFS جریان ارسال می‌کنیم
        while bfs_build_level_graph(nodes, source, sink, level):
            # start دیکشنری‌ای است برای آنکه مکانِ فعلی در لیست یال‌ها را به‌خاطر بسپاریم
            # تا هر بار که یک یال بلااستفاده شد، به یال بعدی برویم.
            start = {node: 0 for node in nodes}

            while True:
                flow_sent = send_flow_dfs(source, float('inf'), sink, level, start)
                if flow_sent <= 0:
                    break
                max_flow += flow_sent

        return max_flow

    nodes.append(source)
    nodes.append(sink)
    return dinic_max_flow(nodes, source, sink)

import math

def solve():
    n, m = map(int, input().split())
    inp = [[0 for _ in range(m)] for _ in range(n)]
    nodes = [Node(f'r{i}' if i < n else f'c{i-n}') for i in range(n+m)]
    source = Node('source')
    sink = Node('sink')
    sum_of_sum_row = 0
    sum_of_sum_col = 0
    bad_input = False
    for i in range(n):
        if bad_input:
            input()
            continue
        sum_floor_row = 0
        sum_row = 0
        new_row = input().split()
        for j, num in enumerate(new_row):
            val = 0
            if num.split('.')[0][0] == '-':
                val = -int(num.split('.')[1])
            else:
                val = int(num.split('.')[1])
            if val == 0:
                continue
            inp[i][j] = val
            sum_row += val
            if val > 0:
                sum_floor_row += 0
            elif val < 0:
                sum_floor_row -= 1000

        if sum_row % (10 ** 3) != 0 and not bad_input:
            print("NO")
            bad_input = True
        
        diff_row = int((sum_row - sum_floor_row) / (10**3))
        if diff_row != 0:
            add_edge(source, nodes[i], diff_row)
            sum_of_sum_row += diff_row
        
    if bad_input:
        return
    
    for j in range(m):
        sum_col = 0
        sum_floor_col = 0
        for i in range(n):
            sum_col += inp[i][j]
            if inp[i][j] > 0:
                sum_floor_col += 0
            elif inp[i][j] < 0:
                sum_floor_col -= 1000
        if sum_col % (10 ** 3) != 0:
            print("NO")
            return
        diff_col = int((sum_col - sum_floor_col) / (10**3))
        if diff_col != 0:
            add_edge(nodes[j+n], sink, diff_col)
            sum_of_sum_col += diff_col
            
        
    if sum_of_sum_row != sum_of_sum_col:
        print("NO")
        return
    
    result = []
    for i in range(n):
        tmp = []
        for j in range(m):
            e = None
            if inp[i][j] != 0:
                 e = add_edge(nodes[i], nodes[j+n], 1)
            else:
                e = Edge(0, 0)
            tmp.append(e)
        result.append(tmp)
        
    max_flow = solve_netflow(nodes, source, sink)
    
    if max_flow != sum_of_sum_row:
        print("NO")
        return
    
    print("YES")
    
    for i in range(n):
        for j in range(m):
            if result[i][j].capacity == 0:
                print(0, end=" ")
            else:
                print(result[i][j].flow, end=" ")
        print()
    

t = int(input())
for _ in range(t):
    solve()
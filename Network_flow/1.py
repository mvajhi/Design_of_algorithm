'''
link: https://chatgpt.com/share/678434a7-db2c-8001-8ce5-39cf90155cfe
صورت سوال
برای این سوال باید از شبکه جریان استفاده کنی
یک گرافی دوبخشی باید درست کنی هر خانه را یک راس در نظر بگیر و یک گراف دوبخشی تشکیل بده به این صورت که هر گره در یک بخش است و همسایه هایش در بخش دیگر (شبیه صفحه شطرنج) بعد چون نباید مربع تشکیل بشه از گره s به راس های یکی از بخش ها وصل کن و ظرفیت آنها را با توجه به ورودی تنظیم کن اگر هیچ خطی کشیده نشده در اطراف اون خونه ظرفیتش ۳ اگر یک خط هست ظرفیت ۲ اگر ۲ خط هست ظرفیتش رو یک بگذار برای اون بخش دیگر هم به t وصل کن با همین منطق سپس بین اون دو بخش بین هر دو راسی که مجاور هستند و خط کشیده نشده یک یال با ظرفیت یک بگذار و در نهایت ظرفیت نهایی را چاپ کن
یه موردی آنهایی که در کناره و گوشه ها هستند و بعضی از همسایه های آنها موجود نیست به ازای همسایه هایی که موجود نیست یال بزن به t (اگر در بخش مربوط به s بودند اگر در بخش متصل به t بودند به s یال بزن) و ظرفیتش رو تعداد همسایه هایی که نیست و همچنین خط مربوط به آن هم کشیده نشده بگذار مثلا اگر کناره هست و در بخش t قرار دارد و همچنین خط آن قسمت کناره کشیده نشده یک یال با ظرفیت ۱ بزن به s ولی اگر خطش کشیده شده بود ظرفیتش صفر میشه و این موضوع برای گوشه ها هم که ۲ همسایه موجود نیست صادق است همچنین اگر کلا یک ردیف یا ستون باشد ۳ همسایه ندارد و همچنین اگر کلا یک خانه باشد ۴ همسایه ندارد که باید در نظر بگیری

link: https://chatgpt.com/share/6784358e-216c-8001-960c-7dea46742761
این کد رو وقتی میفرستم محدودیت زمانی می خوره. تا میشه از نظر زمانی بهبود بده
کدی که نوشته بودم

Traceback (most recent call last):
  File "/home/mvajhi/code/Design_of_algorithm/Network_flow/1.py", line 102, in <module>
    solve()
  File "/home/mvajhi/code/Design_of_algorithm/Network_flow/1.py", line 99, in solve
    dinic, source, sink = create_graph(n, grid)
                          ^^^^^^^^^^^^^^^^^^^^^
  File "/home/mvajhi/code/Design_of_algorithm/Network_flow/1.py", line 77, in create_graph
    if grid[i_grid + di][j_grid + dj] in '|-':
       ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
IndexError: list index out of range

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
    def __init__(self):
        self.edge = []
        self.is_full = True

class edge:
    def __init__(self, to, capacity):
        self.to = to
        self.capacity = capacity
        self.flow = 0
        self.rev = None  

def add_edge(u, v, capacity):
    """
    این تابع بین دو گره u و v دو یال (اصلی و معکوس) اضافه می‌کند.
    """
    forward_edge = edge(v, capacity)
    backward_edge = edge(u, 0)  # یال معکوس با ظرفیت صفر
    # اتصال مراجع یال‌ها برای دسترسی به یکدیگر
    forward_edge.rev = backward_edge
    backward_edge.rev = forward_edge
    # قرار دادن یال‌ها در adjacency list
    u.edge.append(forward_edge)
    v.edge.append(backward_edge)


def read_input():
    n = int(input().strip())
    grid = []
    for _ in range(2 * n - 1):
        grid.append(list(input().strip()))
    return n, grid

def create_nodes(n, grid):
    source = Node()
    sink = Node()
    
    nodes = []
    for i in range(n):
        for j in range(n):
            new_node = Node()
            is_left = (i + j) % 2 == 0
            i_grid = 2 * (i+1) - 1
            j_grid = 2 * (j+1) - 1
            
            # محاسبه ظرفیت راس
            count = 0
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if grid[i_grid + di][j_grid + dj] == '|' or grid[i_grid + di][j_grid + dj] == '-':
                    continue
                count += 1
            
            # اگر صفر نبود به s یا t یال می‌زنیم
            if count - 1 > 0:
                new_node.is_full = False
                if is_left:
                    # new_edge = edge(new_node, count - 1)
                    # source.edge.append(new_edge)
                    add_edge(source, new_node, count - 1)
                else:
                    # new_edge = edge(sink, count - 1)
                    # new_node.edge.append(new_edge)
                    add_edge(new_node, sink, count - 1)
            
            nodes.append(new_node)
    
    for i in range(n):
        for j in range(n):
            index = i*n + j
            # اگر قابل استفاده بود ادامه می دیم
            if nodes[index].is_full:
                continue
            is_left = (i + j) % 2 == 0
            i_grid = 2 * (i+1) - 1
            j_grid = 2 * (j+1) - 1
            
            count_out_of_range = 0
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if grid[i_grid + di][j_grid + dj] == '|' or grid[i_grid + di][j_grid + dj] == '-':
                    continue
                ni, nj = i + di, j + dj
                # زدن یال به گره‌های مجاور
                if 0 <= ni < n and 0 <= nj < n:
                    if is_left and not nodes[ni*n + nj].is_full:
                        # new_edge = edge(nodes[ni*n + nj], 1)
                        # nodes[index].edge.append(new_edge)
                        add_edge(nodes[index], nodes[ni*n + nj], 1)
                else:
                    # اگر خارج از محدوده بود به s یا t یال می‌زنیم
                    count_out_of_range += 1

            if count_out_of_range > 0:
                if is_left:
                    # new_edge = edge(sink, count_out_of_range)
                    # nodes[index].edge.append(new_edge)
                    add_edge(nodes[index], sink, count_out_of_range)
                else:
                    # new_edge = edge(nodes[index], count_out_of_range)
                    # source.edge.append(new_edge)
                    add_edge(source, nodes[index], count_out_of_range)
                
    return nodes, source, sink

def solve(nodes, source, sink):
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



n, grid = read_input()
nodes, source, sink = create_nodes(n-1, grid)
print(solve(nodes, source, sink))
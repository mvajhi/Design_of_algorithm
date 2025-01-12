class Node:
    def __init__(self):
        self.edge = []
        self.is_full = True

class edge:
    def __init__(self, to, capacity):
        self.to = to
        self.capacity = capacity
        self.flow = 0

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
                    new_edge = edge(new_node, count - 1)
                    source.edge.append(new_edge)
                else:
                    new_edge = edge(sink, count - 1)
                    new_node.edge.append(new_edge)
            
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
                        new_edge = edge(nodes[ni*n + nj], 1)
                        nodes[index].edge.append(new_edge)
                else:
                    # اگر خارج از محدوده بود به s یا t یال می‌زنیم
                    count_out_of_range += 1

            if count_out_of_range > 0:
                if is_left:
                    new_edge = edge(sink, count_out_of_range)
                    nodes[index].edge.append(new_edge)
                else:
                    new_edge = edge(nodes[index], count_out_of_range)
                    source.edge.append(new_edge)
                
    return nodes, source, sink

def solve(nodes, source, sink):
    from collections import deque
    def bfs_find_path(nodes, source, sink):
        """
        یک تابع BFS برای پیدا کردن مسیری با ظرفیت باقیمانده مثبت از مبدأ تا مقصد،
        مسیر را در قالب یک دیکشنری parent ذخیره می‌کند که با دنبال‌کردن آن می‌توان
        مسیر یال‌ها را بازسازی کرد.
        """
        queue = deque()
        queue.append(source)

        # این دیکشنری در نهایت مشخص می‌کند که گره فعلی از طریق کدام گره آمده و از کدام یال استفاده شده
        parent = {node: None for node in nodes}

        while queue:
            u = queue.popleft()
            for e in u.edge:
                # ظرفیت باقیمانده = ظرفیت - جریان
                if e.capacity - e.flow > 0 and parent[e.to] is None and e.to != source:
                    parent[e.to] = (u, e)  # ذخیرهٔ (گره مبدا, یال)
                    if e.to == sink:
                        # اگر به گره مقصد رسیدیم، مسیر را بازمی‌گردانیم
                        return parent
                    queue.append(e.to)
        return parent

    def edmond_karp(nodes, source, sink):
        """
        الگوریتم ادموند کارپ برای محاسبه جریان ماکزیمم از مبدأ (گره‌ای که is_source=True دارد)
        تا مقصد (گره‌ای که is_sink=True دارد). در پایان، مقدار جریان ماکزیمم را برمی‌گرداند.
        """
        max_flow = 0

        # تا زمانی که مسیری با ظرفیت باقیمانده پیدا می‌شود، جریان را افزایش می‌دهیم
        while True:
            parent_map = bfs_find_path(nodes, source, sink)

            # اگر به گره مقصد نرسیدیم، یعنی مسیر اشباع شده و دیگر مسیر افزایش‌دهنده وجود ندارد
            if parent_map[sink] is None:
                break
            
            # پیدا کردن کمترین ظرفیت باقیمانده در مسیر
            flow = float('inf')
            current_node = sink

            # با دنبال کردن parent_map از مقصد تا مبدأ، کمترین ظرفیت باقیمانده را پیدا می‌کنیم
            while current_node != source:
                u, e = parent_map[current_node]
                remaining_capacity = e.capacity - e.flow
                flow = min(flow, remaining_capacity)
                current_node = u

            # باز هم از مقصد تا مبدأ حرکت می‌کنیم و جریان را به اندازه flow به هر یال اضافه می‌کنیم
            current_node = sink
            while current_node != source:
                u, e = parent_map[current_node]
                e.flow += flow
                # اگر لازم باشد یال برعکس (برای جریان بازگشتی) را نیز به لیست یال‌های u اضافه می‌کنیم
                # یا اگر وجود دارد، مقدار جریان آن را کم می‌کنیم
                # در این ساختار لازم است بررسی کنیم آیا یال برعکس از e.to به u وجود دارد یا خیر
                # و در صورت نبودن، آن را ایجاد کنیم
                reverse_edge = None
                for rev_e in e.to.edge:
                    if rev_e.to == u:
                        reverse_edge = rev_e
                        break
                if not reverse_edge:
                    reverse_edge = edge(u, 0)  # یال برعکس با ظرفیت 0
                    e.to.edge.append(reverse_edge)
                reverse_edge.flow -= flow

                current_node = u

            max_flow += flow

        return max_flow

    nodes.append(source)
    nodes.append(sink)
    return edmond_karp(nodes, source, sink)



n, grid = read_input()
nodes, source, sink = create_nodes(n-1, grid)
print(solve(nodes, source, sink))
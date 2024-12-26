# https://chatgpt.com/share/676c1ee8-2ef0-8001-9625-6cd111d3d65c
'''
یک نقشه دارم که هر خانه می تواند '.','#','1','2','3' باشد
خانه های ۱ به همدیگر متصل هستند و خانه های ۲ و ۳ هم به همین شکل.
خانه های نقطه به معنی مسیر هستند و خانه های # به معنی دیوار.
خانه های نقطه یک آرایه به طول ۳ دارند که حداقل فاصله به ازای هر خانه عددی را نشان می دهد.
این مقادیر را پر کن.

خط اول ورودی شامل دو عدد صحیح nn و mm است که به ترتیب تعداد سطرها و ستون‌های نقشه را مشخص می‌کنند. (1≤n,m≤1000)(1≤n,m≤1000)

هر یک از nn خط بعدی شامل mm کاراکتر است که سطرهای نقشه را توصیف می‌کنند.

5 5
.2...
#2.3.
.#..#
.#.11
#..#.
حال می خوام کمترین فاصله ۲و۱ را با یکدیگر به دست بیارم
همچنین برای ۲و۳
برای ۱و۳
'''
from collections import deque

# ورودی خوانی
n, m = map(int, input().split())
grid = [input().strip() for _ in range(n)]

# فاصله برای هر نوع عدد (1، 2، 3)
distances = [[[float('inf')] * 3 for _ in range(m)] for _ in range(n)]

# جستجوی BFS برای هر نوع خانه
for target in range(1, 4):  # برای خانه‌های '1'، '2'، '3'
    queue = deque()
    visited = [[False] * m for _ in range(n)]
    
    # اضافه کردن همه خانه‌های هدف به صف
    for i in range(n):
        for j in range(m):
            if grid[i][j] == str(target):
                queue.append((i, j, 0))
                visited[i][j] = True
    
    # BFS
    while queue:
        x, y, d = queue.popleft()
        distances[x][y][target - 1] = d
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny] and grid[nx][ny] != '#':
                visited[nx][ny] = True
                queue.append((nx, ny, d + 1))
    
def min_distance_between_types(type1, type2):
    queue = deque()
    visited = [[False] * m for _ in range(n)]
    
    # اضافه کردن تمام خانه‌های type1 به صف
    for i in range(n):
        for j in range(m):
            if grid[i][j] == str(type1):
                queue.append((i, j, 0))
                visited[i][j] = True
    
    # BFS برای یافتن نزدیک‌ترین خانه type2
    while queue:
        x, y, d = queue.popleft()
        if grid[x][y] == str(type2):  # اگر به نوع دوم رسیدیم
            return d
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny] and grid[nx][ny] != '#':
                visited[nx][ny] = True
                queue.append((nx, ny, d + 1))
    return float('inf')  # اگر هیچ مسیری پیدا نشد

# محاسبه کمترین فاصله‌ها
distance_1_2 = min_distance_between_types(1, 2) - 1
distance_2_3 = min_distance_between_types(2, 3) - 1
distance_1_3 = min_distance_between_types(1, 3) - 1

sum_of_two_min = sum(sorted([distance_1_2, distance_2_3, distance_1_3])[:2])

# چاپ خروجی
for i in range(n):
    for j in range(m):
        if grid[i][j] == '.':
            sum_of_two_min = min(sum_of_two_min, sum(distances[i][j]) - 2)
print(sum_of_two_min)

# for i in range(n):
#     for j in range(m):
#         if grid[i][j] == '.':
#             print(distances[i][j], end='|')
#         else:
#             print('    ' + grid[i][j] + '    ', end='|')
#     print()
def solve():
    import sys
    input_data = sys.stdin.read().strip().splitlines()
    
    n = int(input_data[0])  # اندازه شبکه
    # خواندن کل ماتریس (2n-1) سطر
    matrix = input_data[1:(2*n)]
    
    # در ساختار dots and boxes، تعداد کل خطوط ممکن:
    # افقی: n * (n-1)
    # عمودی: (n-1) * n
    # مجموع خطوط = 2 * n * (n - 1)
    
    # گام 1: تشخیص خطوط موجود
    # ساخت لیست/مجموع خطوط افقی و عمودی رسم‌شده
    # برای سادگی، از دو مجموعه جدا استفاده می‌کنیم
    
    # lines_horiz: خطوط افقی رسم‌شده به‌صورت ((i, j), (i, j+1))
    # lines_vert:  خطوط عمودی رسم‌شده به‌صورت ((i, j), (i+1, j))
    
    lines_horiz = set()
    lines_vert = set()
    
    # در ماتریس ورودی:
    # کاراکتر '-' در مختصات (2i-1, 2j) نشان‌دهنده خط افقی بین نقاط (i,j) و (i,j+1)
    # کاراکتر '|' در مختصات (2i, 2j-1) نشان‌دهنده خط عمودی بین نقاط (i,j) و (i+1,j)
    
    # توجه: در کد زیر، اندیس‌ها را از 0 استفاده می‌کنیم و با دقت تبدیل می‌کنیم
    for row in range(2*n - 1):
        for col in range(2*n - 1):
            char = matrix[row][col]
            # خط افقی
            if (row % 2 == 0) and (col % 2 == 1) and (char == '-'):
                # row = 2i-1 => i = row//2 + 1 -- اما اینجا از صفر شروع می‌کنیم
                # col = 2j   => j = col//2
                i = row // 2
                j = col // 2
                lines_horiz.add(( (i, j), (i, j+1) ))
            # خط عمودی
            if (row % 2 == 1) and (col % 2 == 0) and (char == '|'):
                i = row // 2
                j = col // 2
                lines_vert.add(( (i, j), (i+1, j) ))
    
    # گام 2: برای هر مربع 1x1 تعداد اضلاع تشکیل‌دهنده را محاسبه کنیم
    # squares[(i,j)] بیانگر تعداد خطوط رسم‌شده مربع بالا-چپ با مختصات (i,j),
    # که شامل نقاط (i,j), (i,j+1), (i+1,j), (i+1,j+1) می‌شود.
    squares = {}
    for i in range(n-1):
        for j in range(n-1):
            count_edges = 0
            # اضلاع مربع
            if ((i, j), (i, j+1)) in lines_horiz:
                count_edges += 1
            if ((i+1, j), (i+1, j+1)) in lines_horiz:
                count_edges += 1
            if ((i, j), (i+1, j)) in lines_vert:
                count_edges += 1
            if ((i, j+1), (i+1, j+1)) in lines_vert:
                count_edges += 1
            squares[(i, j)] = count_edges
    
    # مجموعه‌ی همه خطوط افقی ممکن (برای بررسی خط‌های جدید)
    all_horiz = set()
    for i in range(n):
        for j in range(n-1):
            all_horiz.add(((i, j), (i, j+1)))
    
    # مجموعه‌ی همه خطوط عمودی ممکن
    all_vert = set()
    for j in range(n):
        for i in range(n-1):
            all_vert.add(((i, j), (i+1, j)))
    
    # خطوطی که هنوز کشیده نشده‌اند
    remaining_horiz = all_horiz - lines_horiz
    remaining_vert  = all_vert  - lines_vert
    
    # تابع کمکی که چک کند با اضافه کردن یک خط،
    # آیا مربعی به 4 ضلع می‌رسد یا خیر
    def forms_square(edge_is_vert, edge):
        """
        edge_is_vert = True  => edge is a vertical edge
        edge_is_vert = False => edge is a horizontal edge
        edge in form ((r1, c1), (r2, c2))
        """
        # مربع‌هایی که ممکن است تحت تاثیر این خط قرار گیرند را پیدا می‌کنیم
        # یک خط افقی می‌تواند در بالای یک مربع یا در پایین یک مربع باشد
        # یک خط عمودی می‌تواند در چپ یک مربع یا در راست یک مربع باشد
        
        # لیست مختصات مربع‌هایی که ممکن است این خط در دور آن‌ها باشد:
        possible_squares = []
        
        if not edge_is_vert:
            # خط افقی
            # edge: ((i, j), (i, j+1))
            (i, j1), (i, j2) = edge
            # می‌تواند بالای مربعی با (i, j1) => (i, j1+1), (i+1, j1), ...
            # پس مربع بالا-چپ آن می‌شود (i, j1)
            # یا ممکن است پایین مربعی باشد به مختصات (i-1, j1)
            possible_squares.append((i, j1))
            possible_squares.append((i-1, j1))
        else:
            # خط عمودی
            # edge: ((i1, j), (i2, j))
            (i1, j), (i2, j) = edge
            possible_squares.append((i1, j))
            possible_squares.append((i1, j-1))
        
        for sq in possible_squares:
            if sq in squares:  # اگر واقعاً مربعی به این مختصات وجود داشته باشد
                # بررسی کنیم آیا با اضافه کردن این خط، square[sq] == 3 می‌شود؟
                # در آن صورت با افزودن خط فعلی، عددش 4 خواهد شد => یک مربع بسته می‌شود
                if squares[sq] == 3:
                    return True
        return False

    moves = 0
    # الگوریتم تکرارشونده:
    # تا زمانی که می‌توان خطی را پیدا کرد که باعث بسته شدن هیچ مربعی نشود، آن را اضافه می‌کنیم.
    
    # برای به‌دست‌آوردن "بدترین حالت" (حداکثر تعداد حرکت‌ها بدون ایجاد مربع)،
    # در هر مرحله فقط خطوطی را اضافه می‌کنیم که منجر به تکمیل مربع نمی‌شوند.
    # اگر هیچ خط ایمنی وجود نداشت، الگوریتم پایان می‌یابد.
    
    while True:
        safe_edge_found = False
        
        # به دنبال اولین خط ایمن در remaining_horiz
        to_remove = None
        for edge in remaining_horiz:
            if not forms_square(False, edge):
                # این خط ایمن است
                safe_edge_found = True
                moves += 1
                to_remove = edge
                break
        if to_remove is not None:
            # حذف از remaining_horiz و آپدیت squares
            remaining_horiz.remove(to_remove)
            # آپدیت شمارش ضلع‌های مربعی که تحت تاثیر هستند
            (i, j1), _ = to_remove
            # مربع بالا
            if (i, j1) in squares:
                squares[(i, j1)] += 1
            # مربع پایین (i-1, j1)
            if (i-1, j1) in squares:
                squares[(i-1, j1)] += 1
            continue
        
        # اگر در remaining_horiz چیزی پیدا نشد؛ می‌رویم سراغ remaining_vert
        to_remove = None
        for edge in remaining_vert:
            if not forms_square(True, edge):
                safe_edge_found = True
                moves += 1
                to_remove = edge
                break
        if to_remove is not None:
            remaining_vert.remove(to_remove)
            # آپدیت squares
            (i1, j), _ = to_remove
            if (i1, j) in squares:
                squares[(i1, j)] += 1
            if (i1, j-1) in squares:
                squares[(i1, j-1)] += 1
            continue
        
        # اگر هیچ خطی پیدا نشد، خارج می شویم
        if not safe_edge_found:
            break
    
    print(moves)

solve()
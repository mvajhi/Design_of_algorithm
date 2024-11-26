# https://poe.com/s/IJ842bZ11U0P34iZU7Tq
# صورت سوال
def max_actors_in_show(t, test_cases):
    results = []
    
    for case in test_cases:
        n, k, ages = case
        total_actors = 0
        
        # ابتدا تعداد افراد را برای هر سن به دو دسته تقسیم می کنیم
        for i in range(n):
            # تعداد افرادی که می توانند در این گروه باشند
            total_actors += (ages[i] // 2) * 2
        
        # اکنون افراد باقیمانده را محاسبه می کنیم
        remaining_actors = sum(ages[i] % 2 for i in range(n))
        
        # تعداد باقیمانده را به گروه‌های ممکن تقسیم کنید
        total_actors += min(remaining_actors, (k - total_actors // 2) * 2)
        
        results.append(total_actors)
    
    return results

# ورودی نمونه
t = int(input())
test_cases = []
for _ in range(t):
    n, k = map(int, input().split())
    ages = list(map(int, input().split()))
    test_cases.append((n, k, ages))

# خروجی
results = max_actors_in_show(t, test_cases)
for result in results:
    print(result)
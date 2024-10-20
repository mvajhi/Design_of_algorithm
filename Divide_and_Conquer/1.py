# https://poe.com/s/M8VPIUlnJt0M5zSiGke6
# صورت سوال

import sys
import math

MOD = 10**9 + 7

# پیش‌محاسبه ترکیب‌ها با استفاده از اصل پاسکال
def precompute_combinations(n, mod):
    comb = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        comb[i][0] = comb[i][i] = 1
        for j in range(1, i):
            comb[i][j] = (comb[i-1][j-1] + comb[i-1][j]) % mod
    return comb

# بازگشتی برای محاسبه تعداد حالات
def count_ways(arr, comb, mod):
    if len(arr) <= 1:
        return 1
    root = arr[0]
    left = [x for x in arr if x < root]
    right = [x for x in arr if x > root]
    
    left_ways = count_ways(left, comb, mod)
    right_ways = count_ways(right, comb, mod)
    
    # تعداد راه‌های ترکیب کردن زیرآرایه چپ و راست
    total_ways = comb[len(arr) - 1][len(left)]
    
    return (total_ways * left_ways % mod) * right_ways % mod

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    
    comb = precompute_combinations(n, MOD)
    
    result = count_ways(arr, comb, MOD)
    
    print(result - 1)
    
solve()
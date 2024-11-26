def check(mid, ages, k, n):
    # ages = _ages[:]
    pre = ages[0]
    count = 0
    for i in range(n - 2):
        new_count = (pre + ages[i + 1]) // mid
        count += new_count
        pre = ages[i+1] - max(0, new_count * mid - ages[i])

    return count >= k

def solve(data):
    n, k, ages = data
    
    if n == 1:
        print((ages[0] // k )* k)
        return
    if n == 0:
        print(0)
        return
    
    max_count = ages[0]
    for i in range(1, n-1):
        max_count = max(max_count, ages[i] + ages[i+1])
    min_count = max_count // k
    
    ans = 0
    while min_count <= max_count:
        mid = (min_count + max_count) // 2
        if check(mid, ages, k, n):
            min_count = mid + 1
            ans = mid
        else:
            max_count = mid - 1
            
    print(ans * k)
    

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    ages = list(map(int, input().split()))
    solve((n, k, ages))

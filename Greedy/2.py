# https://poe.com/s/40H0bjcnwQjGZDBdum5S
t = int(input())
for _ in range(t):
    a, b, c, d = map(int, input().split())
    s = input()
    
    if len(s) != a + b + 2 * c + 2 * d:
        print("NO")
        continue
    
    
    count_HP = 0
    count_PH = 0
    count_H = 0
    count_P = 0

    for i in range(len(s)):
        if s[i:i+2] == "HP":
            count_HP += 1
        if s[i:i+2] == "PH":
            count_PH += 1
        if s[i] == "H":
            count_H += 1
        if s[i] == "P":
            count_P += 1
    
    # count_H = max(0, count_H - (c+d))
    # count_P = max(0, count_P - (c+d))
    
    # if count_HP >= c and count_PH >= d and count_H >= a and count_P >= b:
    if count_H == a + c + d and count_P == b + c + d:
        print("YES")
    else:
        print("NO")
    
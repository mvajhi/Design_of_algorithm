# https://poe.com/s/40H0bjcnwQjGZDBdum5S
# صورت سوال
t = int(input())  # تعداد تست ها
for _ in range(t):
    # خواندن ورودی هر تست
    a, b, c, d = map(int, input().split())
    s = input()
    
    # مرحله 1: بررسی طول رشته
    if len(s) != a + b + 2 * c + 2 * d:
        print("NO")
        continue
    
    # مرحله 2: شمارش زیررشته های "HP" و "PH"
    count_HP = 0
    count_PH = 0
    i = 0
    while i < len(s) - 1:
        if s[i:i+2] == "HP":
            count_HP += 1
            i += 2
        elif s[i:i+2] == "PH":
            count_PH += 1
            i += 2
        else:
            i += 1
    
    # مرحله 3: بررسی مطابقت تعداد زیررشته ها با c و d
    if count_HP != c or count_PH != d:
        print("NO")
        continue
    
    # مرحله 4: بررسی تعداد حروف باقی مانده برای "H" و "P"
    remaining_H = s.count("H") - count_HP - count_PH
    remaining_P = s.count("P") - count_HP - count_PH
    
    if remaining_H == a and remaining_P == b:
        print("YES")
    else:
        print("NO")
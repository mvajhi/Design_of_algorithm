def aladdin_win_probability(n, m, k):
    size_of_dp = n + 1
    dp = [0.0] * (size_of_dp)
    dp[0] = 1.0

    for i in range(1, size_of_dp):
        for j in range(min(k, i), 0, -1):
            if i - j >= m:
                break
            if i - j >= 0:
                dp[i] += dp[i - j] / k

    win_probability = sum(dp[m:n + 1]) 
    return win_probability

# print(f"{aladdin_win_probability(8, 1, 8):.6f}")
# print(f"{aladdin_win_probability(5, 1, 10):.6f}")
# print(f"{aladdin_win_probability(23, 19, 9):.6f}")

n, m, k = map(int, input().split())
print(f"{aladdin_win_probability(n, m, k):.6f}")
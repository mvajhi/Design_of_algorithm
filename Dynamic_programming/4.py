# https://chatgpt.com/share/672d2ab0-b168-8001-a628-6f89a0556df3
# صورت سوال
def maxCoins(statues):
    n = len(statues)
    dp = [[0] * n for _ in range(n)]
    
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j + 1):
                left = statues[i - 1] if i > 0 else 1
                right = statues[j + 1] if j < n - 1 else 1
                before = dp[i][k - 1] if k != i else 0
                after = dp[k + 1][j] if k != j else 0
                dp[i][j] = max(dp[i][j], before + left * statues[k] * right + after)
    
    return dp[0][n - 1]

n = int(input())
statues = list(map(int, input().split()))
print(maxCoins(statues))

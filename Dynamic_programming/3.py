# https://chatgpt.com/share/672d1de7-23ac-8001-88cd-1a1db40732e5
# صورت سوال
MOD = 100000000

def symbolic_arrangements(n, m, v, c):
    dp = [[[[0] * (c + 1) for _ in range(v + 1)] for _ in range(m + 1)] for _ in range(n + 1)]
    dp[0][0][0][0] = 1

    for i in range(n + 1):
        for j in range(m + 1):
            for k in range(v + 1):
                for l in range(c + 1):
                    if i < n and k < v:
                        dp[i + 1][j][k + 1][0] = (dp[i + 1][j][k + 1][0] + dp[i][j][k][l]) % MOD
                    if j < m and l < c:
                        dp[i][j + 1][0][l + 1] = (dp[i][j + 1][0][l + 1] + dp[i][j][k][l]) % MOD

    result = 0
    for k in range(v + 1):
        for l in range(c + 1):
            result = (result + dp[n][m][k][l]) % MOD

    return result

n, m, v, c = map(int, input().split())
print(symbolic_arrangements(n, m, v, c))

# print(symbolic_arrangements(1, 2, 13, 1))
# print(symbolic_arrangements(4, 2, 1, 1))
# print(symbolic_arrangements(3, 2, 2, 1))

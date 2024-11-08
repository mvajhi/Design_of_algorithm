n = int(input())
cost = list(map(int, input().split()))
items = [input() for _ in range(n)]
items_reverse = [item[::-1] for item in items]
INF = float('inf')
dp = [[INF] * 2 for _ in range(n)]
dp[0][0] = 0
dp[0][1] = cost[0]

for i in range(1, n):
    if items[i] >= items[i - 1]:
        dp[i][0] = dp[i - 1][0]
    if items_reverse[i] >= items[i - 1]:
        dp[i][1] = dp[i - 1][0] + cost[i]
    if items[i] >= items_reverse[i - 1]:
        dp[i][0] = min(dp[i][0], dp[i - 1][1])
    if items_reverse[i] >= items_reverse[i - 1]:
        dp[i][1] = min(dp[i][1], dp[i - 1][1] + cost[i])


result = min(dp[-1])
if result == INF:
    print(-1)
else:
    print(result)
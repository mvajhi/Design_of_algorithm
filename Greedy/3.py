# https://chatgpt.com/share/6745ac51-8294-8001-8f6b-c3ba9542871f
# صورت پروژه

start_point = 0
start = 0

def is_beautiful(heights, k):
    n = len(heights)
    for i in range(start, n - 1):
        valid = False
        for j in range(i + 1, min(i + k + 1, n)):
            if heights[j] < heights[i]:
                valid = True
                break
        if not valid:
            start_point = max(0, i - 1)
            return False
    return True

def can_beautify(n, k, heights):
    # Check if the initial arrangement is already beautiful
    if is_beautiful(heights, k):
        return "YES"
    
    start = start_point
    # Try swapping all pairs of books, excluding the last book
    for i in range(start, n - 1):
        for j in range(i + 1, n):  # Exclude the last book (index n-1)
            if heights[i] > heights[j]:
                heights[i], heights[j] = heights[j], heights[i]
                if is_beautiful(heights, k):
                    return "YES"
                # Swap back
                heights[i], heights[j] = heights[j], heights[i]
    
    return "NO"

# Input reading
n, k = map(int, input().split())
heights = list(map(int, input().split()))
heights.append(0)  # Add a dummy book at the end

# Output the result
print(can_beautify(n, k, heights))

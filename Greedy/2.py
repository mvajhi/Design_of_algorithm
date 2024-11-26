# https://poe.com/s/tSeuKg7QRX5HBRuXODkI
# صورت سوال
def is_beautiful(n, k, heights):
    # Stack to maintain the next smaller element to the right
    next_smaller = [-1] * n
    stack = []
    
    # Traverse from right to left to find the next smaller element for each book
    for i in range(n - 1, -1, -1):
        while stack and heights[stack[-1]] >= heights[i]:
            stack.pop()
        if stack:
            next_smaller[i] = stack[-1]
        stack.append(i)
    
    # Check if the current arrangement is beautiful
    for i in range(n):
        if next_smaller[i] != -1 and next_smaller[i] - i > k:
            break
    else:
        # If the loop completes without breaking, the arrangement is already beautiful
        return "YES"
    
    # Now try to see if one swap can make the arrangement beautiful
    for i in range(n - 1):
        if heights[i] > heights[i + 1]:
            # Try swapping heights[i] and heights[i+1] and check again
            heights[i], heights[i + 1] = heights[i + 1], heights[i]
            
            # Recompute next_smaller array after the swap
            next_smaller = [-1] * n
            stack = []
            for j in range(n - 1, -1, -1):
                while stack and heights[stack[-1]] >= heights[j]:
                    stack.pop()
                if stack:
                    next_smaller[j] = stack[-1]
                stack.append(j)
            
            # Check if the new arrangement is beautiful
            for j in range(n):
                if next_smaller[j] != -1 and next_smaller[j] - j > k:
                    break
            else:
                # If the loop completes without breaking, the arrangement is now beautiful
                return "YES"
            
            # Revert the swap
            heights[i], heights[i + 1] = heights[i + 1], heights[i]
    
    return "NO"

# Input reading
n, k = map(int, input().split())
heights = list(map(int, input().split()))

# Output the result
print(is_beautiful(n, k, heights))
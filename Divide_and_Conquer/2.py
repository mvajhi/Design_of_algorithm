# https://chatgpt.com/share/6714fb95-3428-8001-82df-9e25f4eeb807
# write merge sort

LOWER_BOUND = 0
UPPER_BOUND = 0
count = 0

def check_conditions(left_half, right_half):
    global count
    tmp = 0
    j = 0
    for i in left_half:
        while j < len(right_half) and right_half[j] - i < LOWER_BOUND:
            j += 1
        tmp += j
    
    j = len(right_half) - 1
    for i in left_half[::-1]:
        while j >= 0 and right_half[j] - i > UPPER_BOUND:
            j -= 1
        tmp += len(right_half) - j - 1
    
    
    # print(left_half, right_half, tmp, len(right_half) * len(left_half) - tmp)
    count += len(right_half) * len(left_half) - tmp
        
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        merge_sort(left_half)
        merge_sort(right_half)
        check_conditions(left_half, right_half)
        merge(arr, left_half, right_half)

def merge(arr, left_half, right_half):
    i = j = k = 0
    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]:
            arr[k] = left_half[i]
            i += 1
        else:
            arr[k] = right_half[j]
            j += 1
        k += 1
    while i < len(left_half):
        arr[k] = left_half[i]
        i += 1
        k += 1
    while j < len(right_half):
        arr[k] = right_half[j]
        j += 1
        k += 1
        
def convert_to_sum(arr):
    for i in range(1, len(arr)):
        arr[i] += arr[i-1]
    return arr

def get_input():
    arr = list(map(int, input().split()))
    global count, LOWER_BOUND, UPPER_BOUND
    LOWER_BOUND, UPPER_BOUND = list(map(int, input().split()))
    return arr

def main():
    arr = get_input()
    arr = convert_to_sum(arr)
    global count
    for i in range(len(arr)):
        if LOWER_BOUND <= arr[i] <= UPPER_BOUND:
            count += 1
    # print(arr, LOWER_BOUND, UPPER_BOUND)
    merge_sort(arr)
    print(count)

if __name__ == "__main__":
    main()
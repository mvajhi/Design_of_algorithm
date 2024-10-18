inp = dict()

def parse_input():
    # use GPT https://chatgpt.com/share/67077cd3-99d4-8001-806a-81fb07a09235
    # کدش رو به زبان cpp بزن
    # (ارسال صورت سوال)
    n, k, A, B = map(int, input().split())
    queue = sorted(map(int, input().split()))
    queue_index = 0
    
    global inp    
    inp = {"n": n,"k": k,"A": A,"B": B,"queue": queue, "queue_index": queue_index, "len": len(queue)}

def solve(first, last):
    cost = -1
    count = 0
    if first == last:
        while inp["queue_index"] <= inp["len"] - 1 and inp["queue"][inp["queue_index"]] == first + 1:
            inp["queue_index"] += 1
            count += 1

        if count == 0:
            cost = inp["A"]
        else:
            cost = inp["B"] * count
            
        return count, cost
    
    # split the array into two parts
    countL, costL = solve(first, (first+last)//2)
    countR, costR = solve((first+last)//2+1, last)
    
    # find the minimum cost to solve the problem
    count = countL + countR
    if count == 0:
        cost = inp["A"]
    else:
        cost = inp["B"] * count * (last - first + 1)
    
    if cost > costL + costR:
        cost = costL + costR
    
    return count, cost
    
    

def main():
    parse_input()
    print(solve(0, 2**inp["n"]-1)[1])
    
if __name__ == "__main__":
    main()
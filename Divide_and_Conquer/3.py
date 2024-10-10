inp = dict()

def parse_input():
    n, k, A, B = map(int, input().split())
    tmp = map(int, input().split())
    queue = [0 for i in range(2**n)]
    for i in tmp:
        queue[i-1] += 1  
    
    global inp    
    inp = {"n": n,"k": k,"A": A,"B": B,"queue": queue}

def solve(first, last):
    cost = -1
    count = -1
    if first == last:
        if inp["queue"][first] == 0:
            cost = inp["A"]
            count = 0
        else:
            cost = inp["B"] * inp["queue"][first]
            count = inp["queue"][first]
            
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
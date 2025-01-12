class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lines = []
    
    def add_line(self, line):
        self.lines.append(line)

def read_input():
    n = int(input().strip())
    grid = []
    for _ in range(2 * n - 1):
        grid.append(list(input().strip()))
    return n, grid

def create_nodes(n, grid):
    nodes = []
    for i in range(1, 2*n, 2):
        for j in range(1, 2*n, 2):
            nodes.append(Node(i, j))
    return nodes

def add_possible_lines(nodes, grid, n):
    for node in nodes:
        x, y = node.x, node.y
        if x > 1:  # Top line
            if grid[x-2][y] == '-':
                node.add_line('top')
        if x < 2*n-2:  # Bottom line
            if grid[x+2][y] == '-':
                node.add_line('bottom')
        if y > 1:  # Left line
            if grid[x][y-2] == '|':
                node.add_line('left')
        if y < 2*n-2:  # Right line
            if grid[x][y+2] == '|':
                node.add_line('right')

def calculate_moves(nodes):
    move_count = 0
    for node in nodes:
        move_count += len(node.lines)
    return move_count

n, grid = read_input()
nodes = create_nodes(n, grid)
add_possible_lines(nodes, grid, n)
result = calculate_moves(nodes)
print(result)
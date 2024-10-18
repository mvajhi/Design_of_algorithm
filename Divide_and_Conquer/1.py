def main():
    len_inp, inp = get_input()
    print((inp))
    bst = create_bst(inp, len_inp)
    bst.show()
    result = Dvide_and_Conquer(bst)
    print(result)

def get_input():
    return int(input()), list(map(int, input().split()))

def create_bst(inp, len_inp):
    bst = BST()
    for i in inp:
        bst.insert(i)
    return bst

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert(self.root, key)

    def _insert(self, node, key):
        if key < node.key:
            if node.left is None:
                node.left = Node(key)
            else:
                self._insert(node.left, key)
        else:
            if node.right is None:
                node.right = Node(key)
            else:
                self._insert(node.right, key)

    def show(self):
        if self.root is not None:
            self._show(self.root)
            
    def _show(self, node):
        if node is not None:
            self._show(node.left)
            print(str(node.key) + ' ')
            self._show(node.right)

if __name__ == "__main__":
    main()
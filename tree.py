class BinaryNode:
    def __init__(self, value):
        self.value = value
        self.left_child = None
        self.right_child = None

class BinarySearchTree:
    def __init__(self):
        self.head = None

    def add_node(self, value):
        self.head = self._add_recursive(self.head, value)

    def _add_recursive(self, current, value):
        if not current:
            return BinaryNode(value)
        if value < current.value:
            current.left_child = self._add_recursive(current.left_child, value)
        elif value > current.value:
            current.right_child = self._add_recursive(current.right_child, value)
        return current

    def remove_node(self, value):
        self.head = self._remove_recursive(self.head, value)

    def _remove_recursive(self, current, value):
        if not current:
            return current
        if value < current.value:
            current.left_child = self._remove_recursive(current.left_child, value)
        elif value > current.value:
            current.right_child = self._remove_recursive(current.right_child, value)
        else:
            if not current.left_child:
                return current.right_child
            elif not current.right_child:
                return current.left_child
            temp = self._find_minimum(current.right_child)
            current.value = temp.value
            current.right_child = self._remove_recursive(current.right_child, temp.value)
        return current

    def _find_minimum(self, node):
        while node.left_child:
            node = node.left_child
        return node

    def find_node(self, value):
        return self._find_recursive(self.head, value)

    def _find_recursive(self, current, value):
        if not current or current.value == value:
            return current
        if value < current.value:
            return self._find_recursive(current.left_child, value)
        return self._find_recursive(current.right_child, value)

    def print_inorder(self):
        self._inorder_recursive(self.head)

    def _inorder_recursive(self, current):
        if current:
            self._inorder_recursive(current.left_child)
            print(current.value, end=" ")
            self._inorder_recursive(current.right_child)


class RedBlackNode:
    def __init__(self, value):
        self.value = value
        self.left_child = None
        self.right_child = None
        self.parent = None
        self.color = 1  # 1 for red, 0 for black

class RedBlackTree:
    def __init__(self):
        self.NIL = RedBlackNode(0)
        self.NIL.color = 0
        self.NIL.left_child = None
        self.NIL.right_child = None
        self.head = self.NIL

    def add_node(self, value):
        node = RedBlackNode(value)
        node.parent = None
        node.left_child = self.NIL
        node.right_child = self.NIL
        node.color = 1

        y = None
        x = self.head

        while x != self.NIL:
            y = x
            if node.value < x.value:
                x = x.left_child
            else:
                x = x.right_child

        node.parent = y
        if y == None:
            self.head = node
        elif node.value < y.value:
            y.left_child = node
        else:
            y.right_child = node

        if node.parent == None:
            node.color = 0
            return

        if node.parent.parent == None:
            return

        self._fix_insert(node)

    def _fix_insert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right_child:
                u = k.parent.parent.left_child
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left_child:
                        k = k.parent
                        self._rotate_right(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self._rotate_left(k.parent.parent)
            else:
                u = k.parent.parent.right_child
                if u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right_child:
                        k = k.parent
                        self._rotate_left(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self._rotate_right(k.parent.parent)
            if k == self.head:
                break
        self.head.color = 0

    def _rotate_left(self, x):
        y = x.right_child
        x.right_child = y.left_child
        if y.left_child != self.NIL:
            y.left_child.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.head = y
        elif x == x.parent.left_child:
            x.parent.left_child = y
        else:
            x.parent.right_child = y
        y.left_child = x
        x.parent = y

    def _rotate_right(self, x):
        y = x.left_child
        x.left_child = y.right_child
        if y.right_child != self.NIL:
            y.right_child.parent = x
        y.parent = x.parent
        if x.parent == None:
            self.head = y
        elif x == x.parent.right_child:
            x.parent.right_child = y
        else:
            x.parent.left_child = y
        y.right_child = x
        x.parent = y

    def remove_node(self, value):
        self._remove_node_helper(self.head, value)

    def _remove_node_helper(self, node, value):
        z = self.NIL
        while node != self.NIL:
            if node.value == value:
                z = node
            if node.value <= value:
                node = node.right_child
            else:
                node = node.left_child
        if z == self.NIL:
            print("Value not found in the tree")
            return
        y = z
        y_original_color = y.color
        if z.left_child == self.NIL:
            x = z.right_child
            self._transplant(z, z.right_child)
        elif z.right_child == self.NIL:
            x = z.left_child
            self._transplant(z, z.left_child)
        else:
            y = self._find_minimum(z.right_child)
            y_original_color = y.color
            x = y.right_child
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right_child)
                y.right_child = z.right_child
                y.right_child.parent = y
            self._transplant(z, y)
            y.left_child = z.left_child
            y.left_child.parent = y
            y.color = z.color
        if y_original_color == 0:
            self._fix_delete(x)

    def _fix_delete(self, x):
        while x != self.head and x.color == 0:
            if x == x.parent.left_child:
                s = x.parent.right_child
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self._rotate_left(x.parent)
                    s = x.parent.right_child
                if s.left_child.color == 0 and s.right_child.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.right_child.color == 0:
                        s.left_child.color = 0
                        s.color = 1
                        self._rotate_right(s)
                        s = x.parent.right_child
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right_child.color = 0
                    self._rotate_left(x.parent)
                    x = self.head
            else:
                s = x.parent.left_child
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self._rotate_right(x.parent)
                    s = x.parent.left_child
                if s.right_child.color == 0 and s.right_child.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left_child.color == 0:
                        s.right_child.color = 0
                        s.color = 1
                        self._rotate_left(s)
                        s = x.parent.left_child
                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left_child.color = 0
                    self._rotate_right(x.parent)
                    x = self.head
        x.color = 0

    def _transplant(self, u, v):
        if u.parent == None:
            self.head = v
        elif u == u.parent.left_child:
            u.parent.left_child = v
        else:
            u.parent.right_child = v
        v.parent = u.parent

    def _find_minimum(self, node):
        while node.left_child != self.NIL:
            node = node.left_child
        return node

    def find_node(self, value):
        return self._find_node_helper(self.head, value)

    def _find_node_helper(self, node, value):
        if node == self.NIL or value == node.value:
            return node != self.NIL
        if value < node.value:
            return self._find_node_helper(node.left_child, value)
        return self._find_node_helper(node.right_child, value)

    def print_inorder(self):
        self._print_inorder_helper(self.head)

    def _print_inorder_helper(self, node):
        if node != self.NIL:
            self._print_inorder_helper(node.left_child)
            print(node.value, end=" ")
            self._print_inorder_helper(node.right_child)
# Create a Binary Search Tree
bst = BinarySearchTree()

# Test Case 1: Add nodes
bst.add_node(10)
bst.add_node(5)
bst.add_node(15)
bst.add_node(3)
bst.add_node(7)
bst.add_node(13)
bst.add_node(18)

# Expected Output (Inorder traversal should give a sorted sequence)
print("Inorder traversal of Binary Search Tree:")
bst.print_inorder()  # Expected: 3 5 7 10 13 15 18
print()

# Test Case 2: Find a node
print("Finding node with value 7:", bst.find_node(7) is not None)  # Expected: True
print("Finding node with value 20:", bst.find_node(20) is not None)  # Expected: False

# Test Case 3: Remove a node
bst.remove_node(5)
print("Inorder traversal after removing 5:")
bst.print_inorder()  # Expected: 3 7 10 13 15 18
print()

# Test Case 4: Remove a node with two children
bst.remove_node(10)
print("Inorder traversal after removing 10:")
bst.print_inorder()  # Expected: 3 7 13 15 18
print()
# Create a Red-Black Tree
rbt = RedBlackTree()

# Test Case 1: Add nodes
rbt.add_node(10)
rbt.add_node(5)
rbt.add_node(15)
rbt.add_node(3)
rbt.add_node(7)
rbt.add_node(13)
rbt.add_node(18)

# Expected Output (Inorder traversal)
print("Inorder traversal of Red-Black Tree:")
rbt.print_inorder()  # Expected: 3 5 7 10 13 15 18
print()

# Test Case 2: Find a node
print("Finding node with value 7:", rbt.find_node(7))  # Expected: True
print("Finding node with value 20:", rbt.find_node(20))  # Expected: False

# Test Case 3: Remove a node
rbt.remove_node(5)
print("Inorder traversal after removing 5:")
rbt.print_inorder()  # Expected: 3 7 10 13 15 18
print()

# Test Case 4: Remove a node with two children
rbt.remove_node(10)
print("Inorder traversal after removing 10:")
rbt.print_inorder()  # Expected: 3 7 13 15 18
print()


"""OUTPUT:

Inorder traversal of Binary Search Tree:
3 5 7 10 13 15 18 
Finding node with value 7: True     
Finding node with value 20: False   
Inorder traversal after removing 5: 
3 7 10 13 15 18 
Inorder traversal after removing 10:
3 7 13 15 18 
Inorder traversal of Red-Black Tree:
3 5 7 10 13 15 18
Finding node with value 7: True
Finding node with value 20: False
Inorder traversal after removing 5:
3 7 10 13 15 18
Inorder traversal after removing 10:
3 7 13 15 18"""
# Name: Sterling Violette
# OSU Email: violetts@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 2/27/2023
# Description: a BST class that mimics a binary search tree
#              has methods such as add, remove, contains that
#              can allow a user to edit or get info from the BST


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Takes a value in as an object argument and adds it to the
        tree, does not return anything but makes changes to
        tree
        """
        #declare
        node = BSTNode(value)
        target_location = self._root
        tl = target_location
        none_location = 0
        flag = 0

        #if the tree itself is empty
        if tl == None:
            self._root = node
            none_location = 1
            return

        #not empty, iterate until target location is found
        while none_location != 1 and flag == 0:
            if tl == None:
                none_location = 1
                flag = 1
            if flag != 1:
                old_location = tl
                if value >= tl.value:
                    tl = tl.right
                elif value < tl.value:
                    tl = tl.left
                else:
                    return

        #set the target location to the value
        if value >= old_location.value:
            old_location.right = node
        elif value < old_location.value:
            old_location.left = node

    def remove(self, value: object) -> bool:
        """
        takes a object value in as an argument, scans to see if it exists,
        returns false if it dosent, removes and returns true if it does
        exist
        """
        parent = None
        node = self._root
        #see if the node actually exists
        while node != None and node.value != value:
            parent = node
            if value < node.value:
                node = node.left
            else:
                node = node.right
        #node dosent exist, exit
        if node == None:
            return False
        #node exists... continue

        #node has more than one child trees
        if node.left != None and node.right != None:
            #find the leftmost child of the right subtree (inorder_sucessor)
            parent_successor = node
            successor = node.right

            while successor.left != None:
                parent_successor = successor
                successor = successor.left
            node.value = successor.value
            node = successor
            parent = parent_successor

        #if the node has a subtree
        if node.left == None:
            child = node.right
        else:
            child = node.left

        #node replaced by child
        if parent == None:
            root = child
        elif parent.left == node:
            parent.left = child
        else:
            parent.right = child
        if self._root == node:
            self._root = child
        return True

    def contains(self, value: object) -> bool:
        """
        takes an object value in as an argument and
        returns true if it exists in the tree,
        false otherwise
        """
        target_location = self._root
        tl = target_location
        #start looking
        while tl != None:
            if value == tl.value:
                return True
            elif value < tl.value:
                tl = tl.left

            else:
                tl = tl.right
        #we dident find it
        return False

    def inorder_traversal(self) -> Queue:
        """
        takes no arguments, performs an inorder traversal of the
        tree returns a queue object of nodes visited
        """
        queue = Queue()
        current_location = self._root
        previous_location = None

        #actually a safe loop, go through iter
        cl = current_location
        while cl:
            if cl.left == None:
                queue.enqueue(cl.value)
                cl = cl.right
            else:
                previous_location = cl.left
                pl = previous_location
                while pl.right and pl.right != cl:
                    pl = pl.right

                if pl.right == None:
                    pl.right = cl
                    cl = cl.left
                else:
                    pl.right = None
                    queue.enqueue(cl.value)
                    cl = cl.right

        return queue


    def find_min(self) -> object:
        """
        finds minimum value, no arguments, returns object
        as mininum
        """
        #min on left, so find bottom left
        if self._root == None:
            return None
        else:
            while self._root.left:
                self._root = self._root.left
            return self._root.value

    def find_max(self) -> object:
        """
        finds max value, no arguments, returns object
        as maximum
        """
        #max on right, so find bottom right, copy logic from min
        if self._root == None:
            return None
        else:
            while self._root.right:
                self._root = self._root.right
            return self._root.value

    def is_empty(self) -> bool:
        """
        returns true if tree is empty, false otherwise
        """
        #if the root is empty, there are no children
        if self._root == None:
            return True
        else:
            return False

    def make_empty(self) -> None:
        """
        makes the tree empty
        """
        #wipes family history :'(
        self._root = None



# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

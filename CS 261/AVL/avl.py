# Name: Sterling Violette
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 2/27/2023
# Description: An AVL class that inherits the BST class.
#              Mimics the usage of an AVL tree by using
#              balancing. Has method such as add and remove,
#              as well as helper methods for add and remove.


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Takes an object value in as an argument and
        adds the value to the tree, rebalancing as
        necessary using helper methods
        """
        node = AVLNode(value)
        #use bst method to see if its empty
        if self.is_empty() == True:
            self._root = node
            if self._root == node:
                return
        else:
            #not empty... continue
            target_location = self._root
            flag = 0
            while value == value and flag == 0:
                #if its less than
                if value < target_location.value:
                    if target_location.left == None:
                        target_location.left = node
                        node.parent = target_location
                        flag = 1
                    elif target_location.left != None:
                        target_location = target_location.left

                #if greater than
                elif value > target_location.value:
                    if target_location.right == None:
                        target_location.right = node
                        node.parent = target_location
                        flag = 1
                    elif target_location.right != None:
                        target_location = target_location.right
                #stop infinite loop case
                else:
                    return
                #update and rebalance
            if flag == 1:
                while target_location != None and flag == 1:
                    self._update_height(target_location)
                    self._rebalance(target_location)
                    target_location = target_location.parent

    def remove(self, value: object) -> bool:
        """
        takes an object value in as an argument, and
        if it is found, removes the node and returns true,
        otherwise returns false, rebalances as necessary using
        helper methods
        """
        #use bst method to see if is empty
        if self.is_empty() == True:
            return False
        else:
            flag = 0
            #set to root initially
            target_location = self._root
            while value == value and flag == 0:
                #if we found it, iter 1 this is root
                if value == target_location.value:
                    target_location_parent = target_location.parent

                    #if its the root
                    if target_location_parent == None:
                        #create node holder
                        target_location_parent = AVLNode(value)
                        target_location_parent.height = None
                        target_location_parent.right = target_location

                    #if its a parent, parents always have children
                    if target_location.right != None and target_location.left != None:
                        #remove the trees
                        holder = self._remove_two_subtrees(target_location_parent, target_location)

                    #if its a child, ie no children themselves
                    elif target_location.right == None and target_location.left == None:

                        #determine location placement
                        tlp_value = target_location_parent.value
                        tl_value = target_location.value

                        if tl_value >= tlp_value:
                            target_location_parent.right = None
                        elif tl_value < tlp_value:
                            target_location_parent.left = None
                        #finally
                        holder = target_location_parent

                    else:
                        #simplify writing for target_location
                        tl_right = target_location.right
                        tl_left = target_location.left
                        tl_value = target_location.value

                        #same for parent... this might make it more confusing actually
                        tlp_left = target_location_parent.left
                        tlp_right = target_location_parent.right
                        tlp_value = target_location_parent.value
                        #one or other is child
                        if tl_right == None or tl_left == None:

                            #right child
                            if tl_right == None:
                                child = tl_left
                            #left child
                            elif tl_left == None:
                                child = tl_right
                            child.parent = target_location_parent

                            if value >= tlp_value:
                                target_location_parent.right = child
                            elif value < tlp_value:
                                target_location_parent.left = child
                            #finally
                            holder = target_location_parent

                    #catch a case where the root was the value...
                    if holder.height == None:
                        holder =None
                    #root case
                    if target_location_parent.height == None:
                        self._root = target_location_parent.right
                        if self._root == None:
                            return True
                        target_location_parent = None
                        self._root.parent = None
                    #exit loop
                    flag = 1

                #determine if place is left
                elif value <= target_location.value:
                    target_location = target_location.left
                    #dosent exist check
                    if target_location== None:
                        return False

                #determine if place is right
                elif value > target_location.value:
                    target_location = target_location.right
                    #dosemnt exist check
                    if target_location == None:
                        return False

            while value == value and holder != None:
                self._rebalance(holder)
                self._update_height(holder)
                #continue checking
                holder = holder.parent

            #finally
            if flag == 1:
                return True

    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        takes a remove parent node, the removal node, in as arguments
        and removes two subtrees of them
        """
        new_parent = remove_node.right
        np = new_parent
        #check for right
        if np.left == None:
            remove_node.value = np.value
            remove_node.right = np.right
            if remove_node.right != None:
                remove_node.right.parent = remove_node
            return remove_node

        #if left parent is not none, look through until end
        if np.left != None and remove_parent == remove_parent:
            while np.left != None and remove_parent == remove_parent:
                np= np.left

        new_parent_parent = np.parent
        remove_node.value = np.value

        #if its the right no looking needed
        if np.right != None:
            np.right.parent = new_parent_parent

        new_parent_parent.left = np.right
        return new_parent_parent

    def _balance_factor(self, node: AVLNode) -> int:
        """
        takes a node in as the argument and determins the balance
        factor, returns factor as int
        """
        factor = (self._get_height(node.right) - self._get_height(node.left))
        return factor

    def _get_height(self, node: AVLNode) -> int:
        """
        takes a node in as an argument, and returns the height of the node
        """
        if node == None:
            #-1 if none as dosent exist
            return -1
        elif node != None:
            return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        takes a node in as an argument, and rotates left, returns
        avl node child
        """
        child = node.right
        flag = 0
        node.right = child.left
        #check for right
        if node.right != None:
            node.right.parent = node
            child.parent = node.parent
            child.left = node
            node.parent = child
        #we can update still
        else:
            child.parent = node.parent
            child.left = node
            node.parent = child
        #consider parents
        if child.parent != None:
            if node.value >= child.parent.value:
                child.parent.right = child
                flag = 1
            elif node.value < child.parent.value:
                child.parent.left = child
                flag = 1

        flag = 1
        #we made changes, update
        if flag == 1:
            self._update_height(child.right)
            self._update_height(child.left)
            self._update_height(child)
            self._update_height(child.parent)
        return child

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        takes a node in as an argument, and rotates right, returns
        avl node child
        """
        #can use logic from rotate left, but reversed :)
        child = node.left
        flag = 0
        node.left = child.right
        #check for right
        if node.left != None:
            node.left.parent = node
            child.right = node
            child.parent = node.parent
            node.parent = child
        #we can update still
        else:
            child.right = node
            child.parent = node.parent
            node.parent = child
        #consider parents
        if child.parent != None:
            if node.value >= child.parent.value:
                child.parent.right = child
                flag = 1
            elif node.value < child.parent.value:
                child.parent.left = child
                flag = 1

        flag = 1
        #we made changes, update
        if flag == 1:
            self._update_height(child.right)
            self._update_height(child.left)
            self._update_height(child)
            self._update_height(child.parent)
        return child

    def _update_height(self, node: AVLNode) -> None:
        """
        takes a node in as an argument, and changes its heigth,
        returns nothing but makes changes
        """
        #node could be none, exit if so
        if node == None:
            return
        #not none
        #find biggest heigth
        if self._get_height(node.right) >= self._get_height(node.left):
            maximum = self._get_height(node.right)
        elif self._get_height(node.right) < self._get_height(node.left):
            maximum = self._get_height(node.left)
        node.height = maximum + 1 #+1 for iterable consideration...

    def _rebalance(self, node: AVLNode) -> None:
        """
        takes a node in, and rebalances, used heavily for rebalacning
        on the add and remove methods specifcially
        """
        if node.parent == None:
            self._root = node

        #see if balances
        if self._balance_factor(node) < -1:
            #check left
            if self._balance_factor(node.left) > 0:
                #we need to rotate left
                node.left = self._rotate_left(node.left)
                node = self._rotate_right(node)

            elif self._balance_factor(node.left) <= 0:
                #we need to rotate right
                node = self._rotate_right(node)

        #see if balanced
        elif self._balance_factor(node) > 1:
            #check right
            if self._balance_factor(node.right) < 0:
                #we need to rotate left
                node.right = self._rotate_right(node.right)
                node = self._rotate_left(node)

            elif self._balance_factor(node.right) >= 0:
                node = self._rotate_left(node)

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

# Author: Sterling Violette
# GitHub username: Sterlinghv
# Date: 11/8/2022
# Description: A program that implements the ideas behind a linked list and functions with it
#              such as adding a node, reversing a list etc.. but all functions are done using recursion

class Node:
    """
    represents a single node in a linked list of nodes
    """
    def __init__(self, val):
        """
        creates a new node object
        """
        self.data = val
        self.next = None

class LinkedList:
    """
    This class represents a linked list of nodes
    """
    def __init__(self):
        """
        creates a new linked list
        """
        self._head = None

    def get_head(self):
        """
        returns the head aka the first node
        """
        return self._head

    def display(self):
        """
        recursive display method
        """
        self.display_helper(self._head)

    def display_helper(self, node):
        """recursive display helper method"""
        if node is None:
            return
        self.display_helper(node.next)

    def contains(self, key):
        """
        recursive contains method
        """
        return self.contains_helper(key, self._head)

    def contains_helper(self, key, node):
        """
        recursive contains helper method
        """
        if node is None:
            return False
        if node.data == key:
            return True
        return self.contains_helper(key, node.next)

    def insert_helper(self, val, pos, node):
        """
        recursive insert helper method
        """
        if node.next is None:
            node.next = Node(val)
        elif pos == 0:
            temp = node.next
            node.next = Node(val)
            node.next.next = temp
        else:
            self.insert_helper(val, pos - 1, node.next)

    def insert(self, val, pos):
        """
        recursive insert method
        """
        if self._head is None:
            self.add(val)
            return
        if pos == 0:
            temp = self._head
            self._head = Node(val)
            self._head.next = temp
        else:
            self.insert_helper(val, pos - 1, self._head)

    def reverse_helper(self, node):
        """
        recursive reverse helper method
        """
        if node.next is None:
            return node
        else:
            current_next = node.next
            new_head = self.reverse_helper(node.next)
            node.next = None
            current_next.next = node
            return new_head

    def reverse(self):
        """
        recursive reverse method
        """
        if self._head is None:
            return
        self._head = self.reverse_helper(self._head)

    def add_helper(self, val, node):
        """
        recursive add helper method
        """
        if node.next is None:
            node.next = Node(val)
        else:
            self.add_helper(val, node.next)

    def add(self, val):
        """
        recursive add
        """
        if self._head is None:
            self._head = Node(val)
        else:
            self.add_helper(val, self._head)

    def remove_helper(self, val, node):
        """
        recursive remove helper method
        """
        if node.next is None:
            return
        elif node.next.data == val:
            node.next = node.next.next
        else:
            self.remove_helper(val, node.next)

    def remove(self, val):
        """
        recursive remove method
        """
        if self._head is None:
            return
        if self._head.data == val:
            self._head = self._head.next
        else:
            self.remove_helper(val, self._head)

    def plain_list_helper(self, node):
        """
        helper method for turning a linked list into a python list helper
        """
        if node is None:
            return []
        else:
            plain_list = []
            plain_list.append(node.data)
            plain_list.extend(self.plain_list_helper(node.next))
            return plain_list

    def to_plain_list(self):
        """
        recursive method that turns a linked list into a normal python list
        """
        if self._head is None:
            return []
        return self.plain_list_helper(self._head)

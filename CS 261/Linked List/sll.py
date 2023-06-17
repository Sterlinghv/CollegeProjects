# Name: Sterling Violette
# OSU Email: violetts@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 3
# Due Date: 2/13/2023
# Description: Single linked list data structure
#              implementation that has many methods
#              that alter the list such as inserting at back,
#              and removing at front.


from SLNode import *


class SLLException(Exception):
    """
    Custom exception class to be used by Singly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class LinkedList:
    def __init__(self, start_list=None) -> None:
        """
        Initialize new linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = SLNode(None)

        # populate SLL with initial values (if provided)
        # before using this feature, implement insert_back() method
        if start_list is not None:
            for value in start_list:
                self.insert_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'SLL ['
        node = self._head.next
        while node:
            out += str(node.value)
            if node.next:
                out += ' -> '
            node = node.next
        out += ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        length = 0
        node = self._head.next
        while node:
            length += 1
            node = node.next
        return length

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return not self._head.next

    # ------------------------------------------------------------------ #

    def insert_front(self, value: object) -> None:
        """
        Adds a new value taken in as an argument to the front
        """

        node = SLNode(value)
        node.next = self._head.next
        self._head.next = node

    def insert_back(self, value: object) -> None:
        """
        Adds a new node value as an agument to the end
        """
        temp = self._head

        #move
        while temp.next:
            temp = temp.next
        temp.next = SLNode(value)

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Inserts a new value as an argument at the specified index
        """
        #declare
        node = SLNode(value)
        count = 0

        if index < 0:
            raise SLLException
        else:
            #if index is 0 insert to front of list
            if index == 0:
                node.next = self._head.next
                self._head.next = node

            else:
                #start at beginning of linked list and iterate until index is reached
                temp = self._head
                while temp is not None:

                    if count == index:
                        node.next = temp.next
                        temp.next = node
                        return

                    temp = temp.next
                    count += 1

                if temp is None:
                    raise SLLException

    def remove_at_index(self, index: int) -> None:
        """
        takes an index int as argument and removes the node
        in that index
        """
        #declare
        count = 0

        if self.is_empty():
            raise SLLException
        if self._head is None:
            raise SLLException
        if index < 0:
            raise SLLException

        if index == 0:
            node_delete = self._head
            self._head = self._head.next
            node_delete = None
        else:
            temp = self._head
            while temp is not None:
                if count == index:
                    node_delete = temp.next
                    temp.next = temp.next.next
                    node_delete = None
                    return
                temp = temp.next
                count += 1
                if temp.next is None:
                    raise SLLException()

    def remove(self, value: object) -> bool:
        node = self._head
        """
        takes a value as an object argument and traverses the list
        if it finds the value, it removes it
        """

        #find first appearance of value
        while node:
            if node.value == value:
                break
            prev = node
            node = node.next
        if node is None:
            return False
        #if found point previous node to next node
        else:
            prev.next = node.next
            return True

    def count(self, value: object) -> int:
        """
        counts the number of times the argument value is
        seen in the list
        """
        node = self._head

        count = 0
        # find each appearance of key and increment count
        while node:
            if node.value == value:
                count += 1
            node = node.next
        return count

    def find(self, value: object) -> bool:
        """
        returns true or false based upon if the agrument object
        was found in the list
        """
        node = self._head

        count = 0
        #find if occurence of value exists, if so return True, else return False
        while node:
            if node.value == value:
                return True
            node = node.next
        return False

    def slice(self, start_index: int, size: int) -> "LinkedList":
        """
        returns a new linked list based upon the requested
        arguments of start index, and then how big
        """
        #exceptions checkers...
        if start_index < 0:
            raise SLLException
        if size < 0:
            raise SLLException
        if start_index > self.length():
            raise SLLException
        if start_index == self.length():
            raise SLLException
        if size > self.length():
            raise SLLException
        if start_index + size > self.length():
            raise SLLException

        #declare
        count = 0
        node = self._head
        link_list = LinkedList()

        #iterate until start index is reached
        while count != start_index + 1 and node is not None:
            count += 1
            node = node.next
        #when start index is reached add values to back of new linked list until size is equal to 1
        while size >= 1 and node is not None:
            link_list.insert_back(node.value)
            node = node.next
            size -= 1
        #if size is 1 and count is greater than or equal to size, then raise exception
        if size == 1 and count >= size:
            raise Exception

        return link_list


if __name__ == "__main__":

    # print("\n# insert_front example 1")
    # test_case = ["A", "B", "C"]
    # lst = LinkedList()
    # for case in test_case:
    #     lst.insert_front(case)
    #     print(lst)

    # print("\n# insert_back example 1")
    # test_case = ["C", "B", "A"]
    # lst = LinkedList()
    # for case in test_case:
    #     lst.insert_back(case)
    #     print(lst)

    # print("\n# insert_at_index example 1")
    # lst = LinkedList()
    # test_cases = [(0, "A"), (0, "B"), (1, "C"), (3, "D"),(-1, "E"), (5, "F")]
    # for index, value in test_cases:
    #     print("Inserted", value, "at index", index, ": ", end="")
    #     try:
    #         lst.insert_at_index(index, value)
    #         print(lst)
    #     except Exception as e:
    #         print(type(e))

    # print("\n# remove_at_index example 1")
    # lst = LinkedList([1, 2, 3, 4, 5, 6])
    # print(f"Initial LinkedList : {lst}")
    # for index in [0, 2, 0, 2, 2, -2]:
    #     print("Removed at index", index, ": ", end="")
    #     try:
    #         lst.remove_at_index(index)
    #         print(lst)
    #     except Exception as e:
    #         print(type(e))

    # print("\n# remove example 1")
    # lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    # print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    # for value in [7, 3, 3, 3, 3]:
    #     print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
    #           f"\n {lst}")

    # print("\n# remove example 2")
    # lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    # print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    # for value in [1, 2, 3, 1, 2, 3, 3, 2, 1]:
    #     print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
    #           f"\n {lst}")

    # print("\n# count example 1")
    # lst = LinkedList([1, 2, 3, 1, 2, 2])
    # print(lst, lst.count(1), lst.count(2), lst.count(3), lst.count(4))

    # print("\n# find example 1")
    # lst = LinkedList(["Waldo", "Clark Kent", "Homer", "Santa Claus"])
    # print(lst)
    # print(lst.find("Waldo"))
    # print(lst.find("Superman"))
    # print(lst.find("Santa Claus"))

    print("\n# slice example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ll_slice = lst.slice(1, 3)
    print("Source:", lst)
    print("Start: 1 Size: 3 :", ll_slice)
    ll_slice.remove_at_index(0)
    print("Removed at index 0 :", ll_slice)

    print("\n# slice example 2")
    lst = LinkedList([10, 11, 12, 13, 14, 15, 16])
    print("Source:", lst)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1)]
    for index, size in slices:
        print("Start:", index, "Size:", size, end="")
        try:
            print(" :", lst.slice(index, size))
        except:
            print(" : exception occurred.")

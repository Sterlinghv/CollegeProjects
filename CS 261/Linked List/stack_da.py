# Name: Sterling Violette
# OSU Email: violetts@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 3
# Due Date: 2/13/2023
# Description: Uses a dynamic array class to act as a stack
#              and has varios methods that pop, push and return the
#              top of the dynamic array


from dynamic_array import *

class StackException(Exception):
    """
    Custom exception to be used by Stack class
    DO NOT CHANGE THIS METHOD IN ANY WAY
    """
    pass


class Stack:
    def __init__(self):
        """
        Init new stack based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._da = DynamicArray()

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "STACK: " + str(self._da.length()) + " elements. ["
        out += ', '.join([str(self._da[i]) for i in range(self._da.length())])
        return out + ']'

    def is_empty(self) -> bool:
        """
        Return True is the stack is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.is_empty()

    def size(self) -> int:
        """
        Return number of elements currently in the stack
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.length()

    # -----------------------------------------------------------------------

    def push(self, value: object) -> None:
        """
        Takes a value in as an argument object and
        pushes the value to the end of the DA
        """
        #can use append :)
        self._da.append(value)

    def pop(self) -> object:
        """
        removes the top element of the stack in DA and
        returns it
        """
        if self.is_empty():
            raise StackException()
        else:
            #store value at last index of dynamic array
            value = self._da.get_at_index(self.size() - 1)

            #remove value at last index of dynamic array
            self._da.remove_at_index(self.size() - 1)
            return value

    def top(self) -> object:
        """
        returns the value at the top of the stack only
        """
        if self.is_empty():
            raise StackException()
        else:
            return self._da.get_at_index(self.size() - 1)

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    # print("\n# push example 1")
    # s = Stack()
    # print(s)
    # for value in [1, 2, 3, 4, 5]:
    #     s.push(value)
    # print(s)

    print("\n# pop example 1")
    s = Stack()
    try:
        print(s.pop())
    except Exception as e:
        print("Exception:", type(e))
    for value in [1, 2, 3, 4, 5]:
        s.push(value)
    for i in range(6):
        try:
            print(s.pop())
        except Exception as e:
            print("Exception:", type(e))

    print("\n# top example 1")
    s = Stack()
    try:
        s.top()
    except Exception as e:
        print("No elements in stack", type(e))
    s.push(10)
    s.push(20)
    print(s)
    print(s.top())
    print(s.top())
    print(s)

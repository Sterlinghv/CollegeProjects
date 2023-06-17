# Name:
# OSU Email:
# Course: CS261 - Data Structures
# Assignment:
# Due Date:
# Description:


from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return 'HEAP ' + str(heap_data)

        def add(self, node: object) -> None:
            """

            """
            self._heap.append(node)
            length = self._heap.length()
            length = length - 1
            index = length
            parent_index = index - 1
            parent_index = parent_index // 2

            while parent_index >= 0:
                index_value = self._heap.get_at_index(index)
                parent_index_value = self._heap.get_at_index(parent_index)
                if index_value < parent_index_value:
                    self._heap[index], self._heap[parent_index] = self._heap[parent_index], self._heap[index]
                index = index - 1
                index = index // 2
                parent_index = index - 1
                parent_index = parent_index // 2

        def is_empty(self) -> bool:
            """

            """
            if self._heap.length() == 0:
                return True
            else:
                return False

        def get_min(self) -> object:
            """

            """
            if self.is_empty() == True:
                raise MinHeapException
            else:
                minimum = self._heap.get_at_index(0)
                return minimum

        def remove_min(self) -> object:
            """

            """
            if self.is_empty():
                raise MinHeapException
            min_element = self._heap[0]
            self._heap[0] = self._heap[self._heap.length() - 1]
            self._heap.remove_at_index(self._heap.length() - 1)
            _percolate_down(self._heap, 0)
            return min_element

        def build_heap(self, da: DynamicArray) -> None:
            """

            """
            self._heap = copy.deepcopy(da)
            for heapify_idx in range(self._heap.length() - 1, -1, -1):
                idx = heapify_idx
                _percolate_down(self._heap, idx)

        def size(self) -> int:
            """

            """
            size = self._heap.length()
            return size

        def clear(self) -> None:
            """

            """
            heap = MinHeap()
            data = heap._heap
            self._heap = data

    def heapsort(da: DynamicArray) -> None:
        """

        """
        for heapify_idx in range(da.length() - 1, -1, -1):
            idx = heapify_idx
            _percolate_down(da, idx)

        for size in range(da.length(), 0, -1):
            da[0], da[size - 1] = da[size - 1], da[0]
            parent = 0
            while 2 * parent + 1 < size - 1:
                left_idx = 2 * parent + 1
                right_idx = left_idx + 1
                left_val = da[left_idx]
                if 2 * parent + 2 == size - 1:
                    right_val = left_val
                else:
                    right_val = da[right_idx]
                swap_idx = left_idx
                if left_val > right_val:
                    swap_idx = right_idx
                if da[parent] <= da[swap_idx]:
                    break
                da[parent], da[swap_idx] = da[swap_idx], da[parent]
                parent = swap_idx

    def _percolate_down(da: DynamicArray, parent: int) -> None:
        """
        This method percolates down item by index `parent` in the `da`
        """
        while 2 * parent + 1 < da.length():
            left_idx = 2 * parent + 1
            right_idx = left_idx + 1
            left_val = da[left_idx]
            if 2 * parent + 2 == da.length():
                right_val = left_val
            else:
                right_val = da[right_idx]
            swap_idx = left_idx
            if left_val > right_val:
                swap_idx = right_idx
            if da[parent] <= da[swap_idx]:
                break
            da[parent], da[swap_idx] = da[swap_idx], da[parent]
            parent = swap_idx

    # ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)

    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)

    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)

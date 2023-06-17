# Name: Sterling Violette
# OSU Email: violetts@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 2
# Due Date: 1/06/2023
# Description: A dynamic array class that can scale and changes its
# capacity based upon various functions. Helper functions
# are also included that do things such as finding the mode, and
# mapping and filtering.


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        function that takes a new capacity argument as an integer
        if new capacity is 0 or less than current size, return nothing
        if its greater, then add capacity to array object
        """
        #validation checks
        if new_capacity == 0:
            return
        if new_capacity < self._size:
            return
        else:
            new_data = StaticArray(new_capacity)
            #copy data from old array to new array and set
            #old arrays data to new arrays data
            for index in range(self._size):
                new_data.set(index, self._data[index])
            self._data = new_data
            self._capacity = new_capacity

    def append(self, value: object) -> None:
        """
        appends a value into an array, if size is maxed out,
        doubles capacity via the resize method, otherwise just
        sets the last index of size to the value
        """
        if self._size == self._capacity:
            #double
            self.resize(2 * self._capacity)
        index = self._size
        self._data[index] = value
        self._size += 1

    def insert_at_index(self, index: int, value: object) -> None:
        """
        takes two arguments, index as an int and value of item to
        be inserted at that index. Uses resize to double capacity
        if current capacity is maxxed
        """
        if index < 0:
            raise DynamicArrayException
        if index > self._size:
            raise DynamicArrayException
        else:
            if self._capacity == self._size:
                self.resize(2 * self._capacity)
            tick = 0
            for count_index in range(index, self._size):
                if tick == 0:
                    holder_data = self._data[count_index + 1]
                    self._data[count_index + 1] = self._data[count_index]
                    tick += 1
                else:
                    holder_data_2 = self._data[count_index + 1]
                    self._data[count_index + 1] = holder_data
                    holder_data = holder_data_2
            self._data[index] = value
            self._size += 1

    def remove_at_index(self, index: int) -> None:
        """
        function that takes an index as an integer and remove the value
        of the array at said index, also changes capacity based on checks
        """
        if index < 0:
            raise DynamicArrayException
        if index > self._size - 1:
            raise DynamicArrayException
        else:
            flag = 0
            #first check, if size less than 1/4'th cap, and the size * 2 is gt or eq to 10
            #we know we are safe to reduce the size without going below 10
            if self._size < self._capacity / 4 and self._size * 2 >= 10 and self._capacity >= 10:
                self.resize(self._size * 2)
                #set flag, so we wont do anything else
                flag = 1

            #second catch to the case when size is less than 10, and its capacity is
            #also less than 10, we dont want to do anything except
            #set flag
            if self._size < 10 and self._capacity < 10 and flag == 0:
                #set flag, so we wont do anything else
                flag = 1

            #last check, if size is less than 1/4'th cap, but also cap is gt or eq to 10,
            #then the minimum cap we can set is 10
            if self._size < self._capacity / 4 and self._capacity >= 10 and flag == 0:
                self.resize(10)
                #set flag, so we wont do anything else
                flag = 1

            stop = (self._size - 1)
            for count_index in range(index, stop):
                if count_index > stop:
                    count_index += 1
                else:
                    holder_data = self._data[count_index]
                    self._data[count_index] = self._data[count_index + 1]
            self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        function that takes two arguments of start index and size both ints
        start index referes to where in the original DA to start, and size
        refers to how many items ++ it should collect and put into
        another DA, which is  returned
        """
        #raise exceptions if:
        if start_index > self._size - 1:
            raise DynamicArrayException
        if start_index < 0:
            raise DynamicArrayException
        if (start_index + size) - 1 > self._size - 1:
            raise DynamicArrayException
        if size < 0:
            raise DynamicArrayException
        else:
            #create new DA, and store the range
            newArr = DynamicArray()
            for index in range(start_index, start_index + size):
                data = self._data[index]
                newArr.append(data)
            return newArr

    def merge(self, second_da: "DynamicArray") -> None:
        """
        function that merges two dynamic arrays together.
        takes 1 argument which is the second DA, and appends each value in
        second DA to the first DA
        """
        for index in range(second_da._size):
            value = second_da._data[index]
            self.append(value)

    def map(self, map_func) -> "DynamicArray":
        """
        function that takes another function and applies said
        function to all items within a dynanmic array. Then returns
        a new dynamic array with all the applied values
        """
        newArr = DynamicArray()
        #apply function to all value and append
        for index in range(self._size):
            value = self._data[index]
            new_value = map_func(value)
            newArr.append(new_value)
        return newArr

    def filter(self, filter_func) -> "DynamicArray":
        """
        function that takes another function and applies
        said function to all items within a dynamic array. Then returns
        a new dynamic array with all the applied values where the function
        return true
        """
        newArr = DynamicArray()
        #apply function to all value and append
        for index in range(self._size):
            value = self._data[index]
            bool_value = filter_func(value)
            if bool_value == True:
                newArr.append(value)
        return newArr

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        function that takes another function, and applies
        it to all the values, but accumulates the values
        until there is only 1 output remaining, and that
        is what is returned
        """
        if self._size == 0:
            return initializer
        if initializer == None:
            output = self._data[0]
            for index in range(self._size - 1):
                value = self._data[index]
                next_value = self._data[index + 1]
                output = reduce_func(output, next_value)
        #we have an initilizer, need to account for it
        else:
            output = initializer
            next_value = self._data[0]
            for index in range(self._size):
                value = self._data[index]
                output = reduce_func(output, next_value)
                next_value = self._data[index + 1]
        return output



def find_mode(arr: DynamicArray) -> (DynamicArray, int):
    """
    function that takes in a dynamic array as an argument
    and finds the mode of the array, then outputs mode items
    and frequency into a tuple
    """
    #first we need to find the max
    current_item_count = 0
    max = 1
    item_max = arr.get_at_index(0)
    for index in range(arr.length()):
        current_item = arr.get_at_index(index)
        if index == 0:
            previous_item = current_item
            current_item_count += 1
        else:
            if current_item == previous_item:
                current_item_count += 1
            if current_item != previous_item:
                current_item_count = 1
            if current_item_count > max:
                max = current_item_count
                item_max = current_item
        previous_item = current_item

    #this is to catch if the max is only 1
    newArr = DynamicArray()
    if max == 1:
        for index in range(arr.length()):
            value = arr.get_at_index(index)
            newArr.append(value)

    #now we use very similar find max logic
    #but if the item count is equal to the max,
    #add it to new array
    again_flag = 0
    current_item_count = 0
    for index in range(arr.length()):
        current_item = arr.get_at_index(index)
        if index == 0:
            previous_item = current_item
            current_item_count += 1
        else:
            if current_item == previous_item:
                current_item_count += 1
                if current_item_count == max:
                    newArr.append(current_item)
            if current_item != previous_item:
                current_item_count = 1
        previous_item = current_item

    final_tuple = (newArr, max)
    return final_tuple

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# merge example 1")
    da = DynamicArray([1, 2, 3, 4, 5])
    da2 = DynamicArray([10, 11, 12, 13])
    print(da)
    da.merge(da2)
    print(da)

    print("\n# merge example 2")
    da = DynamicArray([1, 2, 3])
    da2 = DynamicArray()
    da3 = DynamicArray()
    da.merge(da2)
    print(da)
    da2.merge(da3)
    print(da2)
    da3.merge(da)
    print(da3)

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
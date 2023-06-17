# Name: Sterling Violette
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Description: Methods for altering a HashMap class that
# uses quadratic probing. Methods include remove, put, get and
# others including iter and next methods

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Takes a key argument as a string and a value and an object argument
        and inserts or updates the key-value pair in the hash map.
        """

        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        quadratic_probe = 0
        hash_func_key = self._hash_function(key)
        bucket = hash_func_key % self._capacity
        initial_bucket = bucket

        while True:
            target = self._buckets[bucket]
            #if empty or tombstone is found store the key and value

            if target is None or target.is_tombstone:
                self._buckets[bucket] = HashEntry(key, value)
                self._size += 1
                break

            #if exists update value
            elif target.key == key:
                self._buckets[bucket].value = value
                break

            #increment quadratic_probe and calculate next bucket
            quadratic_probe += 1
            bucket = (initial_bucket + quadratic_probe ** 2) % self._capacity
        

    def table_load(self) -> float:
        """
        Takes no arguments but calculates and returns the table load.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        This method takes no arguments but calculates and
        returns the number of empty buckets in the hash map.
        """
        empty_bucket = 0
        length = self._buckets.length()
        #iterate through all buckets in DA
        for index in range(length):
            if self._buckets[index] is None or self._buckets[index].is_tombstone:
                empty_bucket += 1

        return empty_bucket

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes a new capacity in as an integer argument and
        resizes the hash map by creating a new DA with the
        specified new_capacity. It then and inserts into the new DA.
        """
        if new_capacity >= self._size:

            new_buckets = DynamicArray()
            new_capacity = self._next_prime(new_capacity)

            #new DynamicArray with None values
            for bogus_index in range(new_capacity):
                new_buckets.append(None)

            #update to new values
            old_buckets = self._buckets
            self._size = 0
            self._buckets = new_buckets
            self._capacity = new_capacity

            #iterate through all the buckets in old_buckets
            length = old_buckets.length()
            for index in range(length):
                item = old_buckets[index]

                if item is not None and not item.is_tombstone:
                    #use put method to add
                    self.put(item.key, item.value)

    def get(self, key: str) -> object:
        """
        Takes a key in as a str argument then retrieves the value
        associated with the given key in the hash map. It uses quadratic probing
        to search for the key in case of collisions. If the key is found it
        returns the object otherwise it returns none
        """
        #define
        hash_func_key = self._hash_function(key)
        bucket = hash_func_key % self._capacity
        initial_bucket = bucket
        quadratic_probe = 0

        while True:
            target = self._buckets[bucket]

            #if none, we know it dosent exist exit
            if target is None:
                return None
            #matches key and not tomb, we got it
            elif target.key == key and not target.is_tombstone:
                return target.value

            #continue quadratic probing
            quadratic_probe += 1
            capacity = self._capacity
            bucket = (initial_bucket + quadratic_probe ** 2) % capacity

    def contains_key(self, key: str) -> bool:
        """
        Takes in a key as a str argument, then checks if the
        hash map contains the given key. It uses quadratic probing
        to search for the key in case of collisions. If the key
        is found, it returns true else false
        """
        #define
        hash_func_key = self._hash_function(key)
        bucket = hash_func_key % self._capacity
        initial_bucket = bucket
        quadratic_probe = 0

        while True:
            target = self._buckets[bucket]

            #if is none, exit
            if target is None:
                return False

            #we found it
            elif target.key is key and not target.is_tombstone:
                return True

            #continue looking via probing
            quadratic_probe += 1
            bucket = (initial_bucket + quadratic_probe ** 2) % self._capacity

    def remove(self, key: str) -> None:
        """
        Takes in a key as a str argument and removes a key value
        pair from the hash map. If the key is found it marks the entry as
        a tombstone and decrements the size of the hash map.
        """
        #define
        hash_func_key = self._hash_function(key)
        bucket = hash_func_key % self._capacity
        initial_bucket = bucket
        quadratic_probe = 0

        while True:
            target = self._buckets[bucket]

            #does not exist, exit
            if target is None:
                break

            #exists
            elif target.key == key and not target.is_tombstone:
                target.is_tombstone = True
                self._size -= 1
                break

            #continue
            quadratic_probe += 1
            bucket = (initial_bucket + quadratic_probe ** 2) % self._capacity

    def clear(self) -> None:
        """
        Takes in no arguments but clears the entire hash
        map by setting all the entries in the DA to None.
        """
        clear = None
        length = self._buckets.length()
        for index in range(length):
            self._buckets[index] = clear
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Takes no arguments in but creates a new DA containing
        all non tombstone key-value pairs. It iterates through all
        the buckets in the hash map and appends the (key, value) tuple.
        """
        keys_and_values = DynamicArray()

        for bucket in range(self._capacity):
            target = self._buckets[bucket]
            if target is not None and not target.is_tombstone:
                keys_and_values.append((target.key, target.value))

        return keys_and_values

    def __iter__(self):
        """
        Takes no arguments and initializes the iterator for the HashMap class.
        It sets the initial index to 0 and returns the iterator
        """
        self.index = 0
        iterator = self
        return iterator

    def __next__(self):
        """
        Takes no arguments but is called during the iteration of hash map.
        It finds the next non empty and non tombstone entry in the hash map.
        """
        try:
            item = None
            while item is None or item.is_tombstone is True:
                item = self._buckets.get_at_index(self.index)
                self.index += 1

        except DynamicArrayException:
            raise StopIteration

        return item


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

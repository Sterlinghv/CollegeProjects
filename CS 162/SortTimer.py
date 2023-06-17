# Author: Sterling Violette
# GitHub username: Sterlinghv
# Date: 11/16/2022
# Description: Program that compares the time complexity of two sorting algos,
#              in this case, bubble sort and insertion sort. Then graphs
#              the difference in time complexity.

import time
import random
import matplotlib.pyplot as pyplot
import functools

def bubble_sort(a_list):
    """
    Sorts a_list in ascending order
    """
    for pass_num in range(len(a_list) - 1):
        for index in range(len(a_list) - 1 - pass_num):
            if a_list[index] > a_list[index + 1]:
                temp = a_list[index]
                a_list[index] = a_list[index + 1]
                a_list[index + 1] = temp

def insertion_sort(a_list):
    """
    Sorts a_list in ascending order
    """
    for index in range(1, len(a_list)):
        value = a_list[index]
        pos = index - 1
        while pos >= 0 and a_list[pos] > value:
            a_list[pos + 1] = a_list[pos]
            pos -= 1
        a_list[pos + 1] = value

def sort_timer(func):
    """
    decorator for a function that determines the time complexity
    """
    @functools.wraps(func)
    def wrapper(a_list):
        start_time = time.perf_counter()
        func(a_list)
        end_time = time.perf_counter()
        time_elapsed = (end_time - start_time)
        return time_elapsed
    return wrapper


def compare_sorts(bubble, insert):
    """
    compares time complexity of bubble and insert sort
    and then plots the data
    """
    #generate random lists
    list_of_lists1 = []
    list_of_lists2 = []
    x_values = []
    for step in range(1000, 10001, 1000):
        holder_list1 = []
        holder_list2 = []
        x_values.append(step)
        for random_number_index in range(0, step):
            random_num = random.randint(1, 10000)
            holder_list1.append(random_num)
            holder_list2.append(random_num)
        list_of_lists1.append(holder_list1)
        list_of_lists2.append(holder_list2)

    #run the sorts with the random lists
    bubble_times = []
    insertion_times = []
    for run in range(0, 10, 1):
        bubble_times.append(bubble(list_of_lists1[run]))
        insertion_times.append(insert(list_of_lists2[run]))

    #bubble sort line
    pyplot.plot(x_values, bubble_times, 'ro--', linewidth=2, label='Bubble Sort - Time Complexity')
    #insertion sort line
    pyplot.plot(x_values, insertion_times, 'go--', linewidth=2, label='Insertion Sort - Time Complexity')
    pyplot.legend(loc="upper left")
    pyplot.show()

compare_sorts(sort_timer(bubble_sort), sort_timer(insertion_sort))
'''
Write the implementation to solve the powerset problem discussed in the exercise
of the exploration: Backtracking. Name your function powerset(inputSet). Name
your file PowerSet.py
Given a set of n distinct numbers return its power set.
Example1 :
Input: [1,2,3]
Output: [[1, 2, 3], [1, 2], [1, 3], [1], [2, 3], [2], [3], []]
Example2 :
Input: []
Output: [[]]
Note: An empty set is also included in the powerset.
'''

def powerset(input):
    def backtrack(starter, targetSet):
        #define
        holder = list(targetSet)
        power.append(holder)
        stop = len(input)
        for index in range(starter, stop):
            #add the value from inputSet at the current index to targetSet..
            targetValue = input[index]
            targetSet.append(targetValue)
            backtrack(index +1, targetSet)
            targetSet.pop()

    power = []
    backtrack(0, [])
    return power

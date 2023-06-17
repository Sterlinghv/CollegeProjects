'''
Given a list of numbers, return a subsequence of non-consecutive numbers in the form of a
list that would have the maximum sum. When the numbers are all negatives your code
should return []
Example 1: Input: [7,2,5,8,6]
Output: [7,5,6] (This will have sum of 18)
Example 2: Input: [-1, -1, 0]
Output: [0] (This is the maximum possible sum for this array)
Example 3: Input: [-1, -1, -10, -34]
Output: []
a. Implement the solution of this problem using dynamic Programming. Name your
function max_independent_set(nums).
'''

def max_independent_set(nums):
    #if there are no nums to process, return empty list
    if not nums:
        return []

    numsLength = len(nums)
    #initialize memory table list
    memory = []
    indexer = numsLength + 1
    for bogusIndex in range(indexer):
        memory.append((0, []))  

    #fill memory list with the maxium sum and corresponding sub sequence
    for index in range(1, indexer): 
        max_sum_two_positions_back = memory[index - 2][0]
        include_current = max_sum_two_positions_back + nums[index - 1]
        max_sum_previous_position = memory[index -1][0]
        exclude_current = max_sum_previous_position

        #compare the maximum sum when including and excluding the current number
        if include_current > exclude_current:
            new_max_sum = include_current  
            new_subsequence = memory[index - 2][1] +[nums[index - 1]]
        else:
            new_max_sum = exclude_current 
            new_subsequence = memory[index -1][1] 

        memory[index] = (new_max_sum, new_subsequence)


    return memory[numsLength][1]
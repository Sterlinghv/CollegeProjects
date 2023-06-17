'''
Given a collection of amount values (A) and a target sum (S), find all unique combinations in
A where the amount values sum up to S. Return these combinations in the form of a list.
Each amount value may be used only the number of times it occurs in list A. The solution set
should not contain duplicate combinations. Amounts will be positive numbers.
Return an empty list if no possible solution exists.
Example: A = [11,1,3,2,6,1,5]; Target Sum = 8
Result = [[3, 5], [2, 6], [1, 2, 5], [1, 1, 6]]
a. Describe a backtracking algorithm to solve this problem.
b. Implement the solution in a function amount(A, S). Name your file Amount.py
'''

def amount(A, S):
    def backtrace(index, current_sum, path):
        if current_sum == S:
            result.append(list(path))
            return
        
        #if the current sum is greater than the target sum...
        if current_sum > S:
            return
        
        #the index is out of bounds return...
        if index == len(A):
            return
        
        else:
            stop = len(A)
            #iterate through the amount values from the current index
            for index2 in range(index, stop):
                if (index2 > index and A[index2] == A[index2 -1]):
                    continue
                else:
                    #add the current amount to the path and update current sum
                    path.append(A[index2])
                    backtrace(index2+1, current_sum + A[index2],  path)
                    path.pop()

    A.sort()
    result = list()
    backtrace(0, 0, [])
    return result

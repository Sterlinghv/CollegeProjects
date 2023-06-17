'''
You are given a 3-D puzzle. The length and breadth of the puzzle is given by a 2D matrix
puzzle[m][n]. The height of each cell is given by the value of each cell, the value of
puzzle[row][column] give the height of the cell [row][column]. You are at [0][0] cell and you
want to reach to the bottom right cell [m-1][n-1], the destination cell. You can move either
up, down, left, or right. Write an algorithm to reach the destination cell with minimal effort.
How effort is defined: The effort of route is the maximum absolute difference between two
consecutive cells.
If a route requires us to cross heights: 1, 3, 4, 6, 3, 1
The absolute differences between consecutive cells is: |1-3| = 2, |3-4|=1, |4-6|=2,
|6-3|=3, |3-1|=2; this gives us the values: {2, 1, 2, 3, 2}. The maximum value of
these absolute differences is 3. Hence the effort required on this path will be: 3.
Example:
Input: puzzle[][] = [[1, 3, 5], [2, 8, 3], [3, 4, 5]]
Output: 1
Explanation: The minimal effort route would be [1, 2, 3, 4, 5] which has an effort of
value 1. This is better than other routes for instance, route [1, 3, 5, 3, 5] which has
an effort of 2.
'''

def minEffort(puzzle):
    #declare
    places = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    queue = [(0, 0, 0)]
    ma1, ma2 = len(puzzle), len(puzzle[0])
    complexity = []

    #prepare queue
    for _ in range(ma1):
        row = []
        for _ in range(ma2):
            row.append(float('inf'))
        complexity.append(row)
    complexity[0][0] = 0

    while queue:
        #pop first element
        effort, row, colunm = queue.pop(0)

        for place, data in places:
            row_holder, column_holder = row + place, colunm + data
            if 0 <= row_holder < ma1 and 0 <= column_holder < ma2:
                height = puzzle[row_holder][column_holder] - puzzle[row][colunm]
                #take the value of the height difference
                a_height = abs(height)
                if a_height > effort:
                    complexity_holder = a_height
                else:
                    complexity_holder = effort
                if complexity[row_holder][column_holder] > complexity_holder:
                    complexity[row_holder][column_holder] = complexity_holder
                    #append and sort
                    queue.append((complexity_holder, row_holder, column_holder))
                    queue.sort()

    return complexity[-1][-1]
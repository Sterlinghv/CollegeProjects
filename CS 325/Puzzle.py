'''
Apply Graph traversal to solve a problem (Portfolio Project Problem):
You are given a 2-D puzzle of size MxN, that has N rows and M column (M and N can be
different). Each cell in the puzzle is either empty or has a barrier. An empty cell is marked by
- (hyphen) and the one with a barrier is marked by #. You are given two coordinates from
the puzzle (a,b) and (x,y). You are currently located at (a,b) and want to reach (x,y). You can
move only in the following directions.
L: move to left cell from the current cell
R: move to right cell from the current cell
U: move to upper cell from the current cell
D: move to the lower cell from the current cell
You can move to only an empty cell and cannot move to a cell with a barrier in it. Your goal
is to reach the destination cells covering the minimum number of cells as you travel from the
starting cell.

Input: board, source, destination.
Puzzle: A list of lists, each list represents a row in the rectangular puzzle. Each
element is either - for empty (passable) or # for obstacle (impassable). The same
as in the example.
Example:
Puzzle = [
['-', '-', '-', '-', '-'],
['-', '-', '#', '-', '-'],
['-', '-', '-', '-', '-'],
['#', '-', '#', '#', '-'],
['-', '#', '-', '-', '-']
]

source: A tuple representing the indices of the starting position, e.g. for the upper
right corner, source=(0, 4).
destination: A tuple representing the indices of the goal position, e.g. for the lower
right corner, goal=(4, 4).

Output: A list of tuples representing the indices of each position in the path. The first tuple
should be the starting position, or source, and the last tuple should be the destination. If
there is no valid path, None should be returned. Not an empty list, but the None object.
Note: The order of these tuples matters, as they encode a path. Each position in the path
must be empty (correspond to a ‘-’ on the board) and adjacent to the previous position.

Example 1 (consider above puzzle)
Input: puzzle, (0,2), (2,2)
Output: [(0, 2), (0, 1), (1, 1), (2, 1), (2, 2)]
Example 2 (consider above puzzle)
Input: puzzle, (0,0), (4,4)
Output: [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]
Example 3: (consider above puzzle)
Input: puzzle, (0,0), (4,0)
Output: None
'''

def solve_puzzle(board, source, destination):
    #define
    queue = [(source, [source], '')] 
    directions = [(0, -1, 'L'), (0, 1, 'R'), (-1, 0, 'U'), (1, 0, 'D')]
    rows, cols = len(board), len(board[0])
    visited = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append(False)
        visited.append(row)

    #begin
    while queue: 
        (x, y), path, direction_string = queue.pop(0)
        if (x, y) == destination:
            return path, direction_string
        for dindex, dyindex, direction in directions:
            nindex, nyindex = x + dindex, y + dyindex
            #if nx and ny are within the grid
            if nindex >= 0 and nindex < rows and nyindex >= 0 and nyindex < cols:  
                #if the cell has not been visited before
                if not visited[nindex][nyindex]:
                    #if the cell is not an obstacle 
                    if board[nindex][nyindex] != '#':
                        queue.append(((nindex, nyindex), path + [(nindex, nyindex)], direction_string + direction))
                        visited[nindex][nyindex] = True 
    return None
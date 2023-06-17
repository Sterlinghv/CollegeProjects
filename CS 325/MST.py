'''
Implement Prims algorithm Name your function Prims(G). Include function in the file
MST.PY. You can either use brute force approach or priority queue. Try to see if you can
come up with a solution using priority queue.
Input: a graph represented as an adjacency matrix
For example, the graph in the Exploration would be represented as the below
(where index 0 is A, index 1 is B, etc.).
input = [
[0, 8, 5, 0, 0, 0, 0],
[8, 0, 10, 2, 18, 0, 0],
[5, 10, 0, 3, 0, 16, 0],
[0, 2, 3, 0, 12, 30, 14],
[0, 18, 0, 12, 0, 0, 4],
[0, 0, 16, 30, 0, 0, 26],
[0, 0, 0, 14, 4, 26, 0]
]
Output: a list of tuples, wherein each tuple represents an edge of the MST as (v1, v2,
weight)
For example, the MST of the graph in the Exploration would be represented as the
below.
output = [(0, 2, 5), (2, 3, 3), (3, 1, 2), (3, 4, 12), (2, 5, 16), (4, 6, 4)]
Note: the order of edge tuples within the output does not matter; additionally, the
order of vertices within each edge does not matter. For example, another valid
output would be below (v1 and v2 in the first edge are flip-flopped; the last two
edges in the list are flip-flopped).
output = [(2, 0, 5), (2, 3, 3), (3, 1, 2), (3, 4, 12), (4, 6, 4), (2, 5, 16)]
'''

#deal with some logic of heaps
def minKey(key, mst_set_placement):
    min_index_holder = -1
    min_val_holder = float('inf')
    for vindexer in range(len(key)):
        if key[vindexer] < min_val_holder and mst_set_placement[vindexer] == False:
            min_val_holder = key[vindexer]
            min_index_holder = vindexer

    return min_index_holder

def Prims(G):
    V = len(G)
    key = [float('inf')] * V
    parent = [None] * V
    key[0] = 0
    output = []
    mst_set_placement = [False] * V
    parent[0] = -1

    for _ in range(V):
        u = minKey(key, mst_set_placement)
        
        if u == -1:  #check to stop or not
            continue

        mst_set_placement[u] = True

        for v in range(V):
            isEdgePresent = G[u][v] > 0
            isVertexNotInMST = mst_set_placement[v] == False
            isEdgeSmaller = key[v] > G[u][v]

            if isEdgePresent and isVertexNotInMST and isEdgeSmaller:
                key[v] = G[u][v]
                parent[v] = u

    for i in range(1, len(parent)):
        if parent[i] != -1:  #ensure the parent is not None
            parent_node = parent[i]
            current_node = i
            edge_weight = G[i][parent[i]]
            
            edge = (parent_node, current_node, edge_weight)
            
            output.append(edge)

    return output
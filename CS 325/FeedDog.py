'''
You are a pet store owner and you own few dogs. Each dog has a specific hunger level given
by array hunger_level [1..n] (ith dog has hunger level of hunger_level [i]). You have couple of
dog biscuits of size given by biscuit_size [1...m]. Your goal to satisfy maximum number of
hungry dogs. You need to find the number of dogs we can satisfy.
If a dog has hunger hunger_level[i], it can be satisfied only by taking a biscuit of size
biscuit_size [j] >= hunger_level [i] (i.e biscuit size should be greater than or equal to hunger
level to satisfy a dog.)
If no dog can be satisfied return 0.
Conditions:
You cannot give same biscuit to two dogs.
Each dog can get only one biscuit.
Example 1:
Input: hunger_level[1,2,3], biscuit_size[1,1]
Output: 1
Explanation: Only one dog with hunger level of 1 can be satisfied with one cookie of
size 1.
Example 2:
Input: hunger_level[2, 1], biscuit_size[1,3,2]
Output: 2
Explanation: Two dogs can be satisfied. The biscuit sizes are big enough to satisfy the
hunger level of both the dogs.
a. Describe a greedy algorithm to solve this problem
b. Write an algorithm implementing the approach. Your function signature should be
feedDog(hunger_level, biscuit_size); hunger_level, biscuit_size both are one
dimention arrays . Name your file FeedDog.py
'''

def feedDog(hunger_level, biscuit_size):
    # Define and filter...
    hunger_level.sort()
    biscuit_size.sort()
    dogs_satisfied =0
    hunger_index = 0
    sizeOfHunger = len(hunger_level)
    sizeOfBiscuit =len(biscuit_size)
    
    for biscuit_index in range(sizeOfBiscuit):
        #see if hunger_index is in the bounds of the hunger_level
        if hunger_index>=sizeOfHunger:
            break

        #if the current biscuit can satisfy the current dogs hunger...
        if biscuit_size[biscuit_index] >= hunger_level[hunger_index]:
            dogs_satisfied +=1
            hunger_index += 1

    return dogs_satisfied

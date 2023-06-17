#Name: Sterling Violette
#Class: CS 325
#Assignment: Homework 2

'''
Implement the function kthElement(Arr1, Arr2, k) that was written in part a. Name
your file KthElement.py
Examples:
Arr1 = [1,2,3,5,6] ; Arr2= [3,4,5,6,7] ; k= 5
Returns: 4
Explanation: 5th element in the combined sorted array [1,2,3,3,4,5,5,6,6,7] is 4
'''

#3b:
def kthElement(Arr1, Arr2, k):
    #arg 1 = array, arg 2 = array, arg 3 = desired position k
    if len(Arr1) > len(Arr2):
        temp = Arr1 
        Arr1 = Arr2
        Arr2 = temp  #swap arr1 & arr2
    
    if len(Arr1) == 0:
        return Arr2[k-1]
    
    if k == 1:
        return min(Arr1[0], Arr2[0]) 

    middle_1 = min(k // 2, len(Arr1))
    middle_2 = k - middle_1
    index_1 = (middle_1 - 1)
    index_2 = (middle_2 - 1 )

    if Arr1[index_1] < Arr2[index_2]:
        #discard first middle_1 elements in Arr1 and update k
        new_Arr1 = Arr1[middle_1:]
        new_k = (k - middle_1)
        #return
        return kthElement(new_Arr1, Arr2, new_k)
    
    else:
        #discard first middle_2 elements in Arr2 and update k
        new_Arr2 = Arr2[middle_2:]
        new_k = (k - middle_2)
        #return
        return kthElement(Arr1, new_Arr2, new_k)
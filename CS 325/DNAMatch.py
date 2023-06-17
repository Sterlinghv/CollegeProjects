#Name: Sterling Violette
#Class: CS 325
#Assignment: Homework 3

'''
DNA sequence is made of characters A, C, G and T, which represent nucleotides. A sample
DNA string can be given as ACCGTTTAAAG. Finding similarities between two DNA
sequences is a critical computation problem that is solved in bioinformatics.
Given two DNA strings find the length of the longest common string alignment between
them (it need not be continuous). Assume empty string does not match with anything.
Example: DNA string1: ATAGTTCCGTCAAA ; DNA string2: GTGTTCCCGTCAAA

Length of the best continuous length of the DNA string alignment: 12 (TGTTCCGTCAAA)
a. Implement a solution to this problem using Top-down Approach of Dynamic
Programming, name your function dna_match_topdown(DNA1, DNA2)
b. Implement a solution to this problem using Bottom-up Approach of Dynamic
Programming, name your function dna_match_bottomup(DNA1, DNA2)
'''

#1a:
def dna_match_topdown(dna1, dna2):
    #gather length of two sequences
    n = len(dna1)
    m = len(dna2)
    
    #empty dict
    memoryDict = {}
    
    #finds length of common alignment string
    def match(index1, index2):
        #see if index1 and index2 has already been solved and stored in the dict
        if (index1, index2) in memoryDict:
            return memoryDict[(index1, index2)] 
         
        #see if either index index1 or index2 has reached the end of its sequence if so, set the output to 0
        if (index1 == n or index2 == m):
            memoryDict[(index1, index2)] =0 
        
        #if characters in dna1 and dna2 match, increment the length by 1 and look ahead
        elif (dna1[index1] == dna2[index2]):
            memoryDict[(index1, index2)] = 1 +match((index1 + 1), index2+ 1)
        
        #if the current characters do not match try both...
        else:
            memoryDict[(index1, index2)] = max(match(index1 + 1, index2), match(index1, index2 + 1))
        
        return memoryDict[(index1, index2)]   
    return match(0, 0)


#1b:
def dna_match_bottomup(DNA1, DNA2):
    #gather length of two sequences
    n = len(DNA1)
    m = len(DNA2)
    #list for storing
    holder_list = [0] * (m +1)
    
    #empty table
    targetList = []
    for index1 in range(n + 1):
        targetList.append(holder_list[:])  
    
    #Go over the row indexes of the table from n-1 to 0...
    start = (n - 1)
    stopStep = -1     
    for index1 in range(start, stopStep, stopStep):
        start2 = (m - 1)
        stopStep2 = -1 
        for index2 in range(start2, stopStep2, stopStep2):
            #target in DNA1 and DNA2 match
            if DNA1[index1] == DNA2[index2]:  
                targetList[index1][index2] = 1 + targetList[index1 +1][index2 + 1]
            #targets do not match, move forward in both
            else:  
                if targetList[index1 + 1][index2] > targetList[index1][index2 + 1]:
                    targetList[index1][index2] = targetList[index1 + 1][index2]
                else:
                    targetList[index1][index2] = targetList[index1][index2 + 1]     
    return targetList[0][0]

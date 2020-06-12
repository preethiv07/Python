#You are given a dictionary aDict that maps integer keys to integer values. Write a Python function that returns a list of keys in aDict that map to dictionary values that appear exactly once in aDict. 
#•This function takes in a dictionary and returns a list.
#•Return the list of keys in increasing order.
#•If aDict does not contain any values appearing exactly once, return an empty list.
#•If aDict is empty, return an empty list.
#
#For example:
#If aDict = {1: 1, 3: 2, 6: 0, 7: 0, 8: 4, 10: 0} then your function should return [1, 3, 8]
#If aDict = {1: 1, 2: 1, 3: 1} then your function should return []
#
#

#def uniqueValues(aDict):
#    '''
#    aDict: a dictionary
#    returns: a sorted list of keys that map to unique aDict values, empty list if none
#    '''
#    # Your code here
#    ans=[]
#    aDictcopy=aDict.copy()
#    print ("adictcopy",aDictcopy)
#    for i in aDict.keys():
#        print ("i:",i,"value:",aDict[i])
#        del aDictcopy[i]
#        print ("del adictcopy",aDictcopy)
#        if aDict[i] not in aDictcopy.values():
#            ans.append(i)
#            print ("ANS",ans)
#    
#aDict = {1: 1, 3: 2, 6: 0, 7: 0, 8: 4, 10: 0}
#print (uniqueValues(aDict)    )


def uniqueValues(aDict):
    valL = list(aDict.values())
    setL = set(valL)
    uniqL = []
    for i in setL:
        occ = valL.count(i) 
        if occ == 1:
            uniqL.append(i) 
    outL = []
    for j in aDict.keys():
        if aDict[j] in uniqL:
            outL.append(j)
    outL=sorted(outL)
    return outL

aDict = { 3: 2, 6: 0, 7: 0, 8: 4, 10: 0,1: 1} 
print (uniqueValues(aDict))


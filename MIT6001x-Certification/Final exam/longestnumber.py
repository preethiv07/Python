#Write a function called longestRun, which takes as a parameter a list of integers named L
# (assume L is not empty). This function returns the length of the longest run of 
# monotonically increasing numbers occurring in L. 
# A run of monotonically increasing numbers means that a number at position k+1 
# in the sequence is either greater than or equal to the number at position k 
# in the sequence. 
#
#For example, if L = [10, 4, 6, 8, 3, 4, 5, 7, 7, 2] then your function 
#should return the value 5 because the longest run of monotonically increasing integers 
#in L is [3, 4, 5, 7, 7].
#
#Do not leave any debugging print statements when you paste your code in the box.

def longestRun(L):
    ans=[]
    final=[]
    le=len(L)
    for i in range(le):
        if i==0:
            prev=0
        else:
            prev=L[i-1]
        curr=L[i]
        if curr>=prev:
            ans.append(curr)
#            print (ans)
        else:
            ans=[]
            ans.append(curr)
#        print (len(final))
        if len(final)<len(ans):
            final=ans
#            print ("final",final)
    return (len(final))
    
    
L = [10, 4, 6, 8, 3, 4, 5, 7, 7, 2] 
print (longestRun(L)    )
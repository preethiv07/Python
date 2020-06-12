def laceStrings(s1, s2):
    """
    s1 and s2 are strings.

    Returns a new str with elements of s1 and s2 interlaced,
    beginning with s1. If strings are not of same length, 
    then the extra elements should appear at the end.
    """
    # Your Code Here
    l1= (len(s1))
    l2= (len(s2))
    l=0
    ans=''
    if l1>=l2:
        l=l1
    else:
        l=l2
    for i in range(l):
        try:
            first=s1[i]
        except:
            first=''
        try:
            second=s2[i]
        except:
            second= ''
        ans+=first+second
    return ans


s1='a'    
s2='x'
print (laceStrings(s1, s2))
    
#
# Problem #4: Playing a hand
#

def calculateHandlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    ans=0
    for i in hand.keys():
        ans=ans+hand[i]
    return ans
    #
    #
    

hand = {'a':1, 'q':2, 'l':1, 'm':1, 'u':1, 'i':1}
print (calculateHandlen(hand))    
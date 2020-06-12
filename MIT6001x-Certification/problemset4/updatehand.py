# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 21:45:17 2019

@author: H7853
"""

def updateHand(hand, word):
    '''
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    '''
    newhand=hand.copy()
    for i in word:
        newhand[i]=newhand[i]-1
        if (newhand[i])==0:
            del newhand[i]
    return newhand
    

hand = {'a':1, 'q':1, 'l':2, 'm':1, 'u':1, 'i':1}
word ='quail'
hand = updateHand(hand, word)     
print (hand)
#output = {'l'=1,'m'=1}
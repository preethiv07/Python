# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 12:45:46 2019

@author: H7853
"""

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}
# Problem #1: Scoring a word
#
def getWordScore(word, n):
    bonus=0
    l=len(word)
    ans=0
    if l==0:
        return 0
    else:
        if n==l:
            bonus=50
            #return bonus
        for i in word:
            #print("word:",i,"value:",SCRABBLE_LETTER_VALUES[i])
            ans=ans+SCRABBLE_LETTER_VALUES[i]
        return ((ans*l)+bonus)
    
print(getWordScore('weed', 4))

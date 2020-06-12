# The 6.00 Word Game

import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
   print("  ", len(wordList), "words loaded.")
    return wordList

def getFrequencyDict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def getWordScore(word, n):
    """
    Returns the score for a word. Assumes the word is a valid word.

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first turn.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on (see SCRABBLE_LETTER_VALUES)

    word: string (lowercase letters)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    returns: int >= 0
    """
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



#
# Problem #2: Make sure you understand how this function works and what it does!
#
def displayHand(hand):
    """
    Displays the letters currently in the hand.

    For example:
    >>> displayHand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter,end=" ")       # print all on the same line
    print()                             # print an empty line

#
# Problem #2: Make sure you understand how this function works and what it does!
#
def dealHand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    numVowels = n // 3
    
    for i in range(numVowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(numVowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#
# Problem #2: Update a hand by removing letters
#
def updateHand(hand, word):
    """
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
    """
    newhand=hand.copy()
    for i in word:
        newhand[i]=newhand[i]-1
        if (newhand[i])==0:
            del newhand[i]
    return newhand



#
# Problem #3: Test word validity
#
def isValidWord(word, hand, wordList):
    """
    Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or wordList.
   
    word: string
    hand: dictionary (string -> int)
    wordList: list of lowercase strings
    """
    handlist=hand.copy()
    ans= False
    i=''
    if len(word)>0 and word in wordList:
        try:
            for i in word:
                handlist[i]=handlist[i]-1
                if (handlist[i])==0:
                    del handlist[i]
            ans=True
        except KeyError:
            ans=False
    return ans


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




#def playHand(hand, wordList, n):
#    def displayHandret(hand):
#        ans =''
#        for letter in hand.keys():
#            for j in range(hand[letter]):
#                ans = ans+letter+" "      # print all on the same line
#        return ans                             # print an empty line    
#    
#    totalscore=0
#    i=1
#    while len(hand) >0:
#        print("Current Hand:",displayHandret(hand))
#        word=input('Enter word, or a "." to indicate that you are finished: ')
#        if word==".":
#            break
#        else:
#            if isValidWord(word, hand, wordList)==False:
#            # If the word is not valid:
#                print ("Invalid word, please try again.")
#                print()
#            else:
#                score=getWordScore(word, calculateHandlen(hand))
#                if (i>1 and len(word)==calculateHandlen(hand)):
#                    score-=50    
#                totalscore+=score
#                print ("\" "+word+" \""+" earned "+str(score)+"  points. Total:  "+str(totalscore)+"  points")
#                print()
#                hand=updateHand(hand, word)
#                i+=1
#    if word==".":
#        print("Goodbye! Total score:",totalscore,"points.")
#    else:
#        print("Run out of letters. Total score: ",totalscore," points.")


#def playHand(hand, wordList, n):
#    totalscore=0
#    handcopy=hand.copy()
#    while hand != {}:
#        ans=''
#        for letter in hand.keys():
#            for j in range(hand[letter]):
#                ans = ans+letter+" "
#        print("Current Hand:",ans)
#        word=input('Enter word, or a "." to indicate that you are finished: ')
#        if word==".":
#            break
#        else:
#            if isValidWord(word, hand, wordList)==False:
#                print ("Invalid word, please try again.")
#                print()
#            else:
#                score=getWordScore(word, calculateHandlen(handcopy))
#                totalscore+=score
#                print ('"',word,'"',"earned",score,' points. Total: ',totalscore,' points')
#                print()
#                hand=updateHand(hand, word)
#    if hand=={}:
#        print("Run out of letters. Total score: ",totalscore," points.")
#    elif word==".":
#        print("Goodbye! Total score:",totalscore,"points.")
    #add two more lines -line1
    #add two more lines -line2
    #add two more lines -line3

def playHand(hand, wordList, n): 
    def displayHandret(hand):
        ans =''
        for letter in hand.keys():
            for j in range(hand[letter]):
                ans = ans+letter+" "     
        return ans                            
    
    score=0# Keep track of the total score 
    while calculateHandlen(hand)!=0:# As long as there are still letters left in the hand: 
        print ("Current Hand:",displayHandret(hand))# Display the hand 
        word=input('Enter word, or a "." to indicate that you are finished: ')# Ask user for input 
        if word=='.':
            print("Goodbye! Total score:",score,"points.")
            return score
        else:# Otherwise (the input is not a single period): 
            if isValidWord(word, hand, wordList)==False:# If the word is not valid:             
                print ("Invalid word, please try again.")# Reject invalid word (print a message followed by a blank line) 
                print ()
            elif isValidWord(word, hand, wordList)==True:# Otherwise (the word is valid): 
                scorep=getWordScore(word,n) 
                score+=scorep
                print ('"',word,'"',"earned",scorep,' points. Total: ',score,' points') 
                print()
                hand=updateHand(hand,word)# Update the hand  
    print("Run out of letters. Total score: ",score," points.")
    return score 
    
n=7
wordList = loadWords()
hand = {'a': 2, 'e': 2, 'p': 1, 'r': 1, 't': 1}
playHand(hand, wordList, n)
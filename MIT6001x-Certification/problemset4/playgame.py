import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

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

def playHand(hand, wordList, n):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word or a single period (the string ".") 
      to indicate they're done playing
    * Invalid words are rejected, and a message is displayed asking
      the user to choose another word until they enter a valid word or "."
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters or the user
      inputs a "."

      hand: dictionary (string -> int)
      wordList: list of lowercase strings
      n: integer (HAND_SIZE; i.e., hand size required for additional points)
      
    """
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
    


HAND_SIZE=10
def playGame(wordList):
    """
    Allow the user to play an arbitrary number of hands.
 
    1) Asks the user to input 'n' or 'r' or 'e'.
      * If the user inputs 'n', let the user play a new (random) hand.
      * If the user inputs 'r', let the user play the last hand again.
      * If the user inputs 'e', exit the game.
      * If the user inputs anything else, tell them their input was invalid.
 
    2) When done playing the hand, repeat from step 1
    """
    hand={} 
    while True: 
        choice=input("Enter n to deal a new hand, r to replay the last hand, or e to end game: ") 
        if(choice=='n'): 
            hand=dealHand(HAND_SIZE) 
            playHand(hand,wordList,HAND_SIZE) 
        elif(choice=='r'): 
            if(hand=={}): 
                print("You have not played a hand yet. Please play a new hand first!") 
            else: 
                #hand=hand.copy() 
                playHand(hand,wordList,HAND_SIZE) 
        elif(choice=='e'): 
            break 
        else: 
            print("Invalid command.") 
            continue 

wordList = loadWords()
print (playGame(wordList))        
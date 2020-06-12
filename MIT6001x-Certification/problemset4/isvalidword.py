
#
# Problem #3: Test word validity
#

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
    
def test_isValidWord(wordList):
    """
    Unit test for isValidWord
    """
    failure=False
    # test 1
    word = "hello"
    handOrig = getFrequencyDict(word)
    handCopy = handOrig.copy()

    if not isValidWord(word, handCopy, wordList):
        print("FAILURE: test_isValidWord()")
        print("\tExpected True, but got False for word: '" + word + "' and hand:", handOrig)

        failure = True

    # Test a second time to see if wordList or hand has been modified
    if not isValidWord(word, handCopy, wordList):
        print("FAILURE: test_isValidWord()")

        if handCopy != handOrig:
            print("\tTesting word", word, "for a second time - be sure you're not modifying hand.")
            print("\tAt this point, hand ought to be", handOrig, "but it is", handCopy)

        else:
            print("\tTesting word", word, "for a second time - have you modified wordList?")
            wordInWL = word in wordList
            print("The word", word, "should be in wordList - is it?", wordInWL)

        print("\tExpected True, but got False for word: '" + word + "' and hand:", handCopy)

        failure = True
    
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

#test
def test_isValidWord(wordList):
    """
    Unit test for isValidWord
    """
    failure=False
    # test 1
    word = "hello"
    handOrig = getFrequencyDict(word)
    handCopy = handOrig.copy()

    if not isValidWord(word, handCopy, wordList):
        print("FAILURE: test_isValidWord()")
        print("\tExpected True, but got False for word: '" + word + "' and hand:", handOrig)

        failure = True

    # Test a second time to see if wordList or hand has been modified
    if not isValidWord(word, handCopy, wordList):
        print("FAILURE: test_isValidWord()")

        if handCopy != handOrig:
            print("\tTesting word", word, "for a second time - be sure you're not modifying hand.")
            print("\tAt this point, hand ought to be", handOrig, "but it is", handCopy)

        else:
            print("\tTesting word", word, "for a second time - have you modified wordList?")
            wordInWL = word in wordList
            print("The word", word, "should be in wordList - is it?", wordInWL)

        print("\tExpected True, but got False for word: '" + word + "' and hand:", handCopy)

        failure = True


    # test 2
    hand = {'r': 1, 'a': 3, 'p': 2, 'e': 1, 't': 1, 'u':1}
    word = "rapture"

    if  isValidWord(word, hand, wordList):
        print("FAILURE: test_isValidWord()")
        print("\tExpected False, but got True for word: '" + word + "' and hand:", hand)

        failure = True        

    # test 3
    hand = {'n': 1, 'h': 1, 'o': 1, 'y': 1, 'd':1, 'w':1, 'e': 2}
    word = "honey"

    if  not isValidWord(word, hand, wordList):
        print("FAILURE: test_isValidWord()")
        print("\tExpected True, but got False for word: '"+ word +"' and hand:", hand)

        failure = True                        

    # test 4
    hand = {'r': 1, 'a': 3, 'p': 2, 't': 1, 'u':2}
    word = "honey"

    if  isValidWord(word, hand, wordList):
        print("FAILURE: test_isValidWord()")
        print("\tExpected False, but got True for word: '" + word + "' and hand:", hand)
        
        failure = True

    # test 5
    hand = {'e':1, 'v':2, 'n':1, 'i':1, 'l':2}
    word = "evil"
    
    if  not isValidWord(word, hand, wordList):
        print("FAILURE: test_isValidWord()")
        print("\tExpected True, but got False for word: '" + word + "' and hand:", hand)
        
        failure = True
        
    # test 6
    word = "even"

    if  isValidWord(word, hand, wordList):
        print("FAILURE: test_isValidWord()")
        print("\tExpected False, but got True for word: '" + word + "' and hand:", hand)
        print("\t(If this is the only failure, make sure isValidWord() isn't mutating its inputs)")
        
        failure = True        

    if not failure:
        print("SUCCESS: test_isValidWord()")
        #end of test
    
        
hand= {'n':1, 'o':2, 'e':1, 'd':1, 'r':1, 'z':1}
word='zooned'
wordList=loadWords()
print (wordList)
print (isValidWord(word, hand, wordList))
print (test_isValidWord(wordList))
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 21:36:45 2019

@author: H7853
"""

# Hangman game
#

# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)

import random

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
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def chooseWord(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = loadWords()


def hangman(secretWord):
    '''
    secretWord: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many 
      letters the secretWord contains.

    * Ask the user to supply one guess (i.e. letter) per round.

    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computers word.

    * After each round, you should also display to the user the 
      partially guessed word so far, as well as letters that the 
      user has not yet guessed.

    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE...


# When you've completed your hangman function, uncomment these two lines
# and run this file to test! (hint: you might want to pick your own
# secretWord while you're testing)


def isWordGuessed(secretWord, lettersGuessed):
    '''
    secretWord: string, the word the user is guessing
    lettersGuessed: list, what letters have been guessed so far
    returns: boolean, True if all the letters of secretWord are in lettersGuessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE...
#    RESULT :secretWord = 'apple' 
#    lettersGuessed = ['e', 'i', 'k', 'p', 'r', 's']
#    print(isWordGuessed(secretWord, lettersGuessed))
#    False
    ans=True
    for  i in secretWord:
        if i in lettersGuessed:
            ans=ans and True
            #print('guess',lettersGuessed)
            #print('secretword',i)
            #print (ans)
        else:
            return False
    return ans
        
#print(isWordGuessed('apple' ,  ['l','a','p']))        

def getGuessedWord(secretWord, lettersGuessed):
    i=0
    display=''
    for a in secretWord:
        if a in lettersGuessed:
            display=display+a+" "
        else:
            display+='_ '
        i+=1
    return display
        
#secretWord = 'apple' 
#lettersGuessed = ['e', 'i', 'k', 'p', 'r', 's','o']
#print(getGuessedWord(secretWord, lettersGuessed))
#output _ p p _ e 

def getAvailableLetters(lettersGuessed):
    '''
    lettersGuessed: list, what letters have been guessed so far
    returns: string, comprised of letters that represents what letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE...
    import string
    notguess=''
    for j in string.ascii_lowercase:
        if j not in lettersGuessed:
            notguess=notguess+j
    #print ('notguee',notguess)
    return notguess
    
#lettersGuessed = ['e', 'i', 'k', 'p', 'r', 's']
#print(getAvailableLetters(lettersGuessed))
#abcdfghjlmnoqtuvwxyz

def hangman(secretWord):
    print("Welcome to the game, Hangman!")
    l=len(secretWord)
    print("I am thinking of a word that is",str(l),"letters long.")
    print("-------------")
    mistakesMade=8
    lettersGuessed=[]
    templettersGuessed=[]
    guesslower=''
    guess=''
    c=0
    while mistakesMade>0:
        print("You have",mistakesMade,"guesses left.")
        print("Available letters: ",getAvailableLetters(lettersGuessed))
        guess= input ("Please guess a letter:")
        guesslower=guess.lower()
        lettersGuessed.extend(guesslower)
        #print(lettersGuessed)
        if guesslower in templettersGuessed:
            ee=getGuessedWord(secretWord, lettersGuessed)
            print("Oops! You've already guessed that letter:",ee)
            print("-------------")
        else:
            if guesslower in secretWord:
                gg=getGuessedWord(secretWord, lettersGuessed)
                print ("Good guess:",gg)
                print("-------------")
                if isWordGuessed(secretWord, lettersGuessed):
                    print("Congratulations, you won!")
                    break           
            else:
                ff=getGuessedWord(secretWord, lettersGuessed)
                print ("Oops! That letter is not in my word: ",ff)            
                print("-------------")
                mistakesMade-=1
        templettersGuessed.extend(guesslower)
    check=isWordGuessed(secretWord, lettersGuessed)    
    if  check==False and mistakesMade<1:
        print ('Sorry, you ran out of guesses. The word was '+str(secretWord)+'.')
     
import string

### DO NOT MODIFY THIS FUNCTION ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print('Loading word list from file...')
    # inFile: file
    in_file = open(file_name, 'r')
    # line: string
    line = in_file.readline()
    # word_list: list of strings
    word_list = line.split()
    print('  ', len(word_list), 'words loaded.')
    in_file.close()
    return word_list

### DO NOT MODIFY THIS FUNCTION ###
def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

### DO NOT MODIFY THIS FUNCTION ###
def get_story_string():
    """
    Returns: a joke in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    ### DO NOT MODIFY THIS METHOD ###
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    ### DO NOT MODIFY THIS METHOD ###
    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    ### DO NOT MODIFY THIS METHOD ###
    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]
    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''

        lower=(string.ascii_lowercase) #starts 97-122
        upper=(string.ascii_uppercase) #starts 65-90
        assert 0<=shift<26
        ordfirstlower=ord('a')
        ordlastlower=ord('z')
        ordfirstupper=ord('A')
        ordlastupper=ord('Z')
        masterdict={}
        for letter in (lower+upper):
            origord=ord(letter)
            neword=ord(letter)+shift
            if 97<=origord <=122: # check lower case letter
                if  neword >122:
                    newchar=chr((ordfirstlower+((neword-ordlastlower)-1)))
                else:
                    newchar=chr(neword)
            elif 65<=origord <=90:  # check upper case letter
                if  neword >90:
                    newchar=chr((ordfirstupper+((neword-ordlastupper)-1)))
                else:
                    newchar=chr(neword)
            masterdict[letter]=newchar
        return masterdict
    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        assert 0<=shift<26
        #text=self.message_text
        ans=''
        dicta=self.build_shift_dict(shift)
        for i in self.message_text:
            if ord('a')<=ord(i)<=ord('z') or ord('A')<=ord(i) <=ord('Z'):
                ans=ans+dicta[i]
            else:
                ans=ans+i
        self.message_text=ans
        return self.message_text

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encrypting_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        Hint: consider using the parent class constructor so less 
        code is repeated
        '''
        Message.__init__(self, text)
        self.message_text=text
        #self.valid_words=Message.get_valid_words(self)
        self.shift=shift
        self.encrypting_dict=Message.build_shift_dict(self,shift)
        self.message_text_encrypted=Message.apply_shift(self,shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encrypting_dict(self):
        '''
        Used to safely access a copy self.encrypting_dict outside of the class
        
        Returns: a COPY of self.encrypting_dict
        '''
        return   self.encrypting_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return  self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift (ie. self.encrypting_dict and 
        message_text_encrypted).
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        #self.shift
        self.__init__(self.message_text, shift)


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)
        self.message_text=text
        #self.valid_words=Message.get_valid_words(self)
        #self.valid_words = load_words(WORDLIST_FILENAME)
        
    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are  equally good such that they all create 
        the maximum number of you may choose any of those shifts (and their
        corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        dictshiftwords={}
        messagetextcopy=self.message_text[:]
        for shift in range(26):
            word=''
            totalrealwords=0            
            self.message_text=messagetextcopy
            word=self.apply_shift(shift)
            textlist=word.split(" ") #get each word within the text
            for word in textlist:
                if is_word( self.valid_words, word):
                    totalrealwords+=1
            dictshiftwords[shift]=totalrealwords
        (shift,noofwords)=(max(dictshiftwords.items(), key=lambda k: k[1])) # return shift for the max value (max real words)
        self.message_text=messagetextcopy
        (shift,noofwords)=(shift,self.apply_shift(shift))
        return ((shift,noofwords))
        
            
        

#Example test case (PlaintextMessage)
plaintext = PlaintextMessage('hello', 2)
print('Expected Output: jgnnq')
print('Actual Output:', plaintext.get_message_text_encrypted())
    
#Example test case (CiphertextMessage)
ciphertext = CiphertextMessage('jgnnq yqtnf')
#print('Expected Output:', (24, 'hello'))
print('Actual Output:', ciphertext.decrypt_message())


def decrypt_story():
        '''
         return the appropriate shiftvalue and unencrypted story string for story
        '''
        return (CiphertextMessage(get_story_string() ).decrypt_message())
            
print (decrypt_story())

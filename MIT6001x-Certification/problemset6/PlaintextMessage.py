#Problem 2 - PlaintextMessage 
#
#0.0/15.0 points (graded)
# 
#
#
#For this problem, the graders will use our implementation of the Message class, so don't worry if you did not get the previous parts correct.
#
#PlaintextMessage is a subclass of Message and has methods to encode a string using a specified shift value. Our class will always create an encoded version of the message, and will have methods for changing the encoding.
#
#Implement the methods in the class PlaintextMessage according to the specifications in ps6.py. The methods you should fill in are:
#•__init__(self, text, shift): Use the parent class constructor to make your code more concise. 
#•The getter method get_shift(self)
#•The getter method get_encrypting_dict(self): This should return a COPY of self.encrypting_dict to prevent someone from mutating the original dictionary.
#•The getter method get_message_text_encrypted(self)
#•change_shift(self, shift): Think about what other methods you can use to make this easier. It shouldn’t take more than a couple lines of code.
#
#Paste your implementation of the entire PlaintextMessage class in the box below.
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
        text=self.message_text
        ans=''
        dicta=self.build_shift_dict(shift)
        for i in text:
            if ord('a')<=ord(i)<=ord('z') or ord('A')<=ord(i) <=ord('Z'):
                ans=ans+dicta[i]
            else:
                ans=ans+i
        self.message_text=ans
        return self.message_text
        
#b= Message("#@Hello^!112 45H")
##*TEST  BUILD SHIFT
#print (b.build_shift_dict(3))
##dicttest=b.build_shift_dict(2)
##a=string.ascii_uppercase
##for i in a:
##    print (i,"=",dicttest[i])
### test length of dict
##print("len:",len(dicttest))
##***************
##*APPLY  BUILD SHIFT
##print (b.get_message_text())
#print (b.apply_shift(3))


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

        
p=PlaintextMessage('1.Hello!',21)
print (p.get_shift())
d=p.get_encrypting_dict()
e=p.get_message_text_encrypted()
#f=p.change_shift(2)
#e=p.get_message_text_encrypted()
print ( e)
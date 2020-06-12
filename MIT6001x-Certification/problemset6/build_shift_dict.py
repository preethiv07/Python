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
        
b= Message("hello")
#print (b.build_shift_dict(5))
dicttest=b.build_shift_dict(2)
a=string.ascii_uppercase
for i in a:
    print (i,"=",dicttest[i])
# test length of dict
print("len:",len(dicttest))

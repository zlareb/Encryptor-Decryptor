import string

def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    return wordlist

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

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story


WORDLIST_FILENAME = 'words.txt'

# The code above this line had been provided by MIT

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        Returns: self.message_text
        '''
        return self.message_text
    
    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        Returns: a COPY of self.valid_words
        '''
        words = self.valid_words.copy()
        return words

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        has 52 keys of all the uppercase letters and all the lowercase
        letters.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        alphalower = string.ascii_lowercase
        alphaupper = string.ascii_uppercase
        alphadict = {}
        for alphabet in alphalower:
            newindex = alphalower.find(alphabet) + shift
            correspondingletter = alphalower[newindex % len(alphalower)]
            alphadict[alphabet] = correspondingletter

        for alphabet in alphaupper:
            newindex = alphaupper.find(alphabet) + shift
            correspondingletter = alphaupper[newindex % len(alphaupper)]
            alphadict[alphabet] = correspondingletter
        
        return alphadict

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
        mappingdict = self.build_shift_dict(shift)
        newstring = ''

        # goes through the message_text's indexes in ascending order
        # if that position of the string is a letter, add the corresponding value associated with that letter in the mappingdict 
        for letter in self.message_text:
            if letter in string.ascii_letters:
                newstring += mappingdict[letter]
            else:
                newstring += letter
        
        return newstring


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
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)
        self.shift = shift
        self.encryption_dict = super().build_shift_dict(shift)
        self.message_text_encrypted = super().apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift
    
    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        dict = self.encryption_dict.copy
        return dict

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''        
        self.shift = shift
        self.encryption_dict = super().build_shift_dict(shift)
        self.message_text_encrypted = super().apply_shift(shift)

        


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words("words.txt")

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, we add them to a list and choose the 
        shift at position 0

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        wordcount_dict = {}     # stores shift values as keys and the number of valid words generated by applying that shift value to the text as values

        # applies all possible shift values to the message text
        # checks how many valid words are generated by applying those shift values and stores that in wordcount_dict as wordcount_dict[shift value] = words generated
        for i in range(1,26):
            decryptedstring = super().apply_shift(26-i)
            listofwords = decryptedstring.split(' ')
            for word in listofwords:
                if is_word(self.valid_words, word): 
                    wordcount_dict[26-i] = wordcount_dict.get(26-i,0) + 1

        # finds the shift value that generates the highest number of words
        highestvalue = 0 
        for value in wordcount_dict.values():
            if value > highestvalue:
                highestvalue = value
        bestshiftvalue = [shiftval for shiftval,numofwords in wordcount_dict.items() if numofwords == highestvalue][0]
        
        decryptedtext = super().apply_shift(bestshiftvalue)

        return (bestshiftvalue, decryptedtext)
    

if __name__ == '__main__':

   print("Hello, I provide a 2-in-1 encryption and decryption service.")

   while True:
        enc_or_dec = input("Do you want to encrypt a message or decrypt it? Please enter 'e' for encryption and 'd' for decryption: ")
        textinput = input("Please enter your text: ")
        if (enc_or_dec == 'e' or enc_or_dec == 'd') and isinstance(textinput,str):
            break
        else:
            print("Invalid input! Please try again.")
            continue
                        
   if enc_or_dec == 'e':
        shiftvalue = input("How many letters down the alphabet do you want to shift each letter by? For example, enter 2 if you want 'a' to be changed to 'c': ")
        while True:
            try:
               shiftvalue = int(shiftvalue)
               break
            except:
               print("Invalid input! Please try again.")
               continue

        print("You have chosen to encrypt the text '" + textinput + "' with a shift value " + shiftvalue + ".")
        plaintext = PlaintextMessage(textinput,shiftvalue)
        print("Encrypted text:", plaintext.get_message_text_encrypted())
    
   else:
        print("You have chosen to decrypt the text '" + textinput + "'")
        ciphertext = CiphertextMessage(textinput)
        print("The shift value and the decrypted text is as follows:", ciphertext.decrypt_message())
       
    
       
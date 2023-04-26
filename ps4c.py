import string
from ps4a import get_permutations

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


WORDLIST_FILENAME = 'words.txt'

VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

# The code above this line had been provided by MIT

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
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
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        words = self.valid_words.copy()
        return words
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        vowel_dict = {}
        vowels_permutation_lower = vowels_permutation.lower()
        vowels_permutation_upper = vowels_permutation.upper()

        for i in range(5):
            vowel_dict[VOWELS_LOWER[i]] = vowels_permutation_lower[i]
            vowel_dict[VOWELS_UPPER[i]] = vowels_permutation_upper[i]

        return vowel_dict

    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        words = self.get_message_text()

        # if the letter is a vowel, replace it with the corresponding value associated with that vowel in the given dict    
        for index in range(len(words)):
            if words[index] in VOWELS_LOWER or words[index] in VOWELS_UPPER:
                words = words[:index] + transpose_dict[words[index]] + words[index+1:]
            else:
                continue
                    
        return words


        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self,text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''

        permsofvowels = get_permutations('aeiou')
        wordcount_dict = {}                        # stores permutations as keys and the number of valid words generated by applying that permutation to the text as values
        
        for i in permsofvowels:
            dict = super().build_transpose_dict(i)
            permappliedtext = super().apply_transpose(dict)
            words = permappliedtext.split()
            for word in words:
                if is_word(self.valid_words, word):
                    wordcount_dict[i] = wordcount_dict.get(i,0) + 1
            
        highestvalue = 0 
        for value in wordcount_dict.values():
            if value > highestvalue:
                highestvalue = value

        if highestvalue > 0:
            bestperm = [shiftval for shiftval,numofwords in wordcount_dict.items() if numofwords == highestvalue][0]
            
            finaldict = super().build_transpose_dict(bestperm)
            finaltext = super().apply_transpose(finaldict)
            return finaltext

        else:
            return self.message_text()

    

if __name__ == '__main__':

    welcome = """
    Hello. This is another version of the 2-in-1 encryption & decryption service provided by ps4b.
    In the case of encryption, when you give me a string with the 5 vowels in any order. I replace all the vowels in 
    your given text according to the order you specify.
    For instance if you give me 'ouiea', 'a' in your text will be changed to 'o', 'e' will be changed to 'u', and so on...
    In the case of encryption, if you give me a text with the vowels all mixed up according to a certain ordering of the vowels,
    I can give you back the decrypted text.
    For instance, if you give me 'Hallu Wurld', I will give you back 'Hello World'
    """
    print(welcome)

    while True:
        enc_or_dec = input("Do you want to encrypt a message or decrypt it? Please enter 'e' for encryption and 'd' for decryption: ")
        textinput = input("Please enter your text: ")
        if (enc_or_dec == 'e' or enc_or_dec == 'd') and isinstance(textinput,str):
            break
        else:
            print("Invalid input! Please try again.")
            continue
    
    if enc_or_dec == 'e':
        perm = input("Please enter your unique order of vowels to be applied to your text: ")
        while True:
            if isinstance(perm,str) and len(perm) == 5:
                break
            else:
                print("Invalid input! Please try again.")
                continue

        print("You have chosen to encrypt the text '" + textinput + "' with the following order of vowels: " + perm + ".")
        message = SubMessage(textinput)
        enc_dict = message.build_transpose_dict(perm)
        print("Encrypted text:", message.apply_transpose(enc_dict))

    else:
        print("You have chosen to decrypt the text '" + textinput + "'")
        message = EncryptedSubMessage(textinput)
        print("Decrypted text:", message.decrypt_message())
    
    



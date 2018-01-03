#!/usr/bin/env python3
# encoding: utf-8

'''
Copyright (c) 2018, Sophie Durrant
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL SOPHIE DURRANT BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
VERSION='XKCD Password Generator, v0.1'


from random import SystemRandom
import string
import argparse

#Initialise random numbers using underlying OS for cryptographic security
r = SystemRandom()
r.seed()

#Initialise wordlist. I have used the wordlist from
#https://github.com/first20hours/google-10000-english
#but any list of words will work
f = open("20k.txt")
words = f.readlines()
words = [word[:-1] for word in words] #strip newlines

#Make a word capitalised with a specific probability
def make_uppercase(word, uppercase_probability):
    if r.random() < uppercase_probability:
        return word[0].upper() + word[1:]
    else:
        return word

#Append password with number with specific probability
def add_number(password, maxchar, number_probability):
    if (maxchar is None or len(password) < maxchar) and r.random() < number_probability:
        return password + str(r.randrange(9))
    else:
        return password            

#Add a symbol to password with specific probability
def add_symbol(password, maxchar, symbol_probability):
    if (maxchar is None or len(password) < maxchar) and r.random() < symbol_probability:
        return password + r.choice(string.punctuation)
    else:
        return password
        
def __check_probability(val):
    if (0 <= val and val <= 1):
        return True
    else:
        parser.print_help()
        return False                                

def __check_args(   number_of_words,
                    minchar,
                    maxchar,
                    special_character_probability,
                    start_word_uppercase_probability,
                    number_probability,
                    maxchar_minchar_min_difference,
                    minchar_wordlen_difference_threshold,
                    probability_wordless_iter):
    '''Validates the arguments passed to generate_password()'''
    
    if  (__check_probability(special_character_probability) and
        __check_probability(start_word_uppercase_probability) and
        __check_probability(number_probability) and
        __check_probability(probability_wordless_iter)):
        pass
    else:
        raise ValueError('Probability arguments must be between 0 and 1')
        
    if (probability_wordless_iter == 1.0):
        raise ValueError('The probability that an iteration is wordless must be less than 1')
        
    if (minchar is not None and minchar < 1):
        raise ValueError('Minchar must be a positive integer or NoneType')
        
    if (maxchar is not None and maxchar < 1):
        raise ValueError('Maxchar must be a positive integer or NoneType')
        
    if (number_of_words < 1):
        raise ValueError('number_of_words must be a positive integer')
        
    if (maxchar is not None and minchar is not None and maxchar < minchar):
        raise ValueError('Maxchar cannot be less than minchar')
        
    if (maxchar_minchar_min_difference < 0):
        raise ValueError
        
    if (minchar_wordlen_difference_threshold < 1):
        raise ValueError

#Generates a password with random words, with absolute limits between minchar and maxchar.
#If minchar is a nonzero number, then the generator will keep on generating words until minchar
#is reached. If maxchar is a nonzero number, then if adding a word exceeds maxchar, then that word
#will not be added. If minchar-maxchar is less than 4, then when minchar-length of word < 6, then
#the generator will pre-select words with a length that will fit into maxchar.

#If the generator has generated number_of_words, and has not yet exceeded minchar, it will continue
#to add more words to the password until minchar is reached
def generate_password(number_of_words=4,
                        minchar=None,
                        maxchar=None,
                        special_character_probability=0,
                        start_word_uppercase_probability=0,
                        number_probability=0,
                        maxchar_minchar_min_difference=4,
                        minchar_wordlen_difference_threshold=6,
                        probability_wordless_iter = 0):
    '''Generate password with random words of length between minchar and maxchar inclusive'''
    
    __check_args(   number_of_words,
                    minchar,
                    maxchar,
                    special_character_probability,
                    start_word_uppercase_probability,
                    number_probability,
                    maxchar_minchar_min_difference,
                    minchar_wordlen_difference_threshold,
                    probability_wordless_iter
                )
                        
    password = ""
    
    #Detects if there is a small difference between minchar and maxchar - this will make it
    #inefficient to generate random words of suitable size
    if (minchar is not None and maxchar is not None):
        maxchar_minchar_small_difference = (maxchar - minchar < maxchar_minchar_min_difference)
    else:
        maxchar_minchar_small_difference = False
        
    words_used = 0
          
    while True:    
        #If we have reached minchar and the wordcount then the password is finished
        if (minchar is None or len(password) >= minchar) and words_used == number_of_words:
            return password
        
        #If it is difficult to randomly generate a word of suitable length then filter all words
        #to ones of the desired length. Then randomly choose from these words.        
        #We only want to do this if there are relatively few words that can be randomly generated
        #from a full set of words, as this method reduces entropy.
        if (maxchar_minchar_small_difference):
            letters_to_minchar = minchar - len(password)
            letters_to_maxchar = maxchar - len(password)
            if (letters_to_minchar < minchar_wordlen_difference_threshold):
                word = r.choice([word for word in words if len(word) > letters_to_minchar and len(word) < letters_to_maxchar])
                return password + make_uppercase(word, start_word_uppercase_probability)
        
        #Choose a random word and evaluate if it is of a suitable length to add to password.
        word = r.choice(words)
        if (maxchar is None or len(password) + len(word) <= maxchar) and r.random() < 1 - probability_wordless_iter:
            password = password + make_uppercase(word, start_word_uppercase_probability)
            words_used = words_used + 1
        elif (maxchar is not None and maxchar - len(password) < maxchar_minchar_min_difference):
            return password
        
        #This means that there is no bias towards whether a number is found before a symbol or not
        number_first = (r.random() < 0.5)
        
        #Add numbers and special characters to password between individual words
        if (number_first):
            password = add_number(password, maxchar, number_probability)
            password = add_symbol(password, maxchar, special_character_probability)            
        else:
            password = add_symbol(password, maxchar, special_character_probability)   
            password = add_number(password, maxchar, number_probability)
            
#Create argument parser
parser = argparse.ArgumentParser(description= 'Create a password with the technique depicted in the XKCD comic https://www.xkcd.com/936/')
parser.add_argument('-n', '--number-of-words', '--numwords', type=int, help='Suggests the number of words to be used in the password. If minchar or maxchar is specified, then this may be ignored to ensure the password has a suitable length. Default value is 4.', dest='number_of_words')
parser.add_argument('--minchar', type=int, help='Minimum number of characters in password')
parser.add_argument('--maxchar', type=int, help='Maximum number of characters in password')
parser.add_argument('--special-character', type=float, help='Probability that a special character will occur between words. Must be between 0 and 1 inclusive. Default value is 0', dest='special_character_probability')
parser.add_argument('--capitalize', type=float, help='Probability that a word will be capitalised. Must be between 0 and 1 inclusive. Default value is 0', dest='start_word_uppercase_probability')
parser.add_argument('--special-number', type=float, help='Probability that a number will occur between words. Must be between 0 and 1 inclusive. Default value is 0.', dest='number_probability')
parser.add_argument('--wordless-iteration', type=float, help='Probability that an iteration will not produce a word. This means that longer sequences of special characters can be generated, and can appear at the start of words. Must be greater than or equal to 0, and less than 1. Default value is 0.', dest='probability_wordless_iter')
parser.add_argument('-v', '--version', action='version', version=VERSION)


if (__name__ == '__main__'):
    args = vars(parser.parse_args())
    
    #delete empty arguments
    new_args = {}
    for key in args.keys():
        if args[key] is not None:
            new_args[key] = args[key]
    try:
        print(generate_password(**new_args))
    except ValueError as e:
        parser.print_help()
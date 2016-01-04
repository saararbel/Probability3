from WordSet import WordSet
from collections import Counter

import time

class BigramWordSet(WordSet):
    def __init__(self, words, vocabularySize, unigramWordSet):
        # super(BigramWordSet, self).__init__(zip([dummyWord] + words[:-1], words), vocabularySize)
        super(BigramWordSet, self).__init__(zip(words[:-1], words[1:]), vocabularySize)
        self.unigramWordSet = unigramWordSet
        self.wordToAdjacentWords = self.mapWordToAdjacentWords()

    def mapWordToAdjacentWords(self):
        '''
        Create a dictionary whose keys are the words in the set, and it's value is a list of all the adjacent words
        (words following the given word).
        :param unigramWordSet:
        :return:
        '''
        dict = {}
        for first, second in self.keys():
            if(first not in dict or dict[first] is None):
                dict[first] = []
            dict[first].append(second)

        return dict

    def countAppearances(self, first, second):
        '''
        :param first:
        :param second:
        :return: The number of times the tuple (:first, :second) appeared in the set.
        '''
        return self.wordAppearanceCounter[(first, second)]

    def pLidstone(self, word, lamda):
        '''
        Calculate the Lidstone's Discount probability to :word with :lamda.
        The probability given to the tuple :word to appear. It is calculated using some lambda value - :lamda like so:
        the number of times the tuple appear in the set is added to the given lambda, then this is dicided by the number
        of times the first word in the tuple appeared in the set added to the lambda times the vocabulary's size. We
        divide by the number of times the first word of the tuple appeared in the set due to the fact that it is
        conditional probability, therefor we need to use this in our divider for that the total propability will add up
        to 1.
        :param word:
        :param lamda:
        :return:
        '''
        return (self.wordAppearanceCounter[word] + lamda) / (self.unigramWordSet.countAppearances(word[0]) + self.vocabularySize * lamda)
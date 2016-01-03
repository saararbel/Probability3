from WordSet import WordSet
from collections import Counter

import time

class BigramWordSet(WordSet):
    def __init__(self, words, vocabularySize, unigramWordSet):
        # super(BigramWordSet, self).__init__(zip([dummyWord] + words[:-1], words), vocabularySize)
        super(BigramWordSet, self).__init__(zip(words[:-1], words[1:]), vocabularySize)
        # self.alphaDict = {}
        self.unigramWordSet = unigramWordSet
        self.firstWordDictToSecondCounter = self.generateDict(unigramWordSet)

    def generateDict(self, unigramWordSet):
        dict = {}
        for first, second in self.keys():
            if(first not in dict or dict[first] is None):
                dict[first] = []
            dict[first].append(second)

        return dict

    def countAppearances(self, first, second):
        return self.wordAppearanceCounter[(first, second)]

    def pLidstone(self, word, lamda):
        '''
        The propability of {word} to appear after applying it a lidstone discount with the given {lamda}.
        :param word:
        :param lamda:
        :return:
        '''
        return (self.wordAppearanceCounter[word] + lamda) / (self.unigramWordSet.countAppearances(word[0]) + self.vocabularySize * lamda)
from WordSet import WordSet


class BigramWordSet(WordSet):
    def __init__(self, words, vocabularySize, dummyWord):
        # super(BigramWordSet, self).__init__(zip([dummyWord] + words[:-1], words), vocabularySize)
        super(BigramWordSet, self).__init__(zip(words[:-1], words[1:]), vocabularySize)
        self.alphaDict = {}

    def countAppearances(self, first, second):
        return self.wordAppearanceCounter[(first, second)]

    def pLidstone(self, word, lamda):
        '''
        The propability of {word} to appear after applying it a lidstone discount with the given {lamda}.
        :param word:
        :param lamda:
        :return:
        '''
        first, second = word
        key = (first, lamda)
        if(key not in self.alphaDict or self.alphaDict[key] is None):
            self.alphaDict[key] = sum([self.countAppearances(firstWord, secondWord) for firstWord, secondWord in self.keys() if firstWord == first])
        return (self.wordAppearanceCounter[word] + lamda) / (self.alphaDict[key] + self.vocabularySize * lamda)
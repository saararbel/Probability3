from WordSet import WordSet


class BigramWordSet(WordSet):
    def __init__(self, words, vocabularySize, dummyWord):
        super(BigramWordSet, self).__init__(zip([dummyWord] + words[:-1], words), vocabularySize)

    def countAppearances(self, first, second):
        return self.wordAppearanceCounter[(first, second)]

class BackOffModel:

    def __init__(self, bigramWordSet, unigramWordSet, unigramLamda = 0.1):
        self.bigramWordSet = bigramWordSet
        self.unigramWordSet = unigramWordSet
        self.alphaDict = {}
        self.unigramLidsone = {}
        self.unigramLamda = unigramLamda
        # self.beta = 1 - sum([self.unigramWordSet.pLidstone(tempWord, 0.1) for tempWord in self.unigramWordSet.keys()])
        # self.betaDict = {}

    # order : ... firstWord secondWord ....
    def pBackOff(self, firstWord, secondWord = None, bigramLamda = None):
        if(isinstance(firstWord, tuple)):
            bigramLamda = secondWord
            firstWord, secondWord = firstWord
        if(self.bigramWordSet.countAppearances(firstWord, secondWord) > 0):
            return self.bigramWordSet.pLidstone((firstWord, secondWord), bigramLamda)
        # if(secondWord not in self.unigramLidsone or self.unigramLidsone[secondWord] is None):
        #     self.unigramLidsone[secondWord] = self.unigramWordSet.pLidstone(secondWord, self.unigramLamda)
        return self.getUnigramLidstone(secondWord) * self.calcAlpha(firstWord, bigramLamda)

    def calcAlpha(self, word, bigramLamda):
        key = (word, bigramLamda)
        if(key not in self.alphaDict or self.alphaDict[key] is None):
            mechana , mona = 1.0 , 1.0
            # mona = 1.0
            for tempWord in self.unigramWordSet.keys():
                if(self.bigramWordSet.countAppearances(word, tempWord) > 0):
                    mona -= self.bigramWordSet.pLidstone((word, tempWord), bigramLamda)
                    # mechana -= self.unigramWordSet.pLidstone(tempWord, self.unigramLamda)
                    mechana -= self.getUnigramLidstone(tempWord)
            self.alphaDict[key] = mona / mechana
        return self.alphaDict[key]

    def debug(self):
        word = "the"
        lamda = 0.1
        res = (self.unigramWordSet.vocabularySize - self.unigramWordSet.distinctLength) * self.pBackOff(word,"unseen-word", lamda)
        prop = [self.pBackOff(word,tempWord,lamda) for tempWord, amount in self.unigramWordSet.distinctItems()]
        return res + sum(prop)

    def getUnigramLidstone(self, word):
        if(word not in self.unigramLidsone or self.unigramLidsone[word] is None):
            self.unigramLidsone[word] = self.unigramWordSet.pLidstone(word, self.unigramLamda)
        return self.unigramLidsone[word]
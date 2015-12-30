
class BackOffModel:

    def __init__(self, bigramWordSet, unigramWordSet, lamda):
        self.bigramWordSet = bigramWordSet
        self.unigramWordSet = unigramWordSet
        self.alphaDict = {}


    # order : ... firstWord secondWord ....
    def pBackOff(self, firstWord, secondWord, bigramLamda, alpha):
        word = (firstWord, secondWord)
        if(self.bigramWordSet.countAppearances(firstWord, secondWord) > 0):
            return self.bigramWordSet.pLidstone(word, bigramLamda)
        else :
            return self.unigramWordSet.pLidstone(secondWord, 0.1) * alpha

    def calcAlphaDict(self, lamda):
        for word in self.unigramWordSet.wordAppearanceCounter.keys():
            self.alphaDict[word] = self.calcAlpha(word,lamda)

    def calcAlpha(self, word, bigramLamda):
        mechana , mona = 1.0 , 1.0
        for tempWord,amount in self.unigramWordSet.distinctItems():
            if(self.bigramWordSet.countAppearances(word, tempWord) > 0) :
                mona -= self.bigramWordSet.pLidstone((word, tempWord), bigramLamda)
                mechana -= self.unigramWordSet.pLidstone((tempWord) , 0.1)
        return mona/mechana

    def debug(self):
        word = "the"
        lamda = 0.3
        alpha = self.calcAlpha(word,lamda)
        res = (self.unigramWordSet.vocabularySize - self.unigramWordSet.distinctLength) * self.pBackOff(word,"unseen-word", lamda, alpha)
        prop = [self.pBackOff(word,tempWord,lamda,alpha) for tempWord,am in self.unigramWordSet.distinctItems()]
        return res + sum(prop)
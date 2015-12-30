
class BackOffModel:

    def __init__(self, bigramWordSet, unigramWordSet):
        self.bigramWordSet = bigramWordSet
        self.unigramWordSet = unigramWordSet

    # order : ... firstWord secondWord ....
    def pBackOff(self, firstWord, secondWord, bigramLamda):
        word = (firstWord, secondWord)
        if(self.bigramWordSet.countAppearances(firstWord, secondWord) > 0):
            return self.bigramWordSet.pLidstone(word, bigramLamda)
        return self.unigramWordSet.pLidstone(firstWord, bigramLamda) * self.calcAlpha(secondWord, bigramLamda)

    def calcAlpha(self, word, bigramLamda):
        mechana , mona = 1.0 , 1.0
        for tempWord in self.unigramWordSet.distinctItems():
            if(self.bigramWordSet.countAppearances(tempWord, word) > 0):
                mona -= self.bigramWordSet.pLidstone((tempWord, word), bigramLamda)
                mechana -= self.unigramWordSet.pLidstone((tempWord) , 0.1)
        return mona/mechana





class BackOffModel:

    def __init__(self, bigramWordSet, unigramWordSet, unigramLamda = 0.1):
        self.bigramWordSet = bigramWordSet
        self.unigramWordSet = unigramWordSet
        self.alphaDict = {}
        self.unigramLidsone = {}
        self.unigramLamda = unigramLamda

    # order : ... firstWord secondWord ....
    def pBackOff(self, firstWord, secondWord = None, bigramLamda = None):
        '''
        Calculate the BackOff Discount probability of a tuple (:firstWord, :secondWord).
        If a tuple appeared in the set, then the returned value is the probability given from Lidstone discount of the
        tuple. Otherwise the returned value is the probability given from Lidstone discount (with lambda of 0.1) of
        :secondWord (We approach it as it if were a unigram model) multiplied by the alpha of :firstWord with a lambda
        of :bigramLamda.
        :param firstWord: The former word.
        :param secondWord: The latter word.
        :param bigramLamda:
        :return:
        '''
        # The next if allows calling this method in the following way: pBackOff((firstWord, secondWord), bigramLambda)
        if(isinstance(firstWord, tuple)):
            bigramLamda = secondWord
            firstWord, secondWord = firstWord
        if(self.bigramWordSet.countAppearances(firstWord, secondWord) > 0):
            return self.bigramWordSet.pLidstone((firstWord, secondWord), bigramLamda)
        return self.getUnigramLidstone(secondWord) * self.getAlpha(firstWord, bigramLamda)

    def calcAlpha(self, word, bigramLamda):
        '''
        Basically- The probability mass left for a tuple of (:word, some-word) divided by the probability mass
        left for words that were not following :word in the set.
        :param word:
        :param bigramLamda:
        :return:
        '''
        mechana , mona = 1.0 , 1.0
        if word in self.bigramWordSet.wordToAdjacentWords and self.bigramWordSet.wordToAdjacentWords[word] is not None:
            for tempWord in self.bigramWordSet.wordToAdjacentWords[word]:
                mona -= self.bigramWordSet.pLidstone((word, tempWord), bigramLamda)
                mechana -= self.getUnigramLidstone(tempWord)
        return mona / mechana

    def debug(self):
        word = "the"
        lamda = 0.1
        res = (self.unigramWordSet.vocabularySize - self.unigramWordSet.distinctLength) * self.pBackOff(word,"unseen-word", lamda)
        prop = [self.pBackOff(word,some_word,lamda) for some_word in self.unigramWordSet.keys()]
        return res + sum(prop)

    def getAlpha(self, first_word, bigram_lambda):
        '''
        Optimization used to calculate alpha only once for (:first_word, :bigram_lambda)
        :param first_word:
        :param bigram_lambda:
        :return: the value of :self.calcAlpha(:first_word, :bigram_lambda)
        '''
        key = (first_word, bigram_lambda)
        if(key not in self.alphaDict or self.alphaDict[key] is None):
            self.alphaDict[key] =  self.calcAlpha(first_word, bigram_lambda)
        return self.alphaDict[key]

    def getUnigramLidstone(self, word):
        '''
        This method is used for optimization of the code, in order to calculate Lidstone discount of a given :word only
        once.
        :param word:
        :return:
        '''
        if(word not in self.unigramLidsone or self.unigramLidsone[word] is None):
            self.unigramLidsone[word] = self.unigramWordSet.pLidstone(word, self.unigramLamda)
        return self.unigramLidsone[word]
from collections import Counter
class WordSet(object):
    '''
    Describes a stream of words (as our events), allowing needed methods on them.
    '''
    def __init__(self, words, vocabularySize, n = 1):
        '''
        :param words: A list of words .
        :param vocabularySize: a natural number setting the threshold of our vocabulary size.
        :return: a {WordSet} item
        '''
        # Save the words given to :WordSet as a dictionary with a word as a key, and the number of times it appeared
        # as the value.
        self.wordAppearanceCounter = Counter(words)
        self.length = len(words)
        self.start = words[:n]
        # The number of distinct words appeared.
        self.distinctLength = len(self.wordAppearanceCounter.keys())
        self.vocabularySize = vocabularySize

    def keys(self):
        '''
        :return: An iterable over all the distinct words from the words given to :WordSet
        '''
        return self.wordAppearanceCounter.iterkeys()

    def distinctItems(self):
        '''
        :return: An iterable over all the distinct words and the number of times they appeared, from the words given to the :WordSet
        '''
        return self.wordAppearanceCounter.iteritems()

    def countAppearances(self, word):
        '''
        :param word: The :word to check number of appearances of.
        :return: The number of times it appear in the word list.
        '''
        return self.wordAppearanceCounter[word]

    def pLidstone(self, word, lamda):
        '''
        The propability of :word to appear after applying it a Lidstone discount with the given :lamda. Which is the
        number of times a word appeared in the set added to a lambda divided by the size of the set plus the size of the
        vocabulary times the lambda. That lambda is actually the "reserved" probability we save to give to words that
        did not appear on the test set.
        :param word:
        :param lamda:
        :return:
        '''
        return (self.wordAppearanceCounter[word] + lamda) / (self.length + self.vocabularySize * lamda)

    def pMaximumLikelihoodEstimate(self, word):
        '''
        The propability of :word to appear as defined by the Maximum Likelihod Estimate method. Simply it is the number
        of times :word appeared in the set, divided by the size of the set.
        :param word:
        :return:
        '''
        return float(self.wordAppearanceCounter[word]) / self.length
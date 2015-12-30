
class BackOffModel:

    def __init__(self , trainingWordSet):
        self.trainingWordSet = trainingWordSet

    def pBackOff(self, leftWord, rightWord , lamda):
        # if count(right,left) > 0 then Plidstone
        # else:
        return self.trainingWordSet.pLidstone(leftWord,lamda) *  self.calcAlpha(rightWord)

    def calcAlpha(self, word):
        print 1

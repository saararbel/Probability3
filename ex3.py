import sys

import math
import time

from WordSet import WordSet
from BigramWordSet import BigramWordSet
from BackOffModel import BackOffModel


def generateOutputFile(developmentSetFilename, testSetFilename, firstInputWord, secondInputWord, outputFilename):
    print "Started with: "
    print "\tDevelopment set filename: %s" % developmentSetFilename
    print "\tTest set filename: %s" % testSetFilename
    print "\tInput word: %s" % firstInputWord
    print "\tInput word2: %s" % secondInputWord
    print "\tOutput filename: %s" % outputFilename
    vocabularySize = 300000

    file = open(outputFilename, "w+")
    file.write("#Students:\tSaar Arbel\tBoaz Berman\t315681775\t311504401\n")
    file.write("Output1: " + developmentSetFilename + "\n")
    file.write("Output2: " + testSetFilename + "\n")
    file.write("Output3: " + firstInputWord + " " + secondInputWord + "\n")
    file.write("Output4: " + outputFilename + "\n")
    file.write("Output5: " + str(vocabularySize) + "\n")

    with open(developmentSetFilename, 'rb') as input_file:
        input_file_data = input_file.read()
    words = parse_file_data(input_file_data)

    cuttingIndex = int(round(len(words) * 0.9))
    trainingSet, validationSet = words[:cuttingIndex], words[cuttingIndex:]
    trainingWordSet, validationWordSet = WordSet(trainingSet, vocabularySize), WordSet(validationSet, vocabularySize)
    file.write("Output6: " + str(len(words)) + "\n")
    file.write("Output7: " + str(validationWordSet.length) + "\n")
    file.write("Output8: " + str(trainingWordSet.length) + "\n")
    file.write("Output9: " + str(trainingWordSet.distinctLength) + "\n")
    file.write("Output10: " + str(trainingWordSet.countAppearances(firstInputWord)) + "\n")

    trainingBigramWordSet = BigramWordSet(trainingSet, vocabularySize, trainingWordSet)
    file.write("Output11: " + str(trainingBigramWordSet.countAppearances(firstInputWord, secondInputWord)) + "\n")

    validationBigramWordSet = BigramWordSet(validationSet, vocabularySize, validationWordSet)
    backOffTrainingModel = BackOffModel(trainingBigramWordSet,trainingWordSet)
    backOffValidationModel = BackOffModel(validationBigramWordSet, validationWordSet)

    print str(backOffTrainingModel.bigramWordSet.pLidstone(("bank", "economist"), 0.001)) + " boaz"
    print backOffTrainingModel.pBackOff("bank", "economist",0.1)
    print "Debug %f" % backOffTrainingModel.debug()

    file.write('Output12: ' + str(backOffPerplexity(backOffTrainingModel, backOffValidationModel, 0.0001)) + "\n")
    print "finished 12"
    file.write('Output13: ' + str(backOffPerplexity(backOffTrainingModel, backOffValidationModel, 0.001)) + "\n")
    print "finished 13"
    file.write('Output14: ' + str(backOffPerplexity(backOffTrainingModel, backOffValidationModel, 0.1)) + "\n")
    print "finished 14"
    minperplexity, minlamda = minimumPerplexity(backOffTrainingModel, backOffValidationModel)
    file.write('Output15: ' + str(minlamda) + "\n")
    print "finished 15"
    file.write('Output16: ' + str(minperplexity) + "\n")
    print "finished 16"

    with open(testSetFilename, 'rb') as input_file2:
        input_file_data2 = input_file2.read()
    words2 = parse_file_data(input_file_data2)
    trainingWordSet2 = WordSet(words2,vocabularySize)
    trainingBigramWordSet2 = BigramWordSet(words2, vocabularySize, trainingWordSet2)
    backOffTrainingModel2 = BackOffModel(trainingBigramWordSet2,trainingWordSet2)

    file.write('Output17: ' + str(backOffPerplexity(backOffTrainingModel, backOffTrainingModel2, 0.0003)) + "\n")
    print "finished 17"

    file.write('Output18: ' + str(printTable(backOffTrainingModel,0.001,firstInputWord)))


def printTable(trainingBackOffModel, lamda, firstWord):
    '''
    Create a table filled with your model results.
    :param trainingBackOffModel: BackOffModel. The Back Off Discount Model of the training set.
    :param lamda: float. Rational number.
    :param firstWord: an event. The event that we wish to bind before each of the events seen in the training set for the calculation.
    :return: A String representation of the table.
    '''
    outputLine = '\n'
    combinations = []
    unseen = "UNSEEN_EVENT"
    # Add a computation line for each of the shown events in the training model.
    for word in trainingBackOffModel.unigramWordSet.keys():
        combinations.append((word, trainingBackOffModel.bigramWordSet.countAppearances(firstWord, word), trainingBackOffModel.pBackOff(firstWord, word, lamda)))
    # Add the event of unseen word.
    combinations.append((unseen, trainingBackOffModel.bigramWordSet.countAppearances(firstWord, unseen), trainingBackOffModel.pBackOff(firstWord, unseen, lamda)))
    for index, (word, appearences, propability) in enumerate(sorted(combinations, key = lambda x: x[2], reverse = True)):
        outputLine += str(index) + "\t" + str(word) + "\t" + str(appearences) + "\t" + str(propability) + "\n"

    return outputLine


def frange(x, y, jump):
    '''
    Simple range method needed to work with float.
    :param x: float. Starting value.
    :param y: float. Starting value.
    :param jump: float. Starting value.
    :return:
    '''
    while x < y:
        yield x
        x += jump


def minimumPerplexity(trainingBackOffModel, validationBackOffModel):
    '''
    Calculating the perplexity of each of the lambdas in (0, 0.02] with jumps of 0.0001. Then return the minimum perplexity
     from between the perplexity calculated and its matching lambda.
    :param trainingWordSet: Instance of {BackOffModel}.
    :param validationWordSet: Instance of {BackOffModel}.
    :return: min-perplexity, min-lambda
    '''
    # Start from 0.0001 since the range is (0, 0.02] which means without 0.
    lamdagen = frange(0.0001, 0.02, 0.0001)
    # Calculate the first value for us to have in the equation.
    minlamda = lamdagen.next()
    minperplexity = backOffPerplexity(trainingBackOffModel, validationBackOffModel, minlamda)
    # The calculation of each lambda.
    for lamda in lamdagen:
        currperplexity = backOffPerplexity(trainingBackOffModel, validationBackOffModel, lamda)
        if currperplexity < minperplexity:
            minperplexity = currperplexity
            minlamda = lamda

    return minperplexity, minlamda


def backOffPerplexity(trainingBackOffModel, validationBackOffModel, lamda):
    '''
    Iterate each distinct word in {trainingBackOffWordSet} and sum the ln of his BackOff discount's probability with
    the given {lamda lambda} multiplied by the times it appeared (code optimization), then return the exponentiation
    of base e (due to the fact that we use ln) with the exponent of the previous calculation times -1 divided by the size of the set.
    :param trainingBackOffModel: Instance of {BackOffModel}.
    :param validationBackOffModel: Instance of {BackOffModel}.
    :param lamda: A rational positive number. A lambda for the calculation.
    :return: the perplexity.
    '''
    sum = 0.0
    # Sum all lns (in python, the default base for log used here is e) of BackOff discount of each tuple of words in validation.
    for (firstWord, secondWord), appearances in validationBackOffModel.bigramWordSet.distinctItems():
        sum += math.log(trainingBackOffModel.pBackOff(firstWord, secondWord, lamda)) * appearances
    # The first word has no tuple of (something, first word) so a different calculation is needed.
    sum += math.log(trainingBackOffModel.pBackOff("begin-article", validationBackOffModel.unigramWordSet.start[0], lamda))

    # Then we calculate the e^(-1 * total-ln-of-backoff / N)
    return math.pow(math.e, -1 * sum / validationBackOffModel.unigramWordSet.length)


def parse_file_data(file_data):
    '''
    parses the input file to a sequence (list) of words
    @param file_data: the input file text
    @return: a list of the files words
    '''
    # starting from the 3rd line, every 4th line is an article
    file_lines = file_data.splitlines()[2::4]
    # every article ends with a trailing space,
    # so we get a string with all the words separated by one space
    words = ''.join(file_lines)
    # remove the last trailing space
    words = words[:-1]
    # create a list of all the words
    return words.split(' ')


def main():
    # if len(sys.argv) != 4:
    #   print "How to use: " + sys.argv[
    #     0] + " < development_set_filename > < test_set_filename > < INPUT WORD > < output_filename >"
    #  sys.exit(1)

    development_file_path = sys.argv[1]
    test_file_path = sys.argv[2]
    first_input_word = sys.argv[3]
    second_input_word = sys.argv[4]
    output_file_path = sys.argv[5]

    generateOutputFile(development_file_path, test_file_path, first_input_word, second_input_word, output_file_path)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print "--- %s seconds ---" % (time.time() - start_time)
import sys
from WordSet import WordSet
from collections import Counter

def generateOutputFile(developmentSetFilename, testSetFilename, firstInputWord, secondInputWord, outputFilename):
    print "Program Started"
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
    # output11


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
    #if len(sys.argv) != 4:
     #   print "How to use: " + sys.argv[
       #     0] + " < development_set_filename > < test_set_filename > < INPUT WORD > < output_filename >"
      #  sys.exit(1)

    development_file_path = sys.argv[1]
    test_file_path = sys.argv[2]
    first_input_word = sys.argv[3]
    second_input_word = sys.argv[4]
    output_file_path = sys.argv[5]

    generateOutputFile(development_file_path,test_file_path,first_input_word,second_input_word,output_file_path)

if __name__ == '__main__':
    main()
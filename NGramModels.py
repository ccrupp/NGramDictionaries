# Reads file data and builds language models for the file
# Carson Rupp
# coding: utf-8
import re
import os


def read_data(fileName):
    if os.stat(fileName).st_size == 0:
        print ("The file you have entered is empty, exiting...")
        exit()
    outlist = []
    infile = open(fileName, "r")
    for line in infile:
        outlist.append(line)
    infile.close()
    return outlist


def clean_data(my_data):

    # List of cleaned lines that you return
    newlist = []
    for line in my_data:
        # INSTRUCTION 7 - Multiple white spaces
        line = re.sub(' +', ' ', line)
        # INSTRUCTION 8 - Letters to lowercase
        line = line.lower()
        # INSTRUCTION 4 - Hyphen check
        first = re.sub('--+', ' ', line)
        line = re.sub('-', '', first)
        # Splits each line into separate words
        stringList = line.split(" ")
        # INSTRUCTION 1 - Prefix check
        for j in range(len(stringList)):
            str = stringList[j]
            if str[0].isdigit():
                for i in range(0, len(str)):
                    if not str[i].isdigit():
                        stringList[j] = str[0:i] + " " + str[i:]
                        break
        # INSTRUCTION 1 - Suffix check
        for j in range(len(stringList)):
            str = stringList[j]
            if str[len(str) - 1].isdigit():
                for i in range(len(str) - 1):
                    if str[i].isdigit():
                        stringList[j] = str[0:len(str) - i] + " " + str[len(str) - i:]
                        break

        # INSTRUCTION 6 - Non-Alphanumeric removal
        for j in range(len(stringList)):
            str = stringList[j]
            strBuilder = ""
            for i in range(len(str)):
                if not str[i].isalnum() and not str[i] == "'" and not str[i] == " ":
                    strBuilder += ""
                else:
                    strBuilder += str[i]
            stringList[j] = strBuilder
        # INSTRUCTION 2 and 5 - Number replacement
        finallist = []
        thisline = ""
        for str in stringList:
            if str != stringList[len(stringList) - 1]:
                thisline += str + " "
            else:
                thisline += str
        print thisline
        # print thisline
        result = re.sub("\d+", "num", thisline)
        # print result
        strings = thisline.split(" ")
        newlist.append(thisline)
    return newlist
data = read_data("C:\\Users\\carso\\PycharmProjects\\38003\\HW2\\Testcase.txt")
thislist = clean_data(data)
print thislist

def build_n_gram_dict(n, cleaned_data):
    ngram_dict = {}
    # Lines
    for line in cleaned_data:
        newline = "<s>" + " " + line
        words = newline.split(" ")
        # 
        for i in range(n, len(words) + 1):
            phrase = ""
            for j in range(n, 0, -1):
                phrase += words[i - j] + " "
            phrase = phrase.strip()
            # Adds to the frequency value
            if (phrase in ngram_dict.keys()):
                ngram_dict[phrase] += 1
            # Adds the key to the dictionary and sets the freq to 1
            else:
                ngram_dict[phrase] = 1
    return ngram_dict


# Task 4 - Perplexity
def calculateProb(phrase, ngram_models):
    n = len(phrase)
    firstCount = (ngram_models[n][phrase]) + 1
    secondCount = (ngram_models[n - 1][phrase[0:len(phrase)]]) + 1
    probability = firstCount / secondCount
    return probability


def calculate_PP(test_sentences, ngram_models):
    totalPP = 0
    onegram = ngram_models[1]
    v = len(onegram)
    ngrams = ngram_models.keys()
    ngrams.sort()
    maxngram = ngrams[len(ngrams) - 1]

    # Loops
    currentProb = 0
    # Loops through each sentence
    for j in range(len(test_sentences)):
        sentence = test_sentences[j]
        words = sentence.split(" ")
        sentencePP = 0
        """
        firstTwo = words[0] + " " + words[1]
        twoCount = ngram_models[2][firstTwo]
        oneCount = ngram_models[1][words[0]]
        #Keeps track of the currentProbability of the sentence
        currentProb = (twoCount + 1)/ (oneCount + v)
        """
        # Calculates the probability of the phrases up to the max ngram
        for i in range(1, maxngram):
            phrase = ""
            for k in range(i, 0, -1):
                phrase += words[i - k] + " "
            phrase.strip()
            phraseProb = calculateProb(phrase, ngram_models)
            if currentProb == 0:
                currentProb = phraseProb
            else:
                currentProb *= phraseProb
        # Calculates the probability of the rest of the sentence with max ngram
        for i in range(maxngram, len(words) + 1):
            phrase = ""
            for k in range(maxngram, 0, -1):
                phrase += words[i - k]
            phrase.strip()
            phraseProb = calculateProb(phrase, ngram_models)
            currentProb *= phraseProb
        sentencePP = (currentProb) ** (-1 / len(test_sentences[j]))
        totalPP += sentencePP
    averagePP = (totalPP) / len(test_sentences)
    return averagePP


# Task 5 - Text Generation
def generate_text(ngram_models, text_length, seed_word):
    genText = ""
    ngrams = ngram_models.keys()
    ngrams.sort()
    maxngram = ngrams[len(ngrams) - 1]
    vocab = ngram_models[1].keys()
    context = "<s>" + seed_word
    nextWord = ""
    # Calculates the context until it's of n length
    for i in range(1, maxngram):
        maxProb = -1
        for j in range(0, len(vocab)):
            phrase = context + " " + vocab[j]
            phrase.strip()
            n = len(phrase)
            probability = calculateProb(phrase, ngram_models)
            if probability > maxProb:
                maxProb = probability
                nextword = vocab[j]
        context += nextWord
    genText = context
    for i in range(0, text_length):
        maxProb = -1
        for j in range(0, len(vocab)):
            phrase = context + " " + vocab[j]
            phrase.strip()
            probability = calculateProb(phrase, ngram_models)
            if probability > maxProb:
                maxProb = probability
                nextword = vocab[j]
            genText += " " + nextWord
            genText.strip()
            context = ""
            textList = genText.split(" ")
            for j in range(genText - maxngram, len(textList) - 1):
                context += textList[j] + " "
            context.strip()
    return genText

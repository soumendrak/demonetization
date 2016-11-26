"""
Created by Soumendra Kumar Sahoo
Date: 26th November 2016
Function: This program will calculate the overall sentiment of public
          on the demonetization issue by fetching data from twitter
Future plans:
    1. Data extraction from twitter functionality will be added
    2. Visualization of the sentiments using seaborn/matplotlib module
    3. Performance improvement
    4. Converting it to Unsupervised learning
"""

import csv
import re
from nltk.tokenize import word_tokenize
import math

# AFINN-111 is as of June 2011 the most recent version of AFINN
# filenameAFINN = 'AFINN/AFINN-111.txt'
afinn = {}
with open('AFINN/sentiments.txt') as SentimentFile:
    for row in SentimentFile:
        afinn[row.split('\t')[0]] = int(row.split('\t')[1].strip())

emoticons_str = r'(?:[:=;][oO\-]? [D\)\]\(\]/\\OpP])'

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    # URLs
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')',
                       re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$',
                         re.VERBOSE | re.IGNORECASE)


def sentiment(words):
    """
    Returns a float for sentiment strength based on the input text.
    Positive values are positive valence, negative value are negative valence.
    """
    # words = pattern_split.split(text.lower())
    sentiments = map(lambda word: afinn.get(word, 0), words)
    if sentiments:
        # How should you weight the individual word sentiments?
        # You could do N, sqrt(N) or 1 for example. Here I use sqrt(N)
        sntmnt = float(sum(sentiments)) / math.sqrt(len(sentiments))
    else:
        sntmnt = 0
    return sntmnt


def tokenize(s):
    # return tokens_re.findall(s)
    return word_tokenize(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(
            token) else token.lower() for token in tokens]
    return tokens


def filereader(total=0):
    """
    This has been used to read the csv file
    :return read handler
    """
    with open('demonetization-tweets-Test.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                tweet = row['text']
                total += sentiment(preprocess(tweet))
            except UnicodeDecodeError:
                # There are some characters which can not be handled by Python
                # We need to ignore those characters
                pass
        return total


def main():
    """
    main paragraph to handle the processes
    :return:
    """
    Total = filereader()
    if Total > 0:
        print "Positive sentiments"
    else:
        print "Negative sentiments"


if __name__ == "__main__":
    main()

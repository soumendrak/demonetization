import csv
import re
from nltk.tokenize import word_tokenize
import math

# AFINN-111 is as of June 2011 the most recent version of AFINN
# filenameAFINN = 'AFINN/AFINN-111.txt'
afinn = {}
total = 0
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
        sentiment = float(sum(sentiments)) / math.sqrt(len(sentiments))
    else:
        sentiment = 0
    return sentiment


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
                # tweet = row['text'].decode('utf-8').encode('utf-8')
                tweet = row['text']
                total += sentiment(preprocess(tweet))
                print total
            except UnicodeDecodeError:
                # There are some characters which can not be handled by Python
                # We need to ignore those characters
                pass


def main():
    """
    main paragraph to handle the processes
    :return:
    """
    filereader()


if __name__ == "__main__":
    main()

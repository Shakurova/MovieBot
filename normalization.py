# coding: utf-8

import string
import re
import ujson

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# from stop_words import get_stop_words
# english_stopwords = get_stop_words('en')
# print(english_stopwords)
# ujson.dump(english_stopwords,  open('stopwords.json', 'w'))
english_stopwords = ujson.load(open('stopwords.json'))

LETTERS = string.ascii_lowercase
wordnet_lemmatizer = WordNetLemmatizer()

trash_words = ['Full-screen', 'full screen edition', 'VHS', 'English Subtitled', 'Two-Disc',
               'Blu-ray Combo in DVD Packaging', 'Blu-ray', 'DVD Combo', 'DVD', 'Special Edition', 'Steelbook Case',
               'The Criterion Collection', 'Family Fun Edition', 'full-screen edition', 'Widescreen', '[]', '()']


def normalize(text):
    """ Normalization function. """
    # 1. Lowercase
    text_text = text.lower()

    # 2. Remove non-letters
    letters_only = ''
    for _c in text_text:
        if _c in LETTERS:
            letters_only += _c
        else:
            letters_only += ' '

    # 3. Remove multiple spaces
    while '  ' in letters_only:
        letters_only = letters_only.replace('  ', ' ')

    # 4. Tokenization
    word_list = word_tokenize(letters_only)

    # 5. Lemmatization
    word_list = [wordnet_lemmatizer.lemmatize(word) for word in word_list]

    # 6. Remove stop words
    word_list = [wordnet_lemmatizer.lemmatize(word) for word in word_list if word not in english_stopwords]

    return ' '.join(word_list)


def movie_cleaner(text):
    for t in trash_words:
        text = re.sub('\(.*?\)', '', text)
        text = re.sub('\[.*?\]', '', text)
        text = text.replace(t, '')
    return text
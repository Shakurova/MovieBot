# -*- coding: utf-8 -*-

import ujson
import nltk
from nltk.util import ngrams
import editdistance


def find_title(text, movie_names, movie_db):

    token = nltk.word_tokenize(text)
    ngrm = []
    for i in range(1, 5):
        for t in ngrams(token, i):
            ngrm.append(t)

    # print('!!!', ngrm)
    for ngr in ngrm:
        if ' '.join(ngr) in movie_names:
            return 'full', ' '.join(ngr), movie_db[' '.join(ngr)]
        else:
            for title in movie_names:
                if editdistance.eval(' '.join(ngr), title) < len(title)/3:
                    # print('-' * 10)
                    # print(len(title))
                    # print(title, ' '.join(ngr), editdistance.eval(' '.join(ngr), title))
                    return 'lvnsht', ' '.join(ngr), movie_db[title]

if __name__ == '__main__':

    movie_names = open('movie_names.txt', 'r').read().split('\n')
    movie_db = ujson.load(open('nice_amazon2.json', 'r'))

    input = ['Hi! Can you give me a review of Disappeared', 'Hi! Can you give me a review of Diasppeared', 'What was the score of La Bamba?', 'What was the score of Bamba?',
             'Can you recommend me something like Full House movie?']

    for text in input:
        print(find_title(text, movie_names, movie_db))
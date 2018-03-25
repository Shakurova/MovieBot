# -*- coding: utf-8 -*-

import ujson
import nltk
from nltk.util import ngrams

movie_names_file = 'D:/Data/word2vec/nice_amazon2.json'

def find_title(text, movie_names):

    token = nltk.word_tokenize(text)
    ngrm = []
    for i in range(1, 5):
        for t in ngrams(token, i):
            ngrm.append(t)

    # print('!!!', ngrm)
    for ngr in ngrm:
        if ' '.join(ngr) in movie_names:
            return ' '.join(ngr), movie_names[' '.join(ngr)]


if __name__ == '__main__':

    # movie_names = open('movie_names.txt', 'r').read().split('\n')
    movie_names = ujson.load(open(movie_names_file, 'r'))

    input = ['Hi! Can you give me a review of Disappeared', 'What was the score of La Bamba?',
             'Can you recommend me something like Full House movie?']

    for text in input:
        print(find_title(text, movie_names))
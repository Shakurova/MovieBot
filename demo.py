# -*- coding: utf-8 -*-

import ujson

from gensim.models import KeyedVectors

import tmdbsimple as tmdb


from find_title import find_title
from intent import phrases
from intent.find_intent import IntentFinder
from intent.phrases import questions_answers
from normalization import normalize

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


tmdb.API_KEY = '63d059aa35be3c4f80368d5a192cfe26'
movie_names_file = './intent/movie_names_lower.txt'
movie_names = open(movie_names_file, 'r').read().split('\n')
movie_db = ujson.load(open('./intent/nice_amazon2_lower.json', 'r'))

model = KeyedVectors.load_word2vec_format('../wg3-semantic_space_models/GoogleNews-vectors-negative300.bin', binary=True)
intent_finder = IntentFinder(model)

if __name__ == '__main__':

    message = 'Give me score for full house movie'

    messages = ['Give me score for full house movie', 'Bye', 'Hello!', '']


    # Normalize text
    clean_text = normalize(message)  # for intent
    print('Clean text', clean_text)

    # Calculate Intent
    extracted_intent = intent_finder.model_distance(clean_text)
    print('Calculated intent', extracted_intent)

    if not extracted_intent:
        print('Sorry, could you rephrase')

    else:
        # Movie title extractor
        movie = find_title(message, movie_names)
        print('Extracted movie', movie)

        if movie == "Such a movie wasn't found":
            print("Such a movie wasn't found")

        else:
            if extracted_intent == 'greetings':
                print(phrases.their_greetings)

            elif extracted_intent == 'goodbyes':
                print(phrases.their_goodbyes)

            elif extracted_intent == 'review':
                print('Review:')
                print(movie_db[movie]['review'][0])

            elif extracted_intent == 'score':
                print('Score:')
                search = tmdb.Search()
                response = search.movie(query=movie)
                first = search.results[0]
                print('Popularity:', first['popularity'])
                print(first['title'], first['id'], first['release_date'])

            elif extracted_intent == 'recommendation':
                print('Recommendation:')
                search = tmdb.Search()
                response = search.movie(query=movie)
                first = search.results[0]

                movie = tmdb.Movies(first['id'])
                response = movie.info()
                print('Overview', response['overview'])
                print('Other films', movie.recommendations())


# Todo:
# create a button '\info' and add info about our bot
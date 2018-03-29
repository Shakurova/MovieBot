# -*- coding: utf-8 -*-

import random
import ujson
import sys
import telebot
from gensim.models import KeyedVectors

from find_title import find_title
from intent import phrases
from intent.find_intent import IntentFinder
from intent.phrases import questions_answers
from normalization import normalize

import tmdbsimple as tmdb
import ujson

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

bot = telebot.TeleBot('564436346:AAHNnOHgYONKDixXfRVg8j3pGdNFoaf9IA4')

# API_KEY = 'ee7b99c1'
# MOVIE_DB_URL = 'http://www.omdbapi.com/?apikey={}&?'.format(API_KEY)
tmdb.API_KEY = '63d059aa35be3c4f80368d5a192cfe26'
search = tmdb.Search()

# NYT_URL = '/reviews/search.json'
movie_names_file = './intent/movie_names_lower.txt'
movie_names = open(movie_names_file, 'r').read().split('\n')
movie_db = ujson.load(open('./intent/nice_amazon2_lower.json', 'r'))

model = KeyedVectors.load_word2vec_format('../wg3-semantic_space_models/GoogleNews-vectors-negative300.bin', binary=True)
intent_finder = IntentFinder(model)
print("Bot started")


def is_greeting(message):
    return matches(message, phrases.their_greetings)


def is_goodbye(message):
    return matches(message, phrases.their_goodbyes)


def is_howareyou(message):
    return matches(message, phrases.their_howareyou)


def is_ask_score(message):
    return matches(message, phrases.their_score)


def matches(message, messages):
    split_message = message.text.split(" ")
    contains = False
    for sm in split_message:
        formatted = sm.lower().strip()
        if any(True for g in messages if formatted == g.lower()):
            contains = True
            break
    return contains


@bot.message_handler(content_types=["text"])
def reply_with_intent(message):

    movie = find_title(message.text, movie_names)
    print(movie)

    clean_text = normalize(message.text)  # for intent
    print(clean_text)

    bot.send_message(message.chat.id, clean_text)  # normalized text
    bot.send_message(message.chat.id, movie)  # extracted movie


    # Identify intent
    # calculate distance between the averaged clean_text and each of the phrases
    # find only if movie is found
    bot.send_message(message.chat.id, intent_finder.model_distance(clean_text))

    # If both movie name and intent are identified, query database and API
    if intent_finder.model_distance(clean_text) == 'review':
        bot.send_message(message.chat.id, movie_db[movie]['review'][0])  # extracted review

    # If too small - sorry, could you rephrase?
    # Add intro to bot with description of functions
    if intent_finder.model_distance(clean_text) == 'recommendation':
        response = search.movie(query=movie)
        for s in search.results:
            print(s['title'], s['id'], s['release_date'], s['popularity'])
            movie = tmdb.Movies(s['id'])
            response = movie.info()
            print(response['overview'])
            print(movie.recommendations())


@bot.message_handler(content_types=["text"])
def did_not_understand(message):
    bot.send_message(message.chat.id, random.choice(phrases.my_confusion))

if __name__ == '__main__':
     bot.polling(none_stop=True)

# todo: text normalisation

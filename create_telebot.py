# -*- coding: utf-8 -*-

import random
import ujson
import sys
import telebot
from telebot import types
from gensim.models import KeyedVectors

from find_title import find_title
from intent import phrases
from intent.find_intent import IntentFinder
from intent.phrases import questions_answers
from normalization import normalize

from config import telebot_config, tmdb_config

import tmdbsimple as tmdb
import ujson

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

bot = telebot.TeleBot(telebot_config)

tmdb.API_KEY = tmdb_config
search = tmdb.Search()

movie_names_file = './intent/movie_names_lower.txt'
movie_names = open(movie_names_file, 'r').read().split('\n')
movie_db = ujson.load(open('./intent/nice_amazon2_lower.json', 'r'))

model = KeyedVectors.load_word2vec_format('../wg3-semantic_space_models/GoogleNews-vectors-negative300.bin', binary=True)
intent_finder = IntentFinder(model)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.row('/info')

print("Bot started")


@bot.message_handler(commands=['start'])
def send_message(message):
    bot.send_message(message.chat.id, "You can ask me about your favorite movie review score, recommendations for other movies or a sample review!", reply_markup=markup)


@bot.message_handler(commands=['info'])
def send_message(message):
    bot.send_message(message.chat.id, "You can ask me about your favorite movie review score, recommendations for other movies or a sample review!", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def respond(message):
    text = message.text

    movie = find_title(text, movie_names)
    logging.debug('Extracted movie: {}'.format(movie))

    # Normalize text
    clean_text = normalize(text)  # for intent
    logging.debug('Clean text: {}'.format(clean_text))

    # Calculate Intent
    extracted_intent = intent_finder.model_distance(clean_text)
    logging.debug('Calculated intent: {}'.format(extracted_intent))
    response = None
    if extracted_intent == 'greetings':
        response = random.choice(phrases.my_greetings)

    elif extracted_intent == 'goodbyes':
        response = random.choice(phrases.my_goodbyes)

    elif extracted_intent == 'review':
        if not movie:
            response = "I do not know about that movie."
        else:
            print('Review')
            response = random.choice(movie_db[movie]['review'])[2]

    elif extracted_intent == 'score':
        if not movie:
            response = "I do not know about that movie."
        else:
            print('Score')
            print('movie', movie)
            logging.debug('Score:')
            search = tmdb.Search()
            query = search.movie(query=movie)
            print('query', query)
            first = query['results']
            print(first)
            # first = query.results[0]
            popularity = first['vote_average']
            response = random.choice(phrases.my_score).format(popularity)
            logging.debug('Popularity: {}'.format(popularity))
            logging.debug('{} {} {}'.format(first['title'], first['id'], first['release_date']))

    elif extracted_intent == 'recommendation':
        if not movie:
            response = "Sorry, I do not know about that movie."
        else:
            print('movie', movie)
            logging.debug('Recommendation:')
            search = tmdb.Search()
            query = search.movie(query=movie)
            print('query', query)
            first = query['results']
            print(first)
            # first = query.results[0]
            print(first['id'])
            print(type(first['id']))
            tmdb_movie = tmdb.Movies(first['id'])
            # overview = tmdb_movie.info()['overview']
            response = random.choice(phrases.my_recommendation).format(tmdb_movie.recommendations())
            # logging.debug('Overview: {}'.format(response['overview']))
            logging.debug('Other films: {}'.format(tmdb_movie.recommendations()))

    else:
        response = random.choice(phrases.my_confusion)

    bot.send_message(message.chat.id, response)

if __name__ == '__main__':
     bot.polling(none_stop=True)

# todo: text normalisation

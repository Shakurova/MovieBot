# -*- coding: utf-8 -*-
import logging
import random
import ujson

import telebot
import tmdbsimple as tmdb
from gensim.models import KeyedVectors
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton

import telegram
from find_title import find_title
from intent import phrases
from intent.find_intent import IntentFinder
from normalization import normalize

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)

# Configuration - replace these with your values
TELEBOT_API_KEY = '564436346:AAHNnOHgYONKDixXfRVg8j3pGdNFoaf9IA4'
tmdb.API_KEY = '63d059aa35be3c4f80368d5a192cfe26'
MOVIE_NAMES_FILE = 'D:/Data/Amazon reviews/movie_names_lower.txt'
AMAZON_REVIEWS_FILE = 'D:/Data/Amazon reviews/nice_amazon2_lower.json'
WORD2VEC_MODEL_FILE = 'D:/Data/word2vec/GoogleNews-vectors-negative300.bin'

movie_names = open(MOVIE_NAMES_FILE, 'r').read().split('\n')
movie_db = ujson.load(open(AMAZON_REVIEWS_FILE, 'r'))
model = KeyedVectors.load_word2vec_format('%s' % WORD2VEC_MODEL_FILE, binary=True)
intent_finder = IntentFinder(model)
bot = telebot.TeleBot(TELEBOT_API_KEY)
print("Bot started.")
features_button_label = 'What can I do?'


@bot.message_handler(content_types=["text"])
def respond(message):
    text = message.text

    if text == features_button_label:
        bot.send_message(message.chat.id,
                         "You can ask me about your favorite movie review score, recommendations for other movies or a sample review!")
        return

    movie = find_title(text, movie_names)
    logging.debug('Extracted movie: {}'.format(movie))

    # Normalize text
    clean_text = normalize(text)  # for intent
    logging.debug('Clean text: {}'.format(clean_text))

    # Calculate Intent
    extracted_intent = intent_finder.model_distance(clean_text)
    logging.debug('Calculated intent: {}'.format(extracted_intent))
    response = None
    markup = None
    if extracted_intent == 'greetings':
        kb = [[InlineKeyboardButton(features_button_label, callback_data='/features')]]
        markup = ReplyKeyboardMarkup(kb)
        response = random.choice(phrases.their_greetings)

    elif extracted_intent == 'goodbyes':
        response = random.choice(phrases.their_goodbyes)

    elif extracted_intent == 'review':
        if movie == None:
            response = "I do not know about that movie."
        else:
            response = movie_db[movie]['review'][0]

    elif extracted_intent == 'score':
        if movie == None:
            response = "I do not know about that movie."
        else:
            logging.debug('Score:')
            search = tmdb.Search()
            query = search.movie(query=movie)
            first = query.results[0]
            popularity = first['popularity']
            response = random.choice(phrases.my_score).format(popularity)
            logging.debug('Popularity: {}'.format(popularity))
            logging.debug('{} {} {}'.format(first['title'], first['id'], first['release_date']))

    elif extracted_intent == 'recommendation':
        if movie == None:
            response = "I do not know about that movie."
        else:
            logging.debug('Recommendation:')
            search = tmdb.Search()
            query = search.movie(query=movie)
            first = query.results[0]
            movie = tmdb.Movies(first['id'])
            overview = movie.info()['overview']
            response = random.choice(phrases.my_recommendation).format(overview)
            logging.debug('Overview: {}'.format(response['overview']))
            logging.debug('Other films: {}'.format(movie.recommendations()))

    else:
        response = random.choice(phrases.my_confusion)

    bot.send_message(message.chat.id, response, reply_markup=markup)


if __name__ == '__main__':
     bot.polling(none_stop=True)

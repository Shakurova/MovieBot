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

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

bot = telebot.TeleBot('564436346:AAHNnOHgYONKDixXfRVg8j3pGdNFoaf9IA4')

API_KEY = 'ee7b99c1'
MOVIE_DB_URL = 'http://www.omdbapi.com/?apikey={}&?'.format(API_KEY)

NYT_URL = '/reviews/search.json'
movie_names_file = './intent/movie_names_lower.txt'
movie_names = open(movie_names_file, 'r').read().split('\n')
movie_db = ujson.load(open('./intent/nice_amazon2_lower.json', 'r'))

model = KeyedVectors.load_word2vec_format('../wg3-semantic_space_models/GoogleNews-vectors-negative300.bin', binary=True)
intent_finder = IntentFinder(phrases.questions_answers, model)
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

    best_intent_match = None
    best_intent_score = sys.maxsize
    movie = find_title(message.text, movie_names)
    print(movie)

    clean_text = normalize(message.text)  # for intent
    print(clean_text)

    bot.send_message(message.chat.id, clean_text)  # normalized text
    bot.send_message(message.chat.id, movie)  # extracted movie
    bot.send_message(message.chat.id, movie_db[movie]['review'][0])  # extracted review

    # Identify intent
    # calculate distance between the averaged clean_text and each of the phrases
    intent_finder.calculate_intent(clean_text)


    # answers = intent_finder.find_intent_answers(text)
    # if answers is None:
    #     did_not_understand(message)
    # else:
    #     movie = find_title(text, movie_names, movie_db)
    #
    #     # for questions, answers in questions_answers:
    #     #     text = message.text
    #     #     score = intent_finder.find_intent_answers(text, questions)
    #     #     if score < best_intent_score:
    #     #         best_intent_score = score
    #     #         best_intent_match = answers
    #     bot.send_message(message.chat.id, random.choice(answers).format(movie))


@bot.message_handler(content_types=["text"])
def did_not_understand(message):
    bot.send_message(message.chat.id, random.choice(phrases.my_confusion))

if __name__ == '__main__':
     bot.polling(none_stop=True)

# todo: text normalisation

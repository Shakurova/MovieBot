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

import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

bot = telebot.TeleBot('564436346:AAHNnOHgYONKDixXfRVg8j3pGdNFoaf9IA4')

API_KEY = 'ee7b99c1'
MOVIE_DB_URL = 'http://www.omdbapi.com/?apikey={}&?'.format(API_KEY)

NYT_URL = '/reviews/search.json'
movie_names_file = './intent/movie_names.txt'
movie_names = open(movie_names_file, 'r').read().split('\n')
movie_db = ujson.load(open('./intent/nice_amazon2.json', 'r'))

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
    text = message.text
    answers = intent_finder.find_intent_answers(text)
    if answers is None:
        did_not_understand(message)
    else:
        movie = find_title(text, movie_names, movie_db)

        # for questions, answers in questions_answers:
        #     text = message.text
        #     score = intent_finder.find_intent_answers(text, questions)
        #     if score < best_intent_score:
        #         best_intent_score = score
        #         best_intent_match = answers
        bot.send_message(message.chat.id, random.choice(answers).format(movie))


@bot.message_handler(content_types=["text"])
def did_not_understand(message):
    bot.send_message(message.chat.id, random.choice(phrases.my_confusion))

if __name__ == '__main__':
     bot.polling(none_stop=True)

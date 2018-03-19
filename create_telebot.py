# -*- coding: utf-8 -*-
import random

import telebot
import urllib.request

import phrases

bot = telebot.TeleBot('564436346:AAHNnOHgYONKDixXfRVg8j3pGdNFoaf9IA4')

API_KEY = 'ee7b99c1'
MOVIE_DB_URL = 'http://www.omdbapi.com/?apikey={}&?'.format(API_KEY)

NYT_URL = '/reviews/search.json'


def is_greeting(message):
    return matches(message, phrases.their_greetings)

def is_goodbye(message):
    return matches(message, phrases.their_goodbyes)

def is_ask_score(message):
    return matches(message, phrases.their_ask_score)

# TODO - bug: "w*hi*ch grade are you in?" matches "hi"
def matches(message, messages):
    return any(True for g in messages if message.text.lower() in g.lower() or g.lower() in message.text.lower())

@bot.message_handler(func=is_greeting, content_types=['text'])
def greeting(message):
    bot.send_message(message.chat.id, random.choice(phrases.my_greetings))

@bot.message_handler(func=is_goodbye, content_types=['text'])
def goodbye(message):
    bot.send_message(message.chat.id, random.choice(phrases.my_goodbyes))

@bot.message_handler(func=is_ask_score, content_types=['text'])
def answer_score(message):
    bot.send_message(message.chat.id, "The average score for that movie is {}".format(random.randint(1, 5)))

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, random.choice(phrases.my_confusion))



if __name__ == '__main__':
     bot.polling(none_stop=True)

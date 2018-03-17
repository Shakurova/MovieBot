# -*- coding: utf-8 -*-

import telebot
import tmdbsimple as tmdb
import ujson

bot = telebot.TeleBot('564436346:AAHNnOHgYONKDixXfRVg8j3pGdNFoaf9IA4')
tmdb.API_KEY = '63d059aa35be3c4f80368d5a192cfe26'

movie = tmdb.Movies(603)
response = movie.info()
print(response['overview'])
print(movie.title)
print(movie.budget)
print(movie.reviews()['results'][0])
print(len(movie.reviews()['results']))


print('Recommendations', movie.recommendations())

with open('recommendation.json', 'w') as w:
    ujson.dump(movie.recommendations(), w)


response = movie.releases()
for c in movie.countries:
   if c['iso_3166_1'] == 'US':
        print(c['certification'])

search = tmdb.Search()
response = search.movie(query='The Bourne')
for s in search.results:
    print(s['title'], s['id'], s['release_date'], s['popularity'])


person = tmdb.People(1)
print(person.info())



# similar_movies
# releases
#
# recommendations

# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message):
#     bot.send_message(message.chat.id, message.text)
#
# if __name__ == '__main__':
#      bot.polling(none_stop=True)

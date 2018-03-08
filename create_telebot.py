# -*- coding: utf-8 -*-

import telebot

bot = telebot.TeleBot('564436346:AAHNnOHgYONKDixXfRVg8j3pGdNFoaf9IA4')


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
     bot.polling(none_stop=True)

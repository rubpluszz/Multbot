#! usr/bin/python3
# -*- coding: utf-8 -*-
import telebot
from config import token
from config import admin_id
from game_proces import GameProcess
from _dictionary import start_new_game
from _dictionary import statistics
from _dictionary import rules
from _dictionary import expose_the_next_item



bot = telebot.TeleBot(token)

@bot.message_handler(content_types = ["text"])
def work_bot(message):
    """Дана функція получає текстовів повідомлення від користувача
    викликає екземпляр класссу GameProcess та передає йому всі необхідні дані
    метод returned_game повертає словник з двома елементами адреса картинки та текст відповідь"""
    try:
        print("New message received")
        game = GameProcess(message.text, message.from_user.id, message.from_user.language_code)
        reply = game.returned_message()
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.row(start_new_game[message.from_user.language_code], statistics[message.from_user.language_code], rules[message.from_user.language_code])
        if 'keyboard_list'in reply:
            keyboard.row(reply['keyboard_list'][0])
        if 'image' in reply:
            keyboard.row(reply['keyboard_list'][1], reply['keyboard_list'][2], reply['keyboard_list'][3])
            keyboard.row(reply['keyboard_list'][4], reply['keyboard_list'][5], reply['keyboard_list'][6])
            bot.send_photo(message.chat.id, open(reply['image'], 'rb'))
        bot.send_message(message.chat.id, reply['text'], reply_markup = keyboard, parse_mode = "HTML")
    except Exception as e:
        print(str(e))
        bot.send_message(admin_id, str(e))

if __name__ == '__main__':
    print("Bot start")
    bot.polling(none_stop=True)

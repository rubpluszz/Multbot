#! usr/bin/python3
# -*- coding: utf-8 -*-
import telebot
from config import token
from config import admin_id
from game_proces import GameProcess

bot = telebot.TeleBot(token)

start_new_game = {'uk':'Нова гра','ru':'Новая игра','en':'New game','pl':'Nowa gra' }
statistics = {'uk':'Статистика', 'ru':'Статистика', 'en':'Statistic','pl':'Statystyka'}
rules = {'uk':'Правила', 'ru':'Правила','en':'Rules', 'pl':'Zasady'}
expose_the_next_item = {'uk':'Показати ще кусок картинки',  'ru':'Показать ещё', 'en':'expose the next item ','pl':'Pokazac wiensej'}

@bot.message_handler(content_types = ["text"])
def work_bot(message):
    """Дана функція получає текстовів повідомлення від користувача
    передаэ її в класс GameProces, та вісилає користувачеві
    метод returned_game повертає слоВник з двома елементами адреса картинки та текст відповідь"""
    print('new message')
    game = GameProcess(message)
    reply = game.returned_message()
    print(message.from_user.language_code)
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row(start_new_game[message.from_user.language_code], statistics[message.from_user.language_code], rules[message.from_user.language_code])
    keyboard.row(expose_the_next_item[message.from_user.language_code])
    keyboard.row(reply['keyboard_list'][0], reply['keyboard_list'][1], reply['keyboard_list'][2])
    keyboard.row(reply['keyboard_list'][3], reply['keyboard_list'][4], reply['keyboard_list'][5])
    print(reply)
    if reply['image'] != None:
        bot.send_photo(message.chat.id, open(reply['image'], 'rb'))
    bot.send_message(message.chat.id, reply['text'], reply_markup = keyboard)


if __name__ == '__main__':
     bot.polling(none_stop=True)

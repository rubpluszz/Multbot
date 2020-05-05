from working_with_the_data_base import SqliteWork
from working_with_the_file_system import WorkWithFileSystem
import os
import shutil
import _dictionary

class GameProcess():

    def __init__(self, command, user_id, language):
        """При виклику необхідно в конструктор необхідно передати об'єкт message(повідомлення з телеграма)"""
        self.command = command
        self.user_id = user_id
        if language in ['uk']:
            self.language = language
        else:
            self.language = 'uk'
        self.db = SqliteWork(self.user_id)
        self.fs = WorkWithFileSystem(language)
        self.message_hub = {'/start':self.reply_to_start_message,
                            'Нова гра':self.start_new_game,
                            'Далі':self.next_level,
                            'Показати ще кусок картинки':self.next_round,
                            'Правила':self.rulles,
                            'Статистика':self.statistics,
                            'Продовжити':self.continue_game
                           }

    def returned_message(self):
        """Ця функція отримує команди та сортує їх, получає відповідь від необхідного метода таповертає її телеграм боту
           в словнику reply"""
        print('returned_message')
        if self.command in self.message_hub:
                reply = self.message_hub[self.command]()
        elif self.command in self.fs.return_answer(self.db.return_curent_quest_folder()):
            if int(self.db.return_level_curent_game())<16:
                reply = self.confirmation_of_correct_answer()
                self.db.change_level_curent_game()
            else:
                reply = self.your_win_messages()
                self.db.nullifies_curent_round()
                self.db.nullifies_level_curent_game()
                self.db.change_numbers_win_games()
            self.db.change_total_score()
        else:
            if self.db.return_level_curent_game()==0:
                reply = self.command_is_not()
            else:
                self.db.change_numbers_lose_games()#Збільшує у базі данних кількість програних ігор
                reply = self.not_correct_answer()
                self.db.nullifies_curent_round()
                self.db.nullifies_level_curent_game()
        return reply

    def command_is_not(self):
        """Цей метод викликається коли користувач присилає невідому команду"""
        reply = {'text':_dictionary.this_command_is_not[self.language], 'keyboard_list':_dictionary.further_key[self.language]}
        return reply

    def confirmation_of_correct_answer(self):
       """Ця функція формує повідомлення про правильну відповідь"""
       messages_midle = self.fs.return_block_of_interesting_information(self.db.return_curent_quest_folder())
       reply_answer =  _dictionary.messages_begining_one[self.language]+self.command+_dictionary.messages_begining_thwo[self.language]+messages_midle+_dictionary.messages_end[self.language]+_dictionary.your_winning[self.language]+str(self.db.return_level_curent_game()-self.db.return_curent_round())+_dictionary.krystall
       reply = {'text' : reply_answer, 'keyboard_list':_dictionary.further_key[self.language]}
       return reply

    def start_new_game(self):
        """Це перший метод котрий запускається після отримання повідомлення 'Нова гра'"""
        curent_level = self.db.return_level_curent_game()#Рівень поточної гри
        print('start-game')
        if curent_level == None:#Якщо такого запису немає..
            self.db.add_new_user()#...то додати запис
        else:
            self.db.nullifies_level_curent_game()
            self.db.nullifies_curent_round()
        return(self.first_quest())

    def first_quest(self):
        """Задає завдання на першому рівні"""
        print('first_quest')
        self.db.change_level_curent_game()#...підняти рівень поточної гри на 1
        return(self.next_level())

    def reply_to_start_message(self):
        """Відповідь на повідомлення /start"""
        reply = {'text':_dictionary.reply_to_start[self.language],  }
        return reply

    def not_correct_answer(self):
        """В цьому методі буде здійснено формування повідомлення про поразку в
        котре входить повідмлення що ти програв, інформація про твої досягнення
        а також вивід таблиці лідерів"""
        game_inf = self.db.select_user_information()#повертає всі дані користувача з бази данних
        correct_answer = self.fs.return_answer(game_inf[6])
        total_score = _dictionary.total_score[self.language]+str(game_inf[2])+'\n'
        win_games   = _dictionary.win_games[self.language]+str(game_inf[4])+'\n'
        lost_games  = _dictionary.lost_games[self.language]+str(game_inf[5])+'\n'
        reply = {'text':_dictionary.answer_is_bad[self.language]+ correct_answer + _dictionary.your_scores[self.language]+ total_score + win_games + lost_games + _dictionary.press_new_game_to_start[self.language]}
        return reply

    def your_win_messages(self):
        """В цьому методі буде здійснено формування повідомлення про перемогу в
        котре входить повідмлення що ти переміг, інформація про твої досягнення
        а також вивід таблиці лідерів"""
        reply = {'text':_dictionary.your_win_message_text[self.language],  }
        return reply

    def next_level(self):
        """В цьому методі описано спосіб вибору наступного рівня"""
        image_folder = self.fs.select_a_picture_folder(self.db.return_curent_quest_folder())#Дізнаємся папку з вибраною кртинкою
        self.db.change_curent_quest_folder(image_folder)
        reply = {'text':_dictionary.quest[self.language]+_dictionary.winning_is_possible[self.language]+str(self.db.return_level_curent_game()-self.db.return_curent_round())+_dictionary.krystall,'image':self.fs.picture_for_current_level(image_folder,self.db.return_level_curent_game(), self.db.return_curent_round()),'keyboard_list':self.fs.return_a_list_of_answer_options(image_folder)}
        return reply

    def next_round(self):
        """Cлідуючий раунд в слідуючому раунді рівня бот присилає слідуючий шматок
        картинки гравець повинен старатися відгадати картинку з найменшою кількістю раундів """
        if self.db.return_curent_round() < self.db.return_level_curent_game()-1 :
            self.db.change_current_round()
            reply = self.continue_game()
        elif self.db.return_level_curent_game() == 1:
            image_folder = self.db.return_curent_quest_folder()
            reply = {'text':_dictionary.first_level[self.language]+_dictionary.quest[self.language]+_dictionary.winning_is_possible[self.language]+'1'+_dictionary.krystall,'image':self.fs.picture_for_current_level(image_folder,self.db.return_level_curent_game(), self.db.return_curent_round()),'keyboard_list':self.fs.return_a_list_of_answer_options(image_folder)}
        elif self.db.return_level_curent_game() == 0:
            reply = {'text':_dictionary.not_curent_game[self.language] }
        else:
            image_folder = self.db.return_curent_quest_folder()
            reply = {'text':_dictionary.last_round[self.language]+_dictionary.quest[self.language]+_dictionary.winning_is_possible[self.language]+'1'+_dictionary.krystall,'image':self.fs.picture_for_current_level(image_folder,self.db.return_level_curent_game(), self.db.return_curent_round()),'keyboard_list':self.fs.return_a_list_of_answer_options(image_folder)}
        return reply

    def continue_game(self):
        """Продовжити гру"""
        if self.db.return_level_curent_game() != 0:
            image_folder = self.db.return_curent_quest_folder()
            reply = {'text':_dictionary.quest[self.language]+_dictionary.winning_is_possible[self.language]+str(self.db.return_level_curent_game()-self.db.return_curent_round())+_dictionary.krystall,'image':self.fs.picture_for_current_level(image_folder,self.db.return_level_curent_game(), self.db.return_curent_round()),'keyboard_list':self.fs.return_a_list_of_answer_options(image_folder)}
        else:
            reply = {'text':_dictionary.continue_if_not_current_game[self.language]}
        return reply

    def rulles(self):
        """Цей метод повертає повідомлення з правилами на відповідній мові"""
        reply = {'text':_dictionary.rulles_text[self.language], 'keyboard_list':_dictionary.continue_[self.language]}
        return reply

    def statistics(self):
        """Цей метод повертає статистику гравця"""
        game_inf = self.db.select_user_information()
        answer_text = _dictionary.answer_text[self.language]
        total_score = _dictionary.total_score[self.language]+str(game_inf[2])+'\n'
        win_games   = _dictionary.win_games[self.language]+str(game_inf[4])+'\n'
        lost_games  = _dictionary.lost_games[self.language]+str(game_inf[5])+'\n'
        level_game  = _dictionary.level_game[self.language]+str(game_inf[1])+'/16\n'
        round_level = _dictionary.round_level[self.language]+str(game_inf[3])+'/15\n'
        reply = {'text':answer_text + total_score + win_games + lost_games + level_game + round_level, 'keyboard_list':_dictionary.continue_[self.language] }
        print(reply)
        return reply

from working_with_the_data_base import SqliteWork
from working_with_the_file_system import WorkWithFileSystem
import os
import shutil

class GameProcess():
    """"""
    def __init__(self, message,):
        """При виклику необхідно в конструктор необхідно передати об'єкт message(повыдомлення з телеграма)"""
        self.message = message
        self.command = message.text
        self.user_id = message.from_user.id
        self.language = message.from_user.language_code
        self.db = SqliteWork(self.user_id)
        self.fs = WorkWithFileSystem(message, self.db)
        self.message_hub = {'/start':self.reply_to_start_message,
                            'Нова гра':self.start_new_game,
                            'Далі':self.next_level,
                            'Показати ще кусок картинки':self.next_round,
                            'Правила':self.rulles,
                            'Статистика':self.statistics,
                            'Продовжити':self.continue_game
                           }
        self.quest = {'uk':'Уважно подивіться на картинку та спробуйте відгадати з якого це мультфільма.'}


    def returned_message(self):
        """Ця функція отримує команди та сортує їх, получає відповідь від необхідного метода таповертає її телеграм боту
           в словнику reply"""
        print('returned_message')
        if self.command in self.message_hub:
                reply = self.message_hub[self.command]()
        elif self.command == '   ':#Страховка якщо хтось натисне пусту кнопку
            pass
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
                reply = self.not_correct_answer()
                self.db.nullifies_curent_round()
                self.db.nullifies_level_curent_game()
        return reply

    def command_is_not(self):
        answer = {'uk':'Я не знаю такої команди для зручності використовуйте вбудовану ігрову клавіатуру'}
        reply = {'text':answer[self.language], 'image':None, 'keyboard_list':['   ','Далі','   ','   ','   ','   ']}
        return reply

    def confirmation_of_correct_answer(self):
       """Ця функція формує повідомлення про правильну відповідь"""
       messages_begining = {'uk':f'Так {self.command} це правильна відповідь, я знаю багато цікавого про цей фільм і можу тобі розповісти. Ось наприклад ти знав що, '}
       messages_end = {'uk' : 'Для продовження натисни "Далі".'}
       messages_midle = self.fs.return_block_of_interesting_information(self.db.return_curent_quest_folder())
       reply_answer =  messages_begining[self.language]+messages_midle+messages_end[self.language]
       reply = {'text' : reply_answer, 'image' : None, 'keyboard_list':['   ','Далі','   ','   ','   ','   '] }
       return reply

    def start_new_game(self):
        """Це перший метод котрий запускається після отримання повідомлення 'Нова гра'"""
        curent_level = self.db.return_level_curent_game()#Рівень поточної гри
        print('start-game')
        if curent_level == None:#Яко такого запису немає..
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
        returned_messages = {'uk':'Вітаю тебе мене звуть МультБот і я хочу заграти з тобою гру в котрій треба вгаувати нащви мультфільмів по шматочкам кадрів. Якщо ти теж не проти зіграти зі мною то натисни "Нова гра" натисни "Правила" якщо ти нерозумієш як грати.'}
        reply = {'text':returned_messages[self.language], 'image':None, 'keyboard_list':['   ','   ','   ','   ','   ','   ']}
        return reply

    def not_correct_answer(self):
        """В цьому методі буде здійснено формування повідомлення про поразку в
        котре входить повідмлення що ти програв, інформація про твої досягнення
        а також вивід таблиці лідерів"""
        answer_text = {'uk':f'Нажаль це неправильна відповідь для того щоб почати нову гру натисніть на кнопку "Нова гра".\nОсь твої результати: \n' }
        game_inf = self.db.select_user_information()
        total_score = {'uk':f'Очки_______________________{game_inf[2]}\n'}
        win_games   = {'uk':f'Виграні ігри_______________{game_inf[4]}\n'}
        lost_games  = {'uk':f'Програні ігри______________{game_inf[5]}\n'}
        reply = {'text':answer_text[self.language] + total_score[self.language]+win_games[self.language]+lost_games[self.language], 'image':None, 'keyboard_list':['   ','   ','   ','   ','   ','   ']  }
        return reply

    def your_win_messages(self):
        """В цьому методі буде здійснено формування повідомлення про перемогу в
        котре входить повідмлення що ти переміг, інформація про твої досягнення
        а також вивід таблиці лідерів"""
        your_win_message_text = {'uk':'Ти переміг'}
        reply = {'text':your_win_message_text[self.language], 'image':None, 'keyboard_list':['   ','   ','   ','   ','   ','   ']}
        return reply

    def next_level(self):
        """В цьому методі описано спосіб вибору наступного рівня"""
        image_folder = self.fs.select_a_picture_folder()#Дізнаємся папку з вибраною кртинкою
        self.db.change_curent_quest_folder(image_folder)
        reply = {'text':self.quest[self.language],'image':self.fs.picture_for_current_level(image_folder,self.db.return_level_curent_game(), self.db.return_curent_round()),'keyboard_list':self.fs.return_a_list_of_answer_options(image_folder)}
        return reply

    def next_round(self):
        """Cлідуючий раунд в слідуючому раунді рівня бот присилає слідуючий шматок картинки гравець повинен старатися відгадати картинку з найменшою кількістю раундів """
        if self.db.return_curent_round() < self.db.return_level_curent_game()-1 :
            self.db.change_current_round()
            reply = self.continue_game()
        elif self.db.return_level_curent_game() == 1:
            image_folder = self.db.return_curent_quest_folder()
            first_level = {'uk':"На першому рівні показана цілий кадр тому тобі непотрібні підказки"}
            reply = {'text':first_level[self.language]+self.quest[self.language],'image':self.fs.picture_for_current_level(image_folder,self.db.return_level_curent_game(), self.db.return_curent_round()),'keyboard_list':self.fs.return_a_list_of_answer_options(image_folder)}
        elif self.db.return_level_curent_game() == 0:
            answer_text = {'uk':'Зараз немає ні одної запущеної гри натисніть нова гра щоб розпочати'}
            reply = {'text':answer_text[self.language], 'image':None, 'keyboard_list':['   ','   ','   ','   ','   ','   ']  }
        else:
            image_folder = self.db.return_curent_quest_folder()
            last_round = {'uk':"Це останній раунд для цього рівня ти  маєш дати відповідь"}
            reply = {'text':last_round[self.language]+self.quest[self.language],'image':self.fs.picture_for_current_level(image_folder,self.db.return_level_curent_game(), self.db.return_curent_round()),'keyboard_list':self.fs.return_a_list_of_answer_options(image_folder)}
        return reply


    def continue_game(self):
        """Продовжити гру"""
        image_folder = self.db.return_curent_quest_folder()
        reply = {'text':self.quest[self.language],'image':self.fs.picture_for_current_level(image_folder,self.db.return_level_curent_game(), self.db.return_curent_round()),'keyboard_list':self.fs.return_a_list_of_answer_options(image_folder)}
        return reply

    def rulles(self):
        """Цей метод повертає повідомлення з правилами на відповідній мові"""
        rulles_text = {'uk':"""Відгадай мультфільм це гра вікторина в котрій ви
повинні вгадати назву мультфільма за шматком кадра з
цього мультфільма.

Всі мультфільми в даній версії гри є повнометражними.
Якщо мультфільм є частиною франшизи то за звичай це є перша
частина цієї франшизи винятком являються мультфільми
об'єднані в одну франшизу, але вони немають спільного сюжету
чи персонажів.

На першому рівні гравець повинен вгадати фільм по цілий картинці
На другім картинка розділена на дві частини, на третім три, на
четвертім чотири і так далі аж до шістнадцятого рівня.

Кожне завдання можна вирішити за певну кількість спроб - раундів.
Лічба раундів для кожного рівня дорівнює рівню.
Раунди нумеруються з нуля тобто перший раунд буде мати 0 а
шістнадцятий 15. В кожнім раунді гравцеві буде показуватись
шматок картинки котрий небув показаний раніше.
На першім рівні картинка ціла тому його треба пройти за один раунд.
На шістнадцятім картинка порізана на шістнадцять частин тому його
можна пройти за 16 раундів. Слідуючий раунд починається після
натиснення на кнопку "Показати ще кусок картинки"

Очки на рховуються слідуючим способом. за  кожен рівень нараховуються
кількість очок котра дорівнює рівню мінус раунд на котрому було вгадано
мультфільм

Гра триває доти поки гравець не помилиться. Або не пройде 16 рівнів
Якщо гравець помилився це програш.

Кнопка "Нова Гра" обнуляє результати поточної ігрової сесії та починає
нову гру

Кнопка "Статистика" виводить ваші ігрові досягнення

Решта кнопок для вибору подальших дій.

Натисніть кнопку "Далі" щоб продовжити"""}
        reply = {'text':rulles_text[self.language], 'image':None, 'keyboard_list':['   ','Продовжити','   ','   ','   ','   ']}
        return reply

    def statistics(self):
        """Цей метод повертає статистику гравця"""
        game_inf = self.db.select_user_information()
        answer_text = {'uk':f'Ваші поточні досягнення:\n'}
        total_score = {'uk':f'Очки_______________________{game_inf[2]}\n'}
        win_games   = {'uk':f'Виграні ігри_______________{game_inf[4]}\n'}
        lost_games  = {'uk':f'Програні ігри______________{game_inf[5]}\n'}
        level_game  = {'uk':f'Рівень поточної гри_______{game_inf[1]}/16\n'}
        round_level = {'uk':f'Раунд поточного питання_{game_inf[3]}/15\n'}
        reply = {'text':answer_text[self.language] + total_score[self.language]+win_games[self.language]+lost_games[self.language]+level_game[self.language]+round_level[self.language], 'image':None, 'keyboard_list':['   ','Продовжити','   ','   ','   ','   ']  }
        return reply

if __name__ == "__main__":
    pass

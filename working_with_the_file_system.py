#! -*- coding: utf-8 -*-
import os
from config import image_folder
import random
import _dictionary

class WorkWithFileSystem():
    """В цьому классі описано методи вибору завдання а також відповідного малюнку
       Також тут описано вибір поточного малюнку """

    def __init__(self, language):
        """При виклику необхідно в конструктор необхідно передати language мова телеграм клієнта користувача"""
        self.language = language
    #Послідовність картинок вибирається наступним способом з словника де першим ключем є найменьший дільник назви папки переведеної в int + рівень а другий рівень далі з списку вибирається по номеру раунда
    rules_for_opening_pictures = {2:{1:["001"],
                                     2:["001","002"],
                                     3:["001","003","002"],
                                     4:["004","002","001","003"],
                                     5:["002","001","003","005","004"],
                                     6:["005","004","001","003","006","002"],
                                     7:["004","005","003","001","002","006","007"],
                                     8:["006","002","004","003","001","005","008","007"],
                                     9:["009","006","002","004","003","001","005","008","007"],
                                    10:["003","002","001","007","006","005","004","010","008","009"],
                                    11:["008","009","010","004","005","011","006","007","001","002","003"],
                                    12:["011","012","003","002","001","007","006","005","004","010","008","009"],
                                    13:["012","011","002","013","007","001","005","006","010","004","009","008","003"],
                                    14:["006","003","008","002","009","004","010","005","014","001","007","013","011","012"],
                                    15:["001","003","008","002","009","004","010","015","014","001","007","013","011","012","005"],
                                    16:["004","003","002","001","008","007","006","005","012","011","010","009","016","015","014","013"]},
                                  3:{1:["001"],
                                     2:["002","001"],
                                     3:["003","001","002"],
                                     4:["002","004","003","001"],
                                     5:["001","002","004","003","005"],
                                     6:["006","003","001","005","006","002"],
                                     7:["007","004","005","003","001","002","006"],
                                     8:["008","007","003","001","004","005","006","002"],
                                     9:["006","002","004","003","001","005","008","007","009"],
                                    10:["003","002","001","007","006","005","004","010","008","009"],
                                    11:["008","003","002","001","007","006","005","004","010","011","009"],
                                    12:["011","008","003","002","001","007","006","005","004","010","012","009"],
                                    13:["013","011","008","003","002","001","007","006","005","004","010","012","009"],
                                    14:["006","013","011","008","003","002","001","007","014","005","004","010","012","009"],
                                    15:["005","003","008","013","009","004","010","015","014","001","007","002","011","012","001"],
                                    16:["002","003","004","001","006","007","008","005","010","011","012","009","014","015","016","013"]},
                                  5:{1:["001"],
                                     2:["001","002"],
                                     3:["002","003","001"],
                                     4:["003","004","001","002"],
                                     5:["002","001","005","004","003"],
                                     6:["006","002","004","005","001","003"],
                                     7:["004","003","005","002","001","007","006"],
                                     8:["007","006","002","004","003","001","005","008"],
                                     9:["006","002","004","003","001","005","008","007","009"],
                                    10:["009","001","002","006","007","004","005","008","010","003"],
                                    11:["009","008","004","010","011","005","007","006","002","001","003"],
                                    12:["009","008","002","003","007","001","005","006","004","010","012","011"],
                                    13:["008","011","002","013","010","001","005","006","007","004","009","012","003"],
                                    14:["003","006","002","008","004","009","005","010","001","014","013","007","012","011"],
                                    15:["005","012","011","013","007","001","010","014","015","004","009","002","008","003","001"],
                                    16:["003","002","001","004","007","006","005","008","011","010","009","012","015","014","013","016"]},
                                  7:{1:["001"],
                                     2:["002","001"],
                                     3:["001","002","003"],
                                     4:["004","003","002","001"],
                                     5:["001","002","003","005","004"],
                                     6:["003","006","001","004","002","005"],
                                     7:["001","002","003","004","005","006","007"],
                                     8:["002","006","004","003","008","007","001","005"],
                                     9:["009","007","008","001","003","005","004","002","006"],
                                    10:["001","002","003","005","006","007","008","010","004","009"],
                                    11:["010","009","008","011","005","004","001","007","006","003","002"],
                                    12:["003","012","011","007","001","002","004","005","006","009","008","010"],
                                    13:["002","011","012","001","007","013","010","006","005","008","009","004","003"],
                                    14:["008","003","006","004","009","002","014","005","010","013","007","001","011","012"],
                                    15:["001","003","008","002","009","004","010","015","014","001","007","013","011","012","005"],
                                    16:["001","002","003","004","005","006","007","008","009","010","011","012","013","014","015","016"]}}

    def return_the_list_of_folders_with_images(self):
        """Ця функція повертає список піддеректорій в деректорії images
        ім`ям кожної вкладеної папки  являється цифра від 1 кожна з папок містить
        16 піддерикторій з іменами від одного до 16 (котрі заодно означають рівень
        складності завдання в поточній папці) в папці з адресою "images/1/1" буде
        один малюнок а в "imаges/1/16" буде той же малюнок порізаний на 16 пазлів
        В папку images можна додаавти будьяку кількість  піддіерикторій головне щоб була збережена структура"""
        try:
            folder_list  = os.listdir(image_folder)
            return (folder_list)
        except Exception as e:
            print(str(e), "    >>>WorkWithFileSystem.return_the_list_of_folders_with_images")
            return str(e)

    def select_a_picture_folder(self):
        """Вибрати випадкову папку з картинкою папку з картинкою"""
        try:
            return(random.choice(self.return_the_list_of_folders_with_images()))
        except Exception as e:
            print(str(e), "    >>>WorkWithFileSystem.select_a_picture_folder")
            return str(e)

    def select_rules_to_opening_pictures(self, image_folder, level_curent_game):
        """Цей метод описує спосіб вибору правила для подальшої видачі картинок"""
        try:
            first_number = int(image_folder)+int(level_curent_game)
            print("first_number", first_number)
            dilnyk = [7,5,3,2]
            for i in dilnyk:
                if first_number%i == 0:
                    print("select_rules_to_opening_pictures" , i)
            return (i)
        except Exception as e:
            print(str(e), "    >>>WorkWithFileSystem.select_rules_to_opening_pictures")
            return(str(e))

    def picture_for_current_level(self, image_folder, level_curent_game = "1", curent_round = 0):
        """Вибирає який jpg файл відправити користувачеві
        image_folder - папка з картинкою, level_curent_game -Рівень в поточній ігровій сесії(одночасно ім'я піддиректорії)"""
        try:
            print('picture_for_current_level ',image_folder)
            image = f"images/{image_folder}/{level_curent_game}/image_part_{self.rules_for_opening_pictures[self.select_rules_to_opening_pictures(image_folder, level_curent_game)][int(level_curent_game)][curent_round]}.jpg"
            return(image)
        except Exception as e:
            print(str(e), "    >>>WorkWithFileSystem.picture_for_current_level" )
            return(str(e))

    def return_answer(self, image_folder):
        """Цей метод повертає ім'я мультфільма з inf_{language_code}.txt
        image_folder - папка з картинкою завдванням """
        try:
            f = open(f"images/{image_folder}/inf_{self.language}.txt", "r", encoding = "utf-8")
            return (f.readline())
        except Exception as e:
            print(str(e), "    >>>WorkWithFileSystem.return_answer")
            return(str(e))

    def return_block_of_interesting_information(self, image_folder):
        """Цей метод повертає блок цікавої інформації для виведення користувачеві"""
        try:
            f = open(f"images/{image_folder}/inf_{self.language}.txt", "r", encoding = "utf-8")
            return(random.choice(f.readlines()[1:]))#В нульовім елементі знаходиться назва мультфільма
        except Exception as e:
            print(str(e), "    >>>WorkWithFileSystem.return_block_of_interesting_information")
            return(str(e))

    def return_a_list_of_answer_options(self, image_folder):
        """Цей метод повертає список з правильних та не правильних варіантів відповідей та записує номер правильної відповіді до DB"""
        try:
            image_folder_list = self.return_the_list_of_folders_with_images()#список папок з картинкaми
            list_of_answer = random.choices(image_folder_list, k=6)
            if image_folder in list_of_answer:
                pass
            else:
                list_of_answer[0] = image_folder
            random.shuffle(list_of_answer)
            text_list_of_answer = [_dictionary.expose_the_next_item[self.language][0]]
            for answer in list_of_answer:
                text_list_of_answer.append(self.return_answer(answer))
            return text_list_of_answer
        except Exception as e:
            print(str(e), "    >>>WorkWithFileSystem.return_list_of_answer_options")
            return(str(e))

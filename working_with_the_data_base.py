import sqlite3
from config import database

class SqliteWork():
    """Цей клас працює з базою данних"""

    def __init__(self, user_id):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.user_id = user_id

    def add_new_user(self):
        """Додає нового користувача до бази данних"""
        try:
            self.cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (self.user_id, 0, 0, 0, 0, 0, '0'))
            self.connection.commit()
            print('added new user to db')
            return True
        except Exception as e:
            print(str(e))
            return str(e)

    def return_level_curent_game(self):
        """Повертає значення в level_curent_game
        для визначення рівня поточної гри"""
        try:
            return self.cursor.execute(f"SELECT level_curent_game FROM users WHERE user_id = {self.user_id}").fetchall()[0][0]
        except Exception as e:
            print(str(e))
            return (None)

    def change_level_curent_game(self):
        """Збільшує рівень поточної ігрової сесії на один (поле level_curent_game)"""
        try:
            old_level_curent_game = self.return_level_curent_game()
            self.cursor.execute(f"UPDATE users SET level_curent_game ={int(old_level_curent_game)+1} WHERE user_id = {self.user_id}")
            self.connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return str(e)


    def nullifies_level_curent_game(self):
        """Обнуляє рівень ігрової сесії
            Коли гравець завершує ігрову сесію то
            рівень поточної ігрової сесії дорівнює 0
            поле level_curent_game)"""
        try:
            self.cursor.execute(f"UPDATE users SET level_curent_game = 0 WHERE user_id = {self.user_id}")
            self.connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return str(e)

    def change_current_round(self):
        """ Збільшує рівень current_round на один кожен раз коли користувач бере слідуючий елемент малюнка"""
        try:
            old_curent_round = self.return_curent_round()
            self.cursor.execute(f"UPDATE users SET curent_round = {int(old_curent_round)+1} WHERE user_id = {self.user_id}")
            self.connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return str(e)

    def nullifies_curent_round(self):
        """ Обнуляє значення в сurrent_round коли гравець програє або проходить рівень"""
        try:
            self.cursor.execute(f"UPDATE users SET curent_round = 0 WHERE user_id = {self.user_id}")
            self.connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return str(e)


    def return_curent_round(self):
        """Повертає поточний значення current_round"""
        try:
            return self.cursor.execute(f"SELECT curent_round FROM users WHERE user_id = {self.user_id}").fetchall()[0][0]
        except Exception as e:
            print(str(e))
            return str(e)

    def change_total_score(self):
        """При проходженні рівня збільшує total_score на return_level_curent_game() - return_current_round()"""
        try:
            new_total_score = int(self.return_total_score()) + int(self.return_level_curent_game()) - int(self.return_curent_round())
            self.cursor.execute(f"UPDATE users SET total_score = {new_total_score} WHERE user_id = {self.user_id}")
            self.connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return str(e)

    def return_total_score(self):
        """Повертає значення total_score"""
        try:
            return self.cursor.execute(f"SELECT total_score FROM users WHERE user_id = {self.user_id}").fetchall()[0][0]
        except Exception as e:
            print(str(e))
            return str(e)

    def change_numbers_win_games(self):
        """Збільшує на один кількість виграних ігор(поле numbers_win_game) коли гравець проходить ігрову сесію довжиною в 16 рівнів"""
        try:
            old_numbers_win_game = self.return_numbers_win_games()
            self.cursor.execute(f"UPDATE users SET numbers_win_games = {int(old_numbers_win_game)+1} WHERE user_id = {self.user_id}")
            self.connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return str(e)

    def return_numbers_win_games(self):
        """Повертає кількість виграних ігор"""
        try:
            return self.cursor.execute(f"SELECT numbers_win_games FROM users WHERE user_id = {self.user_id}").fetchall()[0][0]
        except Exception as e:
            print(str(e))
            return str(e)

    def change_numbers_lose_games(self):
        """Збільшує на один кількість програних ігор(поле numbers_lose_games) коли гравець програє сесію"""
        try:
            old_numbers_lose_games = self.return_numbers_lose_games()
            self.cursor.execute(f"UPDATE users SET numbers_lose_games = {int(old_numbers_lose_games)+1} WHERE user_id = {self.user_id}")
            self.connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return str(e)

    def return_numbers_lose_games(self):
        """Повертає кількість програних ігор"""
        try:
            return self.cursor.execute(f"SELECT numbers_lose_games FROM users WHERE user_id = {self.user_id}").fetchall()[0][0]
        except Exception as e:
            print(str(e))
            return str(e)

    def change_curent_quest_folder(self, curent_quest_folder_name):
        """Змінює папку з котрої показують картинку на  поточнім рівні"""
        try:
            self.cursor.execute(f"UPDATE users SET curent_quest_folder = {curent_quest_folder_name} WHERE user_id = {self.user_id}")
            self.connection.commit()
            return True
        except Exception as e:
            print(str(e))
            return str(e)

    def return_curent_quest_folder(self):
        """Повертає кількість програних ігор"""
        try:
            return self.cursor.execute(f"SELECT curent_quest_folder FROM users WHERE user_id = {self.user_id}").fetchall()[0][0]
        except Exception as e:
            print(str(e))
            return str(e)

    def select_user_information(self):
        """Повертає кортеж зі всією інформацією про ігровий прогрес"""
        try:
            return self.cursor.execute(f"SELECT * FROM users WHERE user_id = {self.user_id}").fetchall()[0]
        except Exception as e:
            print(str(e), "   >>>db.select_user_information")
    def __del__(self):
        self.connection.close()

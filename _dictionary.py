#__________nult_heroes_bot _______ Button for  bot____________________________________________________________________________________________________________
start_new_game = {'uk':'Нова гра','ru':'Новая игра','en':'New game','pl':'Nowa gra' }
statistics = {'uk':'Статистика', 'ru':'Статистика', 'en':'Statistic','pl':'Statystyka'}
rules = {'uk':'Правила', 'ru':'Правила','en':'Rules', 'pl':'Zasady'}
expose_the_next_item = {'uk':'Показати ще кусок картинки',  'ru':'Показать ещё', 'en':'Expose the next item ','pl':'Pokazac wiensej'}
error_message = {'uk':'Вибачте щось пішло не так. Ми вже працюємо над цим. Спробуйте виконати іншу дію. Якщо нічого не працює відправти повідомлення з текстом "/start" після чого натиснути "Нова гра" перепрошуємо за незручності'}

#__________GameProcess_________________________________________________________________________________________________________________________________________
quest = {'uk':'Уважно подивіться на картинку та спробуйте відгадати з якого це мультфільма. Щоб краще розгледіти картинку можете тапнутти по ній'}

#________GameProcess.statistics_________________________________________________________________________________________________________________________________
answer_text = {'uk':'Ваші поточні досягнення:\n'}
total_score = {'uk':'Очки_______________________'}
win_games   = {'uk':'Виграні ігри_______________'}
lost_games  = {'uk':'Програні ігри______________'}
level_game  = {'uk':'Рівень поточної гри_______'}
round_level = {'uk':'Раунд поточного питання_'}

#______GameProcess.rulles
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

#_____________________GameProcess.next_round______________________________________________________________________________

last_round = {'uk':"Це останній раунд для цього рівня ти  маєш дати відповідь"}

not_curent_game = {'uk':'Зараз немає ні одної запущеної гри натисніть нова гра щоб розпочати'}

first_level = {'uk':"На першому рівні показана цілий кадр тому тобі непотрібні підказки"}

#_____________________GameProcess.no_correct_answer_________________________________________________________________________
answer_is_bad = {'uk':f'Нажаль це неправильна відповідь для того щоб почати нову гру натисніть на кнопку "Нова гра".\nОсь твої результати: \n' }

#_____________________GameProcess.continue_game______________________________________________________________________________
continue_if_not_current_game = {'uk':'Для початку гри натисніть "Нова гра"'}

#_____________________GameProcess.reply_to_start_message_____________________________________________________________________
returned_messages = {'uk':'Вітаю тебе мене звуть МультБот і я хочу заграти з тобою гру в котрій треба вгаувати нащви мультфільмів по шматочкам кадрів. Якщо ти теж не проти зіграти зі мною то натисни "Нова гра" натисни "Правила" якщо ти нерозумієш як грати.'}

#_____________________GameProcess.confirmation_of_correct_answer

messages_begining_one = {'uk':f'Так ти правий '}
messages_begining_thwo = {'uk':' правильна відповідь, я знаю багато цікавого про цей фільм і можу тобі розповісти. Ось наприклад ти знав що, '}
messages_end = {'uk' : 'Для продовження натисни "Далі".'}

#____________________GameProcess.your_win_messages__________________________________________________________________________________________
your_win_message_text = {'uk':'Це вражаюче. Ти переміг. Можеш рахувати себе справжнім знавцем мультфільмів'}

#___________________GameProcess.command_is_not______________________________________________________________________________________________
this_command_is_not = {'uk':'Я не знаю такої команди для зручності використовуйте вбудовану ігрову клавіатуру'}


#_________________Keyboards___________________________________________________________________________________________________________________----
empty_keys = ['   ','   ','   ','   ','   ','   ']
further_key = {'uk':['   ','Далі','   ','   ','   ','   ']}
continue_ = {'uk':['   ','Продовжити','   ','   ','   ','   ']}

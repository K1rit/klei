def load():
    ret = dict()
    try:
        f = open('setup.dat', 'r', encoding="UTF-8")
        data = f.readlines()
        f.close()
        for s in data:
            s = s.split("=")
            ret[s[0]] = s[1]
    except FileNotFoundError:
        reset_file()
        # reset_record()
        ret = load()

    return ret


def reset_record():
    try:
        f = open("setup.dat", "a", encoding="UTF-8")
        f.write("record=0\n")
        f.close()
    except:
        print("Ошибка сохранения рекорда.")


def reset_file():
    import os
    if os.path.isfile('setup.dat'):
        load_result = load()
    else:
        load_result = dict()

    if 'record' in load_result:
        rec = int(load_result['record'])
    else:
        rec = 0

    try:
        f = open("setup.dat", "w", encoding="UTF-8")
        f.write("level=0\n")
        f.write("stress=0\n")
        f.write("helper=3\n")
        f.write("score=0\n")
        f.write(f"record={rec}\n")
        f.close()
    except:
        print("Ошибка записи файла.")


def save_score_record():
    f = open("setup.dat", "w", encoding="UTF-8")
    f.write(f"level={level}\n")
    f.write(f"stress={stress}\n")
    f.write(f"helper={helper}\n")
    f.write(f"score={score}\n")
    f.write(f"record={record}\n")
    f.close()


def save():
    load_result = load()
    f = open("setup.dat", "w", encoding="UTF-8")
    f.write(f"level={level}\n")
    f.write(f"stress={stress}\n")
    f.write(f"helper={helper}\n")
    f.write(f"score={load_result['score']}")
    f.write(f"record={load_result['record']}")
    f.close()


def load_variables():
    global level, stress, helper, score, record
    load_result = load()
    level = int(load_result['level'])
    stress = int(load_result['stress'])
    helper = int(load_result['helper'])
    score = int(load_result['score'])
    record = int(load_result['record'])


WIDTH = 900
HEIGHT = 640
MARGIN = 50
VERSION = 0.4

font_button = ("Arial", 12)
font_button_game = ("Arial", 14, "bold")
font_authors_caption = ("Arial", 24, "bold")
font_authors_text = ("Arial", 11)
font_caption_text = ("Arial", 13, "bold")
font_game_over = ("Arial", 40, "bold")
font_prize = ("Arial", 50, "bold")
font_win_game = ("Arial", 50, "bold")
font_button_win_game = ("Arial", 13, "bold")
# MAIN_COLOR = "#512DA8"
MAIN_COLOR = "#512DA8"
WHITE_COLOR = "#FFFFFF"
YELLOW_COLOR = "#fff000"
TEXT_COLOR = "#FAFAFA"
# LABEL_WORDS_COLOR = "#BBDEFB"
# BACKGROUND_LABEL_COLOR = "#3f92e4"
BACKGROUND_LABEL_COLOR = "#aed257"
LABEL_TEXT_COLOR = "#1A1A1A"

LIGHT_BLUE_COLOR = "#9acbc2"

application_name = "KLEI"
hard_text = "Самый бесполезный и весёлый русско-английский\nразговорник в игровой форме*"
author_text = """Разработчик:
ученик 10Е класса Алексей Герасименко
ГКОУ РО «Санаторная школа-интернат №28»

Научный руководитель:
учитель информатики и ИКТ Виктор Геннадьевич Трофимов
ГКОУ РО «Санаторная школа-интернат №28»

Проработка словаря:
учитель английского языка Анастасия Владимировна Сумбаева
ГКОУ РО «Санаторная школа-интернат №28»

(с) 2022 Авторская методика. Все права защищены"""
note_text = """* Только для наружного применения. Перед использованием
проконсультируйтесь со своим врачом на резистентность к юмору!"""

rules_text = """
1. Игра по мотивам классических \"Виселок\": загаданную английскую
фразу необходимо угадать по буквам. Почти \"Поле чудес\", только лучше.

2. Фразы разбиты на десять категорий. Общая тематика 'русско-
английский разговорник для туриста'.

3. На принимайте написанное всерьёз, это лишь наша попытка
пошутить в суровых условиях реальности. Или нет.

4. За каждую правильную букву начисляется 1 очко, за неправильную
снимается 3 очка. На основе этой механики формируется рекорд.

5. У вас есть три подсказки. При смене категорий использованные
подсказки восстанавливаются до трёх первоначальных.

6. Уровень стресса показывает количество допущенных ошибок. Можно
ошибиться лишь десять раз. Дальше начинается такой стресс, что уже
не до игры: нервы сдали, вам уготовано поражение.

7. При смене категории уровень стресса снижается вдвое.

8. Вот так оно и работает. Желаем вам успеха!"""

letter_box = 26
letter_box_rus = 15

letter_box_height = 30

helper_text = ["Подсказок нет", "Подсказки: 1", "Подсказки: 2", "Подсказки: 3"]
level = None
stress = None
helper = None
score = None
record = None
load_variables()

# print(state[level_state])
# score = кол-во букв * 2
# sub_score = 8
# I have the computer = 32
#
# * **** *** ********
# q 32 - 8 = 24
# a
# * *a** *** *******

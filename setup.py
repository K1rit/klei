import tkinter


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
        ret = load()

    return ret


def reset_file():
    try:
        f = open("setup.dat", "w", encoding="UTF-8")
        f.write("level=0\n")
        f.write("stress=0\n")
        f.write("helper=3\n")
        f.close()
    except:
        print("Ошибка записи файла.")


def save():
    f = open("setup.dat", "w", encoding="UTF-8")
    f.write(f"level={level}\n")
    f.write(f"stress={stress}\n")
    f.write(f"helper={helper}\n")
    f.close()


def load_variables():
    global level, stress, helper
    load_result = load()
    level = int(load_result['level'])
    stress = int(load_result['stress'])
    helper = int(load_result['helper'])


WIDTH = 800
HEIGHT = 600
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
# MAIN_COLOR = "#3c3f41"
# MAIN_COLOR = "#1976D2"
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

letter_box = 26
letter_box_rus = 15

letter_box_height = 30

helper_text = ["Подсказок нет", "Подсказки: 1", "Подсказки: 2", "Подсказки: 3"]
level = None
stress = None
helper = None

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

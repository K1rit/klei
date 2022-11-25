import tkinter
def load():
    ret = dict()
    try:
        f = open('setup.dat', 'r', encoding="UTF-8")
        data = f.readlines()
        f.close()
        for s in data:
            s = s.split("=")
            if s[0] == "level":
                ret['level'] = s[1]
    except FileNotFoundError:
        f = open("setup.dat", "w", encoding="UTF-8")
        f.write("level=0")
        f.close()
        ret = load()

    return ret

def save():
    f = open("setup.dat", "w", encoding="UTF-8")
    f.write(f"level={level}")
    f.close()

WIDTH = 800
HEIGHT = 600
MARGIN = 50
VERSION = 0.1

level = load()['level']


font_button = ("Arial", 12)
font_button_game = ("Arial", 14, "bold")
font_authors_caption = ("Arial", 24, "bold")
font_authors_text = ("Arial", 11)
font_caption_text = ("Arial", 13, "bold")

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

application_name = "KLEI"
hard_text = "Создано для вас и вашего компьютера!*"
author_text = """Разработчик:
ученик 10Е класса Алексей Герасименко
ГКОУ РО «Санаторная школа-интернат №28»

Научный руководитель:
учитель информатики и ИКТ Виктор Геннадьевич Трофимов
ГКОУ РО «Санаторная школа-интернат №28»

(с) 2022 Авторская методика. Все права защищены"""
note_text = """* Только для наружного применения. Проконсультируйтесь с врачом,
разрешено ли вам смотреть на буквы латинского алфавита."""

level = 0
state = ["5", "4", "3", "неуд.", "кол", "вас выгнали из школы"]
state_lives = 0
letter_box = 26
letter_box_rus = 15

letter_box_height = 30

stress = 0




# print(state[level_state])
# score = кол-во букв * 2
# sub_score = 8
# I have the computer = 32
#
# * **** *** ********
# q 32 - 8 = 24
# a
# * *a** *** *******

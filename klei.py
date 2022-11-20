import tkinter
from tkinter import *
from tkinter import ttk
from setup import *
from services.sound import Sound
from data.json_parser import JSONParser
import time, random

# Сброс всех настроек игры
def reset_game():
    level = 0
    open_play_game()

# Окно игры
def open_play_game():

    Sound().play(Sound.OK_LETS_GO)

    # Метод, получающий нажатую кнопку
    def pressed_char(ch: str, num: int):
        print(f"Нажата кнопка: {ch} {num}")
        buttons[num].config(state="disabled")

        count_good_chars = game_data[level].put_char(ch)
        if count_good_chars > 0:
            Sound().play(Sound.GOOD_CHAR)
        else:
            Sound().play(Sound.BUTTON_PRESS)

        print(count_good_chars, game_data[level].get_proposal(), game_data[level].is_complete())

    def window_play_game_destroy():
        Sound().play(Sound.BUTTON_PRESS)
        window_play_game.destroy()

    # Для вывода
    def start_word():
        # print(game_data[level].words_en)
        # print(game_data[level].words_ru)
        # print(game_data[level].category)
        # print(game_data[level].get_proposal())

        words_lines = game_data[level].get_proposal()

        print(f"У нас {len(words_lines)} строк")

        width = len(words_lines[0]) * 26
        start_x = (WIDTH - width) // 2

        for i in range(len(words_lines[0])):
            if words_lines[0][i] != " ":
                label_word = Label(window_play_game, text=words_lines[0][i], font=("Arial", 18), background=LABEL_WORDS_COLOR)
                label_word.place(width=25, height=30, x=start_x + i * 26, y=MARGIN * 4)
            else:
                label_word = Label(window_play_game, text=words_lines[0][i], background=MAIN_COLOR, font=("Arial", 18))
                label_word.place(width=25, height=30, x=start_x + i * 26, y=MARGIN * 4)

    # Клавиатура 
    def dictionary():
        # shift_x = shift_y = 0
        # count = 0
        #
        # for i in range(ord("A"), ord("U") + 1):
        #     button = Button(window_play_game, text=chr(i), font=("Arial", 15, "bold"))
        #     button.place(x =  550- 100*2 + shift_x, y = 100*4.5 - shift_y)
        #     shift_x += 70
        #     count += 1
        #
        #     if count == 7:
        #         shift_x = count = 0
        #         shift_y -= 50
        keyboard = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        num_element = 0
        for i in range(len(keyboard)):

            # Эта шняга нужна чтобы блоки клавиш располагались по горизонтальному центра окна
            width_key = 2
            height_key = 1
            all_key_width = len(keyboard[i]) * width_key * 19.5
            start_x = (WIDTH - all_key_width) // 2

            for j in range(len(keyboard[i])):
                buttons.append(Button(window_play_game, command=lambda ch=keyboard[i][j], num=num_element: pressed_char(ch, num),
                                      text=keyboard[i][j], font=font_button_game,
                                      width=width_key, height=height_key))
                buttons[-1].place(x=start_x + j * (width_key * 20), y=HEIGHT // 1.6 + i * 50)
                num_element += 1

    window_play_game = Toplevel()
    window_play_game.grab_set()

    # Окно по центру, рассчитывается от размеров экрана
    window_play_game_x = window.winfo_screenwidth() // 2 - WIDTH // 2
    window_play_game_y = window.winfo_screenheight() // 2 - HEIGHT // 2
    window_play_game.geometry(f"{WIDTH}x{HEIGHT}+{window_play_game_x}+{window_play_game_y}")
    window_play_game["bg"] = MAIN_COLOR
    window_play_game.overrideredirect(1)


    buttons = []
    dictionary()
    start_word()

    # Метка - название категории
    label_category = Label(window_play_game, text=game_data[level].category, font=font_caption_text, background=MAIN_COLOR, foreground=LABEL_WORDS_COLOR)
    label_width = label_category.winfo_reqwidth()
    label_category_x = (WIDTH - label_width) // 2
    label_category.place(x=label_category_x, rely=0.91)

    button_exit = Button(window_play_game, text="Сбежать", font=font_button, command=window_play_game_destroy, width=10, pady=3)
    button_exit.place(relx=0.85, rely=0.9)
    button_question = Button(window_play_game, text="?", font=font_button, command = None, width=7, pady=3)
    button_question.place(relx=0.03, rely=0.9)

# Окно авторов
def open_authors():

    def window_authors_destroy():
        Sound().play(Sound.BUTTON_PRESS)
        window_authors.destroy()

    Sound().play(Sound.BUTTON_PRESS)
    window_authors = Toplevel()
    window_authors.grab_set()

    window_authors_x = int(window.winfo_screenwidth() - WIDTH * 0.6) // 2
    window_authors_y = int((window.winfo_screenheight() - HEIGHT * 0.7) // 2)
    window_authors.geometry(f"{int(WIDTH * 0.6)}x{int(HEIGHT * 0.7)}+{window_authors_x}+{window_authors_y}")
    window_authors["bg"] = MAIN_COLOR
    window_authors.overrideredirect(1)

    button_exit = Button(window_authors, text="ОК", font=font_button, command=window_authors_destroy, width=10)
    button_exit.place(relx=0.5, rely=0.90, anchor=CENTER)

    # KLEI
    label_app_name = ttk.Label(window_authors, text=application_name, font=font_authors_caption, background=MAIN_COLOR,
                              foreground=TEXT_COLOR)
    label_app_name.place(relx=0.03, rely=0.04)

    # Слоган, типа что-то того
    label_hard_text = ttk.Label(window_authors, text=hard_text, font=("Arial", 13, "bold"), background=MAIN_COLOR,
                              foreground=TEXT_COLOR)
    label_hard_text.place(relx=0.03, rely=0.15)

    # Текст об авторах
    label_text_authors = ttk.Label(window_authors, text=author_text, font=font_authors_text, background=MAIN_COLOR,
                              foreground=TEXT_COLOR)
    label_text_authors.place(relx=0.03, rely=0.27)

    # Сноска
    label_hard_text = ttk.Label(window_authors, text=note_text, font=("Arial", 9, "bold"), background=MAIN_COLOR,
                              foreground=TEXT_COLOR)
    label_hard_text.place(relx=0.03, rely=0.71)

def quit_game():
    window.quit()

window = Tk()
window.title("Klei")

# Окно по центру, рассчитывается от размеров экрана
POS_X = window.winfo_screenwidth() // 2 - WIDTH // 4
POS_Y = window.winfo_screenheight() // 2 - HEIGHT // 6
window.geometry(f"{WIDTH // 2}x{int(HEIGHT // 2.5)}+{POS_X}+{POS_Y}")

window.resizable(False, False)
window.overrideredirect(1)

# Фоновый цвет в HEX
window["bg"] = MAIN_COLOR

label_version = ttk.Label(text=f"Версия {VERSION}", anchor="sw", background=MAIN_COLOR, foreground=TEXT_COLOR).place(relx=0.03, rely=0.87)

button_continue = Button(window, text="Продолжить", font=font_button, command = open_play_game, width=30, pady=3)
button_continue.place(relx=0.5, rely=0.20, anchor=CENTER)
button_game = Button(window, text="Начать заново", font=font_button, command = reset_game, width=30, pady=3)
button_game.place(relx=0.5, rely=0.38, anchor=CENTER)
button_exit = Button(window, text="Выход", font=font_button, command = quit_game, width=30, pady=3)
button_exit.place(relx=0.5, rely=0.56, anchor=CENTER)
button_authors = Button(window, text="Авторы", font=font_button, command = open_authors, width=30, pady=3)
button_authors.place(relx=0.5, rely=0.74, anchor=CENTER)

if level == 0:
    button_continue["state"] = tkinter.DISABLED

game_data = JSONParser().get_list("data/database.dat", False)

window.mainloop()

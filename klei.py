import tkinter
from tkinter import *
from tkinter import ttk
from setup import *
import setup
from services.sound import Sound
from data.json_parser import JSONParser
import time, random


# Сброс всех настроек игры из ГЛАВНОГО ОКНА
def reset_game():
    setup.level = 0
    open_play_game()


# вкл кнопки
def turn_on():
    pass


# выкл кнопки
def deactivate_button():
    global button_escape, button_help
    button_escape.destroy()
    button_help.destroy()



# Game over
def stop_game():
    global label_game_over

    for i in range(len(buttons)):
        buttons[i].destroy()

    for i in range(len(word_labels)):
        word_labels[i].destroy()
    deactivate_button()
    


# Окно игры
def open_play_game():
    Sound().play(Sound.OK_LETS_GO)

    # Следующий уровень при нажатии на кнопку Хочу ещё!
    def next_level():
        global button_next, word_russian, word_labels
        setup.level += 1
        deactivate_button()
        button_next.destroy()
        for lbl in word_labels:
            lbl.destroy()

        for lbl in word_russian:
            lbl.destroy()
        reset_level()

    def reset_level():
        global buttons, word_labels, word_russian, height_string
        global button_escape, button_help, label_stress, label_category, label_stress_image
        global label_category, stress, button_reset

        word_labels = []
        buttons = []
        word_russian = []
        height_string = 0
        label_stress_image = None
        label_stress = None
        label_category = None

        add_keyboard()
        update_stress()
        start_word()

        # Стресс
        if label_stress is None:
            label_stress = tkinter.Label(window_play_game, text="Стресс:", font=font_caption_text,
                                         background=MAIN_COLOR, foreground=TEXT_COLOR)
            label_stress.place(x=WIDTH - 350, y=17)

        # Метка - название категории
        if label_category is None:
            label_category = Label(window_play_game, text=game_data[setup.level].category, font=font_caption_text,
                                   background=MAIN_COLOR, foreground=TEXT_COLOR)
            label_width = label_category.winfo_reqwidth()
            label_category_x = (WIDTH - label_width) // 2
            label_category.place(x=label_category_x, rely=0.91)

        #    button_exit = Button(window_play_game, text="Сбежать", font=font_button, command=window_play_game_destroy, width=10, pady=3)
        #    button_exit.place(relx=0.85, rely=0.9)

        button_escape = Button(window_play_game, text="Сбежать", font=font_button, command=window_play_game_destroy,
                               width=12, pady=3)
        button_escape.place(relx=0.835, rely=0.9)
        button_help = Button(window_play_game, text=helper_text[helper], font=font_button, width=12, pady=3)
        button_help["command"] = lambda btn=button_help: help_me(btn)
        button_help.place(relx=0.02, rely=0.9)

    #    button_question = Button(window_play_game, text="?", font=font_button, command = None, width=7, pady=3)
    #    button_question.place(relx=0.03, rely=0.9)

    # Подсказка
    def help_me(btn):
        global helper
        helper -= 1
        if helper < 0:
            helper = 0
        btn["text"] = helper_text[helper]

        ch = game_data[setup.level].get_help_char()
        if helper == 0:
            btn["state"] = DISABLED


        # print(f"Буква: {ch}")
        # ABCDEFGH
        #     E
        # 01234567

        num = -1
        for i in range(len(buttons)):
            if num == -1 and buttons[i]["text"] == ch:
                num = i

        pressed_char(ch, num)


    # Функция когда чел соберёт всё
    def win_round():
        global button_next

        Sound().play(Sound.WIN_ROUND)
        for i in range(len(buttons)):
            buttons[i].destroy()

        deactivate_button()

        word = game_data[setup.level].get_translate_ru()

        height_string_rus = len(word) * letter_box_height
        start_y = (HEIGHT - height_string) // 2 + height_string

        code_a = ord("А")
        code_z = ord("Я")

        for i in range(len(word)):
            width_string = len(word[i]) * letter_box_rus
            start_x = (WIDTH - width_string) // 2

            print(word[i])

            word_russian.append(Label(window_play_game, text=word[i], font=("Arial", 16), foreground=YELLOW_COLOR,
                                      background=MAIN_COLOR))

            word_russian[-1].place(x=start_x, y=start_y + i * (letter_box_height - 2),
                                   width=width_string, height=30)

        button_next = Button(window_play_game, text="Хочу ещё!", command=next_level, font=font_button)
        button_next.place(width=200, x=(WIDTH - 200) // 2, y=(HEIGHT - 6) // 2 + 150)


    def update_stress():
        global label_stress_image, image_stress, image_smile

        if label_stress_image is None:
            label_stress_image = []

            for i in range(setup.stress):
                label_stress_image.append(tkinter.Label(window_play_game, image=image_stress, background=MAIN_COLOR))
                label_stress_image[-1].place(x=WIDTH - 276 + i * 26, y=15)

            for i in range(10 - setup.stress):
                label_stress_image.append(tkinter.Label(window_play_game, image=image_smile, background=MAIN_COLOR))
                label_stress_image[-1].place(x=WIDTH - 276 + setup.stress * 26 + i * 26, y=15)

        else:
            for i in range(setup.stress):
                label_stress_image[i]["image"] = image_stress

            for i in range(10 - setup.stress):
                label_stress_image[setup.stress + i]["image"] = image_smile

    # Метод, получающий нажатую кнопку
    def pressed_char(ch: str, num: int):
        global stress, buttons, word_labels, word_russian

        print(f"Нажата кнопка: {ch} {num}")

        # Получит, сколько символов УГАДАНО
        count_good_chars = game_data[setup.level].put_char(ch)

        """
        # ==================================================================================================================
        # Список с переводом
        """

        print(f"Список для вывода перевода: {game_data[setup.level].get_translate_ru()}")

        """
        # ==================================================================================================================
        """

        buttons[num].config(state="disabled")

        if count_good_chars > 0:
            buttons[num]['text'] = ":)"
        else:
            buttons[num]['text'] = ":|"
            setup.stress += 1

            if setup.stress > 10:
                setup.stress = 10
                stop_game()
                button_reset = Button(window_play_game, text="Попробовать еще раз", font=font_button, width=20, pady=7)
                button_reset["command"] = lambda btn=button_reset: reset_game(btn)
                button_reset.place(width=200, x=(WIDTH - 200) // 2, y=(HEIGHT - 6) // 2 + 70)

                label_reset = Label(window_play_game, text="dfjsgfsgf", background=MAIN_COLOR)
                label_reset.place(width=200, x=(WIDTH - 200) // 2, y=(HEIGHT - 6) // 2 + 150)

            
            update_stress()

        # Если собрана вся фраза, то...
        if game_data[setup.level].is_complete():
            win_round()

        if count_good_chars > 0:
            Sound().play(Sound.GOOD_CHAR)
        else:
            Sound().play(Sound.BUTTON_PRESS)
        # Если пользователь угадал БОЛЬШЕ 0 букв,
        # то удаляем все Label и заново их перерисовываем
        if count_good_chars > 0:
            for i in range(len(word_labels)):
                word_labels[i].destroy()
            word_labels.clear()
            start_word()

        print(count_good_chars, game_data[setup.level].get_proposal(), game_data[setup.level].is_complete())

    def window_play_game_destroy():
        Sound().play(Sound.BUTTON_PRESS)
        window_play_game.destroy()

    # Для вывода
    def start_word():
        global height_string
        # print(game_data[setup.level].words_en)
        # print(game_data[setup.level].words_ru)
        # print(game_data[setup.level].category)
        # print(game_data[setup.level].get_proposal())

        # ширина строки в пикселях
        words_lines = game_data[setup.level].get_proposal()

        print(f"У нас {len(words_lines)} строк")
        print(f"У нас {words_lines}")

        height_string = len(words_lines) * letter_box_height
        start_y = (HEIGHT - height_string) // 2 - 50

        code_a = ord("A")
        code_z = ord("Z")

        for i in range(len(words_lines)):

            count_chars = len(words_lines[i])
            if words_lines[i][-1] == " ":
                count_chars -= 1

            width_string = count_chars * letter_box
            start_x = (WIDTH - width_string) // 2

            for j in range(len(words_lines[i])):
                ch = words_lines[i][j]
                # if (ord(ch.upper()) >= code_a or ch == "_") and (ord(ch.upper()) <= code_z or ch == "_"):
                if ch == "_":
                    word_labels.append(Label(window_play_game, text=ch, font=("Arial", 18), foreground=LABEL_TEXT_COLOR,
                                             background=BACKGROUND_LABEL_COLOR))
                    word_labels[-1].place(x=start_x + j * letter_box, y=start_y + i * (letter_box_height + 4), width=25,
                                          height=30)
                elif ord(ch.upper()) >= code_a and ord(ch.upper()) <= code_z:
                    word_labels.append(
                        Label(window_play_game, text=ch, font=("Arial", 18), foreground=WHITE_COLOR,
                              background=MAIN_COLOR))
                    word_labels[-1].place(x=start_x + j * letter_box, y=start_y + i * (letter_box_height + 4),
                                          width=25, height=30)
                elif ch == " ":
                    word_labels.append(Label(window_play_game, text=ch, font=("Arial", 18), background=MAIN_COLOR))
                    word_labels[-1].place(x=start_x + j * letter_box, y=start_y + i * (letter_box_height + 4), width=25,
                                          height=30)
                else:
                    word_labels.append(Label(window_play_game, text=ch, font=("Arial", 18), foreground=WHITE_COLOR,
                                             background=MAIN_COLOR))
                    word_labels[-1].place(x=start_x + j * letter_box, y=start_y + i * (letter_box_height + 4), width=25,
                                          height=30)

    # Клавиатура
    def add_keyboard():
        global buttons

        keyboard = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
        num_element = 0
        buttons = []

        for i in range(len(keyboard)):
            # Эта шняга нужна чтобы блоки клавиш располагались по горизонтальному центра окна
            width_key = 2
            height_key = 1
            all_key_width = len(keyboard[i]) * width_key * 19.5
            start_x = (WIDTH - all_key_width) // 2

            for j in range(len(keyboard[i])):
                buttons.append(
                    Button(window_play_game, command=lambda ch=keyboard[i][j], num=num_element: pressed_char(ch, num),
                           text=keyboard[i][j], font=font_button_game,
                           width=width_key, height=height_key))
                buttons[-1].place(x=start_x + j * (width_key * 20), y=HEIGHT // 1.6 + i * 50)
                num_element += 1

    global button_help, button_escape

    window_play_game = Toplevel()
    window_play_game.grab_set()

    # Окно по центру, рассчитывается от размеров экрана
    window_play_game_x = window.winfo_screenwidth() // 2 - WIDTH // 2
    window_play_game_y = window.winfo_screenheight() // 2 - HEIGHT // 2
    window_play_game.geometry(f"{WIDTH}x{HEIGHT}+{window_play_game_x}+{window_play_game_y}")
    window_play_game["bg"] = MAIN_COLOR
    window_play_game.overrideredirect(1)

    reset_level()

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


# =====================================================================================================================
# ОТСЮДА НАЧИНАЕТСЯ ГЛАВНЫЙ КОД, ЫЫЫЫЫ
# =====================================================================================================================

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

label_version = ttk.Label(text=f"Версия {VERSION}", anchor="sw", background=MAIN_COLOR, foreground=TEXT_COLOR)
label_version.place(relx=0.03, rely=0.87)

button_continue = Button(window, text="Продолжить", font=font_button, command=open_play_game, width=30, pady=3)
button_continue.place(relx=0.5, rely=0.20, anchor=CENTER)

button_game = Button(window, text="Начать заново", font=font_button, command=reset_game, width=30, pady=3)
button_game.place(relx=0.5, rely=0.38, anchor=CENTER)

button_exit = Button(window, text="Выход", font=font_button, command=quit_game, width=30, pady=3)
button_exit.place(relx=0.5, rely=0.56, anchor=CENTER)

button_authors = Button(window, text="Авторы", font=font_button, command=open_authors, width=30, pady=3)
button_authors.place(relx=0.5, rely=0.74, anchor=CENTER)

if setup.level == 0:
    button_continue["state"] = tkinter.DISABLED

game_data = JSONParser().get_list("data/database.dat", False)
# game_data = JSONParser().get_list("data/database.dat", True)

image_stress = tkinter.PhotoImage(file='png/stress.png')
image_smile = tkinter.PhotoImage(file='png/smile.png')

label_stress_image = None
button_help = None
button_escape = None
button_reset = None
label_stress = None
label_category = None

buttons = None
button_next = None

window.mainloop()

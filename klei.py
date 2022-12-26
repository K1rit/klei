import tkinter
from tkinter import *
from tkinter import ttk
from setup import *
import setup
from services.sound import Sound
from data.json_parser import JSONParser


def update_key_on_main_window():
    global button_continue
    if setup.level == 0:
        button_continue["state"] = DISABLED
    else:
        button_continue["state"] = NORMAL


# Создаёт игровое окно
def create_window(new_game=False):
    global window_play_game

    Sound().play(Sound.OK_LETS_GO)

    window_play_game = Toplevel()
    window_play_game.grab_set()

    setup.load_variables()

    # Окно по центру, рассчитывается от размеров экрана
    window_play_game_x = window.winfo_screenwidth() // 2 - WIDTH // 2
    window_play_game_y = window.winfo_screenheight() // 2 - HEIGHT // 2
    window_play_game.geometry(f"{WIDTH}x{HEIGHT}+{window_play_game_x}+{window_play_game_y}")
    window_play_game["bg"] = MAIN_COLOR
    window_play_game.overrideredirect(0)

    if new_game:
        reset_game()
    else:
        open_play_game()


# Сброс всех настроек игры из ГЛАВНОГО ОКНА
def reset_game(btn_repeat=None, btn_main_menu=None, lbl_game_over=None):
    setup.reset_file()
    # setup.reset_record()
    setup.load_variables()

    for task in game_data:
        task.reset_data()

    if btn_repeat is not None:
        btn_repeat.destroy()

    if btn_main_menu is not None:
        btn_main_menu.destroy()

    if lbl_game_over is not None:
        lbl_game_over.destroy()

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

    Sound().play(Sound.LOSE_GAME)

    deactivate_button()


# Окно игры
def open_play_game():
    global window_play_game

    # Анимация выезда категории
    def moving_category(label_category, label_category_x, relY, current_x=WIDTH):
        # Если окно открыто и элемент присутствует
        if label_category.winfo_exists():
            label_category.place(x=current_x, rely=relY)
            if current_x > label_category_x:
                current_x -= 2
                window.after(10, lambda lc=label_category, lcx=label_category_x, rly=relY, cx=current_x: moving_category(lc, lcx, rly, cx))

    # ===========================================================
    # Когда игра закончена и человек победил
    # ===========================================================
    def win_game():
        def win_game_destroy():
            window.focus_set()
            setup.reset_file()
            setup.load_variables()
            update_key_on_main_window()
            window_play_game.destroy()

        Sound().play(Sound.WIN_GAME)

        label_category.destroy()

        label_sas = Label(window_play_game, text="Вы прошли все испытания с честью, просто супер", font=font_caption_text,
                          background=MAIN_COLOR,
                          foreground=LIGHT_BLUE_COLOR)
        label_sas.place(width=450, x=(WIDTH - 450) // 2, y=HEIGHT * 0.15)

        label_win_game = Label(window_play_game, text="ПОБЕДА!", font=font_win_game, background=MAIN_COLOR,
                               foreground=TEXT_COLOR)
        label_win_game.place(width=450, x=(WIDTH - 450) // 2, y=(HEIGHT - 6) // 2 - 180)

        button_win_game = Button(window_play_game, command=win_game_destroy, text="Выйти в главное меню",
                                 font=font_button_win_game)
        button_win_game.place(width=240, x=(WIDTH - 240) // 2, y=(HEIGHT - 6) // 2 + 180)

        image_cat = Label(window_play_game, image=image_cat_win_boc, background=MAIN_COLOR)
        image_cat.place(width=240, x=(WIDTH - 240) // 2, y=(HEIGHT - 6) // 2 - 100)

    # ===========================================================

    # Следующий уровень при нажатии на кнопку Хочу ещё!
    def next_level(label_win_round=None):
        global button_next, word_russian, word_labels

        deactivate_button()
        button_next.destroy()
        for lbl in word_labels:
            lbl.destroy()

        for lbl in word_russian:
            lbl.destroy()

        if label_win_round is not None:
            label_win_round.destroy()

        setup.save_score_record()

        setup.level += 1
        if setup.level == len(game_data):
            win_game()
            return False

        if setup.level > 0:
            if game_data[setup.level].category != game_data[setup.level - 1].category:
                setup.helper = 3
                setup.stress //= 2

        reset_level()

    def reset_level():
        global buttons, word_labels, word_russian, height_string, label_level, label_score_rec
        global button_escape, button_help, label_score, label_stress, label_category, label_stress_image
        global stress, button_reset, old_category
        global button_help, button_escape

        if buttons is not None:
            for i in range(len(buttons) - 1, -1, -1):
                del buttons[i]

        buttons = []

        if word_russian is not None:
            for i in range(len(word_russian) - 1, -1, -1):
                del word_russian[i]
        word_russian = []

        if word_labels is not None:
            for i in range(len(word_labels) - 1, -1, -1):
                del word_labels[i]
        word_labels = []

        height_string = 0

        if label_stress_image is not None:
            for i in range(len(label_stress_image) - 1, -1, -1):
                del label_stress_image[i]
        label_stress_image = None

        if label_stress is not None:
            label_stress.destroy()
        label_stress = None

        if label_category is not None:
            label_category.destroy()
        label_category = None

        if label_level is not None:
            label_level.destroy()
        label_level = None

        if label_score is not None:
            label_score.destroy()
        label_score = None

        if label_score_rec is not None:
            label_score_rec.destroy()
        label_score_rec = None

        # Нужно сбросить всё угаданное, то есть "закрыть" открытые ранее буквы
        game_data[setup.level].reset_data()

        add_keyboard()
        update_stress()
        start_word()

        # Стресс
        if label_stress is None:
            label_stress = tkinter.Label(window_play_game, text="Стресс:", font=font_caption_text,
                                         background=MAIN_COLOR, foreground=TEXT_COLOR)
            label_stress.place(x=WIDTH - 350, y=17)

        # Уровень
        if label_level is None:
            label_level = tkinter.Label(window_play_game, text=f"Уровень: {setup.level + 1}", font=font_caption_text,
                                        background=MAIN_COLOR, foreground=TEXT_COLOR)
            label_level.place(relx=0.5, rely=0.905, anchor=CENTER)

        # Очки
        if label_score is None:
            label_score = tkinter.Label(window_play_game, text=f"Очки: {setup.score}",
                                        font=font_caption_text,
                                        background=MAIN_COLOR, foreground=TEXT_COLOR)
            label_score.place(x=48, y=40)

        # Рекорд
        if label_score_rec is None:
            label_score_rec = tkinter.Label(window_play_game, text=f"Рекорд: {setup.record}",
                                 font=font_caption_text,
                                 background=MAIN_COLOR, foreground=TEXT_COLOR)
            label_score_rec.place(x=30, y=15)

        # Метка - название категории
        if label_category is None:
            label_category = Label(window_play_game, text=game_data[setup.level].category, font=font_caption_text,
                                   background=MAIN_COLOR, foreground=TEXT_COLOR)
            label_width = label_category.winfo_reqwidth()
            label_category_x = (WIDTH - label_width) // 2

            # Если НОВАЯ категория, то звук гонга, иначе звук обыкновенного старта
            if old_category != game_data[setup.level].category:
                Sound().play(Sound.GONG)
                moving_category(label_category, label_category_x, 0.925)
                old_category = game_data[setup.level].category
            else:
                Sound().play(Sound.OK_LETS_GO)
                label_category.place(x=label_category_x, rely=0.925)

        #    button_exit = Button(window_play_game, text="Сбежать", font=font_button, command=window_play_game_destroy, width=10, pady=3)
        #    button_exit.place(relx=0.85, rely=0.9)

        button_escape = Button(window_play_game, text="Сбежать", font=font_button, command=window_play_game_destroy,
                               width=12, pady=3)
        button_escape.place(relx=0.835, rely=0.9)

        button_help = Button(window_play_game, text=helper_text[setup.helper], font=font_button, width=12, pady=3)
        button_help["command"] = lambda btn=button_help: help_me(btn)
        button_help.place(relx=0.02, rely=0.9)

        if setup.helper == 0:
            button_help["state"] = DISABLED

    #    button_question = Button(window_play_game, text="?", font=font_button, command = None, width=7, pady=3)
    #    button_question.place(relx=0.03, rely=0.9)

    # Подсказка
    def help_me(btn):

        # УДАЛИТЬ
        setup.helper -= 1

        if setup.helper < 0:
            setup.helper = 0

        btn["text"] = helper_text[setup.helper]

        ch = game_data[setup.level].get_help_char()
        if setup.helper == 0:
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

        word_prize = game_data[setup.level].get_prize_str()

        label_win = Label(window_play_game, text=word_prize, background=MAIN_COLOR, font=font_prize,
                          fg=LIGHT_BLUE_COLOR)
        label_win.place(width=450, x=(WIDTH - 450) // 2, y=(HEIGHT - 6) // 2 - 180)

        height_string_rus = len(word) * letter_box_height
        start_y = (HEIGHT - height_string) // 2 + height_string

        code_a = ord("А")
        code_z = ord("Я")

        for i in range(len(word)):
            width_string = len(word[i]) * letter_box_rus
            start_x = (WIDTH - width_string) // 2

            # print(word[i])

            word_russian.append(Label(window_play_game, text=word[i], font=("Arial", 16), foreground=YELLOW_COLOR,
                                      background=MAIN_COLOR))

            word_russian[-1].place(x=start_x, y=start_y + i * (letter_box_height - 2),
                                   width=width_string, height=30)

        msg = "Давайте следующую!"
        if setup.level + 1 == len(game_data):
            msg = "Насладиться победой!"

        button_next = Button(window_play_game, text=msg, font=font_button)
        button_next["command"] = lambda qwe=label_win: next_level(qwe)

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

        # print(f"Нажата кнопка: {ch} {num}")

        # Получит, сколько символов УГАДАНО
        count_good_chars = game_data[setup.level].put_char(ch)

        """
        # ==================================================================================================================
        # Список с переводом
        """

        # print(f"Список для вывода перевода: {game_data[setup.level].get_translate_ru()}")

        """
        # ==================================================================================================================
        """

        buttons[num].config(state="disabled")

        # Если человек угадал хотя бы одну букву...
        if count_good_chars > 0:
            buttons[num]['text'] = ":)"
            setup.score += 1
            label_score["text"] = f"Очки: {setup.score}"
            if setup.score >= setup.record:
                setup.record = setup.score
                label_score_rec["text"] = f"Рекорд: {setup.record}"


        else:
            setup.score -= 3
            if setup.score < 0:
                setup.score = 0

            label_score["text"] = f"Очки: {setup.score}"
            buttons[num]['text'] = ":|"
            setup.stress += 1

            Sound().play(Sound.STRESS)

            if setup.stress > 10:
                setup.stress = 10
                stop_game()

                """
                
                СЮДА НАДО ВЫВЕСТИ ПОЛНУЮ ФРАЗУ, ЧТОБЫ ЧЕЛОВЕК ОЗНАКОМИЛСЯ С НЕЙ
                ВОЗМОЖНО, В STOP_GAME НЕ НУЖНО СТИРАТЬ УГАДАННЫЕ БУКВЫ, А ОТКРЫТЬ ИХ ВСЕ
                
                """
                label_game_over = Label(window_play_game, text="ГАМЕ ОВЕР", font=font_game_over, background=MAIN_COLOR,
                                        fg=LIGHT_BLUE_COLOR)
                label_game_over.place(width=400, x=(WIDTH - 400) // 2, y=(HEIGHT - 20) // 2 - 100)

                # Кнопка ВЫХОД В ГЛАВНОЕ МЕНЮ
                button_exit_to_main_menu = Button(window_play_game, text="Главное меню", font=font_button)
                button_exit_to_main_menu["command"] = lambda reset_data=True: window_play_game_destroy(reset_data)
                button_exit_to_main_menu.place(width=200, x=(WIDTH - 200) // 2, y=(HEIGHT - 6) // 2 + 110)

                # Кнопка ПОПРОБОВАТЬ ЕЩЁ РАЗ
                button_repeat_game = Button(window_play_game, text="Попробовать еще раз", font=font_button)
                button_repeat_game["command"] = lambda btn1=button_repeat_game, \
                                                       btn2=button_exit_to_main_menu, \
                                                       lbl1=label_game_over: reset_game(btn1, btn2, lbl1)
                # button_reset["command"] = reset_game
                button_repeat_game.place(width=200, x=(WIDTH - 200) // 2, y=(HEIGHT - 6) // 2 + 70)


                # label_reset = Label(window_play_game, text="dfjsgfsgf", background=MAIN_COLOR)
                # label_reset.place(width=200, x=(WIDTH - 200) // 2, y=(HEIGHT - 6) // 2 + 150)

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

        # print(count_good_chars, game_data[setup.level].get_proposal(), game_data[setup.level].is_complete())

    def window_play_game_destroy(reset_data=False):
        Sound().play(Sound.BUTTON_PRESS)
        if reset_data:
            setup.reset_file()
            setup.load_variables()
        elif setup.level > 0:
            setup.save()
        window.focus_set()
        update_key_on_main_window()
        window_play_game.destroy()

    # Для вывода
    def start_word():
        global height_string
        # print(game_data[setup.level].words_en)
        # print(game_data[setup.level].words_ru)
        # print(game_data[setup.level].category)
        # print(game_data[setup.level].get_proposal())

        # Получит английскую строку
        words_lines = game_data[setup.level].get_proposal()

        # print(f"У нас {len(words_lines)} строк")
        # print(f"У нас {words_lines}")

        height_string = len(words_lines) * letter_box_height
        start_y = (HEIGHT - height_string) // 2 - 50

        code_a = ord("A")
        code_z = ord("Z")

        # Изменить для русского алфавита
        # code_a = ord("А")
        # code_z = ord("Я")

        for i in range(len(words_lines)):

            count_chars = len(words_lines[i])
            if words_lines[i][-1] == " ":
                count_chars -= 1

            width_string = count_chars * letter_box
            start_x = (WIDTH - width_string) // 2

            for j in range(len(words_lines[i])):
                ch = words_lines[i][j]
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

        # Изменить для русского алфавита
        # keyboard = ["ЙЦУКЕНГШЩЗХЪ", "ФЫВАПРОЛДЖЭ", "ЯЧСМИТЬБЮ"]

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

    # TODO DELETE THIS SHIT
    def press_key(event):
        letter = event.char.upper()
        if letter in qwerty:
            pressed_char(letter, qwerty.index(letter))

    qwerty = "QWERTYUIOPASDFGHJKLZXCVBNM"

    # Изменить для русского алфавита
    # qwerty = "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"

    window.bind("<Key>", press_key)

    reset_level()

# Правила игры
def open_rules():
    def window_rules_destroy():
        Sound().play(Sound.BUTTON_PRESS)
        window_rules.destroy()

    window_rules = Toplevel()
    window_rules.grab_set()

    window_root_x = int(window.winfo_screenwidth() - WIDTH * 0.6) // 2
    window_root_y = int((window.winfo_screenheight() - HEIGHT * 0.7) // 2)
    window_rules.geometry(f"{int(WIDTH * 0.6)}x{int(HEIGHT * 0.9)}+{window_root_x}+{window_root_y}")
    window_rules["bg"] = MAIN_COLOR
    window_rules.overrideredirect(0)

    butoon_exit_rules = Button(window_rules, text="А я алмаз, сыграю сейчас", font=font_button, command=window_rules_destroy)
    butoon_exit_rules.place(relx=0.5, rely=0.93, width=300, anchor=CENTER)

    label_rules_caption = Label(window_rules, text="ПРАВИЛА ИГРЫ:", font=font_authors_caption,
                            justify=LEFT, background=MAIN_COLOR, foreground=YELLOW_COLOR)
    label_rules_caption.place(relx=0.04, rely=0.05)

    label_rules_text = Label(window_rules, text=setup.rules_text, font=font_authors_text,
                            justify=LEFT, background=MAIN_COLOR, foreground=TEXT_COLOR)
    label_rules_text.place(relx=0.04, rely=0.15)

# Окно авторов
def open_authors():
    def window_authors_destroy():
        Sound().play(Sound.BUTTON_PRESS)
        window_authors.destroy()

    Sound().play(Sound.BUTTON_PRESS)
    window_authors = Toplevel()
    window_authors.grab_set()

    window_authors_x = int(window.winfo_screenwidth() - WIDTH * 0.55) // 2
    window_authors_y = int((window.winfo_screenheight() - HEIGHT * 0.8) // 2)
    window_authors.geometry(f"{int(WIDTH * 0.55)}x{int(HEIGHT * 0.8)}+{window_authors_x}+{window_authors_y}")
    window_authors["bg"] = MAIN_COLOR
    window_authors.overrideredirect(0)

    button_exit = Button(window_authors, text="ОК", font=font_button, command=window_authors_destroy, width=10)
    button_exit.place(relx=0.5, rely=0.90, anchor=CENTER)

    # KLEI
    label_app_name = ttk.Label(window_authors, text=application_name, font=font_authors_caption, background=MAIN_COLOR,
                               foreground=YELLOW_COLOR)
    label_app_name.place(relx=0.05, rely=0.04)

    # Слоган, типа что-то того
    label_hard_text = ttk.Label(window_authors, text=hard_text, font=("Arial", 13, "bold"), background=MAIN_COLOR,
                                foreground=LIGHT_BLUE_COLOR)
    label_hard_text.place(relx=0.05, rely=0.15)

    # Текст об авторах
    label_text_authors = ttk.Label(window_authors, text=author_text, font=font_authors_text, background=MAIN_COLOR,
                                   foreground=TEXT_COLOR)
    label_text_authors.place(relx=0.05, rely=0.27)

    # Сноска
    label_hard_text = ttk.Label(window_authors, text=note_text, font=("Arial", 9, "bold"), background=MAIN_COLOR,
                                foreground=LIGHT_BLUE_COLOR)
    label_hard_text.place(relx=0.05, rely=0.75)


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
window.geometry(f"{int(WIDTH * 0.45)}x{int(HEIGHT * 0.45)}+{POS_X}+{POS_Y}")

window.resizable(False, False)
window.overrideredirect(0)

# Фоновый цвет в HEX
window["bg"] = MAIN_COLOR

image_stress = tkinter.PhotoImage(file='png/stress.png')
image_smile = tkinter.PhotoImage(file='png/smile.png')
image_cat_win_boc = tkinter.PhotoImage(file='png/bokser.png')

label_version = ttk.Label(text=f"Версия {VERSION}", anchor="sw", background=MAIN_COLOR, foreground=TEXT_COLOR)
label_version.place(relx=0.03, rely=0.9)

label_main_record = ttk.Label(text=f"Рекорд: {setup.record}", anchor="sw", background=MAIN_COLOR, foreground=TEXT_COLOR)
label_main_record.place(relx=0.8, rely=0.9)

button_continue = Button(window, text="Продолжить", font=font_button, command=create_window, width=30, pady=3)
button_continue.place(relx=0.5, rely=0.19, anchor=CENTER)

button_game = Button(window, text="Начать заново", font=font_button,
                     command=lambda new_game=True: create_window(new_game), width=30, pady=3)
button_game.place(relx=0.5, rely=0.34, anchor=CENTER)

button_root = Button(window, text="Правила", font=font_button, command=open_rules, width=30, pady=3)
button_root.place(relx=0.5, rely=0.49, anchor=CENTER)

button_exit = Button(window, text="Выход", font=font_button, command=quit_game, width=30, pady=3)
button_exit.place(relx=0.5, rely=0.64, anchor=CENTER)

button_authors = Button(window, text="Авторы", font=font_button, command=open_authors, width=30, pady=3)
button_authors.place(relx=0.5, rely=0.79, anchor=CENTER)

game_data = JSONParser().get_list(f"data/{setup.filename}", False)

label_stress_image = None
button_help = None
button_escape = None
button_reset = None
label_stress = None
label_score = None
label_score_rec = None
label_category = None
window_play_game = None
label_level = None
height_string = None
word_labels = None
word_russian = None
old_category = ""  # Старая категория, нужна для анимации смены категорий

buttons = None
button_next = None

update_key_on_main_window()

window.mainloop()

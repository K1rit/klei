# pip install winsound.PlaySound
import pip
from threading import Thread
from multiprocessing import Process
import setup

# Здесь проверка на наличие библиотеки для воспроизведения звука
# Если библиотеки нет, Питон предложит установить её
# Если не установлена, то никакого звука и не будет

play_sound = True
try:
    # from winsound.PlaySound import winsound.PlaySound
    import pygame
    pygame.init()
    pygame.mixer.init(48000, 32, 2, 2048)

except ImportError:
    from tkinter import messagebox

    answer = messagebox.askyesno(
        title="Нет библиотеки",
        # message="Если не установить модуль winsound.PlaySound, в программе не будут воспроизводиться звуки. 
        # Установить?") 
        message="Если не установить модуль pygame, в программе не будут воспроизводиться звуки. Установить?")
    if answer:
        # pip.main(["install", "winsound.PlaySound==1.2.2"])
        pip.main(["install", "pygame"])
    else:
        play_sound = False
        messagebox.showerror("Ох-хо-хо", "Звуков не будет.")


class Sound:
    BUTTON_PRESS = 1
    START_GAME = 2
    GOOD_CHAR = 3
    OK_LETS_GO = 4
    WIN_ROUND = 5
    WIN_GAME = 6
    LOSE_GAME = 7
    GONG = 8
    STRESS = 9

    def button_press(self):
        pygame.mixer.Sound("sound/button_press.mp3").play()

    def start_game(self):
        pygame.mixer.Sound("sound/start_game.mp3").play()

    def good_char(self):
        pygame.mixer.Sound("sound/good_char.mp3").play()

    def ok_lets_go(self):
        pygame.mixer.Sound("sound/start_game.mp3").play()

    def win_round(self):
        pygame.mixer.Sound("sound/win_round.mp3").play()

    def win_game(self):
        pygame.mixer.Sound("sound/win_game.mp3").play()

    def lose_game(self):
        pygame.mixer.Sound("sound/lose_game.mp3").play()

    def gong(self):
        pygame.mixer.Sound("sound/gong.mp3").play()

    def stress(self):

        files = ["sound/bad/bad01.mp3",
                 "sound/bad/bad02.mp3",
                 "sound/bad/bad03.mp3",
                 "sound/bad/bad04.mp3",
                 "sound/bad/bad05.mp3",
                 "sound/bad/bad06.mp3",
                 "sound/bad/bad07.mp3",
                 "sound/bad/bad08.mp3",
                 "sound/bad/bad09.mp3",
                 "sound/bad/bad10.mp3"
                 ]
        if setup.stress - 1 < len(files):
            pygame.mixer.Sound(files[setup.stress - 1]).play()

    def play(self, type_sound):
        if not play_sound:
            return False
        if type_sound == Sound.BUTTON_PRESS:
            self.button_press()
        elif type_sound == Sound.START_GAME:
            self.start_game()
        elif type_sound == Sound.GOOD_CHAR:
            self.good_char()
        elif type_sound == Sound.OK_LETS_GO:
            self.ok_lets_go()
        elif type_sound == Sound.WIN_ROUND:
            self.win_round()
        elif type_sound == Sound.WIN_GAME:
            self.win_game()
        elif type_sound == Sound.LOSE_GAME:
            self.lose_game()
        elif type_sound == Sound.GONG:
            self.gong()
        elif type_sound == Sound.STRESS:
            self.stress()

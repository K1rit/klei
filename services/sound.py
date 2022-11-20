# pip install playsound
import pip
from threading import Thread

# Здесь проверка на наличие библиотеки для воспроизведения звука
# Если библиотеки нет, Питон предложит установить её
# Если не установлена, то никакого звука и не будет

play_sound = True
try:
    from playsound import playsound
except ImportError:
    from tkinter import messagebox
    answer = messagebox.askyesno(
        title="Нет библиотеки",
        message="Если не установить модуль playsound, в программе не будут воспроизводиться звуки. Установить?")
    if answer:
        pip.main(["install", "playsound==1.2.2"])
    else:
        play_sound = False
        messagebox.showerror("Ох-хо-хо", "Звуков не будет.")

class Sound:

    BUTTON_PRESS = 1
    START_GAME = 2
    GOOD_CHAR = 3
    OK_LETS_GO = 4

    def button_press(self):
        playsound("sound/button_press.mp3")

    def start_game(self):
        playsound("sound/start_game.mp3")

    def good_char(self):
        playsound("sound/good_char.mp3")

    def ok_lets_go(self):
        playsound("sound/ok_go.mp3")


    def play(self, type_sound):
        if not play_sound:
            return False
        if type_sound == Sound.BUTTON_PRESS:
            Thread(target=self.button_press, daemon=True).start()
        elif type_sound == Sound.START_GAME:
            Thread(target=self.start_game, daemon=True).start()
        elif type_sound == Sound.GOOD_CHAR:
            Thread(target=self.good_char, daemon=True).start()
        elif type_sound == Sound.OK_LETS_GO:
            Thread(target=self.ok_lets_go, daemon=True).start()

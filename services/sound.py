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
    print("Библиотека playsound не установлена. Установите её. ")
    n = input("Установить? (Y/n): ")
    if n.upper() == "Y":
        pip.main(["install", "playsound==1.2.2"])
    else:
        print("Звука не будет.")
        play_sound = False

class Sound:

    BUTTON_PRESS = 1
    START_GAME = 2

    def button_press(self):
        playsound("sound/button_press.mp3")
    def start_game(self):
        playsound("sound/start_game.mp3")

    def play(self, type_sound):
        if not play_sound:
            return False
        if type_sound == Sound.BUTTON_PRESS:
            Thread(target=self.button_press, daemon=True).start()
        elif type_sound == Sound.START_GAME:
            Thread(target=self.start_game, daemon=True).start()

from tkinter import *
import time


def open_win(): #Окно Игры

    def dictionary(): # Клавиши от A до U
        shift_x = shift_y = 0
        count = 0

        for i in range(ord("A"), ord("U") + 1):
            button = Button(text=chr(i),font=("Arial", 15, "bold"))
            button.place(x = 550 - 100*2 + shift_x, y = 100*4.5 - shift_y)
            shift_x += 70
            count += 1
            
            if count == 7:
                shift_x = count = 0
                shift_y -=50
    

    win = Toplevel()
    win.grab_set()
    win.geometry("1200x720+500+300")
    win.overrideredirect(1)


    dictionary()
    

    
    button_Exit = Button(win, text="Выход",font=("Arial", 13, "bold"),command = win.destroy, padx=10, pady=27).place(x=1095, y=620)
    button_Question = Button(win, text="?",font=("Arial", 13, "bold"),command = None, padx=30, pady=27).place(x=1000, y=620)


def open_root(): #Окно Авторов
    root = Toplevel()
    root.grab_set()
    root.geometry("1200x720+500+300")
    root.overrideredirect(1)
    
    batton_Exit = Button(root, text="Выход",font=("Arial", 23, "bold"),command = root.destroy, padx=300, pady=40).pack()


window = Tk()
window.title("Klei")
window.geometry("1200x720+500+300")
window.resizable(False, False)
window.overrideredirect(1)


button_Game = Button(window, text="Играть",font=("Arial", 23, "bold"),command = open_win, padx=300, pady=40).place(relx=0.5, rely=0.20, anchor=CENTER)
button_Exit = Button(window, text="Выход",font=("Arial", 23, "bold"),command = window.quit, padx=300, pady=40).place(relx=0.5, rely=0.45, anchor=CENTER)
button_Authors = Button(window, text="Авторы",font=("Arial", 23, "bold"),command = open_root, padx=300, pady=40).place(relx=0.5, rely=0.70, anchor=CENTER)

window.mainloop()
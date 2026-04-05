import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
def menu(on_begin=None):
    menu = tk.Tk()
    menu.geometry("800x700")
    menu.title("Game - menu")
    title_font  = ("Courier", 20, "bold")
    normal_font  = ("Courier", 15, "bold")
    instructions_title = tk.Label(menu, text = "Game instructions:", font = title_font)
    instructions_title.place(x = 100, y = 100)

    instructions_text = ("Answer as many questions as correctly as you can within the time limit."
                         "In each question, you will be pressented with a string of text,"
                         "that you need  to encrypt or decrypt according to a cypher and a key,"
                         " depending on the question")
    instructions_label = tk.Label(menu, text = instructions_text,font = normal_font, justify="left", wraplength=600 )
    instructions_label.place(x = 100, y = 210)

    def on_press():
        menu.withdraw()
        if on_begin:
            on_begin()



    begin_button = tk.Button(menu, text = "Click to Begin!", font = normal_font, width = 20, height=4, command = on_press)
    begin_button.place(x = 300, y = 400)




    menu.mainloop()
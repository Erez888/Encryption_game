import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

BG      = "#0d0d0f"
CARD    = "#16161a"
ACCENT  = "#7f5af0"
ACCENT2 = "#2cb67d"
TEXT    = "#fffffe"
SUBTEXT = "#94a1b2"
ERR     = "#ff6b6b"
WARN    = "#f4a261"
BORDER  = "#2e2e38"

FONT_TITLE = ("Georgia", 28, "bold")
FONT_LABEL = ("Georgia", 11)
FONT_ENTRY = ("Courier New", 12)
FONT_BTN   = ("Georgia", 12, "bold")
FONT_SMALL = ("Georgia", 9)

def menu(on_begin=None):
    menu_win = tk.Tk()
    menu_win.geometry("800x700")
    menu_win.title("Game - menu")
    menu_win.configure(bg=BG)

    tk.Frame(menu_win, bg=ACCENT, height=4).place(x=0, y=0, relwidth=1)

    instructions_title = tk.Label(menu_win, text="Game Instructions:",
                                  font=FONT_TITLE, bg=BG, fg=ACCENT)
    instructions_title.place(x=100, y=100)

    instructions_text = ("Answer as many questions as correctly as you can within the time limit. "
                         "In each question, you will be presented with a string of text "
                         "that you need to encrypt or decrypt according to a cypher and a key, "
                         "depending on the question.")
    instructions_label = tk.Label(menu_win, text=instructions_text,
                                  font=("Georgia", 12), bg=BG, fg=SUBTEXT,
                                  justify="left", wraplength=600)
    instructions_label.place(x=100, y=210)

    def on_press():
        menu_win.withdraw()
        if on_begin:
            on_begin()

    begin_button = tk.Button(menu_win, text="Click to Begin!",
                             font=FONT_BTN, bg=ACCENT, fg=TEXT,
                             activebackground=ACCENT, activeforeground=TEXT,
                             relief="flat", bd=0, cursor="hand2",
                             width=20, height=4, command=on_press)
    begin_button.place(x=300, y=400)

    menu_win.mainloop()
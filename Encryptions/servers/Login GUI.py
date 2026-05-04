import tkinter as tk
import clinet_work
import socket

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

def luanch_login():
    login_screen = tk.Tk()
    login_screen.geometry("480x640")
    login_screen.title("Login or register")
    login_screen.configure(bg=BG)

    title_lbl = tk.Label(login_screen, text = "Trivia", font=FONT_TITLE, bg=BG, fg= ACCENT)
    title_lbl.place(x = 220, y = 100, anchor="center")


    login_screen.mainloop()
luanch_login()
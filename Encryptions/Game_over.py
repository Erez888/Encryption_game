import tkinter as tk
from Encryptions import Game_instructions as Instructions
from server_work import change_score

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

def Game_over(score, On_begin = None, on_back = None, username = None):
    Game_over_win = tk.Toplevel()
    Game_over_win.geometry("800x700")
    Game_over_win.title("Game over!")
    Game_over_win.configure(bg=BG)


    title_font  = ("Courier", 20, "bold")

    big_title = tk.Label(Game_over_win, text = "Game Over!", font = FONT_TITLE, fg = "red", bg = BG)
    big_title.place(x = 400, y = 300, anchor="center")
    score_label = tk.Label(Game_over_win, text=f"Final Score: {score}", font = title_font, bg=BG, fg=TEXT)
    score_label.place(x = 400, y = 350, anchor="center")

    def Back_to_menu():
        print("Back to menu pressed")
        Game_over_win.destroy()

        def start_game():
            print("start_game called")
            On_begin(username=username, on_back=on_back)

        print("About to open instructions")
        Instructions.menu(on_begin=start_game, on_back=on_back)
        print("Instructions opened")

    menu_btn = tk.Button(Game_over_win, text = "Main Menu", height=4, width=20, font=FONT_BTN, command=Back_to_menu, bg=ACCENT, fg=TEXT,
    activebackground=ACCENT, relief="flat", bd=0)
    menu_btn.place(x = 400, y = 500, anchor="center")






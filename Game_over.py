import tkinter as tk
from Encryptions import Game_instructions as Instructions

def Game_over(score, On_begin = None):
    Game_over_win = tk.Tk()
    Game_over_win.geometry("800x700")
    Game_over_win.title("Game over!")

    title_font  = ("Courier", 20, "bold")

    big_title = tk.Label(Game_over_win, text = "Game Over!", font = ("Courier", 40, "bold"), fg = "red")
    big_title.place(x = 400, y = 300, anchor="center")
    score_label = tk.Label(Game_over_win, text=f"Final Score: {score}", font = title_font)
    score_label.place(x = 400, y = 350, anchor="center")

    def Back_to_menu():
        Game_over_win.destroy()
        Instructions.menu(on_begin= On_begin)

    menu_btn = tk.Button(Game_over_win, text = "Main Menu", height=4, width=20, font=title_font, command=Back_to_menu)
    menu_btn.place(x = 400, y = 500, anchor="center")



    Game_over_win.mainloop()


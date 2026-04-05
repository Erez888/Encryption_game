import tkinter as tk
from tkinter import *
from tkinter import ttk

import Encryptions
menu = tk.Tk()
menu.title("Menu")
menu.geometry("700x700")

options = ["AZBY", "Ceaser cypher"]

dropdown_label = tk.Label(menu, text = "Select an Encryption method:")
dropdown_label.place(x = 90, y = 100)
combo = ttk.Combobox(menu, values= options, state="readonly")
combo.place(x = 100, y = 120)
combo.set("Choose...")


def on_press():
    selected = combo.get()
    if selected == "AZBY":
        menu.destroy()
        AZBY = tk.Tk()
        AZBY.title("AZBY encryption")
        AZBY.geometry("500x500")

        entry = tk.Entry(AZBY, width=30)
        entry.insert(0, "")
        entry.place(x=300, y=40)

        label = tk.Label(AZBY, text="Enter text:", font=("Courier", 10, "bold"))
        label.place(x=300, y=18)

        label2 = tk.Label(AZBY, text="Result:", font=("Courier", 10, "bold"))
        label2.place(x=300, y=90)
    
        result_entry = tk.Entry(AZBY, width=30)
        result_entry.place(x=300, y=110)

        def AZBY(p_text):
            start = "abcdefghijklmnopqrstuvwxyz"
            end = "zyxwvutsrqponmlkjihgfedcba"
            text = ""
            for item in p_text:
                if item.islower() and item in start:
                    num = start.find(item)
                    text += end[num]
                elif item.isupper() and item.lower() in start:
                    num = start.find(item.lower())
                    text += end[num].upper()
                else:
                    text += item
            return text
        def get_input():
            p_text = entry.get()
            encrypted_input = AZBY(p_text)
            result_entry.insert(0, encrypted_input)

        button = tk.Button(AZBY, text="Submit", command=get_input)
        button.place(x=300, y=60)


        AZBY.mainloop()
    #if selected == "Ceaser Cypher":

choose_enc_btn = tk.Button(menu, text = " go to encryption window", command = on_press)
choose_enc_btn.place(x = 100, y = 150)
selected = combo.get()

menu.mainloop()


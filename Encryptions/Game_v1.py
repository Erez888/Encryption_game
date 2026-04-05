import tkinter as tk
from operator import truediv
from pickle import GLOBAL
from tkinter import ttk
from tkinter import messagebox
import nltk # needs pip install
import time
from Encryptions import Game_instructions as instructions
from Encryptions import Ceaser_Cypher as Ceaser
from Encryptions import Zigzag as Zigzag
from Encryptions import Vigenere_cipher as Vigenere
from Encryptions import AZBY



nltk.download('words')
from nltk.corpus import words
import random
import string

def choose_cypher():
    cyphers = ["Ceaser", "Zigzag", "Vigenere", "AZBY"]
    cypher = random.choice(cyphers)
    return cypher

#the length is needed for the rail fence cypher
def choose_key(cypher, length):
    if cypher == "Ceaser":
        key = random.randint(0, 26)
        return key
    elif cypher == "Zigzag":
        key = random.randint(2, length - 1)
        return key
    elif cypher == "Vigenere":
        characters = string.ascii_lowercase
        key = ''.join(random.choices(characters, k=random.randint(2, 5)))
        return key
    elif cypher == "AZBY":
        return  None
    else:
        print("Error generating key")
        return
def generate_question():
    word_list = words.words()

    options = ["Encrypt", "Decrypt"]
    option = random.choice(options)
    if option == "Encrypt":
        question_cypher = choose_cypher()
        question_word = random.choice(word_list).lower()
        question_key = choose_key(cypher=question_cypher, length = len(question_word))
        if question_key is None:
            question_text = f'Encrypt "{question_word}" with {question_cypher}'
        else:
            question_text = f'Encrypt "{question_word}" with {question_cypher} with a key of {question_key}'
        return question_text, question_word, question_cypher, question_key, option
    elif option == "Decrypt":
        question_cypher = choose_cypher()
        question_word = random.choice(word_list).lower()
        question_key = choose_key(cypher=question_cypher, length = len(question_word))
        if question_cypher == "Ceaser":
            encrypted_word = Ceaser.CeaserCyhper(p_text=question_word, key = question_key)
        elif question_cypher == "Zigzag":
            encrypted_word = Zigzag.encrypt(text = question_word, depth = question_key)
        elif question_cypher == "Vigenere":
            encrypted_word = Vigenere.encrypt(message=question_word, key = question_key)
        elif question_cypher == "AZBY":
            encrypted_word = AZBY.AZBY(p_text=question_word)
        if question_key == None:
            question_text = (f"{encrypted_word} was encrypted with {question_cypher}.\n Decrypt it:")
        else:
            question_text = (f"{encrypted_word} was encrypted with {question_cypher}, \n with a key of {question_key}.\n Decrypt it:")
        return question_text, question_word, question_cypher, question_key, option


def Generate_right_option(question_word, question_cypher, question_key, method):
    if method == "Encrypt":
        if question_cypher == "Ceaser":
            correct_option = Ceaser.CeaserCyhper(p_text=question_word, key=question_key)
            return correct_option, question_word,question_cypher, question_key, method
        elif question_cypher == "Zigzag":
            correct_option = Zigzag.encrypt(text = question_word, depth= question_key)
            return correct_option, question_word,question_cypher, question_key, method
        elif question_cypher == "Vigenere":
            correct_option = Vigenere.encrypt(message=question_word, key = question_key)
            return  correct_option, question_word,question_cypher, question_key, method
        elif question_cypher == "AZBY":
            correct_option = AZBY.AZBY(p_text=question_word)
            return correct_option, question_word,question_cypher, question_key, method
    elif method == "Decrypt":
        return question_word, question_word, question_cypher, question_key, method


def Generate_wrong_options(right_option, question_word, question_cypher, question_key, method):
    if method == "Decrypt":
        word_list = words.words()
        wrong_options = []
        while len(wrong_options) < 3:
            option = random.choice(word_list).lower()
            if option != right_option and option not in wrong_options:
                wrong_options.append(option)
        return wrong_options[0], wrong_options[1], wrong_options[2]

    elif method == "Encrypt":
        def generate_one_wrong():
            option_cypher = choose_cypher()
            option_key = choose_key(cypher=option_cypher, length=len(question_word))
            if option_cypher == "Ceaser":
                return Ceaser.CeaserCyhper(p_text=question_word, key=option_key)
            elif option_cypher == "Zigzag":
                return Zigzag.encrypt(text=question_word, depth=option_key)
            elif option_cypher == "Vigenere":
                return Vigenere.encrypt(message=question_word, key=option_key)
            elif option_cypher == "AZBY":
                return AZBY.AZBY(p_text=question_word)

        wrong_options = []
        while len(wrong_options) < 3:
            option = generate_one_wrong()
            if option != right_option and option not in wrong_options:
                wrong_options.append(option)
        return wrong_options[0], wrong_options[1], wrong_options[2]

def Check_ans(selected_answer, correct_answer):
    if selected_answer == correct_answer:
        return True
    else:
        return False



def launch_game():
    game_window = tk.Toplevel()
    game_window.geometry("800x700")
    game_window.title("Game")
    submitted = False
    score = 0
    question_num = 0 #0 because the first instance of load question increases it

    score_lbl = tk.Label(game_window, text=f"score: {score}", font=("Courier", 20, "bold"), fg="lightblue")
    score_lbl.place(x=70, y=20, anchor="center")

    question_num_lbl = tk.Label(game_window, text= f"Question Number {question_num}", font=("Courier", 20, "bold"), fg="lightblue")
    question_num_lbl.place(x = 650, y = 20, anchor="center")

    question_label = tk.Label(game_window, text="", font=("Courier", 20, "bold"), wraplength=600)
    question_label.place(x=400, y=120, anchor="center")

    selected = tk.StringVar()
    radio_font = ("Courier", 18, "bold")
    option1 = tk.Radiobutton(game_window, text="", variable=selected, value="", font=radio_font, width = 20, anchor= "w")
    option2 = tk.Radiobutton(game_window, text="", variable=selected, value="", font=radio_font, width = 20, anchor= "w")
    option3 = tk.Radiobutton(game_window, text="", variable=selected, value="", font=radio_font, width = 20, anchor= "w")
    option4 = tk.Radiobutton(game_window, text="", variable=selected, value="", font=radio_font, width = 20, anchor= "w")
    option1.place(x=400, y=280, anchor="center")
    option2.place(x=400, y=320, anchor="center")
    option3.place(x=400, y=360, anchor="center")
    option4.place(x=400, y=400, anchor="center")

    result_label = tk.Label(game_window, text="", font=("Courier", 20, "bold"))
    result_label.place(x=400, y=560, anchor="center")

    correct_option_holder = [None]

    start = time.perf_counter()

    def Timer():
        display_time = (120 - time.perf_counter()/1000 - start/1000)
        time_label = tk.Label(game_window, text=f"{display_time:.1f}", font = ("Courier", 20, "bold"), fg="lightblue")
        time_label.place(x = 20, y = 20, anchor = "center")
        time_label.config(text = f"{display_time:.1f}")
        print(display_time)
        return

    game_window.after(10, Timer)

    Timer()


    def load_question():
        nonlocal submitted, question_num
        #print(f"submitted: {submitted}, question_num: {question_num}")

        if submitted == True or question_num == 0:
            question_num += 1
            question_num_lbl.config(text=f"Question Number {question_num}")
            submitted = False

            question_text, question_word, question_cypher, question_key, question_method = generate_question()
            correct_option = Generate_right_option(question_word=question_word, question_cypher=question_cypher, question_key=question_key, method=question_method)[0]
            wrong_option1, wrong_option2, wrong_option3 = Generate_wrong_options(right_option=correct_option, question_word=question_word, question_cypher=question_cypher, question_key=question_key, method=question_method)

            correct_option_holder[0] = correct_option
            options = [correct_option, wrong_option1, wrong_option2, wrong_option3]
            random.shuffle(options)

            question_label.config(text=question_text)
            submit_btn.config(state= "active")
            option1.config(text=options[0], value=options[0], state = "normal")
            option2.config(text=options[1], value=options[1], state = "normal")
            option3.config(text=options[2], value=options[2], state = "normal")
            option4.config(text=options[3], value=options[3], state = "normal")
            selected.set(None)
            result_label.config(text="")
        elif question_num >1:
            result_label.config(text="You need to submit an answer first!", anchor="center", fg = "yellow", wraplength= 400)
            #print("blocked")

    def on_submit():
        nonlocal score, submitted
        submitted = True
        option1.config(state="disabled")
        option2.config(state="disabled")
        option3.config(state="disabled")
        option4.config(state="disabled")
        submit_btn.config(state="disabled")
        if Check_ans(selected.get(), correct_option_holder[0]):
            result_label.config(text="Correct!", fg="green")
            score += 1
            score_lbl.config(text=f"score: {score}")
        else:
            result_label.config(text=f"Wrong!\nCorrect Answer: {correct_option_holder[0]}", fg="red", wraplength=600)

    submit_btn = tk.Button(game_window, text="Submit", font=("Courier", 20, "bold"), width=8, height=2, command=on_submit)
    submit_btn.place(x=300, y=480, anchor="center")

    next_question_btn = tk.Button(game_window, text="Next Question", font=("Courier", 20, "bold"), command=load_question)
    next_question_btn.place(x=670, y=650, anchor="center")

    load_question()


instructions.menu(on_begin=launch_game)
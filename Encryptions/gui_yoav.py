import tkinter as tk
from tkinter import messagebox
import chatlib
import client_work
import server_work
from Encryptions import Game_instructions
import threading

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

logged_in = False

def gui_main(on_begin=None):
    global logged_in

    conn = None

    def write_output(text):
        output_text.config(state="normal")
        output_text.delete("1.0", "end")
        output_text.insert("1.0", text)
        output_text.config(state="disabled")

    def do_connect():
        try:
            return client_work.connect(client_work.SERVER_IP, client_work.SERVER_PORT)
        except Exception:
            return None

    def execute_login():
        nonlocal conn
        global logged_in

        username = username_entry.get().strip()
        password = password_entry.get().strip()
        action   = action_var.get()

        if not username:
            messagebox.showwarning("Warning", "Please enter a username.")
            return
        if not password:
            messagebox.showwarning("Warning", "Please enter a password.")
            return

        conn = do_connect()
        if conn is None:
            write_output("Could not connect to server.\nMake sure the server is running.")
            return

        data = chatlib.join_data([username, password])

        if action == "login":
            client_work.build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"], data)
        else:
            client_work.build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["register_msg"], data)

        cmd, msg = client_work.recv_message_and_parse(conn)

        ok_cmds = (
            chatlib.PROTOCOL_SERVER["login_ok_msg"],
            chatlib.PROTOCOL_SERVER["register_ok_msg"],
        )

        if cmd in ok_cmds:
            verb = "Logged in" if action == "login" else "Registered"
            write_output(f"{verb} successfully as '{username}'!")
            exec_btn.config(state="disabled")
            username_entry.config(state="disabled")
            password_entry.config(state="disabled")
            post_frame.pack(pady=8)
            logged_in = True
        else:
            write_output(f"Failed: {msg or 'Authentication error.'}")
            conn.close()
            conn = None

    def get_score():
        if not conn:
            return
        cmd, data = client_work.build_send_recv_parse(
            conn, chatlib.PROTOCOL_CLIENT["get_score_msg"], "")
        if cmd == chatlib.PROTOCOL_SERVER["score_msg"]:
            write_output(f"Your score: {data} pts")
        else:
            write_output(f"Error: {data}")

    def get_highscore():
        if not conn:
            return
        cmd, data = client_work.build_send_recv_parse(
            conn, chatlib.PROTOCOL_CLIENT["get_highscore_msg"], "")
        if cmd == chatlib.PROTOCOL_SERVER["highscore_msg"]:
            write_output(data)
        else:
            write_output(f"Error: {data}")

    def logout():
        nonlocal conn
        global logged_in
        if conn:
            client_work.logout(conn)
            conn = None
        logged_in = False
        post_frame.pack_forget()
        exec_btn.config(state="normal")
        username_entry.config(state="normal")
        password_entry.config(state="normal")
        username_entry.delete(0, "end")
        password_entry.delete(0, "end")
        write_output("Logged out. Please sign in again.")

    # ── build the window ───────────────────────────────────────────
    root = tk.Tk()
    root.title("Encryption Tool")
    root.geometry("500x640")
    root.configure(bg=BG)

    tk.Frame(root, bg=ACCENT, height=4).pack(fill="x")

    tk.Label(root, text="Cipher Trivia", font=FONT_TITLE, bg=BG, fg=ACCENT).pack(pady=(30, 5))
    tk.Label(root, text="Login or register to play", font=FONT_SMALL, bg=BG, fg=SUBTEXT).pack(pady=(0, 20))

    tk.Label(root, text="Username", font=FONT_LABEL, bg=BG, fg=SUBTEXT).pack(anchor="w", padx=80)
    username_entry = tk.Entry(root, width=30, font=FONT_ENTRY, bg=CARD, fg=TEXT,
                              insertbackground=TEXT, relief="flat", bd=6)
    username_entry.pack(pady=(2, 10), padx=80, fill="x")

    tk.Label(root, text="Password", font=FONT_LABEL, bg=BG, fg=SUBTEXT).pack(anchor="w", padx=80)
    password_entry = tk.Entry(root, width=30, font=FONT_ENTRY, bg=CARD, fg=TEXT,
                              insertbackground=TEXT, relief="flat", bd=6, show="*")
    password_entry.pack(pady=(2, 10), padx=80, fill="x")

    action_frame = tk.Frame(root, bg=BG)
    action_frame.pack(pady=5)
    action_var = tk.StringVar(value="login")
    tk.Radiobutton(action_frame, text="Login", variable=action_var, value="login",
                   bg=BG, fg=TEXT, selectcolor=CARD, activebackground=BG,
                   font=FONT_LABEL).pack(side="left", padx=10)
    tk.Radiobutton(action_frame, text="Register", variable=action_var, value="register",
                   bg=BG, fg=TEXT, selectcolor=CARD, activebackground=BG,
                   font=FONT_LABEL).pack(side="left", padx=10)

    exec_btn = tk.Button(root, text="EXECUTE", bg=ACCENT2, fg=TEXT,
                         font=FONT_BTN, relief="flat", bd=0, cursor="hand2",
                         activebackground=ACCENT2, activeforeground=TEXT,
                         command=execute_login)
    exec_btn.pack(pady=15, ipadx=20, ipady=6)

    output_text = tk.Text(root, height=4, width=50, state="disabled",
                          bg=CARD, fg=SUBTEXT, font=FONT_SMALL, relief="flat", bd=6)
    output_text.pack(pady=5, padx=80, fill="x")

    post_frame = tk.Frame(root, bg=BG)
    tk.Button(post_frame, text="My Score", width=12, command=get_score,
              bg=CARD, fg=TEXT, font=FONT_SMALL, relief="flat").pack(side="left", padx=5)
    tk.Button(post_frame, text="High Scores", width=12, command=get_highscore,
              bg=CARD, fg=TEXT, font=FONT_SMALL, relief="flat").pack(side="left", padx=5)
    tk.Button(post_frame, text="Logout", width=10, command=logout,
              bg=ERR, fg=TEXT, font=FONT_SMALL, relief="flat").pack(side="left", padx=5)

    def on_press():
        if logged_in:
            root.withdraw()
            Game_instructions.menu(on_begin=on_begin)
        else:
            write_output("Please log in first.")

    tk.Button(root, text="Begin Game", font=FONT_BTN, bg=ACCENT, fg=TEXT,
              activebackground=ACCENT, activeforeground=TEXT,
              relief="flat", bd=0, cursor="hand2",
              command=on_press).pack(pady=10, ipadx=20, ipady=6)

    def start_server_in_background():
        server_thread = threading.Thread(target=server_work.main, daemon=True)
        server_thread.start()
        write_output("Server started in the background!")
        server_btn.config(state="disabled")

    server_btn = tk.Button(root, text="Open Server", bg=CARD, fg=SUBTEXT,
                           font=FONT_SMALL, relief="flat", command=start_server_in_background)
    server_btn.pack(pady=5)

    root.bind("<Return>", lambda e: execute_login())
    root.mainloop()
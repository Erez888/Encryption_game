import tkinter as tk
from tkinter import messagebox
import chatlib
import server_work
from server_work import main
import client_work
import threading
# ── global socket ──────────────────────────────────────────────
conn = None
# ── helpers ────────────────────────────────────────────────────

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

# ── main action ────────────────────────────────────────────────
def execute_crypto():
    global conn

    username = username_entry.get().strip()
    password = password_entry.get().strip()
    action   = action_var.get()   # "login" or "register"

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
        # lock form, show post-login buttons
        exec_btn.config(state="disabled")
        username_entry.config(state="disabled")
        password_entry.config(state="disabled")
        post_frame.pack(pady=8)
    else:
        write_output(f"Failed: {msg or 'Authentication error.'}")
        conn.close()
        conn = None

# ── post-login actions ─────────────────────────────────────────
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
    global conn
    if conn:
        client_work.logout(conn)
        conn = None
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
root.geometry("500x600")

# username
tk.Label(root, text="Username", font=("Arial", 12, "bold")).pack(pady=(10, 0))
username_entry = tk.Entry(root, width=30)
username_entry.pack(pady=3)

# password
tk.Label(root, text="Password", font=("Arial", 10)).pack(pady=(10, 0))
password_entry = tk.Entry(root, width=30, show="*")
password_entry.pack(pady=5)

# action radio buttons
settings_frame = tk.Frame(root)
settings_frame.pack(pady=10, fill="x", padx=20)

action_frame = tk.LabelFrame(settings_frame, text="Actions")
action_frame.pack(side="right", expand=True, fill="both", padx=5)

action_var = tk.StringVar(value="login")
tk.Radiobutton(action_frame, text="Login",    variable=action_var, value="login").pack(anchor="w")
tk.Radiobutton(action_frame, text="Register", variable=action_var, value="register").pack(anchor="w")

# execute button
exec_btn = tk.Button(root, text="EXECUTE", bg="#4CAF50", fg="white",
                     font=("Arial", 12, "bold"), command=execute_crypto)
exec_btn.pack(pady=15, ipadx=20)

# output area
tk.Label(root, text="Output", font=("Arial", 12, "bold")).pack(pady=(5, 0))
output_text = tk.Text(root, height=5, width=50, state="disabled", bg="#f0f0f0")
output_text.pack(pady=5)

# post-login buttons (hidden until logged in)
post_frame = tk.Frame(root)
tk.Button(post_frame, text="My Score",    width=15, command=get_score).pack(side="left", padx=8)
tk.Button(post_frame, text="High Scores", width=15, command=get_highscore).pack(side="left", padx=8)
tk.Button(post_frame, text="Logout",      width=10, bg="#e74c3c", fg="white",
          command=logout).pack(side="left", padx=8)
def start_server_in_background():
    # This creates a separate background process for the server
    server_thread = threading.Thread(target=server_work.main, daemon=True)
    server_thread.start()
    write_output("Server started in the background!")
    server_btn.config(state="disabled") # Disable button so you don't click it twice
server_btn = tk.Button(root, text="Open Server", bg="#4CAF50", fg="white",
                     font=("Arial", 12, "bold"), command=start_server_in_background)
server_btn.pack(pady=10, ipadx=20)
root.bind("<Return>", lambda e: execute_crypto())
root.mainloop()

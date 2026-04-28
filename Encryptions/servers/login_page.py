import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import sys
import os

# ── Import your existing modules (must be in the same directory) ──
import chatlib
import client_work

# ══════════════════════════════════════════════════════════════
#  COLOURS & FONTS
# ══════════════════════════════════════════════════════════════
BG       = "#0d0d0f"
CARD     = "#16161a"
ACCENT   = "#7f5af0"
ACCENT2  = "#2cb67d"
TEXT     = "#fffffe"
SUBTEXT  = "#94a1b2"
ENTRY_BG = "#242629"
ENTRY_FG = "#fffffe"
ERR      = "#ff6b6b"
BORDER   = "#2e2e38"
WARN     = "#f4a261"

FONT_TITLE = ("Georgia", 28, "bold")
FONT_LABEL = ("Georgia", 11)
FONT_ENTRY = ("Courier New", 12)
FONT_BTN   = ("Georgia", 12, "bold")
FONT_SMALL = ("Georgia", 9)

# ══════════════════════════════════════════════════════════════
#  MAIN APP
# ══════════════════════════════════════════════════════════════
class TriviaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Trivia Game")
        self.geometry("480x640")
        self.resizable(False, False)
        self.configure(bg=BG)

        self.conn          = None
        self.username      = None
        self._server_proc  = None   # subprocess for server_work.py

        self._show_launcher()

    # ──────────────────────────────────────────────────────────
    #  LAUNCHER SCREEN  (Start Server button)
    # ──────────────────────────────────────────────────────────
    def _show_launcher(self):
        self._clear()

        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True)

        tk.Frame(root, bg=ACCENT, height=4).pack(fill="x")

        card = tk.Frame(root, bg=CARD,
                        highlightthickness=1, highlightbackground=BORDER)
        card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=400)

        tk.Label(card, text="TRIVIA", font=FONT_TITLE,
                 bg=CARD, fg=ACCENT).pack(pady=(40, 4))
        tk.Label(card, text="multiplayer quiz game",
                 font=FONT_SMALL, bg=CARD, fg=SUBTEXT).pack()

        tk.Frame(card, bg=BORDER, height=1).pack(fill="x", padx=32, pady=28)

        # ── check if server is already reachable ──
        already_up = self._probe_server()

        # server status indicator
        if already_up:
            status_text = "Server: ✓ already running"
            status_color = ACCENT2
        else:
            status_text = "Server: not running"
            status_color = ERR

        self._srv_status_var = tk.StringVar(value=status_text)
        self._srv_status_lbl = tk.Label(card,
                                        textvariable=self._srv_status_var,
                                        font=FONT_SMALL, bg=CARD, fg=status_color)
        self._srv_status_lbl.pack(pady=(0, 12))

        # Start Server button — disabled if already up
        self._start_srv_btn = tk.Button(
            card, text="✓  Server Already Running" if already_up else "▶  Start Server",
            font=FONT_BTN,
            bg="#1e5c45" if already_up else ACCENT2, fg=TEXT,
            activebackground="#1e5c45" if already_up else ACCENT2,
            activeforeground=TEXT,
            relief="flat", bd=0, pady=12,
            cursor="arrow" if already_up else "hand2",
            state="disabled" if already_up else "normal",
            command=self._start_server)
        self._start_srv_btn.pack(fill="x", padx=32, pady=(0, 10))

        # "Server already running? Go straight to login" button
        self._skip_btn = tk.Button(
            card, text="⚡  Server is already running — Login",
            font=FONT_BTN, bg=ACCENT, fg=TEXT,
            activebackground=ACCENT, activeforeground=TEXT,
            relief="flat", bd=0, cursor="hand2", pady=12,
            command=self._show_login_frame)
        if already_up:
            self._skip_btn.pack(fill="x", padx=32, pady=(0, 10))

        # Connect / Login button (shown after starting server here)
        self._connect_btn = tk.Button(
            card, text="→  Connect & Login",
            font=FONT_BTN,
            bg=ACCENT if already_up else ENTRY_BG,
            fg=TEXT if already_up else SUBTEXT,
            activebackground=ACCENT, activeforeground=TEXT,
            relief="flat", bd=0, pady=12,
            cursor="hand2" if already_up else "arrow",
            state="normal" if already_up else "disabled",
            command=self._show_login_frame)
        if not already_up:
            self._connect_btn.pack(fill="x", padx=32)

        hint = "Server detected — you can log in directly." if already_up else "Start the server first, then connect."
        tk.Label(card, text=hint,
                 font=FONT_SMALL, bg=CARD, fg=SUBTEXT).pack(pady=(14, 0))

    def _probe_server(self):
        """Try a quick TCP connect to see if the server is already up."""
        import socket as _socket
        try:
            s = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((client_work.SERVER_IP, client_work.SERVER_PORT))
            s.close()
            return True
        except Exception:
            return False

    def _start_server(self):
        """Launch server_work.py in a background subprocess."""
        if self._server_proc and self._server_proc.poll() is None:
            messagebox.showinfo("Server", "Server is already running.")
            return

        server_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "server_work.py")
        if not os.path.exists(server_path):
            messagebox.showerror("Error",
                                 f"server_work.py not found at:\n{server_path}")
            return

        try:
            self._server_proc = subprocess.Popen(
                [sys.executable, server_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except Exception as e:
            messagebox.showerror("Error", f"Could not start server:\n{e}")
            return

        # Wait briefly then check it's alive
        self.after(800, self._check_server_started)

    def _check_server_started(self):
        if self._server_proc and self._server_proc.poll() is None:
            # Process is alive → server running
            self._srv_status_var.set("Server: ✓ running")
            self._srv_status_lbl.config(fg=ACCENT2)
            self._start_srv_btn.config(
                text="✓  Server Running",
                bg="#1e5c45", state="disabled", cursor="arrow")
            self._connect_btn.config(
                bg=ACCENT, fg=TEXT,
                activebackground=ACCENT, activeforeground=TEXT,
                state="normal", cursor="hand2")
        else:
            self._srv_status_var.set("Server: failed to start")
            self._srv_status_lbl.config(fg=ERR)

    # ──────────────────────────────────────────────────────────
    #  LOGIN / REGISTER SCREEN
    # ──────────────────────────────────────────────────────────
    def _show_login_frame(self):
        self._clear()

        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True)

        tk.Frame(root, bg=ACCENT, height=4).pack(fill="x")

        card = tk.Frame(root, bg=CARD,
                        highlightthickness=1, highlightbackground=BORDER)
        card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=500)

        tk.Label(card, text="TRIVIA", font=FONT_TITLE,
                 bg=CARD, fg=ACCENT).pack(pady=(36, 2))
        tk.Label(card, text="sign in or create an account",
                 font=FONT_SMALL, bg=CARD, fg=SUBTEXT).pack(pady=(0, 20))

        # ── tabs ──
        tab_frame = tk.Frame(card, bg=CARD)
        tab_frame.pack(fill="x", padx=32)

        self._mode = tk.StringVar(value="login")

        def tab_style(btn, active):
            btn.configure(
                bg=ACCENT if active else ENTRY_BG,
                fg=TEXT   if active else SUBTEXT)

        self._tab_login = tk.Button(
            tab_frame, text="Login", font=FONT_BTN, width=10,
            relief="flat", bd=0, cursor="hand2",
            command=lambda: self._switch_tab("login"))
        self._tab_login.pack(side="left", ipady=8)

        self._tab_reg = tk.Button(
            tab_frame, text="Register", font=FONT_BTN, width=10,
            relief="flat", bd=0, cursor="hand2",
            command=lambda: self._switch_tab("register"))
        self._tab_reg.pack(side="left", ipady=8)

        tab_style(self._tab_login, True)
        tab_style(self._tab_reg,   False)
        self._tab_style_fn = tab_style

        # ── form ──
        self._form_frame = tk.Frame(card, bg=CARD)
        self._form_frame.pack(fill="x", padx=32, pady=(20, 0))

        self._status_lbl = tk.Label(card, text="", font=FONT_SMALL,
                                    bg=CARD, fg=ERR, wraplength=310)
        self._status_lbl.pack(pady=(8, 0))

        # back button
        tk.Button(card, text="← Back", font=FONT_SMALL,
                  bg=CARD, fg=SUBTEXT, relief="flat", bd=0,
                  cursor="hand2",
                  command=self._show_launcher).pack(pady=(6, 0))

        self._build_form()

    def _switch_tab(self, mode):
        self._mode.set(mode)
        self._tab_style_fn(self._tab_login, mode == "login")
        self._tab_style_fn(self._tab_reg,   mode == "register")
        self._status_lbl.config(text="")
        self._build_form()

    def _build_form(self):
        for w in self._form_frame.winfo_children():
            w.destroy()

        mode = self._mode.get()

        self._make_field(self._form_frame, "Username")
        self._entry_user = self._make_entry(self._form_frame)

        self._make_field(self._form_frame, "Password")
        self._entry_pass = self._make_entry(self._form_frame, show="•")

        btn_color = ACCENT if mode == "login" else ACCENT2
        btn_text  = "Sign In" if mode == "login" else "Create Account"

        tk.Button(self._form_frame, text=btn_text, font=FONT_BTN,
                  bg=btn_color, fg=TEXT,
                  activebackground=btn_color, activeforeground=TEXT,
                  relief="flat", bd=0, cursor="hand2", pady=10,
                  command=self._handle_action).pack(fill="x", pady=(20, 0))

        self.bind("<Return>", lambda e: self._handle_action())

    def _make_field(self, parent, text):
        tk.Label(parent, text=text, font=FONT_LABEL,
                 bg=CARD, fg=SUBTEXT, anchor="w").pack(fill="x", pady=(10, 2))

    def _make_entry(self, parent, show=None):
        e = tk.Entry(parent, font=FONT_ENTRY,
                     bg=ENTRY_BG, fg=ENTRY_FG,
                     insertbackground=TEXT,
                     relief="flat", bd=0,
                     highlightthickness=1,
                     highlightbackground=BORDER,
                     highlightcolor=ACCENT,
                     show=show or "")
        e.pack(fill="x", ipady=8)
        return e

    # ── handle login / register ────────────────────────────────
    def _handle_action(self):
        username = self._entry_user.get().strip()
        password = self._entry_pass.get().strip()

        if not username or not password:
            self._status_lbl.config(text="⚠  Please fill in both fields.", fg=ERR)
            return

        self._status_lbl.config(text="Connecting…", fg=SUBTEXT)
        self.update()

        # Use client_work.connect()
        try:
            conn = client_work.connect(client_work.SERVER_IP, client_work.SERVER_PORT)
        except SystemExit:
            self._status_lbl.config(
                text="⚠  Could not connect to server. Is it running?", fg=ERR)
            return
        except Exception as e:
            self._status_lbl.config(text=f"⚠  {e}", fg=ERR)
            return

        self.conn = conn
        mode = self._mode.get()
        data = chatlib.join_data([username, password])

        if mode == "login":
            client_work.build_and_send_message(
                conn, chatlib.PROTOCOL_CLIENT["login_msg"], data)
        else:
            client_work.build_and_send_message(
                conn, chatlib.PROTOCOL_CLIENT["register_msg"], data)

        cmd, msg = client_work.recv_message_and_parse(conn)

        ok_cmds = (chatlib.PROTOCOL_SERVER["login_ok_msg"],
                   chatlib.PROTOCOL_SERVER["register_ok_msg"])

        if cmd in ok_cmds:
            self.username = username
            self._show_dashboard()
        else:
            self._status_lbl.config(
                text=f"⚠  {msg or 'Authentication failed.'}",
                fg=ERR)
            conn.close()
            self.conn = None

    # ──────────────────────────────────────────────────────────
    #  DASHBOARD SCREEN
    # ──────────────────────────────────────────────────────────
    def _show_dashboard(self):
        self._clear()

        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True)

        # top bar
        bar = tk.Frame(root, bg=CARD, height=56,
                       highlightthickness=1, highlightbackground=BORDER)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        tk.Label(bar, text="TRIVIA", font=("Georgia", 16, "bold"),
                 bg=CARD, fg=ACCENT).pack(side="left", padx=20)
        tk.Label(bar, text=f"👤  {self.username}",
                 font=FONT_LABEL, bg=CARD, fg=SUBTEXT).pack(side="right", padx=20)

        content = tk.Frame(root, bg=BG)
        content.pack(fill="both", expand=True, padx=40, pady=30)

        tk.Label(content, text="Welcome back,",
                 font=FONT_SMALL, bg=BG, fg=SUBTEXT).pack(anchor="w")
        tk.Label(content, text=f"{self.username}!",
                 font=("Georgia", 22, "bold"), bg=BG, fg=TEXT).pack(anchor="w")

        tk.Frame(content, bg=ACCENT, height=2).pack(fill="x", pady=16)

        # action buttons — all call client_work functions
        actions = [
            ("🏅  My Score",    self._get_score,     ACCENT),
            ("🏆  High Scores", self._get_highscore, ACCENT2),
            ("🚪  Logout",      self._logout,        "#72757e"),
        ]
        for lbl, cmd_fn, color in actions:
            tk.Button(content, text=lbl, font=FONT_BTN,
                      bg=color, fg=TEXT,
                      activebackground=color, activeforeground=TEXT,
                      relief="flat", bd=0, cursor="hand2",
                      pady=12, anchor="w", padx=16,
                      command=cmd_fn).pack(fill="x", pady=6)

        tk.Label(content, text="Output",
                 font=FONT_SMALL, bg=BG, fg=SUBTEXT).pack(anchor="w", pady=(16, 4))

        self._output = tk.Text(content, font=FONT_ENTRY,
                               bg=CARD, fg=TEXT,
                               insertbackground=TEXT,
                               relief="flat", bd=0,
                               highlightthickness=1,
                               highlightbackground=BORDER,
                               height=8, state="disabled", wrap="word")
        self._output.pack(fill="both", expand=True)

    def _print_output(self, text):
        self._output.config(state="normal")
        self._output.delete("1.0", "end")
        self._output.insert("end", text)
        self._output.config(state="disabled")

    # ── dashboard actions — use client_work functions ──────────
    def _get_score(self):
        # reuse build_send_recv_parse from client_work
        cmd, data = client_work.build_send_recv_parse(
            self.conn, chatlib.PROTOCOL_CLIENT["get_score_msg"], "")
        if cmd == chatlib.PROTOCOL_SERVER["score_msg"]:
            self._print_output(f"Your current score:  {data} pts")
        else:
            self._print_output(f"Error: {data}")

    def _get_highscore(self):
        cmd, data = client_work.build_send_recv_parse(
            self.conn, chatlib.PROTOCOL_CLIENT["get_highscore_msg"], "")
        if cmd == chatlib.PROTOCOL_SERVER["highscore_msg"]:
            self._print_output(data)
        else:
            self._print_output(f"Error: {data}")

    def _logout(self):
        if self.conn:
            client_work.logout(self.conn)
            self.conn = None
        self.username = None
        self._show_launcher()

    # ── cleanup ────────────────────────────────────────────────
    def on_close(self):
        if self.conn:
            try:
                client_work.logout(self.conn)
            except Exception:
                pass
        if self._server_proc and self._server_proc.poll() is None:
            self._server_proc.terminate()
        self.destroy()

    # ── helpers ────────────────────────────────────────────────
    def _clear(self):
        for w in self.winfo_children():
            w.destroy()


# ── entry point ────────────────────────────────────────────────
if __name__ == "__main__":
    app = TriviaApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
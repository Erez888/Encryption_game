import tkinter as tk
from tkinter import messagebox
import chatlib
import client_work

class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Encryption Tool")
        self.root.geometry("500x600")
        self.conn = None  # will hold the socket after connect

        # --- Username ---
        tk.Label(root, text="Username", font=("Arial", 12, "bold")).pack(pady=(10, 0))
        self.input_text = tk.Entry(root, width=30)   # Entry, not Text
        self.input_text.pack(pady=3)

        # --- Password ---
        tk.Label(root, text="Password", font=("Arial", 10)).pack(pady=(10, 0))
        self.key_entry = tk.Entry(root, width=30, show="*")   # Entry, not Text
        self.key_entry.pack(pady=5)

        # --- Settings Frame (Radio Buttons) ---
        settings_frame = tk.Frame(root)
        settings_frame.pack(pady=10, fill="x", padx=20)

        # -- Actions Selection --
        action_frame = tk.LabelFrame(settings_frame, text="Actions")
        action_frame.pack(side="right", expand=True, fill="both", padx=5)

        self.action_var = tk.StringVar(value="login")

        tk.Radiobutton(action_frame, text="Login",    variable=self.action_var, value="login").pack(anchor="w")
        tk.Radiobutton(action_frame, text="Register", variable=self.action_var, value="register").pack(anchor="w")

        # --- Execute Button ---
        self.exec_btn = tk.Button(root, text="EXECUTE", bg="#4CAF50", fg="white",
                                  font=("Arial", 12, "bold"),
                                  command=self.execute_crypto)
        self.exec_btn.pack(pady=15, ipadx=20)

        # --- Output Text Area ---
        tk.Label(root, text="Output", font=("Arial", 12, "bold")).pack(pady=(5, 0))
        self.output_text = tk.Text(root, height=5, width=50, state="disabled", bg="#f0f0f0")
        self.output_text.pack(pady=5)

        # --- Post-login buttons (hidden until logged in) ---
        self.post_frame = tk.Frame(root)

        tk.Button(self.post_frame, text="My Score",   width=15,
                  command=self.get_score).pack(side="left", padx=8)
        tk.Button(self.post_frame, text="High Scores", width=15,
                  command=self.get_highscore).pack(side="left", padx=8)
        tk.Button(self.post_frame, text="Logout",      width=10, bg="#e74c3c", fg="white",
                  command=self.logout).pack(side="left", padx=8)

        # bind Enter key
        self.root.bind("<Return>", lambda e: self.execute_crypto())

    # ── helpers ────────────────────────────────────────────────
    def _write_output(self, text):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", text)
        self.output_text.config(state="disabled")

    def _connect(self):
        """Open a socket to the server using client_work.connect()."""
        try:
            return client_work.connect(client_work.SERVER_IP, client_work.SERVER_PORT)
        except SystemExit:
            return None
        except Exception:
            return None

    # ── main action ────────────────────────────────────────────
    def execute_crypto(self):
        username = self.input_text.get().strip()
        password = self.key_entry.get().strip()
        action   = self.action_var.get()          # "login" or "register"

        if not username:
            messagebox.showwarning("Warning", "Please enter a username.")
            return
        if not password:
            messagebox.showwarning("Warning", "Please enter a password.")
            return

        try:
            conn = self._connect()
            if conn is None:
                self._write_output("❌ Could not connect to server.\nMake sure the server is running.")
                return

            self.conn = conn
            data = chatlib.join_data([username, password])

            if action == "login":
                client_work.build_and_send_message(
                    conn, chatlib.PROTOCOL_CLIENT["login_msg"], data)
            else:
                client_work.build_and_send_message(
                    conn, chatlib.PROTOCOL_CLIENT["register_msg"], data)

            cmd, msg = client_work.recv_message_and_parse(conn)

            ok_cmds = (
                chatlib.PROTOCOL_SERVER["login_ok_msg"],
                chatlib.PROTOCOL_SERVER["register_ok_msg"],
            )

            if cmd in ok_cmds:
                verb = "Logged in" if action == "login" else "Registered"
                self._write_output(f"✅ {verb} successfully as '{username}'!")
                # show post-login buttons, lock form
                self.post_frame.pack(pady=8)
                self.exec_btn.config(state="disabled")
                self.input_text.config(state="disabled")
                self.key_entry.config(state="disabled")
            else:
                self._write_output(f"❌ Failed: {msg or 'Authentication error.'}")
                conn.close()
                self.conn = None

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")

    # ── post-login actions ─────────────────────────────────────
    def get_score(self):
        if not self.conn:
            return
        cmd, data = client_work.build_send_recv_parse(
            self.conn, chatlib.PROTOCOL_CLIENT["get_score_msg"], "")
        if cmd == chatlib.PROTOCOL_SERVER["score_msg"]:
            self._write_output(f"🏅 Your score: {data} pts")
        else:
            self._write_output(f"Error: {data}")

    def get_highscore(self):
        if not self.conn:
            return
        cmd, data = client_work.build_send_recv_parse(
            self.conn, chatlib.PROTOCOL_CLIENT["get_highscore_msg"], "")
        if cmd == chatlib.PROTOCOL_SERVER["highscore_msg"]:
            self._write_output(data)
        else:
            self._write_output(f"Error: {data}")

    def logout(self):
        if self.conn:
            client_work.logout(self.conn)
            self.conn = None
        # re-enable the form
        self.post_frame.pack_forget()
        self.exec_btn.config(state="normal")
        self.input_text.config(state="normal")
        self.key_entry.config(state="normal")
        self.input_text.delete(0, "end")
        self.key_entry.delete(0, "end")
        self._write_output("Logged out. Please sign in again.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()
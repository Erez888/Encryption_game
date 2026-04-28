import tkinter as tk
from tkinter import messagebox
import server_work
import client_work
i

class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Encryption Tool")
        self.root.geometry("500x600")
        # --- Input Text Area ---
        tk.Label(root, text="username", font=("Arial", 12, "bold")).pack(pady=(10, 0))
        self.input_text = tk.Text(root, height=1, width=10)
        self.input_text.pack(pady=3)

        # --- Key Input ---
        # מסגרת כדי לשים את התווית והשדה באותה שורה (אופציונלי, כאן שמתי אחד מתחת לשני לנוחות)
        tk.Label(root, text="password", font=("Arial", 10)).pack(pady=(10, 0))
        self.key_entry = tk.Entry(root, width=10)
        self.key_entry.pack(pady=5)

        # --- Settings Frame (Radio Buttons) ---
        settings_frame = tk.Frame(root)
        settings_frame.pack(pady=10, fill="x", padx=20)


        # -- Actions Selection --
        action_frame = tk.LabelFrame(settings_frame, text="Actions")
        action_frame.pack(side="right", expand=True, fill="both", padx=5)

        self.action_var = tk.StringVar(value="Encrypt")  # ברירת מחדל

        tk.Radiobutton(action_frame, text="login", variable=self.action_var, value="Encrypt").pack(anchor="w")
        tk.Radiobutton(action_frame, text="register", variable=self.action_var, value="Decrypt").pack(anchor="w")

        # --- Execute Button ---
        self.exec_btn = tk.Button(root, text="EXECUTE", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                                  command=self.execute_crypto)
        self.exec_btn.pack(pady=15, ipadx=20)

        # --- Output Text Area ---
        tk.Label(root, text="Output", font=("Arial", 12, "bold")).pack(pady=(5, 0))
        self.output_text = tk.Text(root, height=5, width=50, state="disabled", bg="#f0f0f0")
        self.output_text.pack(pady=5)

    def execute_crypto(self):
        # 1. קבלת הטקסט
        username = self.input_text.get("1.0", "end-1c")# קריאה מהשורה הראשונה ועד הסוף (פחות תו ירידת שורה)
        password = self.key_entry.get("1.0", "end-1c")
        if not username:
            messagebox.showwarning("Warning", "Please enter input text.")
            return

        # 2. קבלת הפרמטרים
        algo = self.algo_var.get()
        action = self.action_var.get()
        result = ""

        try:
            if algo == "login":


            # 4. הצגת התוצאה
            self.output_text.config(state="normal")  # אפשור כתיבה
            self.output_text.delete("1.0", "end")  # ניקוי טקסט קודם
            self.output_text.insert("1.0", result)  # הכנסת טקסט חדש
            self.output_text.config(state="disabled")  # נעילה מחדש

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()
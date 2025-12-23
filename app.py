# app.py
"""
Password Strength Checker — to avoid data breaches
"""

import re
import tkinter as tk
from tkinter import ttk, messagebox
import random, string, threading

# Optional NLTK dictionary check
nltk_words_set = None
try:
    import nltk
    from nltk.corpus import words as nltk_words
    try:
        nltk_words_set = set(word.lower() for word in nltk_words.words())
    except LookupError:
        def download_words():
            nltk.download("words")
        threading.Thread(target=download_words, daemon=True).start()
except:
    nltk_words_set = None

# Regex patterns
SPECIAL_RE = re.compile(r"[!@#$%^&*()_\-+=\[\]{};:'\",.<>/?\\|`~]")

# Common weak patterns
COMMON_PATTERNS = ["password", "qwerty", "admin", "1234", "123456"]

# Utility Functions 

def contains_dictionary_word(pw: str) -> bool:
    pw = pw.lower()

    for c in COMMON_PATTERNS:
        if c in pw:
            return True

    if nltk_words_set:
        for i in range(len(pw) - 3):
            for j in range(i+4, min(len(pw)+1, i+12)):
                if pw[i:j] in nltk_words_set:
                    return True

    return False

def analyze_password(pw: str):
    length = len(pw)
    lower = bool(re.search(r'[a-z]', pw))
    upper = bool(re.search(r'[A-Z]', pw))
    digit = bool(re.search(r'\d', pw))
    special = bool(SPECIAL_RE.search(pw))

    common = contains_dictionary_word(pw)

    score = 0
    score += 20 if length >= 12 else 10 if length >= 8 else 0
    score += 15 if lower else 0
    score += 15 if upper else 0
    score += 15 if digit else 0
    score += 15 if special else 0
    score += 20 if not common else 0

    score = min(score, 100)

    if score >= 80:
        label = "Strong"
    elif score >= 50:
        label = "Medium"
    else:
        label = "Weak"

    suggestions = []
    if length < 8: suggestions.append("Use at least 8 characters.")
    if not upper: suggestions.append("Add uppercase letters.")
    if not lower: suggestions.append("Add lowercase letters.")
    if not digit: suggestions.append("Include numbers.")
    if not special: suggestions.append("Include special characters.")
    if common: suggestions.append("Avoid common dictionary words.")

    return score, label, suggestions


# Attractive GUI

class PasswordChecker(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Password Strength Checker-avoid data breches")
        self.geometry("650x480")
        self.configure(bg="#f4f5f7")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="🔐 Password Strength Checker",
                         font=("Segoe UI", 20, "bold"), bg="#f4f5f7")
        title.pack(pady=10)

        frame = tk.Frame(self, bg="#f4f5f7")
        frame.pack(pady=10)

        tk.Label(frame, text="Enter Password:", font=("Segoe UI", 12),
                 bg="#f4f5f7").grid(row=0, column=0, sticky="w")

        self.pw_var = tk.StringVar()
        self.entry = tk.Entry(frame, textvariable=self.pw_var, width=40,
                              font=("Segoe UI", 11), show="*")
        self.entry.grid(row=1, column=0, padx=5, pady=5)

        self.show_var = tk.BooleanVar()
        tk.Checkbutton(frame, text="Show", variable=self.show_var,
                       command=self.toggle_show, bg="#f4f5f7").grid(row=1, column=1)

        tk.Button(self, text="Check Strength", width=20,
                  command=self.check_strength, bg="#4c84ff", fg="white",
                  font=("Segoe UI", 11, "bold")).pack(pady=5)

        tk.Button(self, text="Generate Strong Password", width=25,
                  command=self.generate_password, bg="#3bb273", fg="white",
                  font=("Segoe UI", 11, "bold")).pack(pady=5)

        # Strength bar
        self.strength_label = tk.Label(self, text="Strength: -",
                                       font=("Segoe UI", 13, "bold"),
                                       bg="#f4f5f7")
        self.strength_label.pack(pady=10)

        self.progress = ttk.Progressbar(self, length=400)
        self.progress.pack(pady=5)

        # Suggestions box
        tk.Label(self, text="Suggestions:", font=("Segoe UI", 12, "bold"),
                 bg="#f4f5f7").pack(pady=(15,0))

        self.suggestion_box = tk.Text(self, width=70, height=7,
                                      font=("Segoe UI", 10))
        self.suggestion_box.pack()

    def toggle_show(self):
        self.entry.config(show="" if self.show_var.get() else "*")

    def check_strength(self):
        pw = self.pw_var.get()
        if not pw:
            messagebox.showwarning("Input Error", "Please enter a password.")
            return

        score, label, suggestions = analyze_password(pw)

        self.progress["value"] = score
        self.progress.update()

        # Color-coded strength label
        if label == "Weak":
            color = "red"
        elif label == "Medium":
            color = "orange"
        else:
            color = "green"

        self.strength_label.config(text=f"Strength: {label} ({score}%)",
                                   fg=color)

        self.suggestion_box.delete(1.0, tk.END)
        for s in suggestions:
            self.suggestion_box.insert(tk.END, f"• {s}\n")

    def generate_password(self):
        password = (
            random.choice(string.ascii_uppercase) +
            random.choice(string.ascii_lowercase) +
            random.choice(string.digits) +
            random.choice("!@#$%^&*")
        )

        password += "".join(random.choice(
            string.ascii_letters + string.digits + "!@#$%^&*"
        ) for _ in range(8))

        password = ''.join(random.sample(password, len(password)))

        self.pw_var.set(password)
        self.check_strength()


if __name__ == "__main__":
    PasswordChecker().mainloop()

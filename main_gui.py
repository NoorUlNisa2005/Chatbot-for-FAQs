"""Simple chat window (Tkinter) for the FAQ chatbot.  Run:  python main_gui.py"""

import tkinter as tk
from tkinter import scrolledtext

from faq_bot import FAQChatbot

BG, USER_BG, BOT_BG = "#f4f6f8", "#d9ecff", "#ffffff"


class ChatApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("ShopEasy FAQ Chatbot")
        self.geometry("560x640")
        self.minsize(420, 480)
        self.configure(bg=BG)

        self.bot = FAQChatbot()
        self._build_widgets()
        self._add_message("Bot", "Hello! 👋 Ask me anything about orders, shipping, returns or payments.")

    def _build_widgets(self) -> None:
        header = tk.Label(self, text="🤖  FAQ Assistant", font=("Segoe UI", 14, "bold"),
                          bg="#2b6cb0", fg="white", pady=10)
        header.pack(fill=tk.X)

        self.chat = scrolledtext.ScrolledText(self, wrap=tk.WORD, state=tk.DISABLED,
                                              font=("Segoe UI", 11), bg=BG, bd=0,
                                              padx=10, pady=10)
        self.chat.pack(fill=tk.BOTH, expand=True)
        self.chat.tag_config("user", background=USER_BG, justify="right",
                             lmargin1=80, lmargin2=80, spacing1=6, spacing3=6)
        self.chat.tag_config("bot", background=BOT_BG, justify="left",
                             rmargin=80, spacing1=6, spacing3=6)
        self.chat.tag_config("hint", foreground="#666666", font=("Segoe UI", 9, "italic"))

        bottom = tk.Frame(self, bg=BG, pady=8, padx=8)
        bottom.pack(fill=tk.X)
        self.entry = tk.Entry(bottom, font=("Segoe UI", 11))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(0, 8))
        self.entry.bind("<Return>", self._on_send)
        self.entry.focus()
        tk.Button(bottom, text="Send", command=self._on_send, bg="#2b6cb0", fg="white",
                  font=("Segoe UI", 10, "bold"), padx=14, pady=4, relief=tk.FLAT).pack(side=tk.RIGHT)

    def _add_message(self, sender: str, text: str, hint: str = "") -> None:
        tag = "user" if sender == "You" else "bot"
        self.chat.config(state=tk.NORMAL)
        self.chat.insert(tk.END, f" {sender}: {text} \n", tag)
        if hint:
            self.chat.insert(tk.END, f"{hint}\n", "hint")
        self.chat.insert(tk.END, "\n")
        self.chat.config(state=tk.DISABLED)
        self.chat.see(tk.END)

    def _on_send(self, _event=None) -> None:
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, tk.END)
        self._add_message("You", text)

        reply = self.bot.get_response(text)
        hint = ""
        if reply.suggestions:
            hint = "Related: " + " | ".join(reply.suggestions)
        self._add_message("Bot", reply.answer, hint)


if __name__ == "__main__":
    ChatApp().mainloop()

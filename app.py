#NOCODESQL main app file
import customtkinter as ctk
import sqlite3
from tkinter import PhotoImage
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NoCodeSQL")
        self.geometry("850x575")
        self.configure(bg="#0F0F0F")
        self.resizable(False, False)
        self.iconbitmap("resources/logo.ico")

if __name__ == "__main__":
    app = App()
    app.mainloop()

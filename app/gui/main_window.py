import tkinter as tk

class MainWindow(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master 
        self.pack()
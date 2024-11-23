import tkinter as tk
from app import MainWindow

class App():
    def __init__(self):
        self.root = tk.Tk()
        self.main_window = MainWindow(self.root)

        pass

    def run(self):
        self.root.mainloop()
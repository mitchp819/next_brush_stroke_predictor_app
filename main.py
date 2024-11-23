from tkinter import Tk
from app import MainWindow

if __name__ == "__main__":
    root = Tk()
    app = MainWindow(master = root)
    app.mainloop()
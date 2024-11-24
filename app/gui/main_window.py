import tkinter as tk
from tkinter import Menu
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass


from app import WINDOW_TITLE, UI_COLOR, TRIM_COLOR, BG_COLOR, BrushTool

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(WINDOW_TITLE)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width - 200}x{screen_height - 200}+5+5")
        self.resizable(True, True)

        self.config_menu()

        main_frame = tk.Frame(self, bg=UI_COLOR)
        main_frame.pack(fill='both',expand=True, padx=10, pady=20)

        inner_frame =tk.Frame(main_frame, 
                              bg=BG_COLOR,
                              border = 3,
                              relief='sunken')
        inner_frame.pack(fill='both', expand= True, padx=2, pady=2)
        
        brush_tool = BrushTool(inner_frame) 



    def config_menu(self):
        menubar = Menu(self)
        self.config(menu = menubar)
        
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label='New')
        file_menu.add_command(label='Open')
        menubar.add_cascade(label="File", menu=file_menu)

        window = Menu(menubar, tearoff=0)
        window.add_command(label='New')
        window.add_command(label='Open')
        menubar.add_cascade(label="Window", menu=window)
        

        
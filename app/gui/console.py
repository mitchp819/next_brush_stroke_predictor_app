import tkinter as tk
from tkinter.scrolledtext import ScrolledText
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app import  UI_COLOR, TRIM_COLOR, CONSOLE_INTRO_TEXT, HEADER_HEIGHT

class AppConsole(tk.Frame):
    def __init__(self, container):
        super().__init__(container)


        main_frame = tk.Frame(container,
                              width=400,
                              bg = UI_COLOR,
                              border=4,
                              relief='raised')
        main_frame.pack(padx=10, pady=5)
        header =tk.Canvas(main_frame,
                          width=400 ,
                          height=HEADER_HEIGHT,
                          bg=TRIM_COLOR)
        header.pack(fill='x', pady=(0,3))

        self.console = ScrolledText(main_frame, 
                                    width = 30, 
                                    height = 4, 
                                    font = ("Consolas", 9))
        self.console.pack(padx=3,pady=3, fill='both')
        self.console['state'] = 'disabled'
        self.print_to_console(CONSOLE_INTRO_TEXT)
        
        
    def print_to_console(self, text):
        self.console['state'] = 'normal'
        self.console.insert('1.0', '\n')
        self.console.insert('1.0', text)
        self.console['state'] = 'disabled'

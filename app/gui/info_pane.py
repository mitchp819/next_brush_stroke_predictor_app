import tkinter as tk
from tkinter import ttk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app import UI_COLOR, BG_COLOR, TRIM_COLOR, SECONDARY_COLOR, HEADER_HEIGHT

class InfoPane(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        main_frame = tk.Frame(container,
                              width=400,
                              height=300,
                              bg = UI_COLOR,
                              border=4,
                              relief='raised')
        main_frame.pack(padx=10, pady=5)
        header =tk.Canvas(main_frame,
                          width=400 ,
                          height=HEADER_HEIGHT,
                          bg=TRIM_COLOR)
        header.pack(fill='x', pady=(0,3))

        loaded_db_label = tk.Label(main_frame,
                                   text="Active Database Generating: ",
                                   justify='left',
                                   bg=UI_COLOR)
        loaded_db_label.pack(fill='x')

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x')

        db_saved_to = tk.Label(main_frame,
                               text="Data Being Saved To: ",
                               justify='left',
                               bg= UI_COLOR)
        db_saved_to.pack(fill='x')
        
        
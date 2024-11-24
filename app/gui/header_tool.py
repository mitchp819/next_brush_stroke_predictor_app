import tkinter as tk
from enum import Enum
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app import UI_COLOR, BG_COLOR, TRIM_COLOR, SECONDARY_COLOR

class HeaderTool(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.data_gather_mode = 'auto'


        main_frame = tk.Frame(container, bg= UI_COLOR)
        self.create_data_gather_tool(main_frame)
        main_frame.pack(fill='x')  
        
        self.toggle_data_gather_mode(self.data_gather_mode)
        

    def create_data_gather_tool(self, container):
        d_g_frame = tk.Frame(container, bg=UI_COLOR)
        label = tk.Label(d_g_frame,
                         text="Data Gather Mode:",
                         bg= UI_COLOR,
                         font=("TkDefaultFont", 10))
        label.pack(side=tk.LEFT)

        self.auto_mode_btn = tk.Button(d_g_frame,
                                 text=" Auto ",
                                 command= lambda: self.toggle_data_gather_mode('auto'),
                                 bg='white',
                                 relief='raised'
                                 )
        self.auto_mode_btn.pack(side=tk.LEFT)
        self.manual_mode_btn = tk.Button(d_g_frame,
                                    text= "Manual",
                                    command= lambda: self.toggle_data_gather_mode('manual'),
                                    bg='darkgrey',
                                    relief='sunken')
        self.manual_mode_btn.pack(side=tk.LEFT)

        self.save_to_dataset_btn = tk.Button(d_g_frame,
                                             text= "Save Brush Stroke",
                                             bg=SECONDARY_COLOR,
                                             relief='groove',
                                             border=3,
                                             font=("TkDefaultFont", 10))
        self.save_to_dataset_btn.pack(side=tk.LEFT)
        d_g_frame.pack(side=tk.LEFT)




    
    def get_data_gather_mode(self):
        return self.data_gather_mode
    
    def toggle_data_gather_mode(self, input):
        if input == 'auto':
            self.data_gather_mode = 'auto'
            self.auto_mode_btn.config(bg='white', relief='raised')
            self.manual_mode_btn.config(bg='darkgrey', relief='sunken')
            self.save_to_dataset_btn.pack_forget()
        if input == 'manual':
            self.data_gather_mode = 'manual'
            self.auto_mode_btn.config(bg='darkgrey', relief='sunken')
            self.manual_mode_btn.config(bg='white', relief='raised')
            self.save_to_dataset_btn.pack(side=tk.LEFT, padx=(5,0))
        pass
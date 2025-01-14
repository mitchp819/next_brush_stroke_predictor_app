import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import askokcancel, showinfo, WARNING
from PIL import Image
import numpy as np
from enum import Enum
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app import UI_COLOR, SECONDARY_COLOR, get_all_DATABASES
#from config_data_window.config_data_main import ConfigDataWindow

class HeaderTool(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.app_console = None
        self.drawing_canvas = None
        self.data_gather_mode = 'auto'

        main_frame = tk.Frame(container, bg= UI_COLOR)
        main_frame.pack(fill='x')  

        save_image_btn = tk.Button(main_frame, 
                                     text = "Save Image",
                                     bg = SECONDARY_COLOR,
                                     relief='groove',
                                     border=3,
                                     command= self.save_image,
                                     font=("TkDefaultFont", 10))
        save_image_btn.pack(side = tk.LEFT, padx=10)
        save_dataset_btn = tk.Button(main_frame, 
                                     text = "Save Dataset",
                                     bg = SECONDARY_COLOR,
                                     relief='groove',
                                     border=3,
                                     command= self.save_dataset_to_db,
                                     font=("TkDefaultFont", 10))
        save_dataset_btn.pack(side=tk.LEFT, padx=10)
        open_config_data_btn = tk.Button(main_frame, 
                                     text = "Configure Data",
                                     bg = SECONDARY_COLOR,
                                     relief='groove',
                                     border=3,
                                     command= self.open_config_data,
                                     font=("TkDefaultFont", 10))
        open_config_data_btn.pack(side=tk.RIGHT, padx=10)
        load_img_btn = tk.Button(main_frame,
                                 text="Load Image",
                                 bg = SECONDARY_COLOR,
                                 relief='groove',
                                 border=3,
                                 command= self.load_image,
                                 font=("TkDefaultFont", 10))
        load_img_btn.pack(side=tk.RIGHT, padx=10)
        flood_canvas_btn= tk.Button(main_frame,
                                    text="Flood Canvas",
                                    bg = SECONDARY_COLOR,
                                    relief='groove',
                                    border=3,
                                    command= self.flood_canvas,
                                    font=("TkDefaultFont", 10))
        flood_canvas_btn.pack(side=tk.RIGHT, padx=10)
        self.create_data_gather_tool(main_frame)
        self.after(200, self.open_config_data)

    def set_drawing_canvas(self, drawing_canvas):
        self.drawing_canvas = drawing_canvas
    def set_app_console(self, app_console):
        self.app_console = app_console
    def set_info_pane(self, info_pane):
        self.info_pane = info_pane

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

        self.reset_stroke_btn = tk.Button(d_g_frame,
                                    text = "Reset Stroke",
                                    command= self.reset_stroke,
                                    relief='groove')
        self.reset_stroke_btn.pack(side=tk.LEFT, padx=10)
        

        self.save_to_dataset_btn = tk.Button(d_g_frame,
                                             text= "Save Brush Stroke",
                                             bg=SECONDARY_COLOR,
                                             relief='groove',
                                             border=3,
                                             command= self.save_to_dataset,
                                             font=("TkDefaultFont", 10))
        self.save_to_dataset_btn.pack(side=tk.LEFT)

        d_g_frame.pack(side=tk.LEFT, padx=10)




    
    def get_data_gather_mode(self):
        return self.data_gather_mode
    
    def toggle_data_gather_mode(self, input):
        if input == 'auto':
            self.data_gather_mode = 'auto'
            self.auto_mode_btn.config(bg='white', relief='raised')
            self.manual_mode_btn.config(bg='darkgrey', relief='sunken')
            self.save_to_dataset_btn.pack_forget()
            self.reset_stroke_btn.pack_forget()
            self.app_console.print_to_console("Data Gather Mode: Auto")
        if input == 'manual':
            self.data_gather_mode = 'manual'
            self.auto_mode_btn.config(bg='darkgrey', relief='sunken')
            self.manual_mode_btn.config(bg='white', relief='raised')
            self.save_to_dataset_btn.pack(side=tk.LEFT, padx=10)
            self.reset_stroke_btn.pack(side=tk.LEFT)
            self.app_console.print_to_console("Data Gather Mode: Manual")
        pass

    def open_config_data(self):
        from app import ConfigDataWindow
        config_window = ConfigDataWindow()
        config_window.set_info_pane(self.info_pane)
        pass

    def save_to_dataset(self):
        self.drawing_canvas.save_stroke_to_dataset()
        pass

    def reset_stroke(self):
        self.drawing_canvas.reset_stroke()
        pass

    def flood_canvas(self):
        self.drawing_canvas.flood_canvas()

    def save_dataset_to_db(self):
        databases = get_all_DATABASES()
        print(databases)
        for db, values in databases.items():
            if values[0] == 1:
                print(f"Saveing Dataset to Database: {db}")
                self.drawing_canvas.save_dataset_to_db(db)
        pass

    def save_image(self):
        self.drawing_canvas.save_image()
        pass

    def load_image(self):
        filetypes = (
            ('png files', '*.png'),
            ('All files', '*.*')
        )
        image_file_path = fd.askopenfilename(title= "Load 128x128 png to canvas",
                                             filetypes=filetypes)
        image = Image.open(image_file_path).convert('L')
        image_array = np.array(image)
        print(image_array.shape)
        if image_array.shape[0] != 128 or image_array.shape[1] != 128:
            if image_array.shape[0] == image_array.shape[1]:
                answer = askokcancel(title="WARNING Image will be scaled to 128x128",
                                    message = f"WARNING: The selected image of size {image_array.shape[0]}x{image_array.shape[1]} will be loaded as a 128x128 black and white image. Select Ok to proceed"
                                    )
            else:
                answer = askokcancel(title="WARNING Image is not square",
                                    message = f"WARNING: The selected image of size {image_array.shape[0]}x{image_array.shape[1]} will be loaded as a 128x128 black and white image. Proceeding will stretch and shrink image to become compatable. Consider croping the image into a square",
                                    icon =WARNING)
                if answer == 1:
                    answer = askokcancel(title="Confirm warp image",
                                    message = f"Are you sure you want to warp the selected {image_array.shape[0]}x{image_array.shape[1]} into a 128x128 black and white image?",
                                    icon =WARNING)
            if answer == 0:
                return
            new_image= image.resize((128, 128), Image.NEAREST)
            image_array = np.array(new_image)
        self.drawing_canvas.load_img_to_canvas(image_array)
        pass

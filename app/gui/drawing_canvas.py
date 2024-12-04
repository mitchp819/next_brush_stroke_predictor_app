import tkinter as tk
from tkinter import ttk
import numpy as np
from PIL import Image
import os
import re

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app import greyscale_value_to_hex, ROOT_DIR, DATA_DIR, get_a_DATABASE, ImageProcessor, get_LOADED_DB

class DrawingCanvasFrame(ttk.Frame):
    def __init__(self, container, image_scalor = 6, image_width = 128, image_height = 128):
        super().__init__(container)

        self.img_x = image_width
        self.img_y = image_height
        self.img_sclr = image_scalor
        self.win_x = self.img_x * self.img_sclr
        self.win_y = self.img_y * self.img_sclr
        self.brush_tool = None
        self.data_gather_tool = None
        self.app_console = None
        self.gen_tool = None

        self.img_generator = ImageProcessor()
        
        #gui
        self.canvas = tk.Canvas(self, width=self.win_x, height=self.win_y, bg='white')
        self.canvas.pack()
        self.pack(side=tk.LEFT, expand= True)

        #numpy arrays for canvas and stroke
        self.np_main_canvas_data = np.ones((self.img_x, self.img_y), dtype= np.uint8) * 255
        self.np_stroke_canvas_data = np.full((self.img_x, self.img_y), -1)
        self.last_canvas = self.np_main_canvas_data.flatten()
        self.compiled_data = None
        self.stroke_count = 0

        #Event binding
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.create_mark)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_released)
        pass

    def set_brush_tool(self, brush_tool):
        self.brush_tool = brush_tool
    def set_data_gather_tool(self, data_gather_tool):
        self.data_gather_tool = data_gather_tool
    def set_app_console(self, app_console):
        self.app_console = app_console
    def set_gen_tool(self, gen_tool):
        self.gen_tool = gen_tool
    
    def on_mouse_down(self, event):
        if  self.data_gather_tool.get_data_gather_mode() == 'auto':
            #Whipe np stroke canvas
            self.np_stroke_canvas_data = np.full((self.img_x, self.img_y), -1)
        self.create_mark(event)
        pass

    def on_mouse_released(self, event):
        if self.data_gather_tool.get_data_gather_mode() == 'auto':
            self.save_stroke_to_dataset()
        pass

    def create_mark(self, event):
        #variables
        greyscale_value = self.brush_tool.get_greyscale_value()
        greyscale_hex = greyscale_value_to_hex(greyscale_value)
        brush_size = self.brush_tool.get_brush_size()
        
        x = event.x // self.img_sclr
        y = event.y // self.img_sclr

        rect = self.canvas.create_rectangle(x * self.img_sclr, y * self.img_sclr,
                            (x + 1) * self.img_sclr, (y + 1) * self.img_sclr,
                            fill= greyscale_hex, outline=greyscale_hex, width= brush_size)

        #converts canvas rect into image coords
        x1, y1, x2, y2 = self.canvas.bbox(rect)
        x1 = int(x1 // self.img_sclr)
        y1 = int(y1 // self.img_sclr)
        x2 = int(x2 // self.img_sclr)
        y2 = int(y2 // self.img_sclr)

        #update np canvas data
        for x in range(x1, x2):
            for y in range(y1, y2):
                if (x < self.img_x and x >= 0 and y < self.img_y and y >= 0):
                    self.np_main_canvas_data[y, x] = greyscale_value
                    self.np_stroke_canvas_data[y, x] = greyscale_value
        pass
    
    def save_stroke_to_dataset(self):
        #flatten and normalize between 0-1
        flat_normal_last_canvas = self.last_canvas.flatten() / 255
        flat_normal_stroke_canvas = self.np_stroke_canvas_data.flatten() /255
        
        #saves color values in array
        filler =  np.array([.5])
        color_data = np.array([self.brush_tool.get_greyscale_value() / 255])
        
        flat_normal_last_canvas = np.concatenate((flat_normal_last_canvas,filler))
        flat_normal_stroke_canvas = np.concatenate((flat_normal_stroke_canvas, color_data))

        insertion_data = np.array([flat_normal_last_canvas, flat_normal_stroke_canvas])
        insertion_data = insertion_data[np.newaxis, :]

        #overwrites data
        self.last_canvas = self.np_main_canvas_data
        self.stroke_count += 1

        #cats insertion data with compiled data
        if self.compiled_data is None:
            self.compiled_data = insertion_data
        else:
            self.compiled_data = np.concatenate((self.compiled_data, insertion_data), axis=0)
        self.app_console.print_to_console("Saved to Dataset: " + str(self.compiled_data.shape))
        print(self.compiled_data.shape)
        pass

    def save_dataset_to_db(self, database_folder):
        pil_main_img = Image.fromarray(self.np_main_canvas_data, mode="L")
        root_path = ROOT_DIR
        ds_id = get_a_DATABASE(database_folder)[1]

        #save npy to folder
        data_relative_path = f'data/{database_folder}/image_data/img{ds_id}data.npy'
        data_absolute_path = os.path.join(root_path, data_relative_path)
        np.save(data_absolute_path, self.compiled_data)

        #save png to folder
        png_relative_path = f'data/{database_folder}/final_image/img{ds_id}.png'
        png_absolute_path = os.path.join(root_path, png_relative_path)
        pil_main_img.save(png_absolute_path)

        self.app_console.print_to_console(f"Dataset saved to Database: {database_folder}")
        print("Image and Data Saved")
        pass

    def reset_stroke(self):
        self.np_stroke_canvas_data = np.full((self.img_x, self.img_y), -1)
        self.app_console.print_to_console("Stroke Data Reset")
        print("Stroke Data Reset")
        pass

    def generate_stroke(self):
        threshold = self.gen_tool.get_threshold()

        gen_database = get_LOADED_DB()
        pre_path = os.path.join(DATA_DIR, f"{gen_database}/gen_data")
        d4_path = os.path.join(pre_path, "4_data.npy")
        d8_path = os.path.join(pre_path, "8_data.npy")
        d16_path = os.path.join(pre_path, "16_data.npy")
        d32_path = os.path.join(pre_path, "32_data.npy")
        d64_path = os.path.join(pre_path, "64_data.npy")
        d128_path = os.path.join(pre_path, "128_data.npy")
        all_downscaled_data_paths = [d128_path, d64_path, d32_path, d16_path, d8_path, d4_path]

        #self.img_generator.set_downscaled_data(all_downscaled_data_paths)
        self.img_generator.set_data(d4_path, d8_path, d16_path, d32_path, d64_path, d128_path)

        #Create input img to be sent for processing
        img_flat = self.np_main_canvas_data.flatten() / 255
        filler =  np.array([.5])
        input_img = np.concatenate((img_flat, filler))
        Image.fromarray(self.np_main_canvas_data.astype('uint8'), 'L').save("assets/similar-images/input_canvas.png")

        #Send input to image_processing script
        output_stroke = self.img_generator.compare_img_with_downscaled_data_set(input_img)
        pass

def get_last_file_id(data_base):
    dir_path = f'data/{data_base}/image_data'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    files_list = [f for f in os.listdir(dir_path)
                  if os.path.isfile(os.path.join(dir_path, f))]
    largest_id = 0
    for file in files_list:
        integers = [int(s) for s in re.findall(r'\d+', file)]
        if(integers[0] > largest_id):
            largest_id = integers[0]
    return largest_id
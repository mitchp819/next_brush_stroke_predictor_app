import tkinter as tk
from tkinter import ttk
from typing import Literal
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

from app import  ImageProcessor, greyscale_value_to_hex, shape_img, get_a_DATABASE, get_LOADED_DB, get_last_file_by_id, canvas_np_img_to_png, UI_COLOR, ASSETS_DIR, DATA_DIR, SIMILAR_IMAGES_DIR

class DrawingCanvasFrame(ttk.Frame):
    """Drawing Canvas Frame that collects (prev-canvas, brush_stroke) pairs and saves as dataset"""
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
        self.info_pane = None

        self.img_generator = ImageProcessor()
        
        #gui
        main_frame = tk.Frame(self,border=3, relief='raised', bg=UI_COLOR)
        main_frame.pack()
        
        self.canvas = tk.Canvas(main_frame, 
                                width=self.win_x, 
                                height=self.win_y, 
                                bg='white',
                                border=2,
                                relief='groove'
                                )
        self.canvas.pack(pady=10,padx=10)
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
    def set_info_pane(self, info_pane):
        self.info_pane = info_pane
    
    def on_mouse_down(self, event):
        if  self.data_gather_tool.get_data_gather_mode() == 'auto':
            self.np_stroke_canvas_data = np.full((self.img_x, self.img_y), -1)
        self.create_mark(event)
        pass

    def on_mouse_released(self, event):
        if self.data_gather_tool.get_data_gather_mode() == 'auto':
            self.save_stroke_to_dataset()
        pass
    
    def create_mark(self, event):
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
        edge_to_shape_ratio = get_edge_to_shape_ratio(self.np_stroke_canvas_data)
        if edge_to_shape_ratio == -1:
            self.app_console.print_to_console("No brush stroke data to save")
            return
        #Create Insertion Data
        edge_to_shape_ratio_np_array = np.array([edge_to_shape_ratio])
        filler =  np.array([.5])
        flat_normal_last_canvas = self.last_canvas.flatten() / 255
        flat_normal_stroke_canvas = self.np_stroke_canvas_data.flatten() /255
        flat_normal_last_canvas = np.concatenate((flat_normal_last_canvas,filler))
        flat_normal_stroke_canvas = np.concatenate((flat_normal_stroke_canvas, edge_to_shape_ratio_np_array))
        insertion_data = np.array([flat_normal_last_canvas, flat_normal_stroke_canvas])
        insertion_data = insertion_data[np.newaxis, :]
        #Overwrites data
        self.last_canvas = self.np_main_canvas_data
        self.stroke_count += 1
        self.np_stroke_canvas_data.fill(-1)
        #Cats insertion data with compiled data
        if self.compiled_data is None:
            self.compiled_data = insertion_data
        else:
            self.compiled_data = np.concatenate((self.compiled_data, insertion_data), axis=0)
        self.app_console.print_to_console("Saved to Dataset: " + str(self.compiled_data.shape))
        print(self.compiled_data.shape)
        pass

    def save_dataset_to_db(self, database_folder:str):
        ds_id = get_a_DATABASE(database_folder)[1]

        #save npy to folder
        data_relative_path = f'{database_folder}/image_data/img{ds_id}data.npy'
        data_absolute_path = os.path.join(DATA_DIR, data_relative_path)
        np.save(data_absolute_path, self.compiled_data)

        #save png to folder
        png_relative_path = f'{database_folder}/final_image/img{ds_id}.png'
        png_absolute_path = os.path.join(DATA_DIR, png_relative_path)
        print(png_absolute_path)
        image_array = self.np_main_canvas_data.astype(np.uint8)
        pil_main_img = Image.fromarray(image_array, mode="L")
        pil_main_img.save(png_absolute_path)

        self.app_console.print_to_console(f"Dataset saved to Database: {database_folder}")
        print("Image and Data Saved")
        pass

    def reset_stroke(self):
        self.np_stroke_canvas_data = np.full((self.img_x, self.img_y), -1)
        self.app_console.print_to_console("Stroke Data Reset")
        self.last_canvas = self.np_main_canvas_data.flatten()
        print("Stroke Data Reset")
        pass

    def generate_stroke(self, type: Literal['any', 'line', 'shape']):
        thresholds :dict = self.gen_tool.get_thresholds()
        print(thresholds)

        gen_database = get_LOADED_DB()
        pre_path = os.path.join(DATA_DIR, f"{gen_database}/gen_data")
        d4_path = os.path.join(pre_path, "4_data.npy")
        d8_path = os.path.join(pre_path, "8_data.npy")
        d16_path = os.path.join(pre_path, "16_data.npy")
        d32_path = os.path.join(pre_path, "32_data.npy")
        d64_path = os.path.join(pre_path, "64_data.npy")
        d128_path = os.path.join(pre_path, "128_data.npy")

        #sets data and thrshold
        self.img_generator.set_data(d4_path, d8_path, d16_path, d32_path, d64_path, d128_path)
        self.img_generator.set_tolerance_dict(thresholds)

        #Create input img to be sent for processing
        img_flat = self.np_main_canvas_data.flatten() / 255
        filler =  np.array([.5])
        input_img = np.concatenate((img_flat, filler))
        Image.fromarray(self.np_main_canvas_data.astype('uint8'), 'L').save(os.path.join(SIMILAR_IMAGES_DIR, "input_img.png"))

        #Send input to image_processing script
        output_stroke = self.img_generator.compare_img_with_downscaled_data_set(input_img, type)
        if not isinstance(output_stroke, np.ndarray):
            print("Error: output_stroke is not a np.ndarray")
            return

        output_stroke = output_stroke[:-1]
        output_stroke = shape_img(output_stroke)

        for row, column_array in enumerate(output_stroke):
            for col, pixel_value in enumerate(column_array):
                pxl255 = int(pixel_value*255)
                if pxl255 >=0:
                    greyscale_hex = greyscale_value_to_hex(pxl255)
                    self.canvas.create_rectangle(col * self.img_sclr, row * self.img_sclr, (col+1) * self.img_sclr, (row+1) * self.img_sclr , outline = greyscale_hex, fill=greyscale_hex)
                    self.np_main_canvas_data[row, col] = pxl255
        
        self.info_pane.set_image_frame()
        pass

    def save_image(self):
        saved_img_folder = os.path.join(ASSETS_DIR, "saved-images")
        larget_id = get_last_file_by_id(saved_img_folder)
        save_name = f"saved_img{larget_id+1}.png"
        print(f"np_main_canvas_data shape = {self.np_main_canvas_data.shape}" )
        image_array = self.np_main_canvas_data.astype(np.uint8)
        image = Image.fromarray(image_array)
        scaled_image = image.resize((128*6, 128*6), Image.NEAREST)
        save_path = os.path.join(saved_img_folder, save_name)
        scaled_image.save(save_path)
        self.app_console.print_to_console(f"Image saved to saved-images folder\n under the name {save_name}")
        pass
        
    def load_img_to_canvas(self, image: np.array):
        for row, column_array in enumerate(image):
            for col, pixel_value in enumerate(column_array):  
                greyscale_hex = greyscale_value_to_hex(pixel_value)
                self.canvas.create_rectangle(col * self.img_sclr, row * self.img_sclr, (col+1) * self.img_sclr,
                                              (row+1) * self.img_sclr , outline = greyscale_hex, fill=greyscale_hex)
                self.np_main_canvas_data[row, col] = pixel_value
        self.last_canvas = self.np_main_canvas_data.flatten()
        pass

    def flood_canvas(self):
        """
        Fills the canvas with a single greyscale value
        Args:
            self (DrawingCanvasFrame): The DrawingCanvasFrame object
        """
        greyscale_value = self.brush_tool.get_greyscale_value()
        greyscale_hex = greyscale_value_to_hex(greyscale_value)

        self.canvas.create_rectangle(0, 0, self.win_x+self.img_sclr, self.win_y+self.img_sclr, fill=greyscale_hex, outline=greyscale_hex)
        self.np_main_canvas_data = np.full((self.img_x, self.img_y), greyscale_value)
        self.np_stroke_canvas_data = np.full((self.img_x, self.img_y), -1)
        self.last_canvas = self.np_main_canvas_data.flatten()

def get_edge_to_shape_ratio(np_stroke_img: np.array):
    edge_count = get_edge_count(np_stroke_img)
    shape_count = get_shape_count(np_stroke_img)
    if shape_count <= 0:
        return -1
    edge_to_shape_ratio = edge_count / shape_count 
    print(f"edge count = {edge_count}, shape count = {shape_count}, ratio = {edge_to_shape_ratio}")
    return edge_to_shape_ratio

def get_edge_count(np_image: np.array):
    edges = np.zeros_like(np_image)
    edge_count = 0
    for x in range(1, np_image.shape[0]-1):
        for y in range(1, np_image.shape[1]-1):
            neighbors_sum = (
                np_image[x-1, y-1] + np_image[x-1, y]
                + np_image[x-1, y+1] + np_image[x, y+1] + np_image[x+1, y+1]
                + np_image[x+1, y] + np_image[x+1, y-1] + np_image[x, y-1]
            )
            neighbors_avg = neighbors_sum/8
            edge_value = abs(np_image[x,y] - neighbors_avg) * 255
            edges[x,y] = edge_value
            if edge_value > 0: 
                edge_count += 1
    Image.fromarray(edges.astype('uint8'), 'L').save(os.path.join(ASSETS_DIR, "edges.png"))
    return edge_count

def get_shape_count(np_image: np.array):
    """
    Counts the number non-blank pixels on a canvas.

    Args:
        np_image (2d np.array): (width, height) = pixel value
    
    Returns:
        int: The Count of non-blank pixels
    """
    shape_count = 0
    for x in range(np_image.shape[0]):
        for y in range(np_image.shape[1]):
            if np_image[x,y] >= 0:
                shape_count += 1
    return shape_count
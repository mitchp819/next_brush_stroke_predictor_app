import tkinter as tk
from tkinter import ttk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app import  UI_COLOR, TRIM_COLOR, SECONDARY_COLOR, HEADER_HEIGHT,greyscale_value_to_hex


class BrushTool(tk.Frame):
    def __init__(self, container, image_scalor = 6):
        super().__init__(container)
        self.img_sclr = image_scalor
        self.brush_size = tk.IntVar()
        self.brush_size.set(1)
        self.greyscale_value = tk.IntVar()
        self.greyscale_value.set(0)

        frame_width = 120
        main_frame = tk.Frame(container,
                              width=120,
                              height=610,
                              bg=UI_COLOR,
                              border = 4,
                              relief='raised')
        main_frame.pack(side = tk.LEFT, padx=10, pady=5)
        header =tk.Canvas(main_frame,
                          width=frame_width ,
                          height=HEADER_HEIGHT,
                          bg=TRIM_COLOR)
        header.pack(fill='x', pady=(0,3))
        self.create_sample_brush_frame(main_frame)
        self.create_slider_frame(main_frame)
        generate_stroke_btn = tk.Button(main_frame,
                                        text="Generate",
                                        font=("TkDefaultFont", 10),
                                        relief='groove',
                                        borderwidth=5 ,
                                        bg = SECONDARY_COLOR)
        generate_stroke_btn.pack( pady = 3, padx=3, fill='x')
        
    def get_greyscale_value(self):
        return self.greyscale_value.get()
    def get_brush_size(self):
        return self.brush_size.get()

    def create_sample_brush_frame(self, container):
        frame = tk.Frame(
            container,
            height = 80,
            width= 80,
            bg= SECONDARY_COLOR,
            border=4,
            relief='groove'
        )

        frame.pack_propagate(False)

        self.sample_brush = tk.Canvas(
            frame,
            width = 30,
            height = 30,
            bg = 'black'
        )
        self.sample_brush.pack(expand=True)
        frame.pack(padx=2,pady=5)
        pass

    def create_slider_frame(self, container):
        slider_frame = tk.Frame(container, bg = UI_COLOR)
        slider_frame.columnconfigure(0, weight=1)
        slider_frame.columnconfigure(1, weight=1)

        self.greyscale_value_label = tk.Label(slider_frame, text="x", bg=UI_COLOR)
        self.greyscale_value_label.grid(column=1, row=0)
        self.brush_size_label = tk.Label(slider_frame, text="x",bg=UI_COLOR)
        self.brush_size_label.grid(column=0, row=0)

        brush_size_slider = tk.Scale(
            slider_frame,
            from_=50,
            to=1,
            length=300,
            orient='vertical',
            variable=self.brush_size,
            showvalue=False,
            width=30,
            bg=SECONDARY_COLOR,
            foreground='black',
            command = self.update_sample_brush
        )
        brush_size_slider.grid(column=0,row=1, padx=3,pady=3)

        greyscale_value_slider = tk.Scale(
            slider_frame,
            from_=255,
            to=0,
            length=300,
            orient='vertical',
            variable=self.greyscale_value,
            showvalue=False,
            width=30,
            bg=SECONDARY_COLOR,
            command = self.update_sample_brush
        )
        greyscale_value_slider.grid(column=1,row=1, padx=3, pady=3)
        
        greyscale_value_txt = tk.Label(slider_frame, text="Color", bg = UI_COLOR)
        greyscale_value_txt.grid(column=1, row=3,pady=3)
        brush_size_txt = tk.Label(slider_frame, text="Size", bg= UI_COLOR)
        brush_size_txt.grid(column=0, row=3, pady=3)

        slider_frame.pack(pady=3, fill='x')
        self.update_sample_brush(0)
        pass

    def update_sample_brush(self,v):
        greyscale_hex = greyscale_value_to_hex(self.greyscale_value.get())
        sample_width = self.brush_size.get() + self.img_sclr
        self.sample_brush.config(
            width = sample_width,
            height = sample_width,
            bg = greyscale_hex
        )
        self.greyscale_value_label.config(text=self.greyscale_value.get())
        self.brush_size_label.config(text= self.brush_size.get())
        pass


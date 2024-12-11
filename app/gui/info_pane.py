import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import os
from PIL import Image
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app import UI_COLOR, BG_COLOR, TRIM_COLOR, SECONDARY_COLOR, HEADER_HEIGHT, ASSETS_DIR

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

        #scrollbar = tk.Scrollbar(self, orient='vertical', command=main_frame.yview)

        self.loaded_db_label = tk.Label(main_frame,
                                   text="Active Database Generating: ",
                                   justify='left',
                                   bg=UI_COLOR)
        self.loaded_db_label.pack(fill='x')

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x')

        self.db_saved_to = tk.Label(main_frame,
                               text="Data Being Saved To: ",
                               justify='left',
                               bg= UI_COLOR)
        self.db_saved_to.pack(fill='x')

        ttk.Separator(main_frame, orient='horizontal').pack(fill='x')

        self.create_info_image_frame(main_frame)
        
        pass 

    def set_loaded_db(self, db: str):
        self.loaded_db_label.config(text= f"Active Database Generating: {db}")
        pass

    def set_db_saved_to(self, db_list: list):
        text_out = "Data Being Saved To: "
        for db in db_list:
            text_out = text_out + db + ", "
        self.db_saved_to.config(text=text_out)
        pass

    def create_info_image_frame(self, container):
        images_frame = tk.Frame(container, bg=UI_COLOR)
        images_frame.pack(fill='x')
        images_frame.columnconfigure(0, weight=1)
        images_frame.columnconfigure(1, weight=1)

        input_img_lbl = tk.Label( images_frame,text = "Input Image")
        input_img_lbl.grid(column=0, row=0, sticky= tk.N)
        similar_img_lbl = tk.Label(images_frame, text="Similar Image ")
        similar_img_lbl.grid(column=1, row=0, sticky= tk.N)

        folder_path = os.path.join(ASSETS_DIR, "similar-images")

        input128img = tk.PhotoImage(file = os.path.join(folder_path, "input_canvas.png"))
        lbl_i128 = tk.Label(images_frame, image=input128img).grid(column=0, row=1, sticky = tk.N, pady=2)
        input64img = tk.PhotoImage(file = os.path.join(folder_path, "input64.png"))
        lbl_i64 = tk.Label(images_frame, image=input64img).grid(column=0, row=2, sticky = tk.N, pady=2)
        input32img = tk.PhotoImage(file = os.path.join(folder_path, "input32.png"))
        lbl_i32 = tk.Label(images_frame, image=input32img).grid(column=0, row=3, sticky = tk.N, pady=2)
        input16img = tk.PhotoImage(file = os.path.join(folder_path, "input16.png"))
        lbl_i16 = tk.Label(images_frame, image=input16img).grid(column=0, row=4, sticky = tk.N, pady=2)
        input8img = tk.PhotoImage(file = os.path.join(folder_path, "input8.png"))
        lbl_i8 = tk.Label(images_frame, image=input8img).grid(column=0, row=5, sticky = tk.N, pady=2)
        input4img = tk.PhotoImage(file = os.path.join(folder_path, "input4.png"))
        lbl_i4 = tk.Label(images_frame, image=input4img).grid(column=0, row=6, sticky = tk.N, pady=2)

        similar128img = tk.PhotoImage(file = os.path.join(folder_path, "similar128.png"))
        lbl_s128 = tk.Label(images_frame, image=similar128img)
        lbl_s128.image = similar128img
        lbl_s128.grid(column=1, row=1, sticky = tk.N, pady=2)

        similar64img = tk.PhotoImage(file = os.path.join(folder_path, "similar64.png"))
        lbl_s64 = tk.Label(images_frame, image=similar64img)
        lbl_s64.image =similar64img
        lbl_s64.grid(column=1, row=2, sticky = tk.N, pady=2)

        similar32img = tk.PhotoImage(file = os.path.join(folder_path, "similar32.png"))
        lbl_s32 = tk.Label(images_frame, image=similar32img)
        lbl_s32.image = similar32img
        lbl_s32.grid(column=1, row=3, sticky = tk.N, pady=2)

        similar16img = tk.PhotoImage(file = os.path.join(folder_path, "similar16.png"))
        lbl_s16 = tk.Label(images_frame, image=similar16img)
        lbl_s16.image = similar16img
        lbl_s16.grid(column=1, row=4, sticky = tk.N, pady=2)

        similar8img = tk.PhotoImage(file = os.path.join(folder_path, "similar8.png"))
        lbl_s8 = tk.Label(images_frame, image=similar8img)
        lbl_s8.image = similar8img
        lbl_s8.grid(column=1, row=5, sticky = tk.N, pady=2)

        similar4img = tk.PhotoImage(file = os.path.join(folder_path, "similar4.png"))
        lbl_s4 = tk.Label(images_frame, image=similar4img)
        lbl_s4.image = similar4img
        lbl_s4.grid(column=1, row=6, sticky = tk.N, pady=2)
        pass
        
        
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import os
from PIL import Image, ImageTk
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

        scroll_frame = self.create_scrollbar(main_frame)

        w = tk.Canvas(scroll_frame, width=380, height=1, bg=UI_COLOR)
        w.pack()

        self.loaded_db_label = tk.Label(scroll_frame,
                                   text="Active Database Generating: ",
                                   justify='left',
                                   bg=UI_COLOR
                                   )
        self.loaded_db_label.pack(fill='x')

        ttk.Separator(scroll_frame, orient='horizontal').pack(fill='x')

        self.db_saved_to = tk.Label(scroll_frame,
                               text="Data Being Saved To: ",
                               justify='left',
                               bg= UI_COLOR)
        self.db_saved_to.pack(fill='x')

        ttk.Separator(scroll_frame, orient='horizontal').pack(fill='x')

        self.create_info_image_frame(scroll_frame)
        
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

    def on_configure(self, event):
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        self.scroll_canvas.itemconfig("window", width = event.width)

    def create_scrollbar(self, container):
        self.scroll_canvas = tk.Canvas(container, width=350, height=300, bg= UI_COLOR)
        scrollbar = ttk.Scrollbar(container, orient='vertical', command=self.scroll_canvas.yview)
        scrollbar.pack(side="right", fill='y')
        self.scroll_canvas.pack(side='left', fill='both', expand=True)
        self.scroll_canvas.configure(yscrollcommand=scrollbar.set)
        scrollable_frame = ttk.Frame(self.scroll_canvas)
        self.scroll_canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
        scrollable_frame.bind("<Configure>", self.on_configure)
        return scrollable_frame

    def load_image(self, grid_container: tk.Frame, row:int, column:int, scale: int, file_name: str):
        folder_path = os.path.join(ASSETS_DIR, "similar-images")
        pil_img = Image.open(os.path.join(folder_path, file_name))
        width, height = pil_img.size
        scaled_img = pil_img.resize((int(width*scale * 1.5), int(height*scale *1.5)), Image.NEAREST)
        tk_img = ImageTk.PhotoImage(scaled_img)
        img_lbl = tk.Label(grid_container, image=tk_img)
        img_lbl.image = tk_img
        img_lbl.grid(column=column, row=row, pady = 3, padx =3)
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

        self.load_image(grid_container= images_frame, row=1, column=0, scale=1, file_name="input_canvas.png")
        self.load_image(grid_container= images_frame, row=2, column=0, scale=2, file_name="input64.png")
        self.load_image(grid_container= images_frame, row=3, column=0, scale=4, file_name="input32.png")
        self.load_image(grid_container= images_frame, row=4, column=0, scale=8, file_name="input16.png")
        self.load_image(grid_container= images_frame, row=5, column=0, scale=16, file_name="input8.png")
        self.load_image(grid_container= images_frame, row=6, column=0, scale=32, file_name="input4.png")



        self.load_image(grid_container= images_frame, row=1, column=1, scale=1, file_name="similar128.png")
        self.load_image(grid_container= images_frame, row=2, column=1, scale=2, file_name="similar64.png")
        self.load_image(grid_container= images_frame, row=3, column=1, scale=4, file_name="similar32.png")
        self.load_image(grid_container= images_frame, row=4, column=1, scale=8, file_name="similar16.png")
        self.load_image(grid_container= images_frame, row=5, column=1, scale=16, file_name="similar8.png")
        self.load_image(grid_container= images_frame, row=6, column=1, scale=32, file_name="similar4.png")



      
        pass
        
        
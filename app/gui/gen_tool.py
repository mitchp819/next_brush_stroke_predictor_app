import tkinter as tk
from tkinter import ttk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app import UI_COLOR, BG_COLOR, TRIM_COLOR, SECONDARY_COLOR
  

class GenerateTool(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.threhold = tk.IntVar()
        self.threhold.set(500)


        main_frame = tk.Frame(container,
                              width=400,
                              height=300,
                              bg = UI_COLOR,
                              border=4,
                              relief='raised')
        main_frame.pack(padx=10, pady=5)
        header =tk.Canvas(main_frame,
                          width=400 ,
                          height=30,
                          bg=TRIM_COLOR)
        header.pack(fill='x', pady=(0,3))

        notebook = self.create_notebook(main_frame)
        basic_tab = tk.Frame(main_frame, bg=UI_COLOR)
        self.pack_gen_thresh_widget(basic_tab)
        adv_gen_tab = self.create_adv_gen_tab(notebook)
        adv_thresh_tab = self.create_adv_thresh_tab(notebook)
        basic_tab.pack()
        adv_gen_tab.pack()
        adv_gen_tab.pack()

        notebook.add(basic_tab, text = "Basic")
        notebook.add(adv_gen_tab, text = "Adv Generation") 
        notebook.add(adv_thresh_tab, text = "Adv Thresholding")
    
    def get_threshold(self):
        return self.threhold

    def create_notebook(self, container):
        style = ttk.Style()
        style.configure('TNotebook', background = BG_COLOR, padding = [0,0,0,0])
        style.configure('TNotebook.Tab', padding=[0,0,10,0])

        notebook = ttk.Notebook(container, style='TNotebook')
        notebook.pack(fill='both', padx=5, pady=5, expand=True)
        return notebook
    
    def pack_gen_thresh_widget(self,container):
        process_img_btn = tk.Button(
            container,
            text="Generate Next Stroke",
            command = self.process_image,
            borderwidth=5,
            relief='groove',
            font=("TkDefaultFont", 10),
            bg=SECONDARY_COLOR
        )
        process_img_btn.pack(fill='x', expand=True, pady=3, padx=3)
        frame = tk.Frame(container,bg=UI_COLOR)
        label = tk.Label(frame, text= "Threshold:", bg= UI_COLOR).pack(side=tk.LEFT, padx=3,pady=3)
        threshold_slider = tk.Scale(frame,
                                    from_=1,
                                    to=1000,
                                    width=20,
                                    orient='horizontal',
                                    variable=self.threhold)
        threshold_slider.pack(side=tk.LEFT, fill='x', expand=True, pady=3, padx=3)
        frame.pack(fill='x', expand=True)
        pass
    
    def create_adv_gen_tab(self, container):
        frame = tk.Frame(container, bg= UI_COLOR)
        label = tk.Label(frame, text="nothing new yet")
        label.pack()
        self.pack_gen_thresh_widget(frame)
        return frame
    
    def create_adv_thresh_tab(self, container):
        frame = tk.Frame(container, bg = UI_COLOR)
        return frame
    
    def process_image(self):
        pass

 
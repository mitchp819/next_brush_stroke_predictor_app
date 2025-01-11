import tkinter as tk
from tkinter import ttk
from typing import Literal
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app import UI_COLOR, BG_COLOR, TRIM_COLOR, SECONDARY_COLOR, HEADER_HEIGHT, RIGHT_PANE_WIDTH
  
DEFAULT_THRESHOLD = 50
class GenerateTool(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.threshold = tk.IntVar()
        self.threshold.set(DEFAULT_THRESHOLD)

        self.threshold128 = tk.IntVar()
        self.threshold64 = tk.IntVar()
        self.threshold32 = tk.IntVar()
        self.threshold16 = tk.IntVar()
        self.threshold8 = tk.IntVar()
        self.threshold4 = tk.IntVar()
        self.threshold128.set(DEFAULT_THRESHOLD)
        self.threshold64.set(DEFAULT_THRESHOLD)
        self.threshold32.set(DEFAULT_THRESHOLD)
        self.threshold16.set(DEFAULT_THRESHOLD)
        self.threshold8.set(DEFAULT_THRESHOLD)
        self.threshold4.set(DEFAULT_THRESHOLD)
        
        self.tab_index = 0

        self.drawing_canvas = None
        self.info_pane = None 
        
        main_frame = tk.Frame(container,
                              width= RIGHT_PANE_WIDTH,
                              height=300,
                              bg = UI_COLOR,
                              border=4,
                              relief='raised')
        main_frame.pack(padx=10, pady=5)
        header =tk.Canvas(main_frame,
                          width= RIGHT_PANE_WIDTH,
                          height=HEADER_HEIGHT,
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
        notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)
        pass
    
    def get_thresholds(self):
        print(self.tab_index)
        if self.tab_index == 2:
            thresholds_dict = {"threshold128": self.threshold128.get() , 
                            "threshold64": self.threshold64.get(),
                            "threshold32": self.threshold32.get(),
                            "threshold16": self.threshold16.get(),
                            "threshold8": self.threshold8.get(),
                            "threshold4": self.threshold4.get()}
        else:
            thresholds_dict = {"threshold128": self.threshold.get() , 
                            "threshold64": self.threshold.get(),
                            "threshold32": self.threshold.get(),
                            "threshold16": self.threshold.get(),
                            "threshold8": self.threshold.get(),
                            "threshold4": self.threshold.get()}
        return thresholds_dict

    def set_drawing_canvas(self, drawing_canvas):
        self.drawing_canvas = drawing_canvas

    def create_notebook(self, container):
        style = ttk.Style()
        style.configure('TNotebook', background = BG_COLOR, padding = [0,0,0,0])
        style.configure('TNotebook.Tab', padding=[0,0,10,0])

        notebook = ttk.Notebook(container, style='TNotebook')
        notebook.pack(fill='both', padx=5, pady=5, expand=True)
        return notebook
    
    def on_tab_selected(self, event):
        selected_tab = event.widget.select()
        self.tab_index = event.widget.index(selected_tab)
    
    def pack_gen_thresh_widget(self,container):
        process_img_btn = tk.Button(
            container,
            text="Generate Next Stroke (Any)",
            command = lambda: self.generate_image("any"),
            borderwidth=5,
            relief='groove',
            font=("TkDefaultFont", 10),
            bg=SECONDARY_COLOR
        )
        process_img_btn.pack(fill='x', expand=True, pady=3, padx=3)
        process_img_btn = tk.Button(
            container,
            text="Generate Next Stroke (Line)",
            command = lambda: self.generate_image("line"),
            borderwidth=5,
            relief='groove',
            font=("TkDefaultFont", 10),
            bg=SECONDARY_COLOR
        )
        process_img_btn.pack(fill='x', expand=True, pady=3, padx=3)
        process_img_btn = tk.Button(
            container,
            text="Generate Next Stroke (Shape)",
            command = lambda: self.generate_image("shape"),
            borderwidth=5,
            relief='groove',
            font=("TkDefaultFont", 10),
            bg=SECONDARY_COLOR
        )
        process_img_btn.pack(fill='x', expand=True, pady=3, padx=3)
        frame = tk.Frame(container,bg=UI_COLOR)
        tk.Label(frame, text= "Threshold:", bg= UI_COLOR).pack(side=tk.LEFT, padx=3,pady=3)
        threshold_slider = tk.Scale(frame,
                                    from_=1,
                                    to=1000,
                                    width=20,
                                    orient='horizontal',
                                    variable=self.threshold)
        threshold_slider.pack(side=tk.LEFT, fill='x', expand=True, pady=3, padx=3)
        
        frame.pack(fill='x', expand=True)
        pass
    
    def create_adv_gen_tab(self, container):
        frame = tk.Frame(container, bg= UI_COLOR)
        label = tk.Label(frame, text="What should go here?\nA grid of different databases to generate from\nHow would those be selected?")
        label.pack()
        return frame
    
    def create_adv_thresh_tab(self, container):
        frame = tk.Frame(container, bg = UI_COLOR)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=3)
        tk.Label(frame, text= "4x4 Threshold:", bg= UI_COLOR).grid(column=0, row=0)
        threshold_slider4 = tk.Scale(frame,
                                    from_=1,
                                    to=1000,
                                    width=20,
                                    orient='horizontal',
                                    variable=self.threshold4,
                                    showvalue=False)
        threshold_slider4.grid(column=1,row=0, sticky='EW')
        tk.Label(frame, text= "8x8 Threshold:", bg= UI_COLOR).grid(column=0, row=1)
        threshold_slider4 = tk.Scale(frame,
                                    from_=1,
                                    to=1000,
                                    width=20,
                                    orient='horizontal',
                                    variable=self.threshold8,
                                    showvalue=False)
        threshold_slider4.grid(column=1,row=1, sticky='EW')
        tk.Label(frame, text= "16x16 Threshold:", bg= UI_COLOR).grid(column=0, row=2)
        threshold_slider4 = tk.Scale(frame,
                                    from_=1,
                                    to=1000,
                                    width=20,
                                    orient='horizontal',
                                    variable=self.threshold16,
                                    showvalue=False)
        threshold_slider4.grid(column=1,row=2, sticky='EW')
        tk.Label(frame, text= "32x32 Threshold:", bg= UI_COLOR).grid(column=0, row=3)
        threshold_slider4 = tk.Scale(frame,
                                    from_=1,
                                    to=1000,
                                    width=20,
                                    orient='horizontal',
                                    variable=self.threshold32,
                                    showvalue=False)
        threshold_slider4.grid(column=1,row=3, sticky='EW')
        tk.Label(frame, text= "64x64 Threshold:", bg= UI_COLOR).grid(column=0, row=4)
        threshold_slider4 = tk.Scale(frame,
                                    from_=1,
                                    to=1000,
                                    width=20,
                                    orient='horizontal',
                                    variable=self.threshold64,
                                    showvalue=False)
        threshold_slider4.grid(column=1,row=4, sticky='EW')
        tk.Label(frame, text= "128x128 Threshold:", bg= UI_COLOR).grid(column=0, row=5)
        threshold_slider4 = tk.Scale(frame,
                                    from_=1,
                                    to=1000,
                                    width=20,
                                    orient='horizontal',
                                    variable=self.threshold128,
                                    showvalue=False)
        threshold_slider4.grid(column=1,row=5, sticky='EW')
        process_img_btn = tk.Button(
            frame,
            text="Generate Next Stroke",
            command = lambda: self.generate_image('any'),
            borderwidth=5,
            relief='groove',
            font=("TkDefaultFont", 10),
            bg=SECONDARY_COLOR
        )
        process_img_btn.grid(column=0, row=6, columnspan=2, sticky='EW', padx=(3,0))
        return frame
    
    def on_configure(self, event):
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        self.scroll_canvas.itemconfig("window", width = event.width)

    def generate_image(self, type: Literal['any', 'line', 'shape']):
        self.drawing_canvas.generate_stroke(type)
        pass

 
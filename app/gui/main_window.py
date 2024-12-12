import tkinter as tk
from tkinter import Menu
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from config_data_window.config_data_main import ConfigDataWindow
from app import WINDOW_TITLE, UI_COLOR, TRIM_COLOR, BG_COLOR, InfoPane, BrushTool, GenerateTool, HeaderTool, DrawingCanvasFrame, AppConsole

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(WINDOW_TITLE)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width - 200}x{screen_height - 200}+5+5")
        self.resizable(True, True)
        self.config(bg=UI_COLOR)

        #self.config_menu()  

        #for testing delete after
        #ConfigDataWindow()

        main_frame = tk.Frame(self, bg=UI_COLOR)
        main_frame.pack(fill='both',expand=True, padx=10, pady=20)

        header_tool_frame = tk.Frame(main_frame, bg=UI_COLOR, height=50)
        header_tool_frame.pack(fill='x')

        inner_frame =tk.Frame(main_frame, 
                              bg=BG_COLOR,
                              border = 3,
                              relief='sunken')
        inner_frame.pack(fill='both', expand= True, padx=2, pady=2)

        right_frame = tk.Frame(inner_frame, bg= BG_COLOR)
        right_frame.pack(side=tk.RIGHT)

        brush_tool = BrushTool(inner_frame) 
        info_pane = InfoPane(right_frame)
        generate_tool = GenerateTool(right_frame)
        app_console = AppConsole(right_frame)
        header_tool = HeaderTool(header_tool_frame)
        drawing_canvas = DrawingCanvasFrame(inner_frame)
        
        
        header_tool.set_drawing_canvas(drawing_canvas)
        header_tool.set_app_console(app_console)
        header_tool.set_info_pane(info_pane)
        drawing_canvas.set_brush_tool(brush_tool)
        drawing_canvas.set_data_gather_tool(header_tool)
        drawing_canvas.set_app_console(app_console)
        drawing_canvas.set_gen_tool(generate_tool)
        drawing_canvas.set_info_pane(info_pane)
        generate_tool.set_drawing_canvas(drawing_canvas)
        brush_tool.set_drawing_canvas(drawing_canvas)

        header_tool.toggle_data_gather_mode('auto')


    def config_menu(self):
        menubar = Menu(self)
        self.config(menu = menubar)
        
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label='New')
        file_menu.add_command(label='Open')
        menubar.add_cascade(label="File", menu=file_menu)

        window = Menu(menubar, tearoff=0)
        window.add_command(label='New')
        window.add_command(label='Open')
        menubar.add_cascade(label="Window", menu=window)
        

        
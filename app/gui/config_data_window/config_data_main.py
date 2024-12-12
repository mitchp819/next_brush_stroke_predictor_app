import tkinter as tk
from tkinter.messagebox import showerror
import os
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass


from app import  AppConsole, set_LOADED_DB, get_LOADED_DB, set_DATABASES, get_all_DATABASES, get_last_file_by_id, UI_COLOR, TRIM_COLOR, SECONDARY_COLOR, BG_COLOR, HEADER_HEIGHT, DATA_DIR
from config_data_window import NewDB
from config_data_window import CompileData

class ConfigDataWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Configure Data")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width - 400}x{screen_height - 400}+105+105")
        self.resizable(True, True)
        self.config(bg=UI_COLOR)

        self.info_pane = None

        #Create list of current active databases
        databases = get_all_DATABASES()
        self.current_db_save_list = []
        for db, values in databases.items():
            if values[0] == 1:
                self.current_db_save_list.append(db)
        print(f"current selected db {self.current_db_save_list}")
        
        self.db_list = create_db_list()
        self.save_to_db_list = self.current_db_save_list

        header =tk.Canvas(self,
                          width=400 ,
                          height=HEADER_HEIGHT,
                          bg=TRIM_COLOR)
        header.pack(fill='x', pady=(0,3),padx=2)
        header_tool_frame = tk.Frame(self, bg=UI_COLOR, height=50)
        header_tool_frame.pack(fill='x')

        main_frame = tk.Frame(self, bg=BG_COLOR, border=4, relief='sunken')
        main_frame.pack(fill='both',expand=True, padx=10, pady=20)
        
        self.create_header(header_tool_frame)
        self.create_load_db_frame(main_frame)
        self.create_save_to_db_frame(main_frame)
        console = AppConsole(main_frame)
        pass

    def set_info_pane(self, info_pane):
        self.info_pane = info_pane 


    def create_header(self, container: tk.Frame):
        header_frame = tk.Frame(container, bg=UI_COLOR)

        new_db_btn = tk.Button(header_frame,
                               text="Create New Database",
                               command= NewDB,
                               bg=SECONDARY_COLOR,
                               font=("TkDefaultFont", 10),
                               border=3,
                               relief='groove')
        new_db_btn.pack(side=tk.LEFT, padx=10)

        load_db_btn = tk.Button(header_frame, 
                                text="Load Database",
                               bg=SECONDARY_COLOR,
                               font=("TkDefaultFont", 10),
                               border=3,
                               relief='groove')
        load_db_btn.pack(side=tk.LEFT, padx=10)

        compile_data_btn = tk.Button(header_frame, 
                                text="Compile Data",
                               bg=SECONDARY_COLOR,
                                command=CompileData,
                               font=("TkDefaultFont", 10),
                               border=3,
                               relief='groove')
        compile_data_btn.pack(side=tk.RIGHT, padx=10)

        header_frame.pack(fill='x', pady=10)
        pass

    def create_load_db_frame(self, container: tk.Frame):
        loaded_db = tk.StringVar()
        loaded_db.set(get_LOADED_DB())
        
        load_db_frame = tk.Frame(container, 
                                 bg = UI_COLOR,
                                 border=4,
                                 relief='ridge')
        header =tk.Canvas(load_db_frame,
                          width=400 ,
                          height=HEADER_HEIGHT,
                          bg=TRIM_COLOR)
        header.pack(fill='x', pady=(0,3))
        label = tk.Label(load_db_frame,
                         text= "Choose Database To Generate From",
                         bg = UI_COLOR,
                         font=("TkDefaultFont", 12))
        label.pack(padx=5)
        for db in self.db_list:
            r = tk.Radiobutton(
                load_db_frame,
                text=db,
                value=db,
                variable= loaded_db,
                justify='left',
                border=3,
                relief='groove',
                font=("TkDefaultFont", 10)
            )
            r.pack(fill='x',padx=5, pady=5)
        save_btn = tk.Button(load_db_frame,
                             text="Save",
                             command=lambda: self.on_loaded_db_change(loaded_db.get()),
                             border=3,
                            relief='raised',
                            font=("TkDefaultFont", 12),
                            bg=SECONDARY_COLOR)
        save_btn.pack(fill='x', padx=5, pady=5)              
        load_db_frame.pack(side=tk.LEFT, padx=3, pady=3)

    def create_save_to_db_frame(self, container: tk.Frame):
        st_db_frame = tk.Frame(container, 
                               bg =UI_COLOR,
                               border=4,
                               relief='ridge')
        header =tk.Canvas(st_db_frame,
                    width=400 ,
                    height=HEADER_HEIGHT,
                    bg=TRIM_COLOR)
        header.pack(fill='x', pady=(0,3))
        label = tk.Label(st_db_frame,
                         text ="Choose Database To Save To",
                         bg = UI_COLOR,
                         font=("TkDefaultFont", 12))
        label.pack(padx=5)
        
        vars = {}
        for db in self.db_list:
            v = tk.IntVar()
            for d in self.save_to_db_list:
                if d == db:
                    v.set(1)
            c = tk.Checkbutton(st_db_frame,
                               text=db,
                               variable=v,
                               command=lambda: self.on_save_to_db_change(vars),
                               justify='left',
                               border=3,
                               relief='groove',
                               font=("TkDefaultFont", 10))
            c.pack(fill='x', padx=5, pady=5)
            vars[db] = v

        save_btn = tk.Button(st_db_frame,
                             text="Save",
                             command=lambda: self.on_save_to_db_saved(self.save_to_db_list),
                             border=3,
                            relief='raised',
                            font=("TkDefaultFont", 12),
                            bg= SECONDARY_COLOR)
        save_btn.pack(fill='x', padx=5, pady=5)              
        st_db_frame.pack(side = tk.LEFT, padx=3, pady=3)
        pass
    
    def on_save_to_db_change(self, vars):
        self.save_to_db_list = [db for db, v in vars.items() if v.get() == 1]
        print(self.save_to_db_list)
        pass

    def on_save_to_db_saved(self, save_to_db_list: list):
        '''Set all db off. Set selected on. If db is new then find id'''
        for all_db in self.db_list:
            save_on = 0
            for saved_db in save_to_db_list:
                if all_db == saved_db:
                    save_on = 1                 
            if save_on == 1:
                set_DATABASES(all_db, 1)
            else:
                set_DATABASES(all_db, 0)
        
        for saved_db in save_to_db_list:
            set_index = 1
            for current_db in self.current_db_save_list:
                if current_db == saved_db:
                    set_index = 0 
            if set_index == 1:
                path = os.path.join(DATA_DIR,f"{saved_db}/image_data")
                largest_id = get_last_file_by_id(path) 
                set_DATABASES(database=saved_db ,dataset_count=largest_id+1)   
        
        print(get_all_DATABASES())
        self.info_pane.set_db_save_to_lbl()
        pass

    def on_loaded_db_change(self, loaded_db):
        correct_file_count = 0
        path = os.path.join(DATA_DIR, f"{loaded_db}/gen_data")
        for item in os.listdir(path):
            if item == "4_data.npy":
                correct_file_count += 1
            if item == "8_data.npy":
                correct_file_count += 1
            if item == "16_data.npy":
                correct_file_count += 1
            if item == "32_data.npy":
                correct_file_count += 1
            if item == "64_data.npy":
                correct_file_count += 1
            if item == "128_data.npy":
                correct_file_count += 1
        if correct_file_count == 6:
            set_LOADED_DB(loaded_db)
            self.info_pane.set_db_generating_lbl()
        else:
            showerror(title="WARNING Data Needs Compiling",
                    message=f"The selected database has not been compiled and will not generate images. Select Compile Data then choose a database")
            self.destroy()
        pass

def create_db_list():
    db_list = os.listdir(DATA_DIR)
    return db_list


import tkinter as tk
import os
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass


from app import UI_COLOR, ROOT_DIR, DATA_DIR, LOADED_DB, set_LOADED_DB, get_LOADED_DB, set_SAVE_TO_DB_LIST, get_SAVE_TO_DB_LIST

class ConfigDataWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Configure Data")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width - 400}x{screen_height - 400}+205+205")
        self.resizable(True, True)
        self.config(bg=UI_COLOR)

        self.db_list = create_db_list()
        self.save_to_db_list = get_SAVE_TO_DB_LIST()

        main_frame = tk.Frame(self, bg=UI_COLOR)
        main_frame.pack(fill='both',expand=True, padx=10, pady=20)
        
        self.create_load_db_frame(main_frame)
        self.create_save_to_db_frame(main_frame)
        pass

    def create_load_db_frame(self, container: tk.Frame):
        loaded_db = tk.StringVar()
        loaded_db.set(get_LOADED_DB())
        
        load_db_frame = tk.Frame(container, bg = UI_COLOR)
        label = tk.Label(load_db_frame,
                         text= "Choose Database To Generate From",
                         bg = UI_COLOR,
                         font=("TkDefaultFont", 12))
        label.pack()
        for db in self.db_list:
            r = tk.Radiobutton(
                load_db_frame,
                text=db,
                value=db,
                variable= loaded_db
            )
            r.pack(fill='x',padx=5, pady=5)
        save_btn = tk.Button(load_db_frame,
                             text="Save",
                             command=lambda: on_loaded_db_change(loaded_db.get()))
        save_btn.pack()              
        load_db_frame.pack(side=tk.LEFT)

    def create_save_to_db_frame(self, container: tk.Frame):
        st_db_frame = tk.Frame(container, bg =UI_COLOR)
        label = tk.Label(st_db_frame,
                         text ="Choose Database to save to",
                         bg = UI_COLOR,
                         font=("TkDefaultFont", 12))
        label.pack()
        
        vars = {}
        for db in self.db_list:
            v = tk.IntVar()
            for d in self.save_to_db_list:
                if d == db:
                    v.set(1)
            c = tk.Checkbutton(st_db_frame,
                               text=db,
                               variable=v,
                               command=lambda: self.on_save_to_db_change(vars))
            c.pack(fill='x', padx=5, pady=5)
            vars[db] = v

        save_btn = tk.Button(st_db_frame,
                             text="Save",
                             command=lambda: on_save_to_db_saved(self.save_to_db_list))
        save_btn.pack()              
        st_db_frame.pack(side = tk.LEFT)
        pass
    
    def on_save_to_db_change(self, vars):
        self.save_to_db_list = [db for db, v in vars.items() if v.get() == 1]
        print(self.save_to_db_list)
        pass

def on_save_to_db_saved(save_to_db_list):
    set_SAVE_TO_DB_LIST(save_to_db_list)
    pass

def on_loaded_db_change(loaded_db):
    set_LOADED_DB(loaded_db)
    pass


def create_db_list():
    db_list = os.listdir(DATA_DIR)
    return db_list


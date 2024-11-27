import tkinter as tk
from tkinter.messagebox import askyesno
import os
import shutil
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app import UI_COLOR, SECONDARY_COLOR, DATA_DIR, HEADER_HEIGHT, TRIM_COLOR, BG_COLOR

class NewDB(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Create New Database")

        self.geometry(f"{500}x{200}+300+300")
        self.resizable(False, False)
        self.config(bg=UI_COLOR)

        main_frame = tk.Frame(self, bg=UI_COLOR)
        main_frame.pack(fill='both',expand=True, padx=2, pady=2)
        header =tk.Canvas(main_frame,
                          width=400 ,
                          height=HEADER_HEIGHT,
                          bg=TRIM_COLOR)
        header.pack(fill='x', pady=(0,3))
        
        title = tk.Label(main_frame,
                         text= "Create a New Database\nWarning validation not implemented!" )
        title.pack()

        grid_frame = tk.Frame(main_frame, bg=BG_COLOR, border=3, relief="sunken")
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=3)
        grid_frame.pack(fill='both', padx=3,pady=3, expand=True)

        
        label = tk.Label(grid_frame, 
                         text= "Database Name: ")
        label.grid(column=0, row=0, padx=3,pady=7, sticky=tk.E)

        db_name = tk.StringVar()
        name_entry = tk.Entry(grid_frame,
                              textvariable=db_name,
                              border=4,
                              relief='raised')
        name_entry.grid(column=1, row=0, padx=3, pady=7)

        cancel_btn = tk.Button(grid_frame, 
                               text="Cancel",
                               command=self.destroy,
                               width=20,
                               border=2,
                               relief='raised')
        cancel_btn.grid(column=0,row=1, padx=3, pady=3 )

        save_btn = tk.Button(grid_frame,
                             text="Save",
                             command=lambda: self.create_new_db(db_name.get()),
                             width=20,
                             border=2,
                             relief='raised')
        save_btn.grid(column=1,row=1, pady=3, padx=3)
        pass

    def create_new_db(self, db_name: str):
        make_dir = askyesno(title="Confirm Database Creation",
                          message=f"Create Database: {db_name}\nWarning no validation\nIncluding special characters may break things (-,./[] .etc)")
        if make_dir:
            fp = os.path.join(DATA_DIR, db_name)
            will_overwrite = os.path.exists(fp)
            confirm_overwrite = False
            if will_overwrite:
                print("file path overwrites data")
                confirm_overwrite = askyesno(title="WARNING Data Will Be Overwritten!",
                                             message=f"WARNING: The database name {db_name} allready exists.\nProceeding will overwrite and delete ALL data in that database")
                if confirm_overwrite:
                    shutil.rmtree(fp)
            if (will_overwrite==False or confirm_overwrite == True):
                os.makedirs(fp)   
                self.destroy()
        pass
         
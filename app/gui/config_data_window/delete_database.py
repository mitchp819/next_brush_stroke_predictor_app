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

class DeleteDatabase(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Delete Database")

        self.geometry(f"{500}x{500}+300+300")
        self.resizable(False, True)
        self.config(bg=UI_COLOR)
        self.db_list = os.listdir(DATA_DIR)

        main_frame = tk.Frame(self, bg=UI_COLOR)
        main_frame.pack(fill='both',expand=True, padx=2, pady=2)
        header =tk.Canvas(main_frame,
                          width=400 ,
                          height=HEADER_HEIGHT,
                          bg=TRIM_COLOR)
        header.pack(fill='x', pady=(0,3))
        
        title = tk.Label(main_frame,
                         text= "Select A Database to Delete\nWARNING Deleted files can not be rocovered" )
        title.pack()
        self.create_db_selection(main_frame)

    def create_db_selection(self, container):
        self.selection = tk.Frame(container, bg=UI_COLOR)
        main_label = tk.Label(self.selection,
                              text="Select Database to Compile",
                              bg=UI_COLOR,
                              relief='raised')
        main_label.pack(fill='x', padx=10, pady=10)

        count = 1
        for db in self.db_list:
            btn = tk.Button(self.selection,
                            text=db,
                            command= lambda db =db: self.confirm_deletion(db),
                            relief='raised'
                            )
            btn.pack(fill="x", padx=15, pady=3)
            count += 1
        self.selection.pack(fill='x', padx=10, pady=10)
        pass

    def confirm_deletion(self, db: str):
        delete_path = os.path.join(DATA_DIR, db)
        answer = askyesno(title= f"Confirm Deletion of {db}",
                 message=f"Confirm Deletion of Database {db}. Data can not be recovered once deleted.\nPath to Deleted Folder: {delete_path}")
        if answer:
            if os.path.exists(delete_path):
                shutil.rmtree(delete_path)
            else:
                print("Error: Path For Deletion Does Not Exist")
        self.destroy()
        pass
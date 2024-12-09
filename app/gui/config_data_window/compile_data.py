import tkinter as tk
from tkinter.messagebox import askyesno, showinfo
import os
import glob
import numpy as np
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

from app import UI_COLOR, SECONDARY_COLOR, DATA_DIR, HEADER_HEIGHT, TRIM_COLOR, BG_COLOR, downscale_to_all_scales_and_save, shape_img

class CompileData(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Compile Data")

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


        self.create_db_selection(main_frame)

    def create_db_selection(self, container):
        self.selection_grid = tk.Frame(container, bg=UI_COLOR)
        self.selection_grid.columnconfigure(0, weight=3)
        self.selection_grid.columnconfigure(1, weight=3)


        main_label = tk.Label(self.selection_grid,
                              text="Select Database to Compile")
        main_label.grid(column=0,row=0)

        count = 1
        for db in self.db_list:
            btn = tk.Button(self.selection_grid,
                            text=db,
                            command= lambda db =db: self.db_settings(container, db))
            btn.grid(column=0, row=count, sticky=tk.EW, pady=3)
            count += 1
    

        self.selection_grid.pack()
        pass

    def db_settings(self, container: tk.Frame, db:str ):
        self.selection_grid.pack_forget()
        settings_frame = tk.Frame(container, bg=UI_COLOR)

        flip_h = tk.IntVar()
        flip_v = tk.IntVar()
        rotate = tk.IntVar()
        title = tk.Label(settings_frame,
                         text=f"Configure Database: {db} for Compiling",
                         font=("TkDefaultFont", 12),
                         bg = UI_COLOR)
        title.pack()
        header_label = tk.Label(settings_frame,
                                text = "Mirroring and Rotating data is a way to\nsubstantually increase the size of the database",
                                justify='left',
                                font=("TkDefaultFont", 10))
        header_label.pack()

        flip_h_check = tk.Checkbutton(settings_frame,
                                      text= "Mirror Data Horizontally",
                                      variable=flip_h,
                                      border = 3,
                                      relief='groove',
                                      font=("TkDefaultFont", 10))
        flip_h_check.pack(fill='x', pady=3)
        flip_v_check = tk.Checkbutton(settings_frame,
                                      text= "Mirror Data Vertically",
                                      variable=flip_v,
                                      border = 3,
                                      relief='groove',
                                      font=("TkDefaultFont", 10))
        flip_v_check.pack(fill='x',pady=3)
        rotate_check = tk.Checkbutton(settings_frame,
                                      text="Rotate Data",
                                      variable=rotate,
                                      border = 3,
                                      relief='groove',
                                      font=("TkDefaultFont", 10))
        rotate_check.pack(fill='x', pady=3)

        footer_label = tk.Label(settings_frame,
                                text="Compiling data may take a long time depending on\nthe size of the database and your personal hardware",
                                justify='left',
                                font=("TkDefaultFont", 10)
                                )
        footer_label.pack(pady=3)
        
        cancel_btn = tk.Button(settings_frame,
                               text = "Cancel",
                               command=lambda: self.cancel_btn(settings_frame, container)
                               )
        cancel_btn.pack(side=tk.LEFT, fill='x')

        save_btn = tk.Button(settings_frame,
                             text=f"Compile {db}",
                             command=lambda: self.compile_data(db=db, flip_h = flip_h.get(), flip_v = flip_v.get(), rotate=rotate.get()))
        save_btn.pack(side=tk.RIGHT, fill='x')


        settings_frame.pack(padx=5, pady=5)
        pass

    def cancel_btn(self, destroy_frame: tk.Frame, container:tk.Frame):
        destroy_frame.destroy()
        self.create_db_selection(container)
    
    def compile_data(self, db, flip_h, flip_v, rotate):
        print(f"{db}, H {flip_h}, V {flip_v}, R {rotate}")
        main_cat_db =  cat_data(database=db)
        final_db = main_cat_db
        if flip_h:
            flipped_h = flip_db_h(main_cat_db)
            final_db = np.concatenate((final_db, flipped_h), axis=0)
        if flip_v:
            flipped_v = flip_db_v(main_cat_db)
            final_db = np.concatenate((final_db, flipped_v), axis=0)
        if rotate:
            rotate_db(main_cat_db)
            #cat with final_db
        
        save_path = os.path.join(DATA_DIR, f'{db}/gen_data')
        downscale_to_all_scales_and_save(final_db, save_path)
        showinfo(title="Compiling Finished",
                 message=f"{db} Compiled and Ready to Generate")
        self.destroy()
        pass

def cat_data(database, console =None):
    path = os.path.join(DATA_DIR, f'{database}/image_data/*.npy')
    print(path)
    files = sorted(glob.glob(path))
    arrays = []

    for f in files:
        arrays.append(np.load(f))

    result = np.concatenate(arrays,axis=0)

    if console != None:
        console.print_to_console(f"Data concatenated into np array shape = {result.shape}") 
 
    print(f"Data concatenated into np array shape = {result.shape}")
    return result

def flip_db_h(main_np):
    output_list = []
    for element in main_np:
        canvas = element[0]
        stroke = element[1]
        c_last = canvas[-1]
        s_last = stroke[-1]
        canvas = canvas[:-1]
        stroke = stroke[:-1]
        shaped_canvas = shape_img(canvas)
        shaped_stroke = shape_img(stroke)
        mirror_canvas = np.flip(shaped_canvas, axis = 1)
        mirror_stroke = np.flip(shaped_stroke, axis = 1)
        flat_canvas = mirror_canvas.flatten()
        flat_stroke = mirror_stroke.flatten()
        final_canvas = np.append(flat_canvas, c_last)
        final_stroke = np.append(flat_stroke, s_last)
        new_element = np.array([final_canvas, final_stroke])
        output_list.append(new_element)
    
    output_np = np.concatenate([output_list], axis=0)
    print("All elements flipped Horizontally")
    print(output_np.shape)
    return output_np

def flip_db_v(main_np):
    output_list = []
    for element in main_np:
        canvas = element[0]
        stroke = element[1]
        c_last = canvas[-1]
        s_last = stroke[-1]
        canvas = canvas[:-1]
        stroke = stroke[:-1]
        shaped_canvas = shape_img(canvas)
        shaped_stroke = shape_img(stroke)
        mirror_canvas = np.flip(shaped_canvas, axis = 0)
        mirror_stroke = np.flip(shaped_stroke, axis = 0)
        flat_canvas = mirror_canvas.flatten()
        flat_stroke = mirror_stroke.flatten()
        final_canvas = np.append(flat_canvas, c_last)
        final_stroke = np.append(flat_stroke, s_last)
        new_element = np.array([final_canvas, final_stroke])
        output_list.append(new_element)
    
    output_np = np.concatenate([output_list], axis=0)
    print("All elements flipped Vertically")
    print(output_np.shape)
    return output_np

def rotate_db(main_np):
    output_list = []
    for element in main_np:
        canvas = element[0]
        stroke = element[1]
        c_last = canvas[-1]
        s_last = stroke[-1]
        canvas = canvas[:-1]
        stroke = stroke[:-1]
        shaped_canvas = shape_img(canvas)
        shaped_stroke = shape_img(stroke)

        r1_canvas = np.rot90(shaped_canvas)
        r1_stroke = np.rot90(shaped_stroke)
        r2_canvas = np.rot90(r1_canvas)
        r2_stroke = np.rot90(r1_stroke)
        r3_canvas = np.rot90(r2_canvas)
        r3_stroke = np.rot90(r2_stroke)

        flat1_canvas = r1_canvas.flatten()
        flat1_stroke = r1_stroke.flatten()
        flat2_canvas = r2_canvas.flatten()
        flat2_stroke = r2_stroke.flatten()
        flat3_canvas = r3_canvas.flatten()
        flat3_stroke = r3_stroke.flatten()

        final1_canvas = np.append(flat1_canvas, c_last)
        final1_stroke = np.append(flat1_stroke, s_last)
        new_element1 = np.array([final1_canvas, final1_stroke])
        output_list.append(new_element1)
        final2_canvas = np.append(flat2_canvas, c_last)
        final2_stroke = np.append(flat2_stroke, s_last)
        new_element2 = np.array([final2_canvas, final2_stroke])
        output_list.append(new_element2)
        final3_canvas = np.append(flat3_canvas, c_last)
        final3_stroke = np.append(flat3_stroke, s_last)
        new_element3 = np.array([final3_canvas, final3_stroke])
        output_list.append(new_element3)
    
    output_np = np.concatenate([output_list], axis=0)
    print("All elements rotated")
    print(output_np.shape)
    pass

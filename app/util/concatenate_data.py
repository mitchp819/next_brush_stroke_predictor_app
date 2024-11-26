import numpy as np
import glob
import os

from app import ROOT_DIR

def cat_data(database, console =None):
    path = os.path.join(ROOT_DIR, f'data/{database}/image_data/*.npy')
    files = sorted(glob.glob(path))
    arrays = []

    for f in files:
        arrays.append(np.load(f))

    result = np.concatenate(arrays,axis=0)

    if console != None:
        console.print_to_console(f"Data concatenated into np array shape = {result.shape}") 

    print(f"Data concatenated into np array shape = {result.shape}")
    np.save(f'NPY_AllImageData{result.shape[2]}.npy', result)
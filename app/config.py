import os
import sys
from app import get_last_file_by_id

#colors
UI_COLOR = '#D5D5D6'
BG_COLOR = '#61606D'
TRIM_COLOR = '#4356C2'
SECONDARY_COLOR = '#C1E5F9'

#text
WINDOW_TITLE = "Next Brush Stroke Predictor"
CONSOLE_INTRO_TEXT = "Next Brush Stroke Predictor Loaded\n<<<System Console>>"

#Numbers
HEADER_HEIGHT = 20
RIGHT_PANE_WIDTH = 450

#Directory Paths
def check_dir(path):
    if not os.path.exists(path):
        print(f"INFO: {path} not found, creating one")
        os.makedirs(path)
    else:
        print(f"INFO: {path} found")
pass

def get_base_path():
    try: 
        base_path = sys.MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return base_path


ROOT_DIR = get_base_path()
DATA_DIR = os.path.abspath(os.path.join(ROOT_DIR, "data"))
ASSETS_DIR = os.path.abspath(os.path.join(ROOT_DIR, "assets"))
SIMILAR_IMAGES_DIR = os.path.abspath(os.path.join(ASSETS_DIR, "similar-images"))
SAVED_IMAGES_DIR = os.path.abspath(os.path.join(ASSETS_DIR, "saved-images"))

check_dir(DATA_DIR)
check_dir(ASSETS_DIR)
check_dir(SIMILAR_IMAGES_DIR)
check_dir(SAVED_IMAGES_DIR)

#Data
try: db_list = os.listdir(DATA_DIR)
except Exception as e: 
    print(f"ERROR: {e}")
    db_list = None

if db_list:
    LOADED_DB = db_list[0]
else:
    LOADED_DB = None
    check_dir(DATA_DIR)

def set_LOADED_DB(input: str):
    global LOADED_DB
    LOADED_DB = input
    print(f"LOADED_DB set to {input}")
def get_LOADED_DB() -> str:
    return LOADED_DB

DATABASES = {}
def set_DATABASES(database:str, save_to = None, dataset_count = None):
    global DATABASES
    if database in DATABASES:
        db_list = DATABASES[database]
    else:
        db_list = [0,0]
    if save_to != None:
        db_list[0] = save_to
    if dataset_count != None:
        db_list[1] = dataset_count
    DATABASES[database] = db_list

def get_a_DATABASE(database:str)-> list:
    return DATABASES[database]
def get_all_DATABASES()->dict:
    return DATABASES

#init DATABASES
for db in db_list:
    first_db_path = os.path.join(DATA_DIR,f"{db}/image_data")
    last_id = get_last_file_by_id(first_db_path)
    set_DATABASES(db, dataset_count= last_id+1)

#set_DATABASES('_master_db',save_to= 1)


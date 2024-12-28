import os
from app import get_last_file_by_id

#colors
UI_COLOR = '#D5D5D6'
BG_COLOR = '#61606D'
TRIM_COLOR = '#4356C2'
SECONDARY_COLOR = '#C1E5F9'

#text
WINDOW_TITLE = "Next Brush Stroke Predictor"
CONSOLE_INTRO_TEXT = "Next Brush Stroke Predictor Loaded\n<<<System Console>>"

#dir paths
current_dir = os.path.dirname(__file__) 
ROOT_DIR = os.path.abspath(os.path.join(current_dir, ".."))
DATA_DIR = os.path.abspath(os.path.join(ROOT_DIR, "data"))
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
ASSETS_DIR = os.path.abspath(os.path.join(ROOT_DIR, "assets"))
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)
SIMILAR_IMAGES_DIR = os.path.abspath(os.path.join(ASSETS_DIR, "similar-images"))
if not os.path.exists(SIMILAR_IMAGES_DIR):
    os.makedirs(SIMILAR_IMAGES_DIR)
SAVED_IMAGES_DIR = os.path.abspath(os.path.join(ASSETS_DIR, "saved-images"))
if not os.path.exists(SAVED_IMAGES_DIR):
    os.makedirs(SAVED_IMAGES_DIR)

#numbers
HEADER_HEIGHT = 20
RIGHT_PANE_WIDTH = 450

#data stuff
db_list = os.listdir(DATA_DIR)

LOADED_DB = db_list[0]
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

set_DATABASES('_master_db',save_to= 1)


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

#numbers
HEADER_HEIGHT = 20

#data stuff
db_list = os.listdir(DATA_DIR)

LOADED_DB = db_list[0]
def set_LOADED_DB(input: str):
    global LOADED_DB
    LOADED_DB = input
    print(f"LOADED_DB set to {input}")
def get_LOADED_DB() -> str:
    return LOADED_DB

SAVE_TO_DB_LIST = [db_list[0]]
def set_SAVE_TO_DB_LIST(input: list):
    global SAVE_TO_DB_LIST
    SAVE_TO_DB_LIST = input
    print(f"SAVE_TO_DB_LIST set to {input}")
def get_SAVE_TO_DB_LIST() -> list:
    return SAVE_TO_DB_LIST

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
    print(DATABASES)

def get_a_DATABASE(database:str)-> list:
    return DATABASES[database]
def get_all_DATABASES()->dict:
    return DATABASES

#init DATABASES
for db in db_list:
    set_DATABASES(db)
set_DATABASES(db_list[0],save_to= 1)


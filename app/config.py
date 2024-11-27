import os

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
LOADED_DB = 'db1'
def set_LOADED_DB(input: str):
    global LOADED_DB
    LOADED_DB = input
    print(f"LOADED_DB set to {input}")
def get_LOADED_DB() -> str:
    return LOADED_DB

SAVE_TO_DB_LIST = ['db1']
def set_SAVE_TO_DB_LIST(input: list):
    global SAVE_TO_DB_LIST
    SAVE_TO_DB_LIST = input
    print(f"SAVE_TO_DB_LIST set to {input}")
def get_SAVE_TO_DB_LIST() -> list:
    return SAVE_TO_DB_LIST



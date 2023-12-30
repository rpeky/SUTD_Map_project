import os
import json

#File handling module

#to come up with folders needed to store data for easier validation
folder_list = ['Master','Working']

def check_folders_exist():
    for folder in folder_list:
        if os.path.isdir(folder):
            continue
        os.mkdir(folder)

def check_file_exist(filename, folder_idx):
    cwd = os.getcwd()
    newdir = os.path.join(cwd, folder_list[folder_idx])
    full_path = os.path.join(newdir, filename)
    return os.path.isfile(full_path)

def save_file_json(tosave, filename, folder_idx):
    cwd = os.getcwd()
    newdir = os.path.join(cwd, folder_list[folder_idx])
    full_path = os.path.join(newdir, filename)
    with open(full_path, 'w') as outfile:
        json.dump(tosave, outfile, sort_keys=True, indent=4, ensure_ascii=False)
        
def load_file_json(filename, folder_idx):
    cwd = os.getcwd()
    newdir = os.path.join(cwd, folder_list[folder_idx])
    full_path = os.path.join(newdir, filename)
    f=open(full_path)
    return json.load(f)

def swap_Master_working_dataset():
    pass

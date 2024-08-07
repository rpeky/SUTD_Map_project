import os
import json

#File handling module

#to come up with folders needed to store data for easier validation
folder_list = ['Master','Working','LookUp','Misc','Log']

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

def rebuild_lookupdir():
    #dirs
    cwd = os.getcwd()
    lkupdir = os.path.join(cwd, 'LookUp')
    masdir = os.path.join(cwd, 'Master')    

    lkdict = load_file_json("Lookup_directory.json", 2)
    lkupcount = 0
    inilkdictcount = len(lkdict)

    rebuild = dict()

    #checks and adds all existing vertices to lookup_directory
    #as per python os documentation
    with os.scandir(masdir) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                jsoncheck = load_file_json(entry, 0)
                print(entry.name)
                for key in jsoncheck:
                    rebuild[key] = entry.name
                    lkupcount+=1

    print("Lookup Keys: {} \nKey Count: {}".format(inilkdictcount, lkupcount))

    #to do:
    #log if the rebuild is more than or less than the original lkup count, output to log in log dir

    print(rebuild)

    #do a cross check, overwrite with rebuilt if not the same
    if (rebuild != lkdict):
        print("override original with rebuild dict")
        save_file_json(rebuild,"Lookup_directory.json",2)
    else:
        print("Validated lookup ref, no errors to correct")

def rebuild_lookupcon():
    cwd = os.getcwd()
    lkupdir = os.path.join(cwd, 'LookUp')
    masdir = os.path.join(cwd, 'Master')

    lkdict = load_file_json("Lookup_connections.json", 2)

    rebuild = dict()

    with os.scandir(masdir) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                jsoncheck = load_file_json(entry, 0)
                print(entry.name)
                for key in jsoncheck:
                    if jsoncheck[key]["Connection_Point"]:
                        rebuild[key]=entry.name

    print(rebuild)

    #do a cross check, overwrite with rebuilt if not the same
    if (rebuild != lkdict):
        print("override original with rebuild dict")
        save_file_json(rebuild,"Lookup_connections.json",2)
    else:
        print("Validated connections, no errors to correct")

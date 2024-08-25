import time
import json

import Graph
import User
import Json_OS_ProcessingFunctions
import Path_query

quits = ['q','Q']

def graphtool_ini():
    f_zone = Area_Selection()
    if f_zone is None:
        print("No area selected, returning to main menu!\n")
        return
    uu=User.User()
    if not uu:
        print("No user detected, returning to main menu!\n")
        return

    lkup = masterlookup_ini()
    cplkup = lookup_connection_ini()
    idlkup = lookup_id_ini()

    gg = Graph.Graph(f_zone, uu.clearance_card, lkup, cplkup, idlkup)
    print(gg.Time_check())
    #print(gg.__dict__)

def masterlookup_ini():
    #for looking up which vertex belongs to which json
    dd_lkup = dict()
    if Json_OS_ProcessingFunctions.check_file_exist("Lookup_directory.json",2):
        dd_lkup = Json_OS_ProcessingFunctions.load_file_json("Lookup_directory.json",2)
    else:
        Json_OS_ProcessingFunctions.save_file_json(dd_lkup,"Lookup_directory.json",2)
    return dd_lkup

def lookup_connection_ini():
    #for connection point json list, run after masterlookup_ini
    dd_cplkup = dict()
    if Json_OS_ProcessingFunctions.check_file_exist("Lookup_connections.json",2):
        dd_cplkup = Json_OS_ProcessingFunctions.load_file_json("Lookup_connections.json",2)
    else:
        Json_OS_ProcessingFunctions.save_file_json(dd_cplkup,"Lookup_connections.json",2)
    return dd_cplkup

def lookup_id_ini():
    #for general lookup based on location ID
    dd_idlkup = dict()
    if Json_OS_ProcessingFunctions.check_file_exist("Lookup_locationID.json",2):
        dd_idlkup = Json_OS_ProcessingFunctions.load_file_json("Lookup_locationID.json",2)
    else:
        Json_OS_ProcessingFunctions.save_file_json(dd_idlkup,"Lookup_locationID.json",2)
    return dd_idlkup

def Area_Selection():
    dd_zones={
        "LEVEL_1":['1'],
        'Building_1':['2','3','4','5','6','7'],
        'Building_2':['2','3','4','5','6','7'],
        'Building_3':['2','3','4','5','6','7'],
        'Building_5':['2','3','4','5','6'],
        'Block_51':['2','3','4','5','6','7','8','9','10','11','12'],
        'Block_53':['2','3','4','5','6','7','8','9','10','11','12'],
        'Block_55':['2','3','4','5','6','7','8','9','10','11','12'],
        'Block_57':['2','3','4','5','6','7','8','9','10','11','12'],
        'Block_59':['2','3','4','5','6','7','8','9','10','11','12'],
        'Sports_and_Recreation_Centre':['2','3'],
        'Special_Zones':['2','3','5']
        }

    B_select = Building_Selection(list(dd_zones.keys()))
    if B_select in quits:
        return None
    F_select = Floor_Selection(dd_zones[B_select])
    A_select = B_select+'_Level_'+F_select+".json"
    print("Loading file: {}\n".format(A_select))
    return A_select

def Building_Selection(buildings):
    selection = ["{:02d}".format(i) for i in range(len(buildings))]
    print("Availiable Buildings:")
    for i in range(len(buildings)):
        print("{:02d}\t{}".format(i, buildings[i]))
    print("Enter q to return to main menu")
    while True:
        b_select = input("\nSelect building to load: ")
        if b_select in selection:
            print("Selected {}".format(buildings[int(b_select)]))
            return buildings[int(b_select)]
        elif b_select in quits:
            return 'q'
        else:
            print("Invalid input!")

def Floor_Selection(floors):
    print("\nAvailiable Levels:")
    for i in floors:
        print("Level {}".format(i))
    while True:
        f_select = input("\nSelect floor to load: ")
        if f_select in floors:
            print("Selected level {}".format(f_select))
            return f_select
        else:
            print("Invalid input!")

def validate_lookupdir():
    Json_OS_ProcessingFunctions.rebuild_lookupdir()
    Json_OS_ProcessingFunctions.rebuild_lookupcon()
    Json_OS_ProcessingFunctions.rebuild_locationID()

def runpq():
    idlkup = lookup_id_ini()
    pq = Path_query.Query()


def main():
    cl_s="\n"*100
    validate_lookupdir()
    options = {
            '0': runpq,
            '1': graphtool_ini,
            '2': validate_lookupdir
            }
    while True:
        try:
            print(cl_s)
            print("SUTD Map Project 2023/2024 Default Page\n")
            print("0 - Run Pathfinding\n1 - Run Graph mapping tool\n2 - Run Lookup directory validation\n")
            ct=input("Enter q to exit mapping tool\nSelect tool to run: ")
            if ct == 'q' or ct == 'Q':
                break
            elif ct in options.keys():
                options[ct]()
        except ValueError:
            print("Invalid input")

if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(time.process_time()-start_time)

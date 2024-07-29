import time
import json

import Graph
import User
import Json_OS_ProcessingFunctions

def testbench():
    f_zone = Area_Selection()
    uu=User.User()
    lkup = masterlookup_ini()
    cplkup = lookup_connection_ini()
    gg = Graph.Graph(f_zone, uu.clearance_card, lkup, cplkup)
    #gg.graph_generation_tool()
    print(gg.Time_check())
    #print(gg.__dict__)

def masterlookup_ini():
    #for looking up which vertex belongs to which json
    dd_lkup = dict()
    Json_OS_ProcessingFunctions.check_folders_exist()
    if Json_OS_ProcessingFunctions.check_file_exist("Lookup_directory.json",2):
        dd_lkup = Json_OS_ProcessingFunctions.load_file_json("Lookup_directory.json",2)
    return dd_lkup

def lookup_connection_ini():
    #for connection point json list, run after masterlookup_ini
    dd_cplkup = dict()
    if Json_OS_ProcessingFunctions.check_file_exist("Lookup_connections.json",2):
        dd_cplkup = Json_OS_ProcessingFunctions.load_file_json("Lookup_connections.json",2)
    return dd_cplkup

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
        'Special_Zones':[]
        }
    B_select = Building_Selection(list(dd_zones.keys()))
    F_select = Floor_Selection(dd_zones[B_select])
    A_select = B_select+'_Level_'+F_select+".json"
    print("Loading file: {}\n".format(A_select))
    return A_select

def Building_Selection(buildings):
    selection = ["{:02d}".format(i) for i in range(len(buildings))]
    print("Availiable Buildings:")
    for i in range(len(buildings)):
        print("{:02d}\t{}".format(i, buildings[i]))
    b_select = input("\nSelect building to load: ")
    if b_select in selection:
        print("Selected {}".format(buildings[int(b_select)]))
        return buildings[int(b_select)]
    else:
        print("Invalid input!")
        return Building_Selection(buildings)

def Floor_Selection(floors):
    print("\nAvailiable Levels:")
    for i in floors:
        print("Level {}".format(i))
    f_select = input("\nSelect floor to load: ")
    if f_select in floors:
        print("Selected level {}".format(f_select))
        return f_select
    else:
        print("Invalid input!")
        return Floor_Selection(floors)

def main():
    #testbench()
    cl_s="\n"*100
    while True:
        print(cl_s)
        print("SUTD Map Project 2023/2024 Default Page\n")
        ct=input("Enter q to exit mapping tool\nAny other key to proceed: ")
        if ct=='q':
            break
        testbench()

def validate_lookupdir():
    Json_OS_ProcessingFunctions.rebuild_lookupdir()
    Json_OS_ProcessingFunctions.rebuild_lookupcon()

if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(time.process_time()-start_time)

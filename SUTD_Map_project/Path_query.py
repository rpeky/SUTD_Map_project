import Json_OS_ProcessingFunctions
#import Graph

quits = ['q','Q']


class Query():
    def __init__(self, idlkup):
        self.dd_locationid = idlkup
        print('test query class')
        print(self.dd_locationid)
        self.welcome_message()
        self.display_options_startpoint()
        self.tempwaitinput()

    def __del__(self):
        print('test del query class')

    def welcome_message(self):
        print("Welcome to Query page\n")

    def display_options_startpoint(self):
        print("\n\n\nStarting location options: \n0 - Enter room ID \n1 - Location list \nq - Quit\n")
        while True:
            try:
                sel = input("Selection: ")
                if sel == 'q' or sel == 'Q':
                    return
                if sel == '0':
                    self.inputroomID()
                    break
                elif sel == '1':
                    self.locationlist()
                    break
                else:
                    print("Input out of index")
            except ValueError:
                print("Not a valid input")

    def tempwaitinput(self):
        temp = input("\nEnter any key to continue:\t\n")

    def locationlist(self):
        print("\n\n\nLocation Listing\n")
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
        'Sports_and_Recreation_Centre':['2','3']
        }
        blist = list(dd_zones.keys())
        bname = None
        for pos, key in enumerate(dd_zones):
            print("{:02d}\t{}".format(pos,key))
        print('q\tquit')

        #building selection
        while True:
            try:
                bld = input("\nBuilding ID: ")
                if bld == 'q' or bld == 'Q':
                    return self.display_options_startpoint()
                bld = int(bld)
                if bld > -1 and bld in range(len(dd_zones)):
                    bname = blist[bld]
                    print("\nSelected {}".format(bname))
                    break

            except ValueError:
                print("Not a valid input")

        #for location selection
        loclen = None
        vnames = None

        #floor selection
        while True:
            try:
                flr = input("\nSelect floor - {}\nq\treturn to main menu\nSelection:\t".format(dd_zones[blist[bld]]))
                if flr == 'q' or flr == 'Q':
                    return
                if flr in dd_zones[blist[bld]]:
                    fname = bname+'_Level_'+flr+'.json'
                    vnames = Json_OS_ProcessingFunctions.pullup_vertices(fname,0)
                    loclen = len(vnames)
                    for i in range(loclen):
                        print("{:02d}\t{}".format(i,vnames[i]))
                    break

            except ValueError:
                print("Not a valid input")

        #location selection
        while True:
            try:
                idx = int(input("\nSelect location index\nSelection:\t"))
                if idx > -1 and idx < loclen:
                    print("Selected {}".format(vnames[idx]))
                    self.startloc(vnames[idx])
                    break
                else:
                    print("Invalid input")
            except ValueError:
                print("Not a valid input")

    def inputroomID(self):
        ls_validID = Json_OS_ProcessingFunctions.pullup_vertices("Lookup_locationID.json", 2)
        while True:
            try:
                #give format example? maybe see how
                rm_id = input("Enter Location ID: ")
                if rm_id in ls_validID:
                    self.translatermIDtovert(rm_id)
                    break
                elif rm_id in quits:
                    return self.display_options_startpoint()
                else:
                    print("Invalid ID / ID not in our database, try again")
            except ValueError:
                print("Not a valid input")

    def translatermIDtovert(self, ID):
        dd_translate = Json_OS_ProcessingFunctions.load_file_json("Lookup_locationID.json",2)
        internalname = dd_translate[ID]
        dd_lookupmap = Json_OS_ProcessingFunctions.load_file_json("Lookup_directory.json",2)
        startmap = dd_lookupmap[internalname]
        print(startmap)

    def startloc(self, loc):
        stpt = loc
        #load map


    def endloc(self, loc):
        edpt = loc
        #load map

    #pathfinding for cross map can be done here

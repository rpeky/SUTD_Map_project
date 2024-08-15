import Json_OS_ProcessingFunctions
#import Graph

quits = ['q','Q']


class Query():
    def __init__(self, idlkup):
        self.dd_locationid = idlkup
        print('test query class')
        print(self.dd_locationid)
        self.welcome_message()
        self.display_options_initial()
        #self.tempwaitinput()

    def __del__(self):
        print('test del query class')

    def welcome_message(self):
        print("Welcome to Query page\n")

    def display_options_initial(self):
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
                    self.locationlsit()
                    break
                else:
                    print("Input out of index")
            except ValueError:
                print("Not a valid input")

    def tempwaitinput(self):
        temp = input("\nEnter any key to continue:\t\n")

    def locationlsit(self):
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
        while True:
            try:
                bld = input("\nBuilding ID: ")
                if bld == 'q' or bld == 'Q':
                    return self.display_options_initial()
                bld = int(bld)
                if bld > -1 and bld in range(len(dd_zones)):
                    bname = blist[bld]
                    print("\nSelected {}".format(bname))
                    break

            except ValueError:
                print("Not a valid input")


        while True:
            try:
                flr = input("\nSelect floor - {}\nq\treturn to main menu\nSelectiona:\t".format(dd_zones[blist[bld]]))
                if flr == 'q' or flr == 'Q':
                    return
                if flr in dd_zones[blist[bld]]:
                    fname = bname+'_Level_'+flr+'.json'
                    vnames = Json_OS_ProcessingFunctions.pullup_vertices(fname,0)
                    for i in range(len(vnames)):
                        print("{:02d}\t{}".format(i,vnames[i]))
                    break

            except ValueError:
                print("Not a valid input")

    def inputroomID(self):
        ls_validID = Json_OS_ProcessingFunctions.pullup_vertices("Lookup_locationID.json", 2)
        while True:
            try:
                #give format example? maybe see how
                rm_id = input("Enter Location ID: ")
                if rm_id in ls_validID:
                    break
                elif rm_id in quits:
                    return self.display_options_initial()
                else:
                    print("Invalid ID / ID not in our database, try again")
            except ValueError:
                print("Not a valid input")

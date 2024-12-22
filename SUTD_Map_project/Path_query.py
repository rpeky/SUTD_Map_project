import Json_OS_ProcessingFunctions
import Graph

quits = ['q','Q']

class Query():
    def __init__(self):
        self.dd_locationid = Json_OS_ProcessingFunctions.load_file_json("Lookup_locationID.json",2)
        self.dd_masterlookup = Json_OS_ProcessingFunctions.load_file_json("Lookup_directory.json",2)

        print('test query class')
        print(self.dd_locationid)
        print(self.dd_masterlookup)
        self.welcome_message()
        self.pathfind_long_rundijk_supermap()
        #self.path_find()
        #self.tempwaitinput()

    def __del__(self):
        print('test del query class')

    def welcome_message(self):
        print("Welcome to Query page\n")

    def display_options_startpoint(self):
        print("\n\n\nLocation options: \n0 - Enter room ID \n1 - Location list \nq - Quit\n")
        loc = None
        while True:
            try:
                sel = input("Selection: ")
                if sel in quits:
                    return
                if sel == '0':
                    loc = self.inputroomID()
                    break
                elif sel == '1':
                    loc = self.locationlist()
                    break
                else:
                    print("Input out of index")
            except ValueError:
                print("Not a valid input")

        return loc

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
                if bld in quits:
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
                if flr in quits:
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

                    break
                else:
                    print("Invalid input")
            except ValueError:
                print("Not a valid input")

        return vnames[idx]

    def inputroomID(self):
        ls_validID = Json_OS_ProcessingFunctions.pullup_vertices("Lookup_locationID.json", 2)
        idloc = None
        while True:
            try:
                #give format example? maybe see how
                rm_id = input("Enter Location ID: ")
                if rm_id in ls_validID:
                    idloc = self.translatermIDtovert(rm_id)
                    break
                elif rm_id in quits:
                    return self.display_options_startpoint()
                else:
                    print("Invalid ID / ID not in our database, try again")
            except ValueError:
                print("Not a valid input")
        return idloc

    def translatermIDtovert(self, ID):
        #lookup ID in lookup table and translate
        dd_translate = Json_OS_ProcessingFunctions.load_file_json("Lookup_locationID.json",2)
        internalname = dd_translate[ID]
        #find which map location belongs to
        dd_lookupmap = Json_OS_ProcessingFunctions.load_file_json("Lookup_directory.json",2)
        startmap = dd_lookupmap[internalname]
        #starting map
        dd_smap = Json_OS_ProcessingFunctions.load_file_json(startmap,0)
        print(dd_smap)
        return internalname

    def startloc(self):
        print("Current location selection")
        sloc = self.display_options_startpoint()
        print("Starting location is {}".format(sloc))
        #load map
        return sloc

    def endloc(self):
        print("\nDestination selection")
        eloc = self.display_options_startpoint()
        print("Destination is {}".format(eloc))
        #load map
        return eloc

    def convertloc_todd(self, vtx):
        dd_conv = None
        dd_lookupmap = None
        #find which map location belongs to
        dd_lookupmap = Json_OS_ProcessingFunctions.load_file_json("Lookup_directory.json",2)
        locmap = dd_lookupmap[vtx]
        #load and return map
        dd_conv = Json_OS_ProcessingFunctions.load_file_json(locmap,0)
        return dd_conv

    def dijkstra(self, sp):
        dd_ref = self.convertloc_todd(sp)
        dd_djk = dict()
        vtxs = set(dd_ref)
        for vtx in vtxs:
            if(vtx==sp):
                dd_djk[vtx] = (0,[])
            else:
                dd_djk[vtx] = (float('inf'),[])
        visited_vtxs = set()
        curr_vtx = sp
        while True:
            #set as visited
            visited_vtxs.add(curr_vtx)
            #set adjacent vtx
            adj_vtx = [i for i in dd_ref[curr_vtx]["Neighbour"].keys() if i in vtxs]

            #update distance
            for adj in adj_vtx:
                #store distance and path to compare
                old_dist = dd_djk[adj][0]
                old_path = dd_djk[adj][1]

                #calculate new distance for the current check
                new_dist = dd_djk[curr_vtx][0] + dd_ref[curr_vtx]["Neighbour"][adj]
                new_path = dd_djk[curr_vtx][1] + [curr_vtx]

                #check diff
                if new_dist < old_dist:
                    dd_djk[adj] = (new_dist, new_path)

            curr_vtx = None
            curr_dist = float('inf')

            #compare which distance is shortest and set value for next interation
            for vtx, tupstore in dd_djk.items():
                if (vtx not in visited_vtxs) and (tupstore[0] < curr_dist):
                    curr_vtx = vtx
                    curr_dist = tupstore[0]

            #end condition, no more vtx to check
            if curr_vtx == None:
                break

        return dd_djk

    #pathfinding for cross map can be done here
    def twosidepfind(self,sloc,eloc):
        #check for error
        if sloc == None or eloc == None or sloc == eloc:
            print("invalid locations")
            return

        #check if pfind in same map, use dijkstra/simle pathfind
        if sloc in self.dd_masterlookup and eloc in self.dd_masterlookup:
            print("Solution found")
            return
        return

    #append graphs and search
    def pathfind_long_assumeleastmaps(self,sloc,eloc):
        start_dd = self.convertloc_todd(sloc)
        end_dd = self.convertloc_todd(eloc)
        #do dijkstras on the supermap to find the shortest map crossing - assumption that crosssing less maps means faster path search

    #to rewrite to fit the new storage format of graph
    def pathfind_long_rundijk_supermap(self):
        superdd = Json_OS_ProcessingFunctions.load_file_json('.supermap.json',0)
        dd_djk = dict()
        vtxs = set(superdd)
        sp = None
        for vtx in vtxs:
            if(sp != None):
                dd_djk[vtx] = (float('inf'),[])
            else:
                curr_vtx = vtx
                dd_djk[vtx] = (0,[])
        visited_vtxs = set()
        while True:
            #set as visited
            visited_vtxs.add(curr_vtx)
            #set adjacent vtx
            adj_vtx = [i for i in superdd[curr_vtx]["Neighbour"].keys() if i in vtxs]
            #update distance
            for adj in adj_vtx:
                #store distance and path to compare
                old_dist = dd_djk[adj][0]
                old_path = dd_djk[adj][1]

                #calculate new distance for the current check
                new_dist = dd_djk[curr_vtx][0] + superdd[curr_vtx]["Neighbour"][adj]
                new_path = dd_djk[curr_vtx][1] + [curr_vtx]

                #check diff
                if new_dist < old_dist:
                    dd_djk[adj] = (new_dist, new_path)

            curr_vtx = None
            curr_dist = float('inf')

            #compare which distance is shortest and set value for next interation
            for vtx, tupstore in dd_djk.items():
                if (vtx not in visited_vtxs) and (tupstore[0] < curr_dist):
                    curr_vtx = vtx
                    curr_dist = tupstore[0]
            #end condition, no more vtx to check
            if curr_vtx == None:
                break
        Json_OS_ProcessingFunctions.save_file_json(dd_djk,".processed_dijk_supermap.json",0)
        #return dd_djk

    def pathfind_long_appended_print(self):
        print(Json_OS_ProcessingFunctions.load_file_json('supermap.json',0))

    def bfs_supermap(self,source,dest):
        pass

    def genetic_supermap(self,source):
        pass

    def antcolony(self, source, dest):
        pass

    def path_find(self):
        print("Pathfinding tool\n")

        sloc = self.startloc()
        eloc = self.endloc()

        if self.convertloc_todd(sloc) == self.convertloc_todd(eloc):
            dd_djk = self.dijkstra(sloc)
            sol_dist = dd_djk[eloc][0]
            sol_path = dd_djk[eloc][1]
            print("Shortest path: {}\nDistance to end point: {}".format(sol_path, sol_dist))
        else:
            pass
            #self.pathfind_long_appendallmaps()

    def translate_internalnameforoutput(self):
        pass

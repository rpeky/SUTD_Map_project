import Json_OS_ProcessingFunctions
import json
import datetime

selection_yes=['1','y','Y','Yes','yes']
selection_no=['0','n','N','No','no']

class Graph():
    def __init__(self, area_file, clearance):
        Json_OS_ProcessingFunctions.check_folders_exist()
        self.dd_graph = dict()
        self.access_clearance = clearance
        self.area_file_tosave = area_file

        if self.check_area_file_exist(area_file):
            print("Loading {} from Master")
            self.dd_graph = Json_OS_ProcessingFunctions.load_file_json(area_file, 0)

        else:
            print("File does not exist")
            self.graph_generation_tool()

    def __del__(self):
        print("Saving to Working folder")
        self.store_solution_Working()
        print('deleting')

#_GRAPH TOOLS_#
    #to think of more conditions of the vertex
    def add_vertex(self):
        vertex_ID = self.query_vertex()
        if vertex_ID not in self.dd_graph.keys():
            neighbours = dict()
            dd_vertex = {
                    "Neighbour":neighbours,
                    "Visited": 0,
                    "Avg_density":1,
                    "Sheltered": True,
                    "Route_intersection": False,
                    "Access_Clearance": list(),
                    "Average_travel_time": None,
                    "Room_ID": None,
                    "Connection_Point": False
                }
            self.dd_graph[vertex_ID] = dd_vertex
        self.neighbour_tool(vertex_ID)

    def neighbour_tool(self, vertex_ID):
        #add escape con
        while True:
            print("Current Graph State: ")
            print(json.dumps(self.dd_graph,indent=4))
            cont = input("\nConfirm adding neighbour to {}?\ny/n: ".format(vertex_ID))
            if cont in selection_yes:
                self.add_neighbour(vertex_ID)
            elif cont in selection_no:
                break
            else:
                print("Invalid input")
                continue

    def add_neighbour(self, vertex_ID):
        print("Enter Neighbour Vertex ID: ")
        neighbour_ID=self.query_vertex()
        confirm_Neighbour_ID = input("\nConfirm adding neighbour {} to {}?\ny/n: ".format(neighbour_ID,vertex_ID))
        if confirm_Neighbour_ID in selection_yes:
            pass
        elif confirm_Neighbour_ID in selection_no:
            self.add_neighbour(vertex_ID)
        else:
            print("Returning to neighbour creation tool")
            self.neighbour_tool(vertex_ID)

        adj_dist=self.add_neighbour_distance()

        self.dd_graph[vertex_ID]["Neighbour"][neighbour_ID]=adj_dist
        if neighbour_ID not in self.dd_graph.keys():
            neighbours = {vertex_ID:adj_dist}
            dd_vertex_new = {
                    "Neighbour":neighbours,
                    "Visited": 0,
                    "Avg_density":1,
                    "Sheltered": True,
                    "Route_intersection": False,
                    "Access_Clearance": list(),
                    "Average_travel_time": None
                }
            self.dd_graph[neighbour_ID] = dd_vertex_new
        else:
            self.dd_graph[neighbour_ID]["Neighbour"][vertex_ID]=adj_dist

    def add_neighbour_distance(self):
        while True:
            try:
                adj_vtx_dist = float(input("Enter distance to adjacent vertex: "))
                if adj_vtx_dist > 0:
                    cont = input("\nConfirm distance {} \ny/n: ".format(adj_vtx_dist))
                    if cont in selection_yes:
                        return adj_vtx_dist
                    else:
                        continue
                else:
                    print("Distance must be more than 0!")
            except ValueError:
                print("Not a number")

    # UI portion for adding vertex information
    def query_vertex(self):
        #to add existing vertex selection
        q_pf=self.query_vertex_Prefix()
        q_hd=self.query_vertex_Heading()
        q_id=self.query_vertex_ID()
        return q_pf+q_hd+q_id

    def query_vertex_Prefix(self):
        pref = ""
        #edit as needed
        ID_prefix = ["LIFT_","ROOM_","DUSTBIN_","INTER_","TOILET_","STAIRS_","ENTRANCE_","MAINROAD_","WALKWAY_"]
        for i in range(len(ID_prefix)):
            print("{:02d}\t{}".format(i, ID_prefix[i]))
        while True:
            try:
                pref=int(input("\nPick a prefix: "))
                if pref>-1 and pref<len(ID_prefix):
                    break
                else:
                    print("out of index")
            except ValueError:
                print("Not a valid input")

        print("\nConfirm selection \n{:02d}\t{}?\n".format(pref,ID_prefix[pref]))
        sel=input("y/n: ")
        if sel in selection_yes:
            print("Selected {}\n".format(ID_prefix[pref]))
            return ID_prefix[pref]
        elif sel in selection_no:
            return self.query_vertex_Prefix()
        else:
            print("Not a valid input\n")
            return self.query_vertex_Prefix()

    def query_vertex_Heading(self):
        direction_heading = ""
        print("Enter heading of vertex [01-36]: ")
        while True:
            #breaks if not in, try something else?
            try:
                pref=int(input())
                if pref>0 and pref<37:
                    direction_heading=format(pref,'02d')
                    break
                else:
                    print("out of index")
            except ValueError:
                print("Not a valid input")

        print("\nConfirm entry: \t{}\n".format(direction_heading))
        sel=input("y/n: ")
        if sel in selection_yes:
            print("Heading {}\n".format(direction_heading))
            return direction_heading+'_'
        elif sel in selection_no:
            return self.query_vertex_Heading()
        else:
            print("Not a valid input\n")
            return self.query_vertex_Heading()

    def query_vertex_ID(self):
        ID = input("Enter ID of vertex: ")
        print("\nConfirm entry: \t{}\n".format(ID))
        sel=input("y/n: ")
        if sel in selection_yes:
            print("ID of vertex: {}\n".format(ID))
            return ID
        elif sel in selection_no:
            print("Re-enter ID\n")
            return self.query_vertex_ID()
        else:
            print("Not a valid input\n")
            return self.query_vertex_ID()

    def save_and_exit(self):
        print("Saving and exiting graph generation tool.")
        self.store_solution_Master()
        self.store_solution_Working()
        print("Saved")


    def graph_generation_tool(self):
        print("Entering graph generation tool for {}".format(self.area_file_tosave[:-5]))
        tool_options = {
            '01': self.add_vertex,
            '02': self.modify_display_existing_vertex,
            #'03': self.change_graph,
            '03': self.save_and_exit
            #need a change graph option to jump graphs maybe

            }

        while True:
            print("\nCurrent Graph State: ")
            print(json.dumps(self.dd_graph, indent=4))
            print("\n")

            print("\nSelect option:\n")
            for key, value in tool_options.items():
                print("{}\t{}".format(key, value.__name__))

            print("q\tExit\n")

            choice_option = input("Enter Choice: ")

            if choice_option == 'q':
                print("Exiting tool and saving")
                self.save_and_exit()
                break

            else:
                selected_option = tool_options.get(choice_option)
                if selected_option:
                    selected_option()
                else:
                    print("Invalid choice. Please select a valid option.\n")

    #store known solutions to be recalculated based on time to adjust for density and for rain
    #pseudo memo by storing solutions that aren't in runtime
    def store_solution_Master(self):
        Json_OS_ProcessingFunctions.save_file_json(self.dd_graph, self.area_file_tosave, 0)

    def store_solution_Working(self):
        Json_OS_ProcessingFunctions.save_file_json(self.dd_graph, self.area_file_tosave, 1)

    def check_area_file_exist(self, area_file):
        #check if master file exists
        return Json_OS_ProcessingFunctions.check_file_exist(area_file, 0)

#_GRAPH TOOLS_#

#_DEBUG PRINT STUFF_#

#_DEBUG PRINT STUFF_#

#_MODIFIER FUNCTIONS_#

    def modify_display_existing_vertex(self):
        vert_list=list(self.dd_graph.keys())
        if len(vert_list)==0:
            print("Empty graph, returning to graph generating tool")
            return
        while True:
            for i in range(len(vert_list)):
                print("{:02d\t{}}".format(i,vert_list[i]))
            print("q\tExit")
            vert_modify = input("\nSelect index of Vertex to modify: ")

            if vert_modify=='q':
                print("returning  to graph generating tool")
                break
            try:
                vert_index = int(vert_modify)
                if 0<=vert_index < len(vert_list):
                    print("Selected {}".format(vert_list[vert_index]))
                    self.display_keys_to_modify(vert_list[vert_index])
                else:
                    print("Invalid choice. Please select a valid option.\n")
            except ValueError:
                print("Invalid choice. Please select a valid option.\n")

    def display_keys_to_modify(self, vert):
        print("Current vertex state:\n")
        print(json.dumps(self.dd_graph[vert], indent=4))
        print('\n')

        modifier_functions = {
            "00": self.Density_modifier_Rare,
            "01": self.Density_modifier_Medium,
            "02": self.Density_modifier_Welldone,
            "03": self.set_Sheltered_False,
            "04": self.set_Sheltered_True,
            "05": self.set_Route_intersection_False,
            "06": self.set_Route_intersection_True,
            "07": self.set_clearance,
            "08": self.set_Average_travel_time,
            "09": self.set_room_ID,
            "10": self.set_Connection_Point_False,
            "11": self.set_Connection_Point_True,
            "12": self.remove_clearance
        }

        m_list = list(modifier_functions.keys())
        selection = [i for i in range(len(m_list))]
        print("Options:\n")
        for i in range(len(m_list)):
            print("{:02d}\t{}".format(i, modifier_functions[m_list[i]].__name__))

        to_modify = input("\nSelect modification: ")
        if to_modify in m_list:
            print("Selected {}".format(modifier_functions[to_modify].__name__))
            modifier_functions[to_modify](vert)
        else:
            print("Invalid input!")
            return self.modify_display_existing_vertex()

    #used to modify the average density based on time, set higher on certain places on certain times
    #used to normalise routes based on density (i.e. a route might be shorter but have more people vs slightly longer route with no people)

    def Time_check(self):
        curr_DT = datetime.datetime.now()
        time_lunch_start='11:45:00'
        time_lunch_end='13:15:00'
        #anti range of lunch
        if datetime.datetime.now().strptime(time_lunch_start,'%H:%M:%S')<curr_DT<datetime.datetime.now().strptime(time_lunch_start,'%H:%M:%S'):
            print("Lunch Rush, adjusting routes")
            #find the specific vertex chokepoints to adjust in dd_graph
            l_vert_tochange=[]
            for i in l_vert_tochange:
                self.Time_Dist_modifier(i,1.5)

        else:
            print("Not lunch rush")
            return


    def Time_Dist_modifier(self, vertex, adj_val):
        self.dd_graph[vertex]["Average_travel_time"]*=adj_val

    def Density_modifier_MANUAL(self, vertex):
        pass

    #set to 1
    def Density_modifier_Rare(self, vertex):
        self.dd_graph[vertex]["Avg_density"]=1

    #set to 1.5
    def Density_modifier_Medium(self, vertex):
        self.dd_graph[vertex]["Avg_density"]=1.5

    #set to 2
    def Density_modifier_Welldone(self, vertex):
        self.dd_graph[vertex]["Avg_density"]=2

    def set_Sheltered_True(self, vertex):
        self.dd_graph[vertex]["Sheltered"]=True

    def set_Sheltered_False(self, vertex):
        self.dd_graph[vertex]["Sheltered"]=False

    def set_Route_intersection_True(self, vertex):
        self.dd_graph[vertex]["Route_intersection"]=True

    def set_Route_intersection_False(self, vertex):
        self.dd_graph[vertex]["Route_intersection"]=False

    def set_visited_MANUAL(self, vertex):
        temp = self.dd_graph[vertex]["Visited"]
        man_visited = input("Set number of times visited for {}:\t".format(vertex))
        self.dd_graph[vertex]["Visited"]=man_visited
        print("Initial visited: {}\nNew visited :{}\n".format(temp, man_visited))

    def set_visited_0(self, vertex):
        self.dd_graph[vertex]["Visited"]=0

    def set_visited_1(self, vertex):
        self.dd_graph[vertex]["Visited"]=1

    def set_Average_travel_time(self, vertex):
        while True:
            try:
                t_time=int(input("Enter average time to travel through this vertex in seconds: "))
                if t_time>=0:
                    break
                else:
                    print("out of index")
            except ValueError:
                print("Not a valid input (number)")

        self.dd_graph[vertex]["Average_travel_time"]=t_time

    def set_room_ID(self, vertex):
        ID_code = input("Enter Location ID code: ")
        self.dd_graph[vertex]["Room_ID"]=ID_code
        #to add this reflection into a lookup table in main, for quick reference

    def set_Connection_Point_True(self, vertex):
        self.dd_graph[vertex]["Connection_Point"]=True

    def set_Connection_Point_False(self, vertex):
        self.dd_graph[vertex]["Connection_Point"]=False

#_MODIFIER FUNCTIONS_#

#_ACCESS MODIFIER FUNCTIONS_#

    def check_Access(self, access_list, clearance_for_vertex):
        return len(set(access_list).intersection(clearance_for_vertex))>0

    def set_clearance(self, vertex):
        #copy availiable clearance from user.py
        c_list=["Fablab_basic","Fablab_Woodwork","Fablab_Metalwork","Hostel_55","Hostel_57","Hostel_59"]
        selection=[i for i in range(len(c_list))]
        print("Set Clearance for vertex: ")
        for i in range(len(c_list)):
            print("{:02d}\t{}".format(i,c_list[i]))
        clearance_select = input("\nSelect index of clearance to add: ")
        if int(clearance_select) in selection:
            #prevent double add (might not matter since itll be converted to a set but make life easy)
            if c_list[int(clearance_select)] in self.dd_graph[vertex]["Access_Clearance"]:
                print("Existing clearance")
                return
            print("{} clearance added to {}".format(c_list[int(clearance_select)],vertex))
            self.dd_graph[vertex]["Access_Clearance"].append(c_list[int(clearance_select)])
        else:
            print("Invalid input!")
            return self.set_clearance(vertex)

        cont = input("\nContinue adding clearance? y/n: ")
        if cont in selection_yes:
            self.set_clearance(vertex)

    def remove_clearance(self, vertex):
        #special case empty and one clearance
        if len(self.dd_graph[vertex]["Access_Clearance"])==0:
            print("No clearance to remove")
            return
        elif len(self.dd_graph[vertex]["Access_Clearance"])==1:
            print("Removing only clearance")
            self.dd_graph[vertex]["Access_Clearance"].clear()
            return
        selection=[i for i in range(len(self.dd_graph[vertex]["Access_Clearance"]))]

        print("Clearances for {}:\n".format(vertex))
        for i in range(len(self.dd_graph[vertex]["Access_Clearance"])):
            print("{:02d}\t{}".format(i, self.dd_graph[vertex]["Access_Clearance"][i]))

        todisc = input("\nSelect index of clearance to remove: ")
        if int(todisc) in selection:
            self.dd_graph[vertex]["Access_Clearance"].remove(self.dd_graph[vertex]["Access_Clearance"][int(todisc)])


        print("Current clearance state for {}:\n".format(vertex))
        for i in self.dd_graph[vertex]["Access_Clearance"]:
            print(i)
        cont = input("\nContinue removing clearance? y/n: ")
        if cont in selection_yes:
            self.remove_clearance(vertex)



#_ACCESS MODIFIER FUNCTIONS_#


#_PATH FINDING FUNCTIONS_#

    #Shortest paths
    def Dijkstra(self, source):
        pass

    def Floyd_Warshall(self, source):
        pass

    #heuristics
    def A_star(self, source, destination):
        pass

    def Ant_colony(self, source):
        pass


#_PATH FINDING FUNCTIONS_#

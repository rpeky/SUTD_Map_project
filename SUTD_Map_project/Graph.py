import Json_OS_ProcessingFunctions
import json
import datetime
import inspect

selection_yes=['1','y','Y','Yes','yes']
selection_no=['0','n','N','No','no']
selection_yes_and_no=selection_yes+selection_no
selection_quits = ['q','Q']

class Graph():
    def __init__(self, area_file, clearance, dd_lkup, dd_cplkup, dd_idlkup):
        #checked outside in main when initialising master lookup
        #Json_OS_ProcessingFunctions.check_folders_exist()
        self.dd_graph = dict()
        self.dd_lkup = dd_lkup
        self.dd_cplkup = dd_cplkup
        self.dd_idlkup = dd_idlkup
        self.access_clearance = clearance
        self.area_file_tosave = area_file
        self.localname = area_file[:-5]

        #check if map of area exists
        if self.check_area_file_exist(area_file):
            print("Loading {} from Master".format(self.localname))
            self.dd_graph = Json_OS_ProcessingFunctions.load_file_json(area_file, 0)
            self.graph_generation_tool()

        else:
            print("File does not exist")
            self.graph_generation_tool()

    def __del__(self):
        print("Saving to Working folder")
        self.store_solution_Working()
        print("Updating Lookup")
        #modify master lookup
        for key in self.dd_graph.keys():
            self.dd_lkup.update({key:self.area_file_tosave})
        #print(json.dump(self.dd_lkup))
        Json_OS_ProcessingFunctions.save_file_json(self.dd_lkup,"Lookup_directory.json",2)
        Json_OS_ProcessingFunctions.save_file_json(self.dd_cplkup,"Lookup_connections.json",2)
        Json_OS_ProcessingFunctions.save_file_json(self.dd_idlkup, "Lookup_locationID.json",2)

        print('deleting')

    # 3 types of query: ask user to select an option from a list/range, or just text
    @classmethod
    def query(cls, query_type, prompt, options=None, quit_option=False, confirm_selected_option=False):
        while True:
            selected_option = None
            while True:
                print()
                # Prompt the user for input
                if query_type == "list":
                    for i, option in enumerate(options):
                        print("{:02d}\t{}".format(i, Graph.get_name_str(option)))
                    if quit_option == True:
                        print("q\tExit")
                elif query_type == 'range':
                    pass
                elif query_type == "text":
                    pass
                user_input = input("\nEnter {}: ".format(prompt))
                if quit_option == True and user_input in selection_quits:
                    return "quit"
                # Ensure the user input is valid
                else:
                    # Input validation for list and range is similar
                    if query_type == "list":
                        min_input, max_input = 0, len(options)
                        try:
                            selected_index = int(user_input)
                            if min_input <= selected_index < max_input:
                                selected_option = options[selected_index]
                            else:
                                print("Out of index. Please select a valid option.\n")
                        except ValueError:
                            print("Invalid choice. Please select a valid option.\n")

                    elif query_type == "range":
                        min_input, max_input = options
                        try:
                            selected_index = int(user_input)
                            if min_input <= selected_index < max_input:
                                selected_option = selected_index
                            else:
                                print("Out of index. Please select a valid option.\n")
                        except ValueError:
                            print("Invalid choice. Please select a valid option.\n")

                    # No input validation for text is needed
                    elif query_type == "text":
                        selected_option = user_input
                        break

            # Let the user confirm his input again
            print("\nEntered input for {}: \n\t{}".format(prompt, Graph.get_name_str(selected_option)))
            if confirm_selected_option == True:
                while True:
                    print("\nConfirm input?")
                    sel = input("y/n: ")
                    if sel in selection_yes:
                        return selected_option
                    elif sel in selection_no:
                        print("Reenter your input\n")
                        break
                    else:
                        print("Invalid input. Please select y/n\n")
            else:
                return selected_option

    @staticmethod
    def get_name_str(obj):
        if inspect.ismethod(obj) or inspect.isfunction(obj):
            return obj.__name__
        else:
            return obj


#_GRAPH TOOLS_#
    #to think of more conditions of the vertex
    #using dictionaries to store the neighbour and its heading since python stores the insertion order of values
    def add_vertex(self):
        vertex_ID = self.query_vertex()
        if vertex_ID not in self.dd_graph.keys():
            neighbours = dict()
            dd_vertex = {
                    "Neighbour":neighbours,
                    "Neighbour_head":dict(),
                    "Visited": 0,
                    "Avg_density":1,
                    "Sheltered": True,
                    "Route_intersection": False,
                    "Access_Clearance": list(),
                    "Average_travel_time": None,
                    "Room_ID": None,
                    "Connection_Point": False,
                    "Connected_vertex": dict()
                }
            self.dd_graph[vertex_ID] = dd_vertex
        self.neighbour_tool(vertex_ID)

    def neighbour_tool(self, vertex_ID):
        #add heading to neighbour in data with distance
        while True:
            self.print_current_graph_state()
            cont = input("\nConfirm adding neighbour to {}?\ny/n: ".format(vertex_ID))
            if cont in selection_yes:
                self.add_neighbour(vertex_ID)
            elif cont in selection_no:
                break
            else:
                print("Invalid input")
                continue

    def add_neighbour(self, vertex_ID):
        while True:
            print("Enter Neighbour Vertex ID: ")
            neighbour_ID=self.query_vertex()
            confirm_Neighbour_ID = input("\nConfirm adding neighbour {} to {}?\ny/n: ".format(neighbour_ID,vertex_ID))
            if confirm_Neighbour_ID in selection_yes:
                adj_dist = self.query_neighbour_distance()
                adj_heading = self.query_neighbour_heading()
                self.dd_graph[vertex_ID]["Neighbour"][neighbour_ID] = adj_dist
                self.dd_graph[vertex_ID]["Neighbour_head"][neighbour_ID] = adj_heading

                # If neighbour is a new vertex, add it to dd_graph
                if neighbour_ID not in self.dd_graph.keys():
                    dd_vertex_new = {
                        "Neighbour": dict(),
                        "Neighbour_head": dict(),
                        "Visited": 0,
                        "Avg_density": 1,
                        "Sheltered": True,
                        "Route_intersection": False,
                        "Access_Clearance": list(),
                        "Average_travel_time": None,
                        "Room_ID": None,
                        "Connection_Point": False,
                        "Connected_vertex": dict()
                    }
                    self.dd_graph[neighbour_ID] = dd_vertex_new

                neighbour_adj_dist = adj_dist
                #neigbour conjugate heading
                neighbour_adj_heading = adj_heading + 180 if adj_heading < 180 else adj_heading - 180
                self.dd_graph[neighbour_ID]["Neighbour"][vertex_ID] = neighbour_adj_dist
                self.dd_graph[neighbour_ID]["Neighbour_head"][vertex_ID] = neighbour_adj_heading
                print("Returning to neighbour creation tool")
                break
            elif confirm_Neighbour_ID in selection_no:
                print("Returning to neighbour creation tool")
                break
            else:
                print("Invalid input")
                continue

    #adds distance and heading
    def query_neighbour_distance(self):
        prompt = "distance to adjacent vertex"
        distance_options = (0, float('inf'))
        distance = Graph.query("range", prompt, distance_options, confirm_selected_option=True)
        return distance
        '''while True:
            try:
                adj_vtx_dist = float(input("Enter distance to adjacent vertex: "))
                if adj_vtx_dist > 0:
                    cont = input("\nConfirm distance: {}m \ny/n: ".format(adj_vtx_dist))
                    if cont in selection_yes:
                        return adj_vtx_dist
                    else:
                        continue
                else:
                    print("Distance must be more than 0!")
            except ValueError:
                print("Not a number")'''

    def query_neighbour_heading(self):
        prompt = "bearing to adjacent vertex"
        bearing_options = (0, 360)
        bearing = Graph.query("range", prompt, bearing_options, confirm_selected_option=True)
        return bearing
        '''while True:
            try:
                adj_vtx_head = int(input("\nEnter bearing to adjacent vertex: "))
                if 0 <= adj_vtx_head < 360:
                    cont = input("\nConfirm heading {} degrees: \ny/n: ".format(adj_vtx_head))
                    if cont in selection_yes:
                        return adj_vtx_head
                    else:
                        continue
                else:
                    print("Heading must be more than 0!")
            except ValueError:
                print("Not a number")'''

    # UI portion for adding vertex information
    #vertex name making
    def query_vertex(self):
        #to add existing vertex selection
        q_pf=self.query_vertex_Prefix()
        q_id=self.query_vertex_ID()
        return self.localname+q_pf+"_"+q_id

    def query_vertex_Prefix(self):
        pref = ""
        # edit as needed
        ID_prefixes = ["LIFT_", "ROOM_", "DUSTBIN_", "INTER_", "TOILET_", "STAIRS_", "ENTRANCE_", "MAINROAD_",
                     "WALKWAY_","BUILDING"]
        prompt = "index of vertex prefix"
        selected_prefix = Graph.query(query_type="list", prompt=prompt, options=ID_prefixes, confirm_selected_option=True)
        return '_' + selected_prefix

    #kiv, removed from naming process since vert heading is now an attribute, may be able to reuse
    def query_vertex_Heading(self):
        prompt = "heading of vertex [01-360]"
        headings_options = (0, 360)
        heading = Graph.query(query_type="range", prompt=prompt, options=headings_options, confirm_selected_option=True)
        heading = format(heading,'02d')
        return heading

    def query_vertex_ID(self):
        prompt = "ID of vertex"
        vertex_ID = Graph.query(query_type="text", prompt=prompt, confirm_selected_option=True)
        return vertex_ID

    def save_and_exit(self):
        print("Saving and exiting graph generation tool.")
        self.store_solution_Master()
        self.store_solution_Working()
        print("Saved")


    def print_current_graph_state(self):
        print("\nCurrent Graph State: ")
        print(json.dumps(self.dd_graph, indent=4))
        print("\n")


    def graph_generation_tool(self):
        print("Entering graph generation tool for {}".format(self.area_file_tosave[:-5]))
        prompt = "tool for graph generation"
        tool_options = [
            self.add_vertex,
            self.modify_display_existing_vertex,
            self.query_pathfind,
            self.display_vertices,
            self.save_and_exit,
        ]

        while True:
            self.print_current_graph_state()
            selected_option = Graph.query("list", prompt,tool_options, quit_option=True)
            if selected_option == "quit":
                print("Exiting graph generation tool and saving")
                self.save_and_exit()
                print("Returning to mapping tool")
                break
            else:
                selected_option()



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

    def verify_endpoint_samegraph(self, endpoint):
        internal_vert_list = list(self.dd_graph.keys())
        return True if (endpoint in internal_vert_list) else False

#_DEBUG PRINT STUFF_#

    def display_vertices(self):
        vert_list=list(self.dd_graph.keys())
        if len(vert_list)==0:
            print("Empty graph")
        for i in range(len(vert_list)):
            print("{:02d}\t{}".format(i,vert_list[i]))
        while True:
            endstare = input("Enter any key to continue:\t")
            break

#_DEBUG PRINT STUFF_#

#_MODIFIER FUNCTIONS_#

    def modify_display_existing_vertex(self):
        vertex_list=list(self.dd_graph.keys())
        if len(vertex_list)==0:
            print("Empty graph, returning to graph generating tool")
            return
        while True:
            prompt = "index of vertex to modify"
            vertex = Graph.query("list", prompt, options=vertex_list, quit_option=True)
            if vertex == "quit":
                print("returning to graph generating tool")
                return
            else:
                self.modify_display_vertex(vertex)

    def modify_display_vertex(self, vertex):
        modifier_functions = [
            self.Density_modifier_Rare,
            self.Density_modifier_Rare,
            self.Density_modifier_Medium,
            self.Density_modifier_Welldone,
            self.set_Sheltered_True,
            self.set_Sheltered_False,
            self.set_Route_intersection_True,
            self.set_Route_intersection_False,
            self.set_visited_MANUAL,
            self.set_visited_0,
            self.set_visited_1,
            self.set_Average_travel_time,
            self.set_room_ID,
            self.set_Connection_Point_True,
            self.set_Connection_Point_False,
            self.set_clearance,
            self.remove_clearance,
            self.add_existing_neighbours,
            self.remove_existing_neighbours,
            self.modify_existing_neighbours_headings,
            self.add_external_connectionpoint,
            self.add_node_description
        ]
        prompt = "modifier function"
        while True:
            to_modify = Graph.query("list", prompt, options=modifier_functions, quit_option=True)
            if to_modify == "quit":
                break
            else:
                to_modify(vertex)

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
                self.Time_Dist_modifier(i,2)

        else:
            print("Not lunch rush")
            return


    def Time_Dist_modifier(self, vertex, adj_val):
        self.dd_graph[vertex]["Average_travel_time"]*=adj_val

    def Density_modifier_MANUAL(self, vertex):
        while True:
            try:
                man_density = int(input("\nSet average density: "))
                if man_density > 0:
                    break
                else:
                    print("Not wihtin valid index > 0")
            except:
                print("\nNot a number, try again\n")
        self.dd_graph[vertex]["Avg_density"]=man_density

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

    def set_visited_add(self, vertex):
        self.dd_graph[vertex]["Visited"]+=1

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
        #to add this reflection into a lookup table in main, for quick reference
        if self.dd_graph[vertex]["Room_ID"] == None:
            #temp prints
            ID_code = input("Enter Location ID code: ")
            print("New room ID {}, appending to lookup".format(ID_code))
            self.dd_graph[vertex]["Room_ID"]=ID_code
            self.dd_idlkup.update({ID_code:vertex})

        else:
            initialID = self.dd_graph[vertex]["Room_ID"]
            while True:
                cont = input("Modify room ID {}?".format(initialID))
                if cont in selection_yes:
                    ID_code = input("Enter Location ID code: ")
                    print("Modified room ID {}, appending to lookup".format(ID_code))
                    self.dd_idlkup.update({ID_code: vertex})
                    self.dd_graph[vertex]["Room_ID"]=ID_code
                elif cont in selection_no:
                    break
                else:
                    print("Invalid input")
                    continue

    def set_Connection_Point_True(self, vertex):
        self.dd_graph[vertex]["Connection_Point"]=True
        self.dd_cplkup.update({vertex:self.area_file_tosave})
        print("Connection point set to True")
        #self.add_external_connectionpoint(vertex)

    def set_Connection_Point_False(self, vertex):
        self.dd_graph[vertex]["Connection_Point"]=False
        tmep = self.dd_cplkup.pop(vertex, None)
        print("Removed: {}".format(tmep))

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

        print("Clearances for {}:\n".format(vertex))
        for i in range(len(self.dd_graph[vertex]["Access_Clearance"])):
            print("{:02d}\t{}".format(i, self.dd_graph[vertex]["Access_Clearance"][i]))
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


    def add_existing_neighbours(self, vertex_ID):
        while True:
            already_neighbours = self.dd_graph[vertex_ID]["Neighbour"].keys()
            # Selection vertices must not already be neighbours, nor can the vertex be a neighbour to itself
            vert_list = [vert for vert in self.dd_graph.keys() if (vert not in already_neighbours) and (vert != vertex_ID)]
            if len(vert_list)==0:
                print("No neighbours to add!\n")
                break
            selection = [i for i in range(len(vert_list))]


            for i in range(len(vert_list)):
                print("{:02d}\t{}".format(i, vert_list[i]))
            to_add_as_neighbour = None
            while True:
                to_add_as_neighbour = input("Enter existing Vertex ID to add as neighbour: ")
                try:
                    if int(to_add_as_neighbour) in selection:
                        print("Selected {}".format(vert_list[int(to_add_as_neighbour)]))
                        break
                    else:
                        print("Invalid input!")
                        continue
                except ValueError:
                    print("Not a valid existing Vertex ID")
            neighbour_ID = vert_list[int(to_add_as_neighbour)]
            confirm_Neighbour_ID = input("\nConfirm adding neighbour {} to {}?\ny/n: ".format(neighbour_ID, vertex_ID))
            if confirm_Neighbour_ID in selection_yes:
                adj_dist = self.query_neighbour_distance()
                adj_heading = self.query_neighbour_heading()
                self.dd_graph[vertex_ID]["Neighbour"][neighbour_ID] = adj_dist
                self.dd_graph[vertex_ID]["Neighbour_head"][neighbour_ID] = adj_heading
                self.dd_graph[neighbour_ID]["Neighbour"][vertex_ID] = adj_dist
                self.dd_graph[neighbour_ID]["Neighbour_head"][vertex_ID] = adj_heading + 180 if adj_heading < 180 else adj_heading - 180
                print("\nNeighbour {} added to {}".format(neighbour_ID, vertex_ID))
            confirm = input("Continue setting an existing vertex as neighbour to {}?\ny/n: ".format(vertex_ID))
            if confirm in selection_no:
                break

    def remove_existing_neighbours(self, vertex_ID):
        while True:
            vert_list = list(self.dd_graph.keys())
            selection = [i for i in range(len(vert_list))]
            for i in range(len(vert_list)):
                print("{:02d}\t{}".format(i, vert_list[i]))
            to_remove_as_neighbour = None
            while True:
                to_remove_as_neighbour = input("Enter existing Vertex ID to remove as neighbour: ")
                if int(to_remove_as_neighbour) in selection:
                    print("Selected {}".format(vert_list[int(to_remove_as_neighbour)]))
                    break
                else:
                    print("Invalid input!")
                    continue
            neighbour_ID = vert_list[int(to_remove_as_neighbour)]
            confirm_Neighbour_ID = input("\nConfirm removing neighbour {} from {}?\ny/n: ".format(neighbour_ID, vertex_ID))
            if confirm_Neighbour_ID in selection_yes:
                if neighbour_ID in self.dd_graph[vertex_ID]["Neighbour"]:
                    del self.dd_graph[vertex_ID]["Neighbour"][neighbour_ID]
                if vertex_ID in self.dd_graph[neighbour_ID]["Neighbour"]:
                    del self.dd_graph[neighbour_ID]["Neighbour"][vertex_ID]
                print("\nNeighbour {} removed from {}".format(neighbour_ID, vertex_ID))
            confirm = input("Continue removing an existing vertex as neighbour from {}?\ny/n: ".format(vertex_ID))
            if confirm in selection_no:
                break

    def modify_existing_neighbours_headings(self, vertex_ID):
        while True:
            neighbours_headings = self.dd_graph[vertex_ID]["Neighbour_head"]
            vert_list = list(neighbours_headings.keys())
            selection = [i for i in range(len(vert_list))]
            for i in range(len(vert_list)):
                print("{:02d}\t{}".format(i, vert_list[i]))
            to_modify_heading = None
            while True:
                to_modify_heading = input("Enter existing neighbour Vertex ID whose heading to modify: ")
                if int(to_modify_heading) in selection:
                    print("Selected {}".format(vert_list[int(to_modify_heading)]))
                    break
                else:
                    print("Invalid input!")
                    continue
            neighbour_ID = vert_list[int(to_modify_heading)]
            existing_heading = neighbours_headings[neighbour_ID]
            new_heading = self.query_neighbour_heading()
            neighbour_new_heading = new_heading + 180 if new_heading < 180 else new_heading - 180
            confirm_modify_heading = input("\nConfirm changing heading of {} from {} to {}?\ny/n: ".format(neighbour_ID, existing_heading, new_heading))
            if confirm_modify_heading in selection_yes:
                self.dd_graph[vertex_ID]["Neighbour_head"][neighbour_ID] = new_heading
                self.dd_graph[neighbour_ID]["Neighbour_head"][vertex_ID] = neighbour_new_heading
            confirm = input("Continue modifying headings of existing neighbours of {}? \ny/n: ".format(vertex_ID))
            if confirm in selection_no:
                break

#_ACCESS MODIFIER FUNCTIONS_#

#_CONNECTION POINT FUNCTIONS_#

    def add_external_connectionpoint(self, vertex):
        #not allowed if not a connection point
        if self.dd_graph[vertex]["Connection_Point"]==False:
            print("Not a connection point\n")
            return
        cont = input("\nConnection Point Tool\nThis node appears to connect to other mapped areas, continue setting link? y/n:\t")
        if cont in selection_yes:
            counter=0
            sel_list=list()
            for point in self.dd_cplkup:
                if (self.dd_cplkup[point]!=self.area_file_tosave) and (point not in self.dd_graph[vertex]["Connected_vertex"]):
                    print("{:02d}\t{}\t{}".format(counter,point,self.dd_cplkup[point]))
                    counter+=1
                    temp_tup = (point, self.dd_cplkup[point])
                    sel_list.append(temp_tup)
            while True:
                try:
                    selec = input("Select Connection Point (q to exit): ")
                    if selec == 'q' or selec == 'Q':
                        return
                    selec = int(selec)
                    if selec>-1 and selec<counter:
                        break
                    else:
                        print("out of index")
                except ValueError:
                    print("Not a valid input")
            self.dd_graph[vertex]["Connected_vertex"].update({sel_list[selec][0]:sel_list[selec][1]})
            #add distance to connected vertex
            con_dist = self.query_neighbour_distance()
            con_heading = self.query_neighbour_heading()
            if sel_list[selec][0] not in self.dd_graph[vertex]["Neighbour"]:
                self.dd_graph[vertex]["Neighbour"][sel_list[selec][0]] = con_dist
                self.dd_graph[vertex]["Neighbour_head"][sel_list[selec][0]] = con_heading
            #add for conjugate,save to master
            dd_mod = Json_OS_ProcessingFunctions.load_file_json(sel_list[selec][1],0)
            if vertex not in dd_mod[sel_list[selec][0]]["Connected_vertex"]:
                dd_mod[sel_list[selec][0]]["Connected_vertex"].update({vertex:self.area_file_tosave})
                dd_mod[sel_list[selec][0]]["Neighbour"][vertex] = con_dist
                dd_mod[sel_list[selec][0]]["Neighbour_head"][vertex] = con_heading
                Json_OS_ProcessingFunctions.save_file_json(dd_mod,sel_list[selec][1],0)

            print("Added connection\n")
            ct = input("Additional vertices? y/n:\t")
            if ct in selection_yes and counter>1:
                return self.add_external_connectionpoint(vertex)
            else:
                print("No additional connections to add")
        else:
            return

    def add_node_description(self, vertex):
        if self.dd_graph[vertex].get("Description") != None:
            print("Update description\n")
            #some update description function
        else:
            vtxdesc = input("Enter vertex context / description: \t")
            print("adding description: {}".format(vtxdesc))
            #some confirm logic
            self.dd_graph[vertex].update({"Description":vtxdesc})

#_CONNECTION POINT FUNCTIONS_#
    def graphswaps(self):
        pass

#_PATH FINDING FUNCTIONS_#

    #Shortest paths
    def Dijkstra_modified(self, startpoint):
        djk_dict = dict()
        vtxs = set(self.dd_graph.keys())
        for vtx in vtxs:
            if (vtx == startpoint):
                djk_dict[vtx] = (0,[])
            else:
                djk_dict[vtx] = (float('inf'),[])
        visited_vtxs = set()
        current_vtx = startpoint
        while True:
            # Mark current vertex as visited
            visited_vtxs.add(current_vtx)

            # Get list of adjacent vertices
            adj_vtxs = [i for i in self.dd_graph[current_vtx]["Neighbour"].keys() if i in vtxs]

            # Update distances of adjacent vertices
            for adj_vtx in adj_vtxs:
                old_dist = djk_dict[adj_vtx][0]
                old_path = djk_dict[adj_vtx][1]
                new_dist = djk_dict[current_vtx][0] + self.dd_graph[current_vtx]["Neighbour"][adj_vtx]
                new_path = djk_dict[current_vtx][1] + [current_vtx]
                if new_dist < old_dist:
                    djk_dict[adj_vtx] = (new_dist,new_path)

            # Unvisited vertex with minimum distance is visited next
            current_vtx = None
            current_vtx_dist = float('inf')
            for vtx, tuptup in djk_dict.items():
                if vtx not in visited_vtxs and tuptup[0] < current_vtx_dist:
                    current_vtx = vtx
                    current_vtx_dist = tuptup[0]
            if current_vtx == None:
                break

        return djk_dict

    def Dijkstra_externalpoints(self, startpoint):
        pass

    def Floyd_Warshall(self, source):
        pass

    #heuristics
    def A_star(self, source, destination):
        pass

    def Ant_colony(self, source):
        pass


#_PATH OUTPUT FUNCTIONS_#

    def query_pathfind(self):
        #need to provide an option to choose points beyond internal graph
        vtxs = list(self.dd_graph.keys())
        for i in range(len(vtxs)):
            print("{:02d}\t{}".format(i, vtxs[i]))
        while True:
            try:
                start_point = int(input("\nSelect index of starting point: "))
                if start_point in range(len(vtxs)):
                    break
                else:
                    print("Not a valid starting point index \n")
            except ValueError:
                print("Not a valid starting point index \n")
        while True:
            try:
                end_point = int(input("\nSelect index of end point: "))
                if end_point in range(len(vtxs)):
                    break
                else:
                    print("Not a valid end point index \n")
            except ValueError:
                print("Not a valid end point index \n")
        if self.verify_endpoint_samegraph(vtxs[end_point]):
            sol = self.Dijkstra_modified(vtxs[start_point])
            print("All solutions:\n")
            print(json.dumps(sol, indent=4))
            print("\nSolution: ")
            self.show_route(sol[vtxs[end_point]][1])

        else:
            print("WIP point out of current graph")

    def show_route(self, ls_sol):
        for i in ls_sol:
            print(i, "\n")


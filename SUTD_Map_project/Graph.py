import Json_OS_ProcessingFunctions

class Graph():
    def __init__(self):
        Json_OS_ProcessingFunctions.check_folders_exist()
        self.dd_graph = dict()  
        
    def __del__(self):
        print('deleting')   
        
#_GRAPH TOOLS_#
    #to think of more conditions of the vertex
    def add_vertex(self):
        
        vertex_ID = self.query_vertex()
        self.neighbours = dict()
        self.dd_vertex = {
                "Neighbour":self.neighbours,
                "Visited": 0,
                "Avg_density":1,
                "Sheltered": True,
                "Route_intersection": False
            }
        self.dd_graph[vertex_ID] = self.dd_vertex
    
    # tuple (distance, ID, special)
    def add_neighbour(self):
        pass   
    
    # UI portion for adding vertex
    def query_vertex(self):
        self.query_vertex()
        

    def query_vertex_Prefix(self):
        ID_prefix = ["LIFT_","ROOM_","DUSTBIN_","IINTER_","TOILET_","STAIRS_"]
        print("Pick a prefix:\n{}".format(ID_prefix))
        pass
        
    def query_vertex_ID(self):
        pass
        
    #store known solutions to be recalculated based on time to adjust for density and for rain
    #pseudo memo by storing solutions that aren't in runtime
    def store_solution(self):
        pass
    
#_GRAPH TOOLS_#
        
#_DENSIRY MODIFIER FUNCTIONS_#

    #used to modify the average density based on time, set higher on certain places on certain times
    #used to normalise routes based on density (i.e. a route might be shorter but have more people vs slightly longer route with no people)
    def Time_check(self):
        pass
    
    def Density_modifier(self):
        pass
    
#_DENSIRY MODIFIER FUNCTIONS_#
    
    
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

class Graph():
    def __init__(self):
        self.dd_graph = dict()  
    
    #to think of more conditions of the vertex
    def add_vertex(self):
        vertex_ID = None
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
        
    def __del__(self):
        print('deleting')
        
    

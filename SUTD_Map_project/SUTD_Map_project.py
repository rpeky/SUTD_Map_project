import time
import Graph
import User
import json


def testbench():

    uu=User.User()
    uu.add_clearance()
    uu.remove_clearance()
    print(uu.__dict__)
    gg = Graph.Graph(uu.clearance_card)
    gg.add_vertex()
    print(gg.__dict__)    


def main():
    testbench()
    


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(time.process_time()-start_time)
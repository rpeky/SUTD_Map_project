import time
import Graph
import User


def testbench():
    gg = Graph.Graph()
    vt_pf = gg.query_vertex_Prefix()
    print(vt_pf)
    uu = User.User()
    uu.add_clearance()
    print(uu.__dict__)

def main():
    testbench()
    


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(time.process_time()-start_time)
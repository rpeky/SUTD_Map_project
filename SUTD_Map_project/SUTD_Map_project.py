import time
import Graph


def testbench():
    gg = Graph.Graph()
    print(gg.__dict__)
    pass

def main():
    testbench()

if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(time.process_time()-start_time)
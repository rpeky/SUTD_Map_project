import time

def testbench():
    print(1+1)
    pass

def main():
    testbench()
    print('test')
    pass

if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(time.process_time()-start_time)
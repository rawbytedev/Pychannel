import asyncio
import time

from channel import Channel, Handler
import multiprocessing as mp
import channel
from fifo import fifo
    
def test_Basic():
    a = Channel()
    child = a.Child() ## note .chile allows to set other process as child of channel
    H = Handler(child, int, 5)
    ch = H.child
    ## the ideal scenario is having Pychannel start those Process itselfs
    proc = mp.Process(target=H.subreceive)
    proc.start()
    procs = mp.Process(target=StartOutside, kwargs={"conn":ch})
    procs.start()
    
    for i in range(100):
        print(a.receive())
    a.close()
def StartOutside(conn):
    b = Channel(conn)
    for i in range(100):
        b.send(i)
    b.close()


def testfifocap():
    chan = fifo(cap=2, obj=str)
    idx = 0
    while chan.CanAdd():
        chan.add(f"hello world {idx+1}")
        idx =idx+1
    chan.add("hey") ## this value never gets added 
    ## blocking is provided by pipe so it doesn't need it
    try:
        chan.pop()
        print("fifo cap: failed")
    except:
        pass
    if idx == 2:
        print("fifo cap: test passed")


def testBlocking():
    a = Channel(int, capacity=10)
    child = a.Child() ## note .chile allows to set other process as child of channel
    ## in future normalize mp.Process for simpler use or switch to async functions
    proc = mp.Process(target=StartOutside, kwargs={"conn":child})
    proc.start()
    ## block
    print(a.receive())
    print("blocking main") ## not exactly blocking but if it stops
    ## requeting data from child child pauses
    time.sleep(2)
    for i in range(1,100):
        if a.receive() != i:
            print("TestFailed")
    print("Test Passed")


if __name__ == "__main__":
    test_Basic()
    #testfifocap()
    #testBlocking()
    
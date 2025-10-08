from channel import Channel
import multiprocessing as mp
from fifo import fifo
    
def test_Basic():
    a = Channel(int, capacity=10)
    child = a.Child() ## note .chile allows to set other process as child of channel
    proc = mp.Process(target=StartOutside, kwargs={"conn":child})
    proc.start()
    for b in range(100):
        data = a.receive()
        if data != b:
            print("testBasic: Failed_test")
            return
    print("testBasic: Passed")
def StartOutside(conn):
    b = Channel(int, False,conn)
    for i in range(100):
        b.send(i)


def testfifocap():
    chan = fifo(cap=2, obj=str)
    idx = 0
    while chan.CanAdd():
        chan.add(f"hello world {idx+1}")
        idx =idx+1
    if idx == 2:
        print("test passed")
    


if __name__ == "__main__":
    test_Basic()
    testfifocap()
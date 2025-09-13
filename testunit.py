from channel import Channel
import multiprocessing as mp
from fifo import fifo
    
def test_StartMain():
    a = Channel("string", capacity=10)
    child = a.Child()

    proc = mp.Process(target=StartOutside, kwargs={"conn":child})
    proc.start()
    for b in range(100):
        data = a.receive()
        print(f"{b}:{data}")

def StartOutside(conn):
    b = Channel("string", False,conn)
    for i in range(100):
        b.send(f"data + idx{i}")
def testfifocap():
    chan = fifo(cap=2, obj=str)
    idx = 0
    while chan.CanAdd():
        chan.add(f"hello world {idx+1}")
        idx =idx+1
    if idx == 2:
        print("test passed")
    


if __name__ == "__main__":
    #test_StartMain()
    testfifocap()
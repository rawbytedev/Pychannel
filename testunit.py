import time

from channel import Channel
import multiprocessing as mp
import channel
from fifo import fifo
    
def test_Basic():
    a = Channel(cap=5, types=int)
    a.initHandle()
    a.startSub(StartOutside)
    for i in range(5):
        print(a.receive())
    time.sleep(1) 
    for i in range(95):
        print(a.receive())
    a.close()
def StartOutside(conn):
    b = Channel(conn)
    for i in range(100):
        b.send(i)
    b.close()


if __name__ == "__main__":
    test_Basic()
    
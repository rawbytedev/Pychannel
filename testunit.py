import time

from channel import Channel
import multiprocessing as mp
import channel
from fifo import fifo
    
def test_Basic():
    a = Channel(cap=5, types=str)
    a.initHandle()
    a.startSub(TypeErrors) ## works if we stick to type
    ## note: channel can't be stopped if thing go too fast
    ## but this clearly show that fifo was used to store 5 items and it stop
    for i in range(5):
        if a.isChan():
            print(a.receive())
    time.sleep(1) 
    for i in range(95):
        if a.isChan():
            print(a.receive())
    a.close()
def StartOutside(conn):
    b = Channel(conn)
    for i in range(100):
        b.send("hi") ## int is an object but not string??
    b.close()

## we need to flush out datas and notify childs to stop sending
def TypeErrors(conn):
    b = Channel(conn=conn)
    for i in range(100):
        if b.isChan():
            b.send(f"Types {i}")

if __name__ == "__main__":
    test_Basic()
    
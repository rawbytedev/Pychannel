import time

from channel import Channel
import multiprocessing as mp
import channel
from fifo import fifo
    
def test_Basic():
    a = Channel(cap=5, types=str)
    a.initHandle()
    a.startSub(func=TypeErrors,value=1) ## works if we stick to type
    ## note: channel can't be stopped if thing go too fast
    ## but this clearly show that fifo was used to store 5 items and it stop
    for i in range(5):
        if a.isChan():
            print(a.receive())
    time.sleep(1) 
    for i in range(95):
        if a.isChan():
            print(a.receive())
    a.close() ## work because we close the channel manually from parent
def StartOutside(conn):
    b = Channel(conn)
    for i in range(100):
        b.send("hi") ## int is an object but not string??
    b.close() ## killing from child doesn't have much effects

## we need to flush out datas and notify childs to stop sending
def TypeErrors(conn, value):
    b = Channel(conn=conn)
    for i in range(100):
        if b.isChan():
            b.send(f"Types {value}:{i}")

if __name__ == "__main__":
    test_Basic()
    
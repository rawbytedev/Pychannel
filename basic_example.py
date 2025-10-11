import time
from channel import Channel


def LightProcessing(conn, data):
    ch = Channel(conn=conn)
    print("Child: Processing Data")
    res = data
    time.sleep(1)
    ch.send(res)

def Main():
    data = input("")
    ch = Channel(types=str, cap=2)
    ch.initHandle()
    ch.startSub(func=LightProcessing, data=data)
    print("doing some other works")
    time.sleep(5)
    print("waiting for child results")
    print(ch.receive()) ## blocks child stills needs 5 sec before finishing
    ch.close() ## close channel after

if __name__ == "__main__":
    Main()
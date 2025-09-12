from channel import Channel
import multiprocessing as mp
def StartMain():
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

if __name__ == "__main__":
    StartMain()
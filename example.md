# Example Uses

## Light Processing Child + Lightweight Main

```python
def LightProcessing(conn, data):
    ch = Channel(conn)
    print("Child: Processing Data")
    res = data
    time.sleep(1)
    ch.send(res)

def Main():
    data = input("")
    ch = Channel(types=str, cap=1)
    ch.initHandle()
    ch.startSub(func=LightProcessing, data=data)
    print("doing some other works")
    time.sleep(5)
    print("waiting for child results")
    print(a.receive()) ## blocks child stills needs 5 sec before finishing
    a.close() ## close channel after

if __name__ == "__main__":
    Main()
```
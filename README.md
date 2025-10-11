# PyChannel

**Go‑style channels in Python** — simple, safe, and powerful inter‑process communication.  
PyChannel brings the elegance of Go’s concurrency model into Python, enabling subprocesses to communicate through typed channels with synchronous or buffered semantics.

---

## Features

-  **Go‑like Channels** — send and receive values between processes with a clean API.  
-  **Unbuffered & Buffered Modes** — synchronous handoff or FIFO/LIFO buffering.  
-  **Composable** — designed to integrate with `multiprocessing` and task orchestration.  
-  **Lightweight** — built on top of Python’s `multiprocessing.Pipe`.  

---

##  Installation

Clone the repo and install locally:

```bash
git clone https://github.com/rawbytedev/pychannel.git
cd pychannel
```

---

##  Usage

### Basic Channel

```python
import time
from Pychannel import Channel


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

```

**Output:**
```
<Input>
doing some other works
Child: Processing Data
waiting for child results
<Input>
```

---

### Buffered FIFO Example

```python
from pychannel.fifo import fifo

q = fifo("str", capacity=2)
q.add("first")
q.add("second")
print(q.pop())  # "first"
print(q.pop())  # "second"
```

---

## Tests

Tests are included in [Tests](./testunit.py)

---

## Project Structure

```
pychannel/
│
├── channel.py        # Core Channel abstraction
├── fifo.py           # FIFO / LIFO buffer implementations
├── exceptions.py     # (planned) custom exceptions
├── example.md        # contains list if applicable example with test code(currently all codes work)
├── testunit.py       # Demo + unit tests
└── README.md
```

---

## Contributing

Pull requests are welcome! For major changes, Improvements, or Suggestions please open an issue first to discuss what you’d like to add.

---

## License

License. See [LICENSE](LICENSE) for details.
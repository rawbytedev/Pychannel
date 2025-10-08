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
from pychannel import Channel
import multiprocessing

def worker(conn):
    ch = Channel("str", main=False, conn=conn)
    ch.send("Hello from subprocess!")

if __name__ == "__main__":
    ch = Channel("str")
    p = multiprocessing.Process(target=worker, args=(ch.Child(),))
    p.start()
    msg = ch.receive()
    print("Main received:", msg)
    p.join()
```

**Output:**
```
Main received: Hello from subprocess!
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

Run the included test suite:

```bash
pytest testunit.py -v
```

---

## Project Structure

```
pychannel/
│
├── channel.py        # Core Channel abstraction
├── fifo.py           # FIFO / LIFO buffer implementations
├── exceptions.py     # (planned) custom exceptions
├── subproc.py        # (planned) orchestration helpers
├── testunit.py       # Demo + unit tests
└── README.md
```

---

## Roadmap

- [ ] Buffered channels integrated with `fifo`  
- [ ] `select`‑like API for waiting on multiple channels  
- [ ] Rich error handling (`ChannelClosedError`, `DeadlockError`)  
- [ ] Async/await integration for modern Python concurrency  
- [ ] Real‑world demos (task queues, pipelines, agent communication)  

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to add.  

---

## License

MIT License. See [LICENSE](LICENSE) for details.
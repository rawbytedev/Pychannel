import time
from channel import Channel

"""
We proved that we can have multiple childs and 1 parent:
for a case: sorting files based on their extension
- we write a method that takes conn and return send "Done" to Parent once it's done
with it's job
- it takes an additionnal arguments exten(extension) which represent the extension to 
look for and sort
- in this case Pychannel integrate cleanly instead of writing a method to handle each
extensions(.py, .bat, .docx, .txt) cases write a single one that handle extension based on inputs
and use Pychannel to start as many subprocess as needed they'll report back when done
This give the following advantages:
- Faster completion of processing; methods faced with a small amount of files
get done faster
- Reusable codes for multiple different extensions

Disadvantages:
- High comsumption of memory(this is normal)
- High cpu-usage

Works well in evironment when we need the Main Process to be alive while ensuring it receives
input from different sources(childs)
The Main listen for incomming inputs and Process them
## first run (Main2)
<input> Hello guys who respond first?
doing some other works
Child 1: Processing Data
Child 2: Processing Data
waiting for child results
Child 1: Hello guys who respond first?
Child 2: Hello guys who respond first?
## second run (Main2)
<input> Who is first?
doing some other works
Child 2: Processing Data
Child 1: Processing Data
waiting for child results
Child 2: Who is first?
Child 1: Who is first?

Current:
Current Pipe modules for communication between Subprocess, threads... blocks when used
this also result in having the Main process wait for them but with Pychannel that changes
because the child can be started early and can finish their execution before the parent
request data from them and the parent stills gets the requested data
This looks closely like Go style channels
For more complexity parent should be able to send data to child who can receive them
and work on it without issue(but this needs to be tested)
The project is in it's early stages and can present multiple errors
working with pipe is quite sensible and mistakes can break everything down
Proposal:
I would like to see the possibility of having nested Parents and turn it into a more
complex communication Pipe
"""

def LightProcessing(conn, data):
    ch = Channel(conn=conn)
    print("Child 1: Processing Data")
    res = data
    time.sleep(1)
    ch.send(f"Child 1: {res}")
    
def Light2Processing(conn, data):
    ch = Channel(conn=conn)
    print("Child 2: Processing Data")
    res = data
    time.sleep(1)
    ch.send(f"Child 2: {res}")

def Main():
    data = input("")
    ch = Channel(types=str, cap=2)
    ch.initHandle() ## this is always needed
    ch.startSub(func=LightProcessing, data=data)
    print("doing some other works")
    time.sleep(5)
    print("waiting for child results")
    print(ch.receive()) ## blocks child stills needs 5 sec before finishing
    ch.close() ## close channel after

def Main2():
    data = input("")
    ch = Channel(types=str, cap=2)
    ch.initHandle()
    ch.startSub(func=LightProcessing, data=data)
    ch.startSub(func=Light2Processing, data=data)
    print("doing some other works")
    time.sleep(5)
    print("waiting for child results")
    print(ch.receive()) ## blocks child stills needs 5 sec before finishing
    print(ch.receive())
    ch.close() ## close channel after

if __name__ == "__main__":
    print("starting example 1")
    Main()
    print("Starting example 2")
    Main2()
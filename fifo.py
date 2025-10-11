## How does blocking works?
    ## simple looping around canAdd until it says true
    ## it will say true when the value was remove that means when a child
    ## calls revc; the first elem of list is removed then sent over
"""
it a FIFO type of list the first elemen added is the First to be removed
it does align with how channels works and with the use of CanAdd we can know whether
the list is full or not size doesn't use len() this is to avoid recomputing the size in case of
large lists so we keep account of the number of elements
Next isObj this ensure that only the chosen object are store
- adding error in case a bad elem type is added to list is planned
for now fifo acts as the back bone for the Python implementation of Golang buffered channels
what's more it can be used for Unbuffered channels(honnestly using fifo to handle unbuffered
channels feels like a waste but getting optimizations right won't make it that bad)
- adding error handling and more errors like channels deadlocks
- adding support for other types for subprocess(cause I only tested with MultiProcessing) next
might be parallel threads 


FILO(First In Last Out) == LIFO(Last In First Out)
LILO(Last In Last Out) == FIFO(First In First Out)
"""
## first added is remove first
class fifo:
    def __init__(self, cap:int,obj:object):
        self.cap = cap
        self.obj = obj
        self.values:list[obj] =[] ## change list to use fifo instead
        
    def isObj(self, val) -> bool:
        if type(val) == self.obj:
            return True
        return False
    
    def obj(self):
        return self.obj
    ## it tells us whether we can add or not if not possible we block until it is free
    ## right now this is the only way
    ## looping to block? need a new way to block 
    def CanAdd(self) -> bool:
        if len(self.values) == self.cap:
            return False
        if len(self.values) < self.cap:
            return True
        ## avoid adding if impossible
        return False
    
    def add(self, value):
        if self.isObj(value):
            if self.CanAdd():
                self.values.append(value)
                return
        return TypeError
    def pop(self) -> object : 
        return self.values.pop(0)
    
    ## fifo.log is for debugging
    def log(self) -> list[object]:
        return self.values
    
    def size(self):
        return len(self.values)
    
    def empty(self):
        self.values = []

## first added item is removed last 
class filo:
    def __init__(self, cap:int,obj:object):
        self.cap = cap
        self.obj = obj
        self.values:list[object] =[]
        
    def isObj(self, val) -> bool:
        if type(val) == self.obj:
            return True
        return False
    ## it tells us whether we can add or not if not possible we block until it is free
    
    def CanAdd(self) -> bool:
        if len(self.values) == self.cap:
            return False
        if len(self.values) < self.cap:
            return True
        ## avoid adding if impossible
        return False
    
    def add(self, value):
        if self.isObj(value):
            if self.CanAdd():
                self.values.append(value)
                return
        return TypeError
            
    def pop(self) -> object : 
        #self.values.remove(value)
        return self.values.pop()
    ## need to change to manual logging of size
    def log(self) -> list[object]:
        return self.values
    
    def size(self):
        return len(self.values)

def testtype(types:object):
    a = fifo(cap = 5,obj=types)
    print(a.add("hi"))

if __name__ == "__main__":
    testtype(str)
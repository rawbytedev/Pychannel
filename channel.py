import multiprocessing as mp
## Each channel uses it
## when initialize any subprocess can use the channel as long as it can access Channel
class Channel:
    ## two type of init for main / subprocess
    ## make(chan type, capacity)
    ## if num of items == capacity block()
    ## channels are FIFO(First In First Out)
    def __init__(self, type:str, main:bool= True, con = None, capacity:int =None):
        ## self.con is used by receiver and self.child by sender
        
        if capacity != None:
            self.cap = capacity
            self.values:list[object]    
        self.type = type
        if con != None:
            self.child = con
            self.main = False
        else:
            self.con, self.child = mp.Pipe()
            self.main = True
    def Child(self):
        if self.main:
            return self.child
     
    def Parent(self):
        if not self.main:
            return self.con
        
    def send(self, value):
        if self.main:
            return "This is the main Process : Receiving Process"
        self.child.send(("Send", value)) 
        ## report for testings
        tag, result = self.child.recv()
    
    def receive(self):
        if self.main:
            cmd, payload = self.con.recv() ## blocks when nothing to receive
            if cmd == "Send":
                self.con.send(("good", "yes"))
                return payload
    
    def capstore(self, value):
        self.values

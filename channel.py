import multiprocessing as mp
from typing import Any

from fifo import fifo
"""
Channel allow to control the amount of data through pipes and block subprocess when cap is reached
subproc wait for cap before resuming
"""
class Channel:
    def __init__(self, typ:object, main:bool= True, conn = None, capacity:int =0):
        ## self.conn is used by receiver and self.child by sender
        store = fifo(capacity, typ)
        if conn != None:
            self.child = conn
            self.main = False
        else:
            self.conn, self.child = mp.Pipe()
            self.main = True
    def Child(self):
        return self.child
     
    def Parent(self):
       return self.conn
        
    def send(self, value):
        """if self.main:
            return "This is the main Process : Receiving Process"""
        self.child.send(("Send", value)) 
        ## report for testings
        tag, result = self.child.recv()
        
    
    def receive(self) -> Any:
        if self.main:
            cmd, payload = self.conn.recv() ## blocks when nothing to receive
            if cmd == "Send":
                self.conn.send(("good", "yes"))
                return payload
    

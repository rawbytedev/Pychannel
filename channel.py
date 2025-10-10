from ast import Store
import asyncio
import multiprocessing as mp
from multiprocessing import process
from multiprocessing.connection import PipeConnection
from typing import Any

from fifo import fifo
"""
Channel allow to control the amount of data through pipes and block subprocess when cap is reached
subproc wait for cap before resuming
Main Process <-> Handler(FIFO) <-> []Childs
Note: self.child is defined only if The channel initialized without conn
"""
class Channel:
    def __init__(self, conn =None):
        self.isChild =False
        if conn == None:
            self.conn, self.child = mp.Pipe()
        else:
            self.isChild = True
            self.conn = conn
    
    def Child(self):
        if self.isChild:
            return 
        return self.child ## works only if parent
    ## represent the connector used to send and receive data
    def Parent(self):# -> Any | PipeConnection[Any, Any]:
       return self.conn
    
    ## start receive data    
    def receive(self) -> Any:
        ## sends signal ready to receive
        self.conn.send(("RECEIVE", "Ready to Receive"))
        cmd, payload = self.conn.recv() ## blocks when nothing to receive
        if cmd == "SEND":
            return payload
        if cmd == "ERROR":
            print(payload)
        if cmd == "CLOSE":
            return "Closed"
        return
    ## used by subprocess
    def send(self, val):
        cmd, payload = self.conn.recv()
        if cmd == "RECEIVE":
            self.conn.send(("SEND", val))
"""
Receive request from Main process and Childs
currently that's the only way I found to ensure blocks works for buffered channels
we'll go with this model and optimize it so Handler become negligible and transparent
we have cmds:
SEND - signal that a payload was sent(payload was sent not ERROR)
ERROR - signal an error with the channel model(e.g DeadLock, channelclosed...)
RECEIVE - signal that it's ready to receive payload(waiting for payload)
CLOSE - signal Handler to close once closed everything sent to pipe is dropped

Handler cmds:
SEND
ERROR
RECEIVE 
Main:
SEND
RECEIVE
CLOSE
Childs:
SEND
RECEIVE
CLOSE

It is recommend for childs to close channels because their the one processing and sending
data to the channel(their are not monitored so it's necessary that their close it once)
their done
"""
class Handler:
    def __init__(self, conn, types:object, cap:int=0) -> None:
        self.conn = conn
        self.types = types
        self.cap = cap
        self.chan = False
        self.store = fifo(cap, types)
        self.subconn, self.child = mp.Pipe()
    
    def startchild(self,func, *args):
        proc = mp.Process(target=func,args=args, kwargs={"conn":self.child})
        proc.start()

    def subreceive(self):
        self.subconn.send(("RECEIVE", "Waiting")) ## subprocess waits for signal # does'nt need to send just signal that channel is open
        while self.chan == False:
            while self.isAdd():
                if self.subconn.poll(0.1):
                    cmd, payload = self.subconn.recv()
                    self.ProcessCMD(cmd, payload)
                if self.conn.poll(0.1):
                    cmd, payload = self.conn.recv()
                    self.ProcessCMD(cmd)
        self.ProcessCMD("ERROR", "Channel is closed")
    
    def ProcessCMD(self,cmd, payload=""):
        if cmd == "SEND": ## from subs
            err = self.fifoAdd(payload)
            if err == TypeError:
                self.Destroy() ## close all and kill all sub
            self.subconn.send(("RECEIVE", "pay"))
        if cmd == "RECEIVE": ## from Main
            if self.size() > 0:
                self.conn.send(("SEND",self.fifoPop()))
            return
        if cmd == "ERROR": ## to main
            self.conn.send(payload)
        
    def Destroy(self):
        print("Destroying")
        pass
    def fifoAdd(self, value):
        return self.store.add(value)
    
    def fifoPop(self):
        return self.store.pop()
    def size(self):
        return self.store.size()
    def isAdd(self):
        return self.store.CanAdd()
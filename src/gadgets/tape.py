from src.config import CSR_PEM, KEY_PEM, LOCALHOST, SERVER_PORT
from .gadget import Gadget, Message

import json
from collections import OrderedDict
from socketio import ClientNamespace
import numpy as np
from threading import Thread
from flask import render_template
import time
from socketio import Client
import pickle
import logging
logging.basicConfig(
    filename='phone.log',
    encoding='utf-8',
    level=logging.DEBUG,
)


class Tape(Gadget):
    '''
    A tape of recorded socket events
    '''
    def __init__(self,name=None,hostname=LOCALHOST,port=SERVER_PORT,**kwargs):
        Gadget.__init__(self,
            config={'name':name},
            hostname=hostname,
            port=port)
        if name is not None:
            self.tape = self.open(name)
        else:
            self.tape = []
            
    def open(self,tape_name):
        with open(tape_name,'r') as tape_file:
            return json.loads(tape_file)     
            
    def write(self,frame):
        # TODO - check that the frame is valid, e.g. has event name and time is after last time
        self.tape.append(frame)
        
    def save(self):
        assert self.name is not None, "Name for tape not defined, can't save"
        with open(self.name,'w') as tape_file:
            tape_file.write(json.dumps(self.tape))
        
    def get_frame(self,in_idx=0,out_idx=-1):
        subtape = self.tape[in_idx:out_idx]
        for f,frame in enumerate(subtape):
            yield frame, f==(len(subtape)-1)
        
    # def play(self):
    #     t_last = self.tape[0]['time']
    #     for frame in self.tape:
    #         self.host.emit(
    #             event=frame['event'],
    #             data=frame['data'],
    #         )
    #         t_event = frame['time']
    #         while (time.time()-t_last)<(t_event-t_last):
    #             continue
    #         t_last = t_event
    #     self.join()
    #     pass
    
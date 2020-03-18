import inputs
import threading
import time
import numpy as np

import socket
import struct

EVENTs_OfInterest = (
    # Joystick left 
    ('ABS_X', 'X'),
    ('ABS_Y', 'Y'),

    # Face Buttons a b
    ('BTN_SOUTH', 'A'),#A
    ('BTN_EAST', 'B'),#B

)
class xBoxGamepad(object):
    def __init__(self):
        self.gamepad=inputs.devices.gamepads[0]
        self.consideredEvents=dict(EVENTs_OfInterest)
        self.runInput=True
        self.maxVal=32768
        self.valueDict={"X":0,"Y":0,"A":False,"B":False}
        self._lock=threading.Lock()
    def readInput(self):
    
        events = self.gamepad.read()
        for event in events:
            key =  event.code
            # with self._lock:
            if key in self.consideredEvents:
                if key=='ABS_X':
                    self.valueDict["X"]=event.state/self.maxVal
                if key=='ABS_Y':
                    self.valueDict["Y"]=event.state/self.maxVal
                if key=="BTN_SOUTH":
                    self.valueDict["A"]=bool(event.state)
                if key=="BTN_EAST":
                    self.valueDict["B"]=bool(event.state)
                      
def getData2():
    xbox.readInput()
    ax=xbox.valueDict['X']
    aBut=xbox.valueDict['A']
    bBut=xbox.valueDict['B']
    if abs(ax)<0.15:
        ax=0
    data=str(float(ax))+":"+str(aBut)+","+str(bBut)
    print(data)
    s=bytes(data,'utf-8')
    dataToSend=struct.pack("%ds" % (len(s),), s)
    c=bytearray(dataToSend)
    return c

xbox=xBoxGamepad()

#TCP_IP = '192.168.178.44'#home laptop
TCP_IP = '192.168.178.26'#home Pc
#TCP_IP = '192.168.43.152'#hotspot
TCP_PORT = 5005
BUFFER_SIZE = 200 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()
print('Connection address:', addr)
while True:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    #print("received data:", data)
    dataToSend=getData2()
    b=bytearray(b'\x0a')
    conn.send(dataToSend+b)
        
conn.close()

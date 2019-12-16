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
lock =threading.Lock()
class MaxSizeList(object):

    def __init__(self, max_length):
        self.max_length = max_length
        self.ls = np.array([])

    def push(self, st):
        if len(self.ls) == self.max_length:
            self.ls=np.delete(self.ls,0)
        self.ls=np.append(self.ls,st)

    def get_list(self):
        return self.ls
    def fillArray(self):
        self.ls=np.zeros(self.max_length)

class xBoxGamepad(object):
    def __init__(self):
        self.gamepad=inputs.devices.gamepads[0]
        self.consideredEvents=dict(EVENTs_OfInterest)
        self.runInput=True
        self.maxVal=32768
        self.valueDict={"X":0,"Y":0,"A":False,"B":False}
        self._lock=threading.Lock()
    def readInput(self):
        while self.runInput:
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
                      
                        
def smartCombiner(historyX,historyY):
    """
    create a value depending on the history of inputs
    if input direction has changed or magnitued we change
    historyX and historyY are numpy 1d arrays. In which
    the most rececnt value is at the end 
    """
    diffX=np.diff(historyX)
    dDiffX=np.diff(diffX)#most recent value is at the end
    #hence for a positve change this works perfectly with diff
    diffY=np.diff(historyY)
    dDiffY=np.diff(diffY)
    #create Vector
    vectorAccelerationlistXY=np.column_stack((diffX,diffY))
    #print(vectorAccelerationlistXY)
    meanChange=np.mean(vectorAccelerationlistXY,axis=0)
    historyCombin=np.column_stack((historyX,historyY))
    #print(np.mean(historyCombin,axis=0))
    ampX=historyX[-1]
    ampY=historyY[-1]
    return ampX
def sendStates(amp,aChanged,bChanged):
    # aChanged=True
    # bChanged=True
    if abs(amp)<0.1:
        amp=0
    with lock:
        text2send.stringToSend=str(float(amp))+":"+str(text2send.changedAFlag)+","+str(text2send.changedBFlag)
    
        
def collectStates():
    
    historyLength=20

    historyX=MaxSizeList(historyLength)
    historyX.fillArray()#filled with zeros
    historyY=MaxSizeList(historyLength)
    historyY.fillArray()
    lastValueA=False
    lastValueB=False
    flagChangeA=False
    flagChangeB=False

    while True:
        #record the past states of the controller
        #as well as set flag if the button press has been released
        #aka when it goes from True to False
        historyX.push(xbox.valueDict["X"])
        historyY.push(xbox.valueDict["Y"])
        if xbox.valueDict["A"]==True:
            lastValueA=True
        else:
            if lastValueA==True:
                #flagChangeA=True
                text2send.changedAFlag=True
                
            lastValueA=False
        if xbox.valueDict["B"]==True:
            lastValueB=True
        else:
            if lastValueB==True:
                # flagChangeB=True
                text2send.changedBFlag=True
                
            lastValueB=False

        #Now we create smart input
        #print(historyX.get_list())
        #print(historyY.get_list())
        amp=smartCombiner(historyX.get_list(),historyY.get_list())
        sendStates(amp,text2send.changedAFlag,text2send.changedAFlag)
        #flagChangeA=flagChangeB=False#reset after send

class SendText(object):
    def __init__(self):
        self.stringToSend=""
        self.changedAFlag=False
        self.changedBFlag=False

def getData():    
    #data=input("x y z i j k w\n").split(" ")
    data=[0, 0, 1, 0, 0, 0, 1]
    data=[float(x) for x in data]
    s=""
    for x in range(3):
        s+=str(data[x])+","
    s=s[0:-1]
    s+=":"
    for x in range(3,7):
        s+=str(data[x])+","
    s=s[0:-1]
    # s=str(data[0]),",",str(data[1]),",",str(data[2]),":",str(data[3]),",",str(data[4]),",",str(data[5]),",",str(data[6])
    
    with lock:
        s+=":"+text2send.stringToSend
    s=bytes(s,'utf-8')
    dataToSend=struct.pack("%ds" % (len(s),), s)
    c=bytearray(dataToSend)
    return c

def getData2():
    with lock:
        data=text2send.stringToSend
    s=bytes(data,'utf-8')
    dataToSend=struct.pack("%ds" % (len(s),), s)
    c=bytearray(dataToSend)
    return c
##### main starts here 
  
text2send=SendText()
xbox=xBoxGamepad()
listenInput=threading.Thread(target=xbox.readInput,daemon=True)
listenInput.start()

prepareStatesTosend=threading.Thread(target=collectStates,daemon=True)
prepareStatesTosend.start()



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
    dataToSend=getData()
    b=bytearray(b'\x0a')
    conn.send(dataToSend+b)
        
conn.close()

        


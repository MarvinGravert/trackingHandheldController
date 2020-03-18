import inputs #for xbox 360
import threading
import time
import numpy as np
import time
from triad_openvr import triad_openvr#vive


import socket
import struct

def getDataVive():  
    
    try:
        [x,y,z, i, j, k,w]=v.devices["controller_1"].get_pose_quaternion()
        #currentPose=[x+0.041,y-0.041,z-0.5,i, j, k, w]#hardcoding the transformation sry. Same rotation just moving the KOS
        currentPose=[x-0.041,y+0.041,z+0.5,-i, -j, -k, w]#hardcoding the transformation sry. Same rotation just moving the KOS
        previousPose=currentPose        
    except (TypeError,ZeroDivisionError) :
        #this occurs when connection to device is lost
        #just use the previously detected pose
        #Zero divisoin error can happen during conversion to quaternion
        if 'previousPose' not in locals():
            previousPose=[0,0,0,0,0,0,1]
        currentPose=previousPose
    
    try:
        #{'unPacketNum': 362, 'trigger': 0.0, 'trackpad_x': 0.0, 'trackpad_y': 0.0, 
        # 'ulButtonPressed': 0, 'ulButtonTouched': 0, 'menu_button': False, 'trackpad_pressed': False, 'trackpad_touched': False, 'grip_button': False}
        inputDict=v.devices["controller_1"].get_controller_inputs()
        xState=inputDict['trackpad_x']
        yState=inputDict['trackpad_y']
        trackpadPressed=inputDict['trackpad_pressed']
        triggerButton=inputDict['trigger']
        menuButton=inputDict['menu_button']
        gripButton=inputDict['grip_button']
        if triggerButton<0.5:
            triggerButton=0.0

        previousInputDict=inputDict
    except (TypeError,KeyError):
        inputDict=previousInputDict
    #we are interested inthe distance to the center of the trackpad
    #though for the first implementation we are just using x
    ###Prepare to send in format x,y,z:i,j,k,w:x_trackpad:trigger,trackpad_pressed, menuButton,grip_button
    #make the numbers floating point
    poseData=[float(x) for x in currentPose]
    
    s=""
    for x in range(3):
        s+=str(poseData[x])+","
    s=s[0:-1]
    s+=":"
    for x in range(3,7):
        s+=str(poseData[x])+","
    s=s[0:-1]#remove the last comma
    s+=":"
    s+=str(float(xState))
    s+=":"
    s+=str(bool(triggerButton))+","+str(trackpadPressed)+","+str(menuButton)+","+str(bool(gripButton))
    print(s)
    s=bytes(s,'utf-8')
    dataToSend=struct.pack("%ds" % (len(s),), s)
    c=bytearray(dataToSend)
    return c

previousPose=[0,0,0,0,0,0,1]
previousInputDict={'trackpad_x':0.0,'trackpad_y':0.0,'trackpad_pressed':False,'grip_button':False,'trigger':0.0,'menu_button':False}
   
v = triad_openvr.triad_openvr()
v.print_discovered_objects()

# while True:
#     start=time.time()
#     getDataVive()
#     end=time.time()
#     diffTime=end-start#time difference in seconds
#     printEveryX=1
#     if diffTime<printEveryX:#prun function every 1 second
#         time.sleep(printEveryX-diffTime)



#TCP_IP = '192.168.178.44'#home laptop
TCP_IP = '192.168.178.26'#home Pc
#TCP_IP = '192.168.43.152'#hotspot
TCP_IP = '192.168.43.138'#alienware hotspot
TCP_PORT = 5005
BUFFER_SIZE = 200 

# while True:
#     dataToSend=getDataVive()
#     b=bytearray(b'\x0a')#end bit so to say
#     print(dataToSend+b)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()
print('Connection address:', addr)
while True:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    #print("received data:", data)
    dataToSend=getDataVive()
    b=bytearray(b'\x0a')#end bit so to say
    conn.send(dataToSend+b)
    
    
# conn.close()

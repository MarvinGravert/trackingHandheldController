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
        currentPose=[x,y,z,i, j, k, w]
        previousPose=currentPose        
    except (TypeError,ZeroDivisionError) :
        #this occurs when connection to device is lost
        #just use the previously detected pose
        #Zero divisoin error can happen during conversion to quaternion
        currentPose=previousPose
    
    try:
        #{'unPacketNum': 362, 'trigger': 0.0, 'trackpad_x': 0.0, 'trackpad_y': 0.0, 
        # 'ulButtonPressed': 0, 'ulButtonTouched': 0, 'menu_button': False, 'trackpad_pressed': False, 'trackpad_touched': False, 'grip_button': False}
        inputDict=v.devices["controller_1"].get_controller_inputs()
        xState=inputDict['trackpad_x']
        yState=inputDict['trackpad_y']
        trackpadPressed=inputDict['trackpad_pressed']
        gripButton=inputDict['grip_button']
        previousInputDict=inputDict
    except (TypeError,KeyError):
        inputDict=previousInputDict
    
    return(currentPose,inputDict)
    

previousPose=[0,0,0,0,0,0,1]
previousInputDict={'trackpad_x':0.0,'trackpad_y':0.0,'trackpad_pressed':False,'grip_button':False}
   
v = triad_openvr.triad_openvr()
v.print_discovered_objects()

while True:
    start=time.time()
    
    print(getDataVive())
    end=time.time()
    diffTime=end-start#time difference in seconds
    printEveryX=1
    if diffTime<printEveryX:#prun function every 1 second
        time.sleep(printEveryX-diffTime)





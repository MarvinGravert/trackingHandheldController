import socket
import struct
import random
from triad_openvr import triad_openvr


v = triad_openvr.triad_openvr()
v.print_discovered_objects()
previousPos=[0,0,0,0,0,0,1]#origin and same orientation
def transformedData(quaternionList):
    x,y,z,i,j,k,w=quaternionList
def getData():
    try:
        data=v.devices["controller_1"].get_pose_quaternion()
        previousPos=data
        print("\r",*data,end="")
        data=transformedData(data)
    except KeyError :
        data=previousPos#in case we lose connection we just take the last known position
        print("LOST CONNECTION")
    s=""
    for x in range(3):
        s+=str(data[x])+","
    s=s[0:-1]
    s+=":"
    for x in range(3,7):
        s+=str(data[x])+","
    s=s[0:-1]
    s=bytes(s,'utf-8')
    dataToSend=struct.pack("%ds" % (len(s),), s)
    c=bytearray(dataToSend)
    return c

TCP_IP = '192.168.178.44'#home laptop
#TCP_IP = '192.168.43.152'#hotspot
TCP_PORT = 5005
BUFFER_SIZE = 100  

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

    
conn, addr = s.accept()
print('Connection address:', addr)
while True:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    #print("received data:", data)#this line is unnessecary
    dataToSend=getData()
    b=bytearray(b'\x0a')#end bit so to day
    conn.send(dataToSend+b)  
conn.close()


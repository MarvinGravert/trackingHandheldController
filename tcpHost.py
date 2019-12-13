import socket
import struct
import random


TCP_IP = '192.168.178.44'#home laptop
#TCP_IP = '192.168.43.152'#hotspot
TCP_PORT = 5005
BUFFER_SIZE = 100  

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
def getData():
    
    data=input("x y z i j k w\n").split(" ")
    data=[float(x) for x in data]
    
    

    # data=[random.random(), 2.55, 3.04,4.04,5.5,6.06,7.77]
    
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
    
conn, addr = s.accept()
print('Connection address:', addr)
while True:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print("received data:", data)
    dataToSend=getData()
    b=bytearray(b'\x0a')
    conn.send(dataToSend+b)  
conn.close()

# data=[1.03, 2.55, 3.04,4.04]
# s=""
# for x in range(2):
#     s+=str(data[x])+","
# s=s[0:-1]
# s+=":"
# for x in range(2,4):
#     s+=str(data[x])+","
# s=s[0:-1]
# s=bytes(s,'utf-8')
# dataToSend=struct.pack("%ds" % (len(s),), s)
# c=bytearray(dataToSend)
# print(c)
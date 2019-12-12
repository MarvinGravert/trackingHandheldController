# import socket
# import struct

# TCP_IP = '192.168.178.26'
# TCP_PORT = 5005
# BUFFER_SIZE = 1024
# MESSAGE = "Hello, World!"
# data=[1.0,2.0]
# sending=struct.pack('dd',*data)

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((TCP_IP, TCP_PORT))
# s.send(sending)
# data = s.recv(BUFFER_SIZE)
# s.close()

# print ("received data:", data)


import socket
import struct


TCP_IP = '192.168.178.44'
TCP_PORT = 5005
BUFFER_SIZE = 100  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
def getData():
    # data=[1,1,1,0,0,0,1]#input("x y z i j k w\n").split(" ")
    # data=[float(x) for x in data]
    # dataToSend=struct.pack('d'*len(data), *data)
    data="Hallo:Welt;IchBims"
    s=bytes(data,'utf-8')
    dataToSend=struct.pack("I%ds" % (len(s),), len(s), s)
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

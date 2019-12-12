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


TCP_IP = '192.168.178.44'
TCP_PORT = 5005
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connection address:', addr)
while True:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print("received data:", data)
    ownData=inp
    conn.send(data)  # echo
conn.close()
import socket
import struct

TCP_IP = '192.168.178.44'#home laptop
#TCP_IP = '192.168.43.152'#hotspot
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
data=[1.0,2.0]
sending=struct.pack('dd',*data)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(sending)
data = s.recv(BUFFER_SIZE)
s.close()

print ("received data:", data)
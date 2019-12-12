import socket
import struct
import sys
UDP_IP = "192.168.178.44"
UDP_PORT = 8051

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print(sys.getsizeof(data))
    unpacked=struct.unpack('ddddddd',data)
    print("received message:", unpacked)
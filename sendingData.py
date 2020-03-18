import triad_openvr
import time
import sys
import struct
import socket
import sys

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address = ('192.168.178.47', 8051)#hololens

# # v = triad_openvr.triad_openvr()
# # v.print_discovered_objects()

# while(True):
#     # start = time.time()
#     # txt = ""
#     #data =  v.devices["tracker_1"].get_pose_quaternion()
#     data=input("x y z i j k w\n").split(" ")
#     data=[float(x) for x in data if x.isdigit()]
#     sent = sock.sendto(struct.pack('d'*len(data), *data), server_address)
#     # print("\r" + txt, end="")
#     # sleep_time = interval-(time.time()-start)
#     # if sleep_time>0:
#     #     time.sleep(sleep_time)


UDP_IP = "192.168.178.44"
UDP_PORT = 8051

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
while True:
    data=input("x y z i j k w\n").split(" ")
    data=[float(x) for x in data if x.isdigit()]
    assert len(data)==7
    sock.sendto(struct.pack('d'*len(data), *data), (UDP_IP, UDP_PORT))



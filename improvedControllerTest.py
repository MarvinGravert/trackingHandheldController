from triad_openvr import triad_openvr
import time
import sys

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

v = triad_openvr.triad_openvr()
v.print_discovered_objects()

if len(sys.argv) == 1:
    interval = 1/250
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[1])
else:
    print("Invalid number of arguments")
    interval = False
    
if interval:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    while(True):
        try:
            start = time.time()
            txt = ""
            pos=v.devices["controller_1"].get_pose_euler()
            for i in pos:
                txt += "%.4f" % i
                txt += " "
            txt+="C1"
            print("\r" + txt, end="")

            for i in v.devices["controller_2"].get_pose_euler():
                txt += "%.4f" % i
                txt += " "
            txt+="C2"
            print("\r" + txt, end="")
            sleep_time = interval-(time.time()-start)
            ax.scatter(pos[0], pos[1], pos[2], c='r', marker='o')
        except TypeError:
            pass
        
        
        
        
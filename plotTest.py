import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time
import random
from matplotlib.animation import FuncAnimation

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
def animate(i):
    ax.cla()
    ax.set_xlim3d(0,1)
    ax.set_ylim3d(0,1)
    ax.set_zlim3d(0,1)
    x=getPoint()#returns a random matrix 1x3
    return ax.scatter3D(x[0][0],x[0][1],x[0][2])
def getPoint():
    return np.random.rand(1,3)
ani = FuncAnimation(fig, animate,  interval=1000)
#fig is the figure we plot onto
#animate is the function who returns a fitting graph object "to add to fig"(the i indicates the frame number)
#repeat, if the animation should show itself again at the end(repeat=False) standard is true
#interval how often the graph is updated(function called)
plt.show()
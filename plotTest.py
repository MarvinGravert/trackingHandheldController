import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time
import random
from matplotlib.animation import FuncAnimation
from scipy.spatial.transform import Rotation as R 

from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
def animate(i):
    ax.cla()
    ax.set_xlim3d(0,1)
    ax.set_ylim3d(0,1)
    ax.set_zlim3d(0,1)
    x=getPoint()#returns a random matrix 1x3
    ax.scatter3D(x[0],x[1],x[2])
    #ax.plot([x[0],1],[x[1],1],[x[2],1],'ro',alpha=0.8, lw=3)
    a = Arrow3D([x[0], 1], [x[1], 1], 
                [x[2],1], mutation_scale=20, 
                lw=3, arrowstyle="-|>", color="r")
    ax.add_artist(a)
    return ax
def getPoint():
    return np.random.rand(3)
    userInput=input("Enter Coordinantes in format x y z")
    userInput=userInput.split(" ")
    userInput=[float(x) for x in userInput]
    return userInput


ani = FuncAnimation(fig, animate,  interval=10)
#fig is the figure we plot onto
#animate is the function who returns a fitting graph object "to add to fig"(the i indicates the frame number)
#repeat, if the animation should show itself again at the end(repeat=False) standard is true
#interval how often the graph is updated(function called)
plt.show()

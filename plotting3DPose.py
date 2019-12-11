#plotting
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

#math modules
import numpy as np
from scipy.spatial.transform import Rotation as R

#vive interface modules
from triad_openvr import triad_openvr
import random

#helper class to create arrowHeads
#source:https://stackoverflow.com/questions/22867620/putting-arrowheads-on-vectors-in-matplotlibs-3d-plot
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

class Plotting3DPose(object):
    """
    Creates 3D Plot object which can be used to plot 3D Pose data dynamicially (at given update rate)
    """
    baseXVec=[5,0,0]
    baseYVec=[0,5,0]
    baseZVec=[0,0,5]
    def __init__(self,interval=1000,numPoses=1,boundary=[10,10,10]):
        """
        interval: min time between updates tothe graph
        numPoses: number of poses that will be plotted(for now only one)
        boundary:list of boundary of the area to be plotted[x,y,z]
        """
        self._interval=interval
        self.numPoses=numPoses#for now just placeholder
        self.fig= plt.figure()#figure to plot onto
        self.ax=self.fig.add_subplot(111, projection='3d')#3d added to the figure
        self.boundary=boundary
        self.poseList=[]
        for i in range(numPoses):
            self.poseList.append([[0,0,0],[0,0,0,1]])#x y z w
    @property
    def interval(self):
        return self._interval
    @interval.setter
    def interval(self,interval):
        self._interval=interval

    def start(self):
        """
        start the plotting
        """
        def _animate(i):
            self.update()#shuold update the pose vector with format (transformation x y z, rotation i j k w)
            self.ax.cla()#clear previous graphs
            #set boundary to not allow for 
            self.ax.set_xlim3d(-self.boundary[0],self.boundary[0])
            self.ax.set_ylim3d(-self.boundary[1],self.boundary[1])
            self.ax.set_zlim3d(-self.boundary[2],self.boundary[2])
            for pose in self.poseList:
                #plot the origin of coordinate system
                x1,y1,z1=pose[0]
                self.ax.plot([x1],[y1],[z1],'go',alpha=0.8, lw=3)
                r=R.from_quat(pose[1])
                xNew=r.apply(self.baseXVec)
                yNew=r.apply(self.baseYVec)
                zNew=r.apply(self.baseZVec)        
                #plot The axis x= blue y= yellow z=red
                #if the axis need to be scaled, scale the base vectors at the top of this class implementation
                xAxis = Arrow3D([x1,xNew[0]+x1], [y1,xNew[1]+y1], [z1,xNew[2]+z1], mutation_scale=20, lw=3, arrowstyle="-|>", color="b")
                yAxis = Arrow3D([x1,yNew[0]+x1], [y1,yNew[1]+y1], [z1,yNew[2]+z1], mutation_scale=20, lw=3, arrowstyle="-|>", color="y")
                zAxis = Arrow3D([x1,zNew[0]+x1], [y1,zNew[1]+y1], [z1,zNew[2]+z1], mutation_scale=20, lw=3, arrowstyle="-|>", color="r")
                self.ax.add_artist(xAxis)
                self.ax.add_artist(yAxis)
                self.ax.add_artist(zAxis)
            return self.ax
        ani = FuncAnimation(self.fig, _animate,  self.interval)
        plt.show()
    
    def update(self):
        """
        update the pose values
        """
        for i in range(self.numPoses):
            userInput=input("enter here new Pose as translation and rotation(quaternion). Format x y z i j k w\n").split(" ")
            #format into 2 lists of three and four entires 
            self.poseList[i]=[[float(x) for x in userInput[0:3] if x.isdigit()],[float(x) for x in userInput[3:] if x.isdigit()]]
    def updateQuaternion(self,newPose,objNumber):
        """
        updates the pose of one of the tracked objects
        newPose: list of two lists, first containing translation pose [x y z] second roation
            as quaternion [i j k w]
        objNumber: which object's pose is supposed to be updated
        """
        self.poseList[objNumber]=newPose
    def updateVive(self):
        try:
            [x,y,z,w, i, j, k]=self.v.devices["controller_1"].get_pose_quaternion()
            self.poseList[0]=[x,y,z,i, j, k, w]
        except TypeError :
            #this occurs when connection to device is lost
            #thus stay at same position and dont change orientation
            self.poseList[0]=self.poseList[1:4]+[0,0,0,1]
    def initVive(self):
        v = triad_openvr.triad_openvr()
        self.v.print_discovered_objects()
        
np.random.seed(0)
test=Plotting3DPose(1000,1)
test.start()


import numpy as np

class MaxSizeList(object):

    def __init__(self, max_length):
        self.max_length = max_length
        self.ls = np.array([])

    def push(self, st):
        if len(self.ls) == self.max_length:
            self.ls=np.delete(self.ls,0)
        self.ls=np.append(self.ls,st)

    def get_list(self):
        return self.ls
    def fillArray(self):
        self.ls=np.zeros(self.max_length)
def smartCombiner(historyX,historyY):
    """
    create a value depending on the history of inputs
    if input direction has changed or magnitued we change
    historyX and historyY are numpy 1d arrays. In which
    the most rececnt value is at the end 
    """
    diffX=np.diff(np.diff(historyX))#most recent value is at the end
    #hence for a positve change this works perfectly with diff
    diffY=np.diff(np.diff(historyY))
    #create Vector
    vectorAccelerationlistXY=np.column_stack((diffX,diffY))
    meanChange=np.mean(vectorAccelerationlistXY,axis=0)
    print(meanChange)
test=MaxSizeList(20)
test.fillArray()
test1=MaxSizeList(20)
test1.fillArray()

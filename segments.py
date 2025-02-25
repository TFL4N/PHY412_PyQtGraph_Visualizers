from abc import ABC
from my_widgets import *
import numpy as np


class Segment(ABC):
    def __init__(self, segment_number):
        self.segment_num = segment_number
    
    def setupScene(self, w):
        pass

    def tearDownScene(self, w):
        pass

    def updateScene(self, w, t):
        pass
    
    
        
class Part1(Segment):
    def __init__(self):
        super().__init__(1)
    
    def setupScene(self, w):        
        w.setWindowTitle("EM Polarization - Part 1")

        w.canvas.setCameraPosition(distance=10,
                                   elevation=0,
                                   azimuth=180)

        # theres apparently a bug in pyqtgraph
        # that depth value is working like in earlier versions
        # move the vector slightly off the origin for better drawing
        w.e_vec = myVectorItem(parentItem=w.axes,
                                  color=[1,0,0,1],
                                  start=[0.0,0.0,0.05],
                                  end=[5.0,0.0,0.05])
        w.e_vec.setDepthValue(5)

        
        
    def updateScene(self, w, t):
        x = 3.0 * np.cos(w.freq*t)
        
        w.e_vec.setPosition(start=[0.0,0.0,0.05],
                            end=[x,0.0,0.05])

class Part2(Segment):
    def __init__(self):
        super().__init__(1)
    
    def setupScene(self, w):        
        w.setWindowTitle("EM Polarization - Part 1")

        w.canvas.setCameraPosition(distance=10,
                                   elevation=0,
                                   azimuth=180)

        # theres apparently a bug in pyqtgraph
        # that depth value is working like in earlier versions
        # move the vector slightly off the origin for better drawing
        w.e_vec = myVectorItem(parentItem=w.axes,
                                  color=[1,0,0,1],
                                  start=[0.0,0.0,0.05],
                                  end=[5.0,0.0,0.05])
        w.e_vec.setDepthValue(5)

        
        
    def updateScene(self, w, t):
        x = 3.0 * np.cos(w.freq*t)
        
        w.e_vec.setPosition(start=[0.0,0.0,0.05],
                            end=[x,0.0,0.05])


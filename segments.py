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


        # hide z-axis
        w.z_label.setVisible(False)
        w.axes.setData(z_visible=False)
        
        # disable previous button
        w.prev_button.setEnabled(False)

    def tearDownScene(self, w):
        # remove e_vec from scene
        w.e_vec.setParentItem(None)
        w.canvas.removeItem(w.e_vec)
        w.e_vec = None

        # undo invisibility changes
        w.z_label.setVisible(True)
        w.axes.setData(z_visible=True)
        
        # re-enable previous button
        w.prev_button.setEnabled(True)
        
    def updateScene(self, w, t):
        x = 3.0 * np.cos(w.freq*t)
        
        w.e_vec.setPosition(start=[0.0,0.0,0.05],
                            end=[x,0.0,0.05])

class Part2(Segment):
    def __init__(self):
        super().__init__(2)
    
    def setupScene(self, w):        
        w.setWindowTitle("EM Polarization - Part 2")

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


    def tearDownScene(self, w):
        # remove e_vec from scene
        w.e_vec.setParentItem(None)
        w.canvas.removeItem(w.e_vec)
        w.e_vec = None
        
    def updateScene(self, w, t):
        x = 3.0 * np.cos(w.freq*t)
        
        w.e_vec.setPosition(start=[0.0,0.0,0.05],
                            end=[x,0.0,0.05])

        # move camera
        duration = 5.0
        if t <= duration:
            elevation = linear_scale(x1=0.0,
                                     x2=10.0,
                                     y2=duration,
                                     y=t)
            azimuth = linear_scale(x1=180.0,
                                   x2=110.0,
                                   y2=duration,
                                   y=t)
        
            w.canvas.setCameraPosition(elevation=elevation,
                                       azimuth=azimuth)



                
# class Part2_Widget(BaseWidget):
#     def setupScene(self):
#         ## axis
#         self.axes = myGLAxisItem()
#         self.axes.setSize(x=5, y=5, z=5)
#         self.axes.lineplot.setData(width=5.0)
#         self.axes.rotate(-90,0,1,0)
#         self.canvas.addItem(self.axes)

#         self.graph = gl.GLLinePlotItem(parentItem=self.axes,
#                                        pos=[0.0,0.0,0.0],
#                                        color=[1.0,1.0,1.0,1.0],
#                                        width=5.0,
#                                        antialias=True,
#                                        mode='line_strip')
#         #self.canvas.addItem(self.graph)

#     def updateScene(self, t):
#         duration = 10.0
#         t = t % duration

#         ts = np.arange(0,t+0.25,0.25)
#         data = np.zeros((ts.size,3))
#         data[:,2] = ts
#         data[:,0] = np.cos(data[:,2])

#         self.graph.setData(pos=data)
        
#         ########################

#         text = gl.GLTextItem(parentItem=self.axes, pos=[0.0,0.0,0.0], text="Origin")
#         #self.canvas.addItem(text)
        
#         # vec = myVectorItem(parentItem=axes,
#         #                    end=[5.0,5.0,5.0])

#         # self.canvas.addItem(vec)

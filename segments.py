from abc import ABC
from my_widgets import *
import numpy as np
import pyqtgraph.opengl as gl


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
        self.e_vec = MyVectorItem(parentItem=w.axes,
                                  color=[1,0,0,1],
                                  start=[0.0,0.0,0.05],
                                  end=[w.magnitude,0.0,0.05])
        self.e_vec.setDepthValue(5)


        # hide z-axis
        w.z_label.setVisible(False)
        w.axes.setData(z_visible=False,
                       x_tick_plane=1)
        
        # disable previous button
        w.prev_button.setEnabled(False)

    def tearDownScene(self, w):
        # remove e_vec from scene
        self.e_vec.setParentItem(None)
        w.canvas.removeItem(self.e_vec)
        self.e_vec = None

        # undo invisibility changes
        w.z_label.setVisible(True)
        w.axes.setData(z_visible=True,
                       x_tick_plane=2)
        
        # re-enable previous button
        w.prev_button.setEnabled(True)
        
    def updateScene(self, w, t):
        x = w.magnitude * np.cos(w.freq*t)
        
        self.e_vec.setPosition(start=[0.0,0.0,0.05],
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
        self.e_vec = MyVectorItem(parentItem=w.axes,
                                  color=[1,0,0,1],
                                  start=[0.0,0.0,0.05],
                                  end=[w.magnitude,0.0,0.05])
        self.e_vec.setDepthValue(5)

    def tearDownScene(self, w):
        # remove e_vec from scene
        self.e_vec.setParentItem(None)
        w.canvas.removeItem(self.e_vec)
        self.e_vec = None
        
    def updateScene(self, w, t):
        x = w.magnitude * np.cos(w.freq*t)
        
        self.e_vec.setPosition(start=[0.0,0.0,0.05],
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


class Part3(Segment):
    def __init__(self):
        super().__init__(3)
    
    def setupScene(self, w):        
        w.setWindowTitle("EM Polarization - Part 3")

        w.canvas.setCameraPosition(distance=10,
                                   elevation=10,
                                   azimuth=110)

        # e vector
        self.e_vec = MyVectorItem(parentItem=w.axes,
                                  color=[1,0,0,1],
                                  start=[0.0,0.0,0.0],
                                  end=[w.magnitude,0.0,0.0])
        self.e_vec.setDepthValue(5)


        # observer
        self.observer = MyGLImageItem(parentItem=w.axes,
                                      pos=[0.0, w.axes.y_min, 0.0],
                                      image='latex/eye_side.png',
                                      height=30)
        

        # dashed line
        self.ob_line = MyDashedLineItem(parentItem=w.axes,
                                        start=[0.0, w.axes.y_max, 0.0],
                                        end=[0.0, w.axes.y_min, 0.0])
        self.ob_line.setDepthValue(4)

    def tearDownScene(self, w):
        # remove e_vec from scene
        self.e_vec.setParentItem(None)
        w.canvas.removeItem(self.e_vec)
        self.e_vec = None
        
        # remove observer from scene
        self.observer.setParentItem(None)
        w.canvas.removeItem(self.observer)
        self.observer = None
        
        # remove e_vec from scene
        self.ob_line.setParentItem(None)
        w.canvas.removeItem(self.ob_line)
        self.ob_line = None
        
    def updateScene(self, w, t):
        duration = 8.0
        z = linear_scale(x2=w.axes.z_max,
                         y2=duration,
                         y=t)
        
        self.e_vec.setPosition(start=[0.0,0.0,z],
                               end=[w.magnitude,0.0,z])
        self.observer.setData(pos=[0.0, w.axes.y_max, z-0.35])
        self.ob_line.setData(start=[0.0,w.axes.y_max,z],
                             end=[0.0,w.axes.y_min,z])

        if t>duration:
            w.restartAnimation()


class Part4(Segment):
    def __init__(self):
        super().__init__(4)
    
    def setupScene(self, w):        
        w.setWindowTitle("EM Polarization - Part 4")

        w.canvas.setCameraPosition(distance=10,
                                   elevation=10,
                                   azimuth=110)


        image_data = np.array([[[255,0,255,200]]], dtype=np.ubyte)
        
        self.up_planes = []
        self.down_planes = []
        self.up_vecs = []
        self.down_vecs = []

        # e graph
        self.graph = gl.GLLinePlotItem(parentItem=w.axes,
                                       pos=[0.0,0.0,0.0],
                                       color=[1.0,0.0,0.0,1.0],
                                       width=3.0,
                                       antialias=True,
                                       mode='line_strip')
        
        
    def tearDownScene(self, w):
        # remove e graph from scene
        self.graph.setParentItem(None)
        w.canvas.removeItem(self.graph)
        self.graph = None

        # remove up vecs
        for v in self.up_vecs:
            v.setParentItem(None)
            w.canvas.removeItem(v)
        self.up_vecs = []
        
        # remove down vecs
        for v in self.down_vecs:
            v.setParentItem(None)
            w.canvas.removeItem(v)
        self.down_vecs = []
        
        
    def updateScene(self, w, t):
        # graph
        zs = np.arange(0,w.axes.z_max+0.1,0.1)
        data = np.zeros((zs.size,3))
        data[:,2] = zs
        data[:,0] = w.magnitude * np.cos(w.freq*data[:,2] - w.freq*t)

        self.graph.setData(pos=data)

        # find first minumim
        # this will be located at some z<=0
        n = np.floor(w.freq / np.pi * (0.0 - t))
        if n % 2 == 0:
            n -= 1

            
        # planes
        #gl.GLImageItem(image_data,
        #               parentItem=w.axes)

        # vector and plane
        cur_z = np.pi*n/w.freq + t
        up_idx = -1
        down_idx = -1
        new_up_vecs = []
        new_down_vecs = []
        while cur_z < w.axes.z_max:
            # check if in bounds of graph
            if cur_z >= 0.0 and cur_z <= w.axes.z_max:
                if n % 2 == 0:
                    # maximum
                    up_idx += 1
                    
                    # get vector
                    vec = None
                    if up_idx < len(self.up_vecs):
                        vec = self.up_vecs[up_idx]
                    else:
                        vec = MyVectorItem(parentItem=w.axes,
                                           color=[1,0,0,1])
                        new_up_vecs.append(vec)
                        
                    # mod vector
                    vec.setVisible(True)
                    vec.setPosition(start=[0.0,0.0,cur_z],
                                    end=[w.magnitude,0.0,cur_z])
                else:
                    # minimum
                    down_idx += 1
                    
                    # get vector
                    vec = None
                    if down_idx < len(self.down_vecs):
                        vec = self.down_vecs[down_idx]
                    else:
                        vec = MyVectorItem(parentItem=w.axes,
                                           color=[0,0,1,1])
                        new_down_vecs.append(vec)
                        
                    # mod vector
                    vec.setVisible(True)
                    vec.setPosition(start=[0.0,0.0,cur_z],
                                    end=[-w.magnitude,0.0,cur_z])

                    
            # loop condition        
            n += 1
            cur_z = np.pi*n/w.freq + t

        #
        # update vector and plane cache
        #
        # up vecs
        for v in new_up_vecs:
            self.up_vecs.append(v)
        for i in range(up_idx+1, len(self.up_vecs)):
            self.up_vecs[i].setVisible(False)
        # down vecs
        for v in new_down_vecs:
            self.down_vecs.append(v)
        for i in range(down_idx+1, len(self.down_vecs)):
            self.down_vecs[i].setVisible(False)


        

class Part5(Segment):
    def __init__(self):
        super().__init__(5)
    
    def setupScene(self, w):        
        w.setWindowTitle("EM Polarization - Part 5")

        w.canvas.setCameraPosition(distance=10,
                                   elevation=10,
                                   azimuth=110)
        

    def tearDownScene(self, w):
        pass
        
    def updateScene(self, w, t):
        pass


                
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

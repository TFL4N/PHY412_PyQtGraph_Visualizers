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
        w.setWindowTitle(f"EM Polarization - Chapter {w.chapter} - Part 1")

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
        y = 0.0
        if w.chapter == 2:
            y = w.magnitude * np.cos(w.freq*t + w.phase_diff)
        
        self.e_vec.setPosition(start=[0.0,0.0,0.05],
                               end=[x,y,0.05])

class Part2(Segment):
    def __init__(self):
        super().__init__(2)
    
    def setupScene(self, w):        
        w.setWindowTitle(f"EM Polarization - Chapter {w.chapter} - Part 2")

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
        y = 0.0
        if w.chapter == 2:
            y = w.magnitude * np.cos(w.freq*t + w.phase_diff)

        
        self.e_vec.setPosition(start=[0.0,0.0,0.05],
                               end=[x,y,0.05])

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
        w.setWindowTitle(f"EM Polarization - Chapter {w.chapter} - Part 3")

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
        x = w.magnitude
        y = 0.0
        if w.chapter == 2:
            y = w.magnitude
        
        self.e_vec.setPosition(start=[0.0,0.0,z],
                               end=[x,y,z])
        self.observer.setData(pos=[0.0, w.axes.y_max, z-0.35])
        self.ob_line.setData(start=[0.0,w.axes.y_max,z],
                             end=[0.0,w.axes.y_min,z])

        if t>duration:
            w.restartAnimation()


class Part4(Segment):
    def __init__(self):
        super().__init__(4)
    
    def setupScene(self, w):        
        w.setWindowTitle(f"EM Polarization - Chapter {w.chapter} - Part 4")

        w.canvas.setCameraPosition(distance=10,
                                   elevation=10,
                                   azimuth=110)

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

        # remove up planes
        for v in self.up_planes:
            v.setParentItem(None)
            w.canvas.removeItem(v)
        self.up_planes = []
        
        # remove down plane
        for v in self.down_planes:
            v.setParentItem(None)
            w.canvas.removeItem(v)
        self.down_planes = []

        
    def updateScene(self, w, t):
        # graph
        zs = np.arange(0,w.axes.z_max+0.1,0.1)
        data = np.zeros((zs.size,3))
        data[:,2] = zs
        data[:,0] = w.magnitude * np.cos(w.freq*data[:,2] - w.freq*t)
        if w.chapter == 2:
            data[:,1] = w.magnitude * np.cos(w.freq*data[:,2] - w.freq*t + w.phase_diff)
           
        self.graph.setData(pos=data)

        # find first minumim
        # this will be located at some z<=0
        n = np.floor(w.freq / np.pi * (0.0 - t))
        if n % 2 == 0:
            n -= 1

        # vector and plane
        cur_z = np.pi*n/w.freq + t

        up_vec_idx = -1
        down_vec_idx = -1
        new_up_vecs = []
        new_down_vecs = []

        up_plane_idx = -1
        down_plane_idx = -1
        new_up_planes = []
        new_down_planes = []
        
        while cur_z < w.axes.z_max:
            # check if in bounds of graph
            if cur_z >= 0.0 and cur_z <= w.axes.z_max:
                if n % 2 == 0:
                    # maximum
                    up_vec_idx += 1
                    up_plane_idx += 1
                    
                    # get vector
                    vec = None
                    if up_vec_idx < len(self.up_vecs):
                        vec = self.up_vecs[up_vec_idx]
                    else:
                        vec = MyVectorItem(parentItem=w.axes,
                                           color=[1,0,0,1])
                        new_up_vecs.append(vec)
                        
                    # mod vector
                    x = w.magnitude
                    y = 0.0
                    if w.chapter == 2:
                        y = w.magnitude 
                    
                    vec.setVisible(True)
                    vec.setPosition(start=[0.0,0.0,cur_z],
                                    end=[x,y,cur_z])

                    # get plane
                    plane = None
                    if up_plane_idx < len(self.up_planes):
                        plane = self.up_planes[up_plane_idx]
                    else:
                        image_data = np.array([[[255,0,0,100]]], dtype=np.ubyte)
                        plane = gl.GLImageItem(image_data,
                                               parentItem=w.axes)
                        
                        new_up_planes.append(plane)
                        
                    # mod plane
                    plane.setVisible(True)
                    plane.resetTransform()
                    plane.scale(w.axes.x_max - w.axes.x_min,
                                0 - w.axes.y_min,
                                1)
                    plane.translate(w.axes.x_min, w.axes.y_min, cur_z)

                    
                else:
                    # minimum
                    down_vec_idx += 1
                    down_plane_idx += 1
                    
                    # get vector
                    vec = None
                    if down_vec_idx < len(self.down_vecs):
                        vec = self.down_vecs[down_vec_idx]
                    else:
                        vec = MyVectorItem(parentItem=w.axes,
                                           color=[0,0,1,1])
                        new_down_vecs.append(vec)
                        
                    # mod vector
                    x = -w.magnitude
                    y = 0.0
                    if w.chapter == 2:
                        y = -w.magnitude 
                    
                    vec.setVisible(True)
                    vec.setPosition(start=[0.0,0.0,cur_z],
                                    end=[x,y,cur_z])
                    
                    # get plane
                    plane = None
                    if down_plane_idx < len(self.down_planes):
                        plane = self.down_planes[down_plane_idx]
                    else:
                        image_data = np.array([[[0,0,255,100]]], dtype=np.ubyte)
                        plane = gl.GLImageItem(image_data,
                                               parentItem=w.axes)
                        
                        new_down_planes.append(plane)
                        
                    # mod plane
                    plane.setVisible(True)
                    plane.resetTransform()
                    plane.scale(w.axes.x_max - w.axes.x_min,
                                0 - w.axes.y_min,
                                1)
                    plane.translate(w.axes.x_min, w.axes.y_min, cur_z)


                    
            # loop condition        
            n += 1
            cur_z = np.pi*n/w.freq + t

        #
        # update vector and plane cache
        #
        # up vecs
        for v in new_up_vecs:
            self.up_vecs.append(v)
        for i in range(up_vec_idx+1, len(self.up_vecs)):
            self.up_vecs[i].setVisible(False)
        # down vecs
        for v in new_down_vecs:
            self.down_vecs.append(v)
        for i in range(down_vec_idx+1, len(self.down_vecs)):
            self.down_vecs[i].setVisible(False)
        # up planes
        for v in new_up_planes:
            self.up_planes.append(v)
        for i in range(up_plane_idx+1, len(self.up_planes)):
            self.up_planes[i].setVisible(False)
        # down planes
        for v in new_down_planes:
            self.down_planes.append(v)
        for i in range(down_plane_idx+1, len(self.down_planes)):
            self.down_planes[i].setVisible(False)

            
class Part5(Segment):
    def __init__(self):
        super().__init__(5)
    
    def setupScene(self, w):        
        w.setWindowTitle(f"EM Polarization - Chapter {w.chapter} - Part 5")

        w.canvas.setCameraPosition(distance=10,
                                   elevation=10,
                                   azimuth=110)


        self.e_vecs = []
        self.dz = 0.25
        count = int(np.floor(w.axes.z_max/self.dz))
        for _ in range(0,count):
            vec = MyVectorItem(parentItem=w.axes,
                               color=[1,0,0,1],
                               start=[0.0,0.0,0.0],
                               end=[w.magnitude,0.0,0.0])
            self.e_vecs.append(vec)
        
        # e graph
        self.e_graph = gl.GLLinePlotItem(parentItem=w.axes,
                                         pos=[0.0,0.0,0.0],
                                         color=[1.0,0.0,0.0,1.0],
                                         width=3.0,
                                         antialias=True,
                                         mode='line_strip')

        

    def tearDownScene(self, w):
        # remove e_graph from scene
        self.e_graph.setParentItem(None)
        w.canvas.removeItem(self.e_graph)
        self.e_graph = None

        # remove e_vecs
        for v in self.e_vecs:
            v.setParentItem(None)
            w.canvas.removeItem(v)
        self.e_vecs = []

        
    def updateScene(self, w, t):
        pt_1_dur = 5.0
        pt_2_dur = 2.0

        if t <= pt_1_dur:
            # part 1
            # show sampled z one by one
            self.e_graph.setVisible(False)

            dt = pt_1_dur / len(self.e_vecs)
            for idx, vec in enumerate(self.e_vecs):
                z = self.dz*(idx+1)
                x = w.magnitude * np.cos(w.freq*z)
                y = 0.0
                if w.chapter == 2:
                    y = w.magnitude * np.cos(w.freq*z + w.phase_diff)

                vec.setPosition(start=[0.0,0.0,z],
                                end=[x,y,z])
                vec.setVisible(idx*dt < t)
        elif t <= pt_1_dur + pt_2_dur:
            # part 2
            # show e graph
            zs = np.arange(0,w.axes.z_max+0.1,0.1)
            data = np.zeros((zs.size,3))
            data[:,2] = zs
            data[:,0] = w.magnitude * np.cos(w.freq*data[:,2])
            if w.chapter == 2:
                data[:,1] = w.magnitude * np.cos(w.freq*data[:,2] + w.phase_diff)

            
            self.e_graph.setData(pos=data)
            self.e_graph.setVisible(True)
        else:
            # part 3
            # animate
            t -= pt_1_dur + pt_2_dur

            # vecs
            for idx, vec in enumerate(self.e_vecs):
                z = self.dz*(idx+1) + t
                z = z % w.axes.z_max
                x = w.magnitude * np.cos(w.freq*z - w.freq*t)
                y = 0.0
                if w.chapter == 2:
                    y = w.magnitude * np.cos(w.freq*z - w.freq*t + w.phase_diff)

                vec.setPosition(start=[0.0,0.0,z],
                                end=[x,y,z])


            # e_graph
            zs = np.arange(0,w.axes.z_max+0.1,0.1)
            data = np.zeros((zs.size,3))
            data[:,2] = zs
            data[:,0] = w.magnitude * np.cos(w.freq*data[:,2] - w.freq*t)
            if w.chapter == 2:
                data[:,1] = w.magnitude * np.cos(w.freq*data[:,2] - w.freq*t + w.phase_diff)


            self.e_graph.setData(pos=data)

class Part6(Segment):
    def __init__(self):
        super().__init__(6)
    
    def setupScene(self, w):        
        w.setWindowTitle(f"EM Polarization - Chapter {w.chapter} - Part 6")

        w.canvas.setCameraPosition(distance=10,
                                   elevation=10,
                                   azimuth=110)


        self.e_vecs = []
        self.b_vecs = []
        self.dz = 0.25
        count = int(np.floor(w.axes.z_max/self.dz))
        for _ in range(0,count):
            vec = MyVectorItem(parentItem=w.axes,
                               color=[1,0,0,1],
                               start=[0.0,0.0,0.0],
                               end=[w.magnitude,0.0,0.0])
            self.e_vecs.append(vec)

            
            vec = MyVectorItem(parentItem=w.axes,
                               color=[0,1,0,1],
                               start=[0.0,0.0,0.0],
                               end=[w.magnitude,0.0,0.0])
            self.b_vecs.append(vec)
        
        # e graph
        self.e_graph = gl.GLLinePlotItem(parentItem=w.axes,
                                         pos=[0.0,0.0,0.0],
                                         color=[1.0,0.0,0.0,1.0],
                                         width=3.0,
                                         antialias=True,
                                         mode='line_strip')

        # b graph
        self.b_graph = gl.GLLinePlotItem(parentItem=w.axes,
                                         pos=[0.0,0.0,0.0],
                                         color=[0.0,1.0,0.0,1.0],
                                         width=3.0,
                                         antialias=True,
                                         mode='line_strip')

        

    def tearDownScene(self, w):
        # remove e_graph from scene
        self.e_graph.setParentItem(None)
        w.canvas.removeItem(self.e_graph)
        self.e_graph = None

        # remove e_vecs
        for v in self.e_vecs:
            v.setParentItem(None)
            w.canvas.removeItem(v)
        self.e_vecs = []

        # remove b_graph from scene
        self.b_graph.setParentItem(None)
        w.canvas.removeItem(self.b_graph)
        self.b_graph = None

        # remove b_vecs
        for v in self.b_vecs:
            v.setParentItem(None)
            w.canvas.removeItem(v)
        self.b_vecs = []

        
    def updateScene(self, w, t):
        # e vecs
        for idx, vec in enumerate(self.e_vecs):
            z = self.dz*(idx+1) + t
            z = z % w.axes.z_max
            x = w.magnitude * np.cos(w.freq*z - w.freq*t)
            y = 0.0
            if w.chapter == 2:
                y = w.magnitude * np.cos(w.freq*z - w.freq*t + w.phase_diff)

            vec.setPosition(start=[0.0,0.0,z],
                            end=[x,y,z])
            
            
        # e_graph
        zs = np.arange(0,w.axes.z_max+0.1,0.1)
        data = np.zeros((zs.size,3))
        data[:,2] = zs
        data[:,0] = w.magnitude * np.cos(w.freq*data[:,2] - w.freq*t)
        if w.chapter == 2:
            data[:,1] = w.magnitude * np.cos(w.freq*data[:,2] - w.freq*t + w.phase_diff)

        
        self.e_graph.setData(pos=data)

        # b vecs
        for idx, vec in enumerate(self.b_vecs):
            z = self.dz*(idx+1) + t
            z = z % w.axes.z_max
            x = w.magnitude * np.cos(w.freq*z - w.freq*t)
            y = 0.0
            if w.chapter == 2:
                y = w.magnitude * np.cos(w.freq*z - w.freq*t + w.phase_diff)

            # rotate by 90 degrees
            temp = x
            x = -y
            y = temp
                
            vec.setPosition(start=[0.0,0.0,z],
                            end=[x,y,z])
            
            
        # b_graph
        zs = np.arange(0,w.axes.z_max+0.1,0.1)
        data = np.zeros((zs.size,3))
        
        x = w.magnitude * np.cos(w.freq*zs - w.freq*t)
        y = np.zeros(zs.size)
        if w.chapter == 2:
            y = w.magnitude * np.cos(w.freq*zs - w.freq*t + w.phase_diff)
        
        # rotate by 90 degrees
        temp = x
        x = -y
        y = temp

        data[:,0] = x 
        data[:,1] = y
        data[:,2] = zs
                
        self.b_graph.setData(pos=data)

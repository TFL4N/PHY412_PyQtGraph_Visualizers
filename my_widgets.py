import numpy as np

from pyqtgraph.Qt import QtGui
from pyqtgraph.Qt import QtCore
from pyqtgraph.Qt.QtCore import Qt
import pyqtgraph.opengl as gl

def linear_scale(x1=0.0,x2=1.0,y1=0.0,y2=1.0,y=0.5):
    return (float(y)-y1)/(y2-y1) * (x2-x1) + x1

class MyTimer(QtCore.QObject):
    'Time units are milliseconds; block is a function type'
    def __init__(self, duration=None, interval=100, block=None):
        super().__init__()

        self.duration = duration
        self.interval = interval
        self.block = block
        self.counter = 0.0
        self.__is_running = False
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(self.interval)
        self.timer.timeout.connect(self.on_timeout)
        
    def start_timer(self):
        self.__is_running = True
        self.timer.start()

    def stop_timer(self):
        self.__is_running = False
        self.timer.stop()

    def is_running(self):
        return self.__is_running
        
    def on_timeout(self):
        if self.duration is not None \
           and self.counter >= self.duration:
            self.timer.stop()

        # call function block with float t in seconds
        if self.block is not None:
            self.block(float(self.counter) / 1000)
            
        self.counter += self.interval


def generate_cone(radius, height, segments):
    """
    Generates vertices for a cone.

    Args:
        radius: Radius of the base of the cone.
        height: Height of the cone.
        segments: Number of segments to divide the base circle into.

    Returns:
        A list of vertex coordinates (x, y, z).
    """
    vertices = []
    faces = []
    
    # Apex of the cone
    vertices.append((0, 0, height))

    # Face index sequence
    # 1,0,2
    # 2,0,3
    # 3,0,4
    # 4,0,1

    faces = np.zeros((segments,3), dtype=int)
    faces[:,0] = np.arange(1,segments+1,1)
    faces[:,2] = np.arange(2,segments+2,1)
    faces[-1,2] = 1
    
    # Base vertices
    for i in range(segments):
        angle = 2 * np.pi * i / segments
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        vertices.append((x, y, 0))


    vertices = np.array(vertices)
        
    return gl.MeshData(vertexes=vertices, faces=faces)


class MyVectorItem(gl.GLGraphicsItem.GLGraphicsItem):
    def __init__(self, start=[0.0,0.0,0.0], end=[1.0,1.0,1.0], color=[1.0,1.0,1.0,1.0], width=1.0, parentItem=None, glOptions='opaque', antialias=True):
        super().__init__()

        self.lineplot = None
        
        self.start = np.array(start)
        self.end = np.array(end)
        self.width = width
        self.tip_height = 0.3
        self.tip_radius = 0.15
        self.color = color

        
        self.lineplot = gl.GLLinePlotItem(
            parentItem=self, glOptions=glOptions, mode='lines', antialias=antialias
        )
        self.lineplot.setData(width=5.0)

        cone_md = generate_cone(radius=self.tip_radius, height=self.tip_height, segments=8)
        self.tip_mesh = gl.GLMeshItem(parentItem=self,
                                      meshdata=cone_md,
                                      color=np.array(color, dtype=float),
                                      smooth=False,
                                      computeNormals=False,
                                      glOptions=glOptions)
        
        
        self.setParentItem(parentItem)
        self.updateLines()

    def setPosition(self, start=[0.0,0.0,0.0], end=[1.0,1.0,1.0]):
        self.start = np.array(start)
        self.end = np.array(end)
        self.updateLines()
        
        
    def updateLines(self):
        if self.lineplot == None:
            return

        pos = np.array([self.start, self.end])
        self.lineplot.setData(pos=pos, color=self.color)

        self.tip_mesh.setColor(self.color)
        self.tip_mesh.resetTransform()
        self.tip_mesh.translate(0,0,-self.tip_height)

        # determine angle between default mesh axis and the vector
        z = np.array([0.0, 0.0, 1.0])
        v = self.end - self.start
        v_len = np.linalg.norm(v)
        angle = np.arccos(np.sum(z*v) / v_len)
        angle = angle * 180 / np.pi # degrees
        
        # rotate tip
        rotate_axis = np.cross(z, v) 
        self.tip_mesh.rotate(angle, rotate_axis[0], rotate_axis[1], rotate_axis[2])

        self.tip_mesh.translate(*self.end)

        self.tip_mesh.setVisible(v_len >= self.tip_height)
        
        self.update()
        
# Inspiration: https://github.com/pyqtgraph/pyqtgraph/blob/master/pyqtgraph/opengl/items/GLAxisItem.py
class MyGLAxisItem(gl.GLGraphicsItem.GLGraphicsItem):    
    def __init__(self, parentItem=None, antialias=True, glOptions='translucent', **kwds):
        super().__init__()

        self.lineplot = None    # mark that we are still initializing
        self.x_major_plot = None
        self.y_major_plot = None
        self.z_major_plot = None

        self.x_label = None
        self.y_label = None
        self.z_label = None

        self.x_min = -5.0
        self.x_max = 5.0
        self.x_step = 1.0
        self.x_tick_plane = 2
        
        self.y_min = -5.0
        self.y_max = 5.0
        self.y_step = 1.0
        self.y_tick_plane = 0

        self.z_min = -5.0
        self.z_max = 5.0
        self.z_step = 1.0
        self.z_tick_plane = 0

        self.major_height = 0.25
        
        self.x_color = [1,1,1,1]
        self.y_color = [1,1,1,1]
        self.z_color = [1,1,1,1]

        self.x_visible = True
        self.y_visible = True
        self.z_visible = True
        
        self.setData(**kwds)
        
        # line plots
        self.lineplot = gl.GLLinePlotItem(
            parentItem=self, glOptions=glOptions, mode='lines', antialias=antialias
        )
        self.lineplot.setData(width=3.0)
        
        self.x_major_plot = gl.GLLinePlotItem(
            parentItem=self, glOptions=glOptions, mode='lines', antialias=antialias
        )
        self.y_major_plot = gl.GLLinePlotItem(
            parentItem=self, glOptions=glOptions, mode='lines', antialias=antialias
        )
        self.z_major_plot = gl.GLLinePlotItem(
            parentItem=self, glOptions=glOptions, mode='lines', antialias=antialias
        )
        
        self.setParentItem(parentItem)
        self.updateLines()

    def setXLabel(self, label):
        # remove old
        # TODO prolly need to remove from gl.view also
        if not self.x_label is None:
            self.x_label.setParentItem(None)
            self.x_label = None

        # check is get removing label
        if label is None:
            return
        
        # add new label
        label.setParentItem(self)
        self.x_label = label
        self.updateLabels()
        
    def setYLabel(self, label):
        # remove old
        # TODO prolly need to remove from gl.view also
        if not self.y_label is None:
            self.y_label.setParentItem(None)
            self.y_label = None

        # check is get removing label
        if label is None:
            return
        
        # add new label
        label.setParentItem(self)
        self.y_label = label
        self.updateLabels()
        
    def setZLabel(self, label):
        # remove old
        # TODO prolly need to remove from gl.view also
        if not self.z_label is None:
            self.z_label.setParentItem(None)
            self.z_label = None

        # check is get removing label
        if label is None:
            return
        
        # add new label
        label.setParentItem(self)
        self.z_label = label
        self.updateLabels()
        
    def setData(self, **kwds):
        args = ['x_min', 'x_max', 'x_step', 'x_tick_plane',
                'y_min', 'y_max', 'y_step', 'y_tick_plane',
                'z_min', 'z_max', 'z_step', 'z_tick_plane',
                'x_color', 'y_color', 'z_color',
                'x_visible', 'y_visible', 'z_visible', 
                'major_height']

        # perform any validation and set values
        for k in kwds.keys():
            if k not in args:
                raise ValueError('Invalid keyword argument: %s (allowed arguments are %s)' % (k, str(args)))

        for arg in args:
            if arg in kwds:
                value = kwds[arg]
                setattr(self, arg, value)

        # done 
        self.updateLines()
        
    
    def updateLines(self):
        if self.lineplot is None:
            # still initializing
            return

        ### axis lines
        pos = []
        color = []
        if self.z_visible:
            pos.append([0, 0, self.z_min, 0, 0, self.z_max])
            color.append(self.z_color)
        if self.y_visible:
            pos.append([0, self.y_min, 0, 0, self.y_max, 0])
            color.append(self.y_color)
        if self.x_visible:
            pos.append([self.x_min, 0, 0, self.x_max, 0, 0])
            color.append(self.x_color)
            
        pos = np.array(pos, dtype=np.float32).reshape((-1, 3))

        color = np.array(color, dtype=np.float32)
        color = np.hstack((color, color)).reshape((-1, 4))

        self.lineplot.setData(pos=pos, color=color)

        ###### Major Ticks
        def buildMajorTickPos(min_val, max_val, step, height, axis, plane):
            neg_ticks = np.arange(-step, min_val-step, -step)
            pos_ticks = np.arange(step, max_val+step, step)
            ticks = np.concatenate((np.flip(neg_ticks), pos_ticks))
            ticks = ticks.repeat(2)

            pos = np.zeros((ticks.size,3))
            pos[:,axis] = ticks
            pos[:,plane] = np.tile([height/2, -height/2], ticks.size//2) 
            
            return pos

        tick_color = np.array([1, 1, 1, 1], dtype=np.float32)
        
        self.x_major_plot.setData(pos=buildMajorTickPos(self.x_min,
                                                        self.x_max,
                                                        self.x_step,
                                                        self.major_height,
                                                        0,
                                                        self.x_tick_plane),
                                  color=self.x_color)
        self.x_major_plot.setVisible(self.x_visible)
        
        self.y_major_plot.setData(pos=buildMajorTickPos(self.y_min,
                                                        self.y_max,
                                                        self.y_step,
                                                        self.major_height,
                                                        1,
                                                        self.y_tick_plane),
                                  color=self.y_color)
        self.y_major_plot.setVisible(self.y_visible)
        
        self.z_major_plot.setData(pos=buildMajorTickPos(self.z_min,
                                                        self.z_max,
                                                        self.z_step,
                                                        self.major_height,
                                                        2,
                                                        self.z_tick_plane),
                                  color=self.z_color)
        self.z_major_plot.setVisible(self.z_visible)

        
        #####
        self.updateLabels()
        self.update()

    def updateLabels(self):
        pad=0.25
        if not self.x_label is None:
            self.x_label.setData(pos=[self.x_max+pad, 0.0, 0.0])
            self.x_label.setVisible(self.x_visible)
        if not self.y_label is None:
            self.y_label.setData(pos=[0.0, self.y_max+pad, 0.0])
            self.y_label.setVisible(self.y_visible)
        if not self.z_label is None:
            self.z_label.setData(pos=[0.0, 0.0, self.z_max+pad])
            self.z_label.setVisible(self.z_visible)

# Inspiration: https://github.com/pyqtgraph/pyqtgraph/blob/master/pyqtgraph/opengl/items/GLTextItem.py
class MyGLImageItem(gl.GLGraphicsItem.GLGraphicsItem):
    """Draws image in 3D but always faces camera"""

    def __init__(self, parentItem=None, **kwds):
        """All keyword arguments are passed to setData()"""
        super().__init__(parentItem=parentItem)
        glopts = kwds.pop('glOptions', 'additive')
        self.setGLOptions(glopts)

        self.pos = np.array([0.0, 0.0, 0.0])
        self.image = None
        self.height = 100
        self.width = 100
        self.__qimage = None
        self.setData(**kwds)



    def setData(self, **kwds):
        """
        Update the data displayed by this item. All arguments are optional;
        for example it is allowed to update text while leaving colors unchanged, etc.

        ====================  ==================================================
        **Arguments:**
        ------------------------------------------------------------------------
        pos                   (3,) array of floats specifying text location.
        image                 string - path to image
        height                integer - image height *will keep aspect ratio
        width                 integer - image width *will keep aspect ratio
        ====================  ==================================================
        """
        args = ['pos', 'image', 'height', 'width']
        for k in kwds.keys():
            if k not in args:
                raise ValueError('Invalid keyword argument: %s (allowed arguments are %s)' % (k, str(args)))
        for arg in args:
            if arg in kwds:
                value = kwds[arg]
                if arg == 'pos':
                    if isinstance(value, np.ndarray):
                        if value.shape != (3,):
                            raise ValueError('"pos.shape" must be (3,).')
                    elif isinstance(value, (tuple, list)):
                        if len(value) != 3:
                            raise ValueError('"len(pos)" must be 3.')
                elif arg == 'image' or arg == 'height' or arg == 'width':
                    self.__qimage = None
                setattr(self, arg, value)
            self.update()



    def paint(self):
        if self.image is None \
           or self.view() is None:
            return

        # load image from file if needed
        if self.__qimage is None:
            self.__qimage = QtGui.QImage()
            if not self.__qimage.load(self.image):
                print(f"Error: Could not load image at {self.image}")
                return
            self.__qimage = self.__qimage.scaled(self.width, self.height,
                                                 Qt.AspectRatioMode.KeepAspectRatio,
                                                 Qt.TransformationMode.SmoothTransformation)
                    
        self.setupGLState()

        project = self.compute_projection()
        vec3 = QtGui.QVector3D(*self.pos)
        text_pos = project.map(vec3).toPointF()

        painter = QtGui.QPainter(self.view())
        painter.drawImage(text_pos, self.__qimage)
        painter.end()

    def compute_projection(self):
        # note that QRectF.bottom() != QRect.bottom()
        rect = QtCore.QRectF(self.view().rect())
        ndc_to_viewport = QtGui.QMatrix4x4()
        ndc_to_viewport.viewport(rect.left(), rect.bottom(), rect.width(), -rect.height())
        return ndc_to_viewport * self.mvpMatrix()


class MyDashedLineItem(gl.GLGraphicsItem.GLGraphicsItem):    
    def __init__(self, parentItem=None, antialias=True, glOptions='opaque', **kwds):
        super().__init__()

        self.lineplot = None    # mark that we are still initializing

        self.color = [1.0,1.0,1.0,1.0]
        self.start = [0.0,0.0,0.0]
        self.end = [1.0,1.0,1.0]
        self.dash_len = 0.25
        self.space_len = 0.25
        
        self.setData(**kwds)
        
        self.lineplot = gl.GLLinePlotItem(
            parentItem=self, glOptions=glOptions, mode='lines', antialias=antialias
        )
        self.lineplot.setData(width=3.0)
        
        
        self.setParentItem(parentItem)
        self.updateLines()

    def setData(self, **kwds):
        args = ['color','start', 'end', 'dash_len', 'space_len']

        # perform any validation and set values
        for k in kwds.keys():
            if k not in args:
                raise ValueError('Invalid keyword argument: %s (allowed arguments are %s)' % (k, str(args)))

        for arg in args:
            if arg in kwds:
                value = kwds[arg]
                if arg == 'start' or arg == 'end':
                    if isinstance(value, np.ndarray):
                        if value.shape != (3,1):
                            raise ValueError('"start/end.shape" must be (3,1).')
                    elif isinstance(value, (tuple, list)):
                        if len(value) != 3:
                            raise ValueError('"len(start/end)" must be 3.')

                setattr(self, arg, value)

        # done 
        self.updateLines()
        
    
    def updateLines(self):
        if self.lineplot is None:
            # still initializing
            return

        ### axis lines
        start = np.array(self.start, dtype=np.float32)
        end = np.array(self.end, dtype=np.float32)
        mag = np.linalg.norm(end - start)
        norm_vec = (end-start)/mag
        count = int(np.ceil(mag / (self.dash_len + self.space_len)))
        
        pos = []
        cur_pos = np.array(start)        
        for _ in range(0,count+1):
            pos.append(cur_pos)
            next_pos = self.dash_len * norm_vec + cur_pos
            if np.all(next_pos > end):
                next_pos = end
                pos.append(end)
            else:
                pos.append(next_pos)
            cur_pos = self.space_len * norm_vec + next_pos

        color = np.array(self.color, dtype=np.float32)
        color = np.tile(color, len(pos)*2).reshape((-1, 4))   
        pos = np.array(pos, dtype=np.float32).reshape((-1, 3))
        
        self.lineplot.setData(pos=pos, color=color)
        
        #####
        self.update()

# borrowed from https://github.com/pyqtgraph/pyqtgraph/blob/master/pyqtgraph/opengl/items/GLAxisItem.py
import numpy as np

from pyqtgraph.Qt import QtGui
from pyqtgraph.Qt import QtCore
from pyqtgraph.Qt.QtCore import Qt
import pyqtgraph.opengl as gl

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


class myVectorItem(gl.GLGraphicsItem.GLGraphicsItem):
    def __init__(self, start=[0.0,0.0,0.0], end=[1.0,1.0,1.0], color=[1.0,1.0,1.0,1.0], width=1.0, parentItem=None, glOptions='opaque', antialias=True):
        super().__init__()

        self.lineplot = None
        
        self.start = np.array(start)
        self.end = np.array(end)
        self.width = width
        self.tip_height = 1.0
        self.tip_radius = 0.5
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
        

class myGLAxisItem(gl.GLGraphicsItem.GLGraphicsItem):    
    def __init__(self, parentItem=None, antialias=True, glOptions='translucent', **kwds):
        super().__init__()

        self.lineplot = None    # mark that we are still initializing
        self.x_major_plot = None
        self.y_major_plot = None
        self.z_major_plot = None

        self.x_min = -5.0
        self.x_max = 5.0
        self.x_step = 1.0
        self.x_tick_plane = 1
        
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
        
       # x_text = gl.GLTextItem(parentItem=self, pos=[self.size()[0],0.0,0.0], text="x")

        self.setParentItem(parentItem)
        self.updateLines()

    def setData(self, **kwds):
        args = ['x_min', 'x_max', 'x_step', 'x_tick_plane',
                'y_min', 'y_max', 'y_step', 'y_tick_plane',
                'z_min', 'z_max', 'z_step', 'z_tick_plane',
                'x_color', 'y_color', 'z_color',
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

        pos = np.array([
            [0, 0, self.z_min, 0, 0, self.z_max],
            [0, self.y_min, 0, 0, self.y_max, 0],
            [self.x_min, 0, 0, self.x_max, 0, 0],
        ], dtype=np.float32).reshape((-1, 3))

        color = np.array([
            self.z_color,     
            self.y_color,     
            self.x_color
        ], dtype=np.float32)

        # color both vertices of each line segment
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
        self.y_major_plot.setData(pos=buildMajorTickPos(self.y_min,
                                                        self.y_max,
                                                        self.y_step,
                                                        self.major_height,
                                                        1,
                                                        self.y_tick_plane),
                                  color=self.y_color)
        self.z_major_plot.setData(pos=buildMajorTickPos(self.z_min,
                                                        self.z_max,
                                                        self.z_step,
                                                        self.major_height,
                                                        2,
                                                        self.z_tick_plane),
                                  color=self.z_color)

        
        #####
        self.update()

class myGLImageItem(gl.GLGraphicsItem.GLGraphicsItem):
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
        if self.image is None:
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

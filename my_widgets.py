# borrowed from https://github.com/pyqtgraph/pyqtgraph/blob/master/pyqtgraph/opengl/items/GLAxisItem.py
import numpy as np

from pyqtgraph.Qt import QtGui
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
    def __init__(self, start=[0.0,0.0,0.0], end=[1.0,1.0,1.0], color=[1.0,1.0,1.0,1.0], width=1.0, parentItem=None, glOptions={}, antialias=True):
        super().__init__()

        self.lineplot = None
        
        self.start = np.array(start)
        self.end = np.array(end)
        self.width = width
        self.tip_height = 1.0
        self.tip_radius = 0.5

        
        self.lineplot = gl.GLLinePlotItem(
            parentItem=self, glOptions=glOptions, mode='lines', antialias=antialias
        )

        cone_md = generate_cone(radius=self.tip_radius, height=self.tip_height, segments=8)
        self.tip_mesh = gl.GLMeshItem(parentItem=self,
                                      meshdata=cone_md,
                                      color=np.array([0,1,1,1], dtype=float),
                                      smooth=False,
                                      computeNormals=False,
                                      glOptions='opaque')
        
        
        self.setParentItem(parentItem)
        self.updateLines()

    def updateLines(self):
        if self.lineplot == None:
            return

        pos = np.array([self.start, self.end])
        color=[1.0,1.0,1.0,1.0]
        self.lineplot.setData(pos=pos, color=color)

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
    """
    **Bases:** :class:`GLGraphicsItem <pyqtgraph.opengl.GLGraphicsItem.GLGraphicsItem>`
    
    Displays three lines indicating origin and orientation of local coordinate system. 
    
    """
    
    def __init__(self, size=None, antialias=True, glOptions='translucent', parentItem=None):
        super().__init__()

        self.lineplot = None    # mark that we are still initializing
        self.x_major_plot = None
        
        if size is None:
            size = QtGui.QVector3D(1,1,1)
        self.setSize(size=size)

        self.lineplot = gl.GLLinePlotItem(
            parentItem=self, glOptions=glOptions, mode='lines', antialias=antialias
        )

        self.x_major_plot = gl.GLLinePlotItem(
            parentItem=self, glOptions=glOptions, mode='lines', antialias=antialias
        )
        
        self.setParentItem(parentItem)
        self.updateLines()

    def setSize(self, x=None, y=None, z=None, size=None):
        """
        Set the size of the axes (in its local coordinate system; this does not affect the transform)
        Arguments can be x,y,z or size=QVector3D().
        """
        if size is not None:
            x = size.x()
            y = size.y()
            z = size.z()
        self.__size = [x,y,z]
        self.updateLines()
        
    def size(self):
        return self.__size[:]
    
    def updateLines(self):
        if self.lineplot is None \
           or self.x_major_plot is None:
            # still initializing
            return

        x,y,z = self.size()

        pos = np.array([
            [0, 0, 0, 0, 0, z],
            [0, 0, 0, 0, y, 0],
            [0, 0, 0, x, 0, 0],
        ], dtype=np.float32).reshape((-1, 3))

        color = np.array([
            [0, 1, 0, 0.6],     # z is green
            [1, 1, 0, 0.6],     # y is yellow
            [0, 0, 1, 0.6],     # x is blue
        ], dtype=np.float32)

        # color both vertices of each line segment
        color = np.hstack((color, color)).reshape((-1, 4))

        self.lineplot.setData(pos=pos, color=color)

        ######
        major_height = 0.25
        x_major_step = 0.5
        ticks = np.arange(x_major_step, self.__size[0]+x_major_step, x_major_step)
        color = [1.0, 1.0, 1.0, 1.0]

        pos = np.zeros((ticks.size*2,3))
        pos[:,0] = ticks.repeat(2)
        pos[:,2] = np.tile([major_height/2, -major_height/2], ticks.size) 

        self.x_major_plot.setData(pos=pos, color=color)

        
        #####
        self.update()

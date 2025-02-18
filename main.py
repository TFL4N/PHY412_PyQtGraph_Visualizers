import sys

from my_widgets import *
import numpy as np

#import pyqt
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt.QtCore import (
    QTimer,
    QObject
    )
from pyqtgraph.Qt.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QSplitter,
    QGridLayout,
    QLabel,
    QSpinBox,
    QCheckBox,
    QComboBox,
    QPushButton,
    QDialog,
    QColorDialog,
    QFileDialog,
    QInputDialog,
    QMessageBox
    )


class MyTimer(QObject):
    'Time units are milliseconds; block is a function type'
    def __init__(self, duration=None, interval=100, block=None):
        super().__init__()

        self.duration = duration
        self.interval = interval
        self.block = block
        self.counter = 0.0
        
        self.timer = QTimer()
        self.timer.setInterval(self.interval)
        self.timer.timeout.connect(self.on_timeout)
        
    def start_timer(self):
        self.timer.start()

    def on_timeout(self):
        if self.duration is not None \
           and self.counter >= self.duration:
            self.timer.stop()

        # call function block with float t in seconds
        if self.block is not None:
            self.block(float(self.counter) / 1000)
            
        self.counter += self.interval


        
class BaseWidget(QWidget):
    def __init__(self, autostart=True):
        super().__init__()

        self.setWindowTitle("Ewald Sphere Popout")
        self.resize(500,500)

        # gl view
        self.canvas = gl.GLViewWidget()
        self.canvas.show()

        # menu options
        opts_layout = QGridLayout()

        l = QLabel("Highlight on Mouse Hover")

        w = QPushButton("Save Image")
        w.clicked.connect(self.handleSaveImagePress)

        opts_layout.addWidget(l, 0, 0)
        opts_layout.addWidget(w, 0, 1)

        
        l = QLabel("Play Animation")

        w = QPushButton("Play")
        w.clicked.connect(self.handlePlayAnimationPress)

        opts_layout.addWidget(l, 1, 0)
        opts_layout.addWidget(w, 1, 1)

        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.canvas)
        main_layout.addLayout(opts_layout)
        
        self.setLayout(main_layout)

        # canvas items
        self.cur_t = 0.0
        self.timer = None
        self.frame = 0
        
        # start
        self.setupScene()
        if autostart:
            self.startAnimating()

    def setupScene(self):
        pass
    
    def updateScene(self, t):
        pass
        
    def updateAndRenderScene(self, t):
        self.updateScene(t)
        self.canvas.grabFramebuffer().save(f'video/take_1/frame_{self.frame}.png')
        self.frame += 1

    def startAnimating(self):
        self.stopAnimating()

        self.timer = MyTimer(block=self.updateAndRenderScene)
        self.timer.start_timer()

    def stopAnimating(self):
        if self.timer is not None:
            self.timer.stop()
            self.timer = None
        
    def playAnimation(self, duration):
        print('playAnimation()')
        # for t in np.arange(0,duration,0.3):
        #     self.updateScene(t)
        #     time.sleep(0.3)

        
        # self.timer = QTimer()
        # self.timer.setInterval(100)
        # self.timer.timeout.connect(self.handleAnimationTimer)
        # self.timer.start()  # Update every 50 ms

        
    def handleSaveImagePress(self, state):
        self.canvas.grabFramebuffer().save('images/fileName.png')

    def handlePlayAnimationPress(self, state):
        self.playAnimation(10)


class Part1_Widget(BaseWidget):
    def setupScene(self):
        ## axis
        self.axes = myGLAxisItem()
        self.axes.setSize(x=5, y=5, z=5)
        self.axes.rotate(-90,0,1,0)
        self.canvas.addItem(self.axes)

        self.graph = gl.GLLinePlotItem(parentItem=self.axes,
                                       pos=[0.0,0.0,0.0],
                                       color=[1.0,1.0,1.0,1.0],
                                       width=5.0,
                                       antialias=True,
                                       mode='line_strip')

        pad = 0.25
        x_label = gl.GLTextItem(parentItem=self.axes, pos=[5.0+pad,0.0,0.0], text="x")
        y_label = gl.GLTextItem(parentItem=self.axes, pos=[0.0,5.0+pad,0.0], text="y")
        z_label = gl.GLTextItem(parentItem=self.axes, pos=[0.0,0.0,5.0+pad], text="z")
        
    def updateScene(self, t):
        duration = 10.0
        t = t % duration

        ts = np.arange(0,t+0.25,0.25)
        data = np.zeros((ts.size,3))
        data[:,2] = ts
        data[:,0] = np.cos(data[:,2])

        self.graph.setData(pos=data)
        
        ########################
        
        # vec = myVectorItem(parentItem=axes,
        #                    end=[5.0,5.0,5.0])

        # self.canvas.addItem(vec)

        
class Part2_Widget(BaseWidget):
    def setupScene(self):
        ## axis
        self.axes = myGLAxisItem()
        self.axes.setSize(x=5, y=5, z=5)
        self.axes.lineplot.setData(width=5.0)
        self.axes.rotate(-90,0,1,0)
        self.canvas.addItem(self.axes)

        self.graph = gl.GLLinePlotItem(parentItem=self.axes,
                                       pos=[0.0,0.0,0.0],
                                       color=[1.0,1.0,1.0,1.0],
                                       width=5.0,
                                       antialias=True,
                                       mode='line_strip')
        #self.canvas.addItem(self.graph)

    def updateScene(self, t):
        duration = 10.0
        t = t % duration

        ts = np.arange(0,t+0.25,0.25)
        data = np.zeros((ts.size,3))
        data[:,2] = ts
        data[:,0] = np.cos(data[:,2])

        self.graph.setData(pos=data)
        
        ########################

        text = gl.GLTextItem(parentItem=self.axes, pos=[0.0,0.0,0.0], text="Origin")
        #self.canvas.addItem(text)
        
        # vec = myVectorItem(parentItem=axes,
        #                    end=[5.0,5.0,5.0])

        # self.canvas.addItem(vec)

        
## build a QApplication before building other widgets
app = pg.mkQApp()

w = Part1_Widget()
w.show()


sys.exit(app.exec())  # Start the Qt event loop. This is crucial for the GUI to function.

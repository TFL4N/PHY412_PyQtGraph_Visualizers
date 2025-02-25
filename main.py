import sys

from my_widgets import *
import numpy as np

import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt.QtCore import (
    Qt
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
    QSlider,
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

        
class BaseWidget(QWidget):
    def __init__(self, start_segment=1):
        super().__init__()

        self.setWindowTitle("EM Polarization")
        self.resize(500,500)

        # gl view
        self.canvas = gl.GLViewWidget()
        self.canvas.show()
        
        # canvas items
        self.timer = None
        self.frame = 0
        self.freq = 0.5
        self.phase_diff = 0.0

        self.prev_button = None
        self.next_button = None

        self.segment = None
        
        # menu options
        opts_layout = QGridLayout()

        l = QLabel("Previous Step")

        w = QPushButton("Previous")
        w.clicked.connect(self.handlePreviousPress)
        self.prev_button = w
        
        opts_layout.addWidget(l, 0, 0)
        opts_layout.addWidget(w, 0, 1)


        l = QLabel("Next Step")

        w = QPushButton("Next")
        w.clicked.connect(self.handleNextPress)
        self.next_button = w
        
        opts_layout.addWidget(l, 1, 0)
        opts_layout.addWidget(w, 1, 1)


        l = QLabel("Restart Animation")

        w = QPushButton("Restart")
        w.clicked.connect(self.handleRestartAnimationPress)

        opts_layout.addWidget(l, 2, 0)
        opts_layout.addWidget(w, 2, 1)

        
        l = QLabel("Frequency")

        w = QSlider(Qt.Horizontal)
        w.setValue(0)
        w.setMinimum(0)
        w.setMaximum(1000)
        w.valueChanged.connect(self.handleFreqChange)

        opts_layout.addWidget(l, 3, 0)
        opts_layout.addWidget(w, 3, 1)


        l = QLabel("Phase")

        w = QSlider(Qt.Horizontal)
        w.setValue(0)
        w.setMinimum(0)
        w.setMaximum(1000)
        w.valueChanged.connect(self.handlePhaseChange)

        opts_layout.addWidget(l, 4, 0)
        opts_layout.addWidget(w, 4, 1)

        # Super user controls
        l = QLabel("Save Image")

        w = QPushButton("Capture")
        w.clicked.connect(self.handleSaveImagePress)

        opts_layout.addWidget(l, 5, 0)
        opts_layout.addWidget(w, 5, 1)


        l = QLabel("Debug Action")

        w = QPushButton("Action")
        w.clicked.connect(self.handleDebugActionPress)

        opts_layout.addWidget(l, 6, 0)
        opts_layout.addWidget(w, 6, 1)

        

        
        ### main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.canvas)
        main_layout.addLayout(opts_layout)
        
        self.setLayout(main_layout)
        
        # start
        self.setupScene()
        self.transitionTo(start_segment)
        
    def setupScene(self):
        self.buildAxes()

    def updateScene(self, t):
        self.segment.updateScene(self, t)
        
    def updateAndRenderScene(self, t):
        self.updateScene(t)
        self.canvas.grabFramebuffer().save(f'video/take_1/frame_{self.frame}.png')
        self.frame += 1
        
    def buildAxes(self):
        self.axes = myGLAxisItem(x_min=-3, x_max=3,
                                 y_min=-3, y_max=3,
                                 z_min=-3, z_max=3,
                                 glOptions='opaque')
        self.axes.rotate(-90,0,1,0)
        self.canvas.addItem(self.axes)

        pad = 0.25
        self.x_label = myGLImageItem(parentItem=self.axes,
                                     pos=[self.axes.x_max+pad,0.0,0.0],
                                     image='latex/vec_e.png',
                                     height=30)
        self.y_label = gl.GLTextItem(parentItem=self.axes,
                                     pos=[0.0,self.axes.y_max+pad,0.0],
                                     text="y")
        self.z_label = myGLImageItem(parentItem=self.axes,
                                     pos=[0.0,0.0,self.axes.x_max+pad],
                                     image='latex/vec_k.png',
                                     height=30)
    #
    # Transitions
    #
    def transitionToNext(self):
        new_seg = self.segment.segment_num + 1
        self.transitionTo(new_seg)

    def transitionToPrev(self):
        new_seg = self.segment.segment_num - 1
        self.transitionTo(new_seg)
    
    def transitionTo(self, segment_num):
        # destroy old scene
        self.stopAnimating()
        if not self.segment is None:
            self.segment.tearDownScene(self)
            self.segment = None
        
        # load next segment class
        _module = __import__('segments')
        _class = None

        if segment_num == 1:
            _class = getattr(_module, 'Part1')
        elif segment_num == 2:
            _class = getattr(_module, 'Part2')
        else:
            print('Unknown segment number')
            
        # start new scene
        self.segment = _class()
        self.segment.setupScene(self)
        self.startAnimating()
        
        
    #
    # Animation Timer Controls
    #
    def restartAnimation(self):
        self.stopAnimating()
        self.startAnimating()
        
    def startAnimating(self):
        self.stopAnimating()

        self.timer = MyTimer(block=self.updateScene)
        self.timer.start_timer()

    def stopAnimating(self):
        if self.timer is not None:
            self.timer.stop_timer()
            self.timer = None
        
    #
    # Button Handlers
    #
    def handlePreviousPress(self, state):
        self.transitionToPrev()

    def handleNextPress(self, state):
        self.transitionToNext()
    
    def handleRestartAnimationPress(self, state):
        self.restartAnimation()

    def handleFreqChange(self, val):
        min_freq = 0.5
        max_freq = 5.0
        val = float(val)/1000
        val *= max_freq - min_freq
        val += min_freq
        self.freq = val

        self.restartAnimation()

    def handlePhaseChange(self, val):
        pass

    def handleSaveImagePress(self, state):
        self.canvas.grabFramebuffer().save('images/fileName.png')
    
    def handleDebugActionPress(self, state):
        print(self.canvas.cameraPosition())
        print(self.canvas.opts)


        
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

        
## build a QApplication before building other widgets
app = pg.mkQApp()

w = BaseWidget()
w.show()


sys.exit(app.exec())  # Start the Qt event loop. This is crucial for the GUI to function.

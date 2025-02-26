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
    QGridLayout,
    QLabel,
    QSlider,
    QCheckBox,
    QPushButton
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
        self.magnitude = 3.0
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
        self.axes = MyGLAxisItem(x_min=-3, x_max=3,
                                 y_min=-3, y_max=3,
                                 z_min=-3, z_max=3,
                                 glOptions='opaque')
        self.axes.rotate(-90,0,1,0)
        self.canvas.addItem(self.axes)

        pad = 0.25
        self.x_label = MyGLImageItem(parentItem=self.axes,
                                     pos=[self.axes.x_max+pad,0.0,0.0],
                                     image='latex/hat_e_1.png',
                                     height=30)
        self.y_label = MyGLImageItem(parentItem=self.axes,
                                     pos=[0.0,self.axes.y_max+pad,0.0],
                                     image='latex/hat_e_2.png',
                                     height=30)
        self.z_label = MyGLImageItem(parentItem=self.axes,
                                     pos=[0.0,0.0,self.axes.z_max+pad],
                                     image='latex/hat_k.png',
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
        elif segment_num == 3:
            _class = getattr(_module, 'Part3')
        elif segment_num == 4:
            _class = getattr(_module, 'Part4')
        elif segment_num == 5:
            _class = getattr(_module, 'Part5')
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
        self.freq = linear_scale(x1=0.5,
                                 x2=5.0,
                                 y2=1000,
                                 y=val)
        self.restartAnimation()

    def handlePhaseChange(self, val):
        pass

    def handleSaveImagePress(self, state):
        self.canvas.grabFramebuffer().save('images/fileName.png')
    
    def handleDebugActionPress(self, state):
        print(self.canvas.cameraPosition())
        print(self.canvas.opts)


        
## build a QApplication before building other widgets
app = pg.mkQApp()

w = BaseWidget()
w.show()


sys.exit(app.exec())  # Start the Qt event loop. This is crucial for the GUI to function.

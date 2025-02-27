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
    def __init__(self, start_segment=1, start_chapter=1):
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
        self.phase_diff_int = 0

        self.prev_part_button = None
        self.next_part_button = None
        self.prev_chapter_button = None
        self.next_chapter_button = None
        self.pause_button = None
        self.right_circ_button = None
        self.left_circ_button = None
        
        self.freq_label = None
        self.phase_diff_label = None
        self.phase_diff_slider = None

        self.chapter = None
        self.segment = None
        
        # menu options
        opts_layout = QGridLayout()
        opts_layout.setColumnStretch(0,1)
        opts_layout.setColumnStretch(1,1)

        w = QPushButton("Previous Part")
        w.clicked.connect(self.handlePreviousPartPress)
        self.prev_part_button = w
        
        opts_layout.addWidget(w, 0, 0)

        w = QPushButton("Next Part")
        w.clicked.connect(self.handleNextPartPress)
        self.next_part_button = w
        opts_layout.addWidget(w, 0, 1)

        w = QPushButton("Previous Chapter")
        w.clicked.connect(self.handlePreviousChapterPress)
        self.prev_chapter_button = w
        opts_layout.addWidget(w, 1, 0)

        w = QPushButton("Next Chapter")
        w.clicked.connect(self.handleNextChapterPress)
        self.next_chapter_button = w
        opts_layout.addWidget(w, 1, 1)

        w = QPushButton("Restart Animation")
        w.clicked.connect(self.handleRestartAnimationPress)
        opts_layout.addWidget(w, 2, 0)

        w = QPushButton("Pause Animation")
        w.clicked.connect(self.handlePauseAnimationPress)
        self.pause_button = w
        opts_layout.addWidget(w, 2, 1)

        
        l = QLabel("Frequency")
        self.freq_label = l
        self.updateFreqLabel()

        w = QSlider(Qt.Horizontal)
        w.setValue(0)
        w.setMinimum(0)
        w.setMaximum(1000)
        w.valueChanged.connect(self.handleFreqChange)

        opts_layout.addWidget(l, 3, 0)
        opts_layout.addWidget(w, 3, 1)


        l = QLabel("Relative Phase")
        self.phase_diff_label = l
        self.updatePhaseDiffLabel()
        
        w = QSlider(Qt.Horizontal)
        w.setValue(0)
        w.setMinimum(-2)
        w.setMaximum(2)
        w.valueChanged.connect(self.handlePhaseChange)
        self.phase_diff_slider = w
        
        opts_layout.addWidget(l, 4, 0)
        opts_layout.addWidget(w, 4, 1)

        w = QPushButton("Right Circular")
        w.clicked.connect(self.handleRightCircularPress)
        self.right_circ_button = w
        opts_layout.addWidget(w, 5, 0)

        w = QPushButton("Left Circular")
        w.clicked.connect(self.handleLeftCircularPress)
        self.left_circ_button = w
        opts_layout.addWidget(w, 5, 1)

        
        # Super user controls
        if False:
            l = QLabel("Save Image")
            
            w = QPushButton("Capture")
            w.clicked.connect(self.handleSaveImagePress)
            
            opts_layout.addWidget(l, 6, 0)
            opts_layout.addWidget(w, 6, 1)
        

            l = QLabel("Debug Action")
            
            w = QPushButton("Action")
            w.clicked.connect(self.handleDebugActionPress)
            
            opts_layout.addWidget(l, 7, 0)
            opts_layout.addWidget(w, 7, 1)

        
        ### main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.canvas)
        main_layout.addLayout(opts_layout)
        
        self.setLayout(main_layout)
        
        # start
        self.setupScene()
        self.transitionTo(start_segment, start_chapter)
        
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
                                 glOptions='translucent')
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
    def transitionToNextPart(self):
        new_seg = self.segment.segment_num + 1
        new_chapter = self.chapter
        if new_seg > 6:
            new_seg = new_seg % 6
            new_chapter += 1
        self.transitionTo(new_seg, new_chapter)

    def transitionToPrevPart(self):
        new_seg = self.segment.segment_num - 1
        new_chapter = self.chapter
        if new_seg < 1:
            new_seg = 6
            new_chapter -= 1
        self.transitionTo(new_seg, new_chapter)
    
    def transitionToNextChapter(self):
        self.transitionTo(self.segment.segment_num,
                          self.chapter + 1)

    def transitionToPrevChapter(self):
        self.transitionTo(self.segment.segment_num,
                          self.chapter - 1)
    
    def transitionTo(self, segment_num, chapter_num):
        # destroy old scene
        self.stopAnimating()
        if not self.segment is None:
            self.segment.tearDownScene(self)
            self.segment = None

        # chapter updates
        self.chapter = chapter_num

        self.next_chapter_button.setDisabled(not (self.chapter < 3))
        self.prev_chapter_button.setDisabled(not (self.chapter > 1))

        self.next_part_button.setDisabled(self.chapter == 3 and segment_num == 6)
        self.prev_part_button.setDisabled(self.chapter == 1 and segment_num == 1)
        
        if self.chapter == 3:
            self.phase_diff_label.setHidden(False)
            self.phase_diff_slider.setHidden(False)
            self.right_circ_button.setHidden(False)
            self.left_circ_button.setHidden(False)
        else:
            self.phase_diff_label.setHidden(True)
            self.phase_diff_slider.setHidden(True)
            self.right_circ_button.setHidden(True)
            self.left_circ_button.setHidden(True)
            self.phase_diff_int = 0
            self.phase_diff = 0.0
            self.updatePhaseDiffLabel()
            self.phase_diff_slider.setValue(0)
            
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
        elif segment_num == 6:
            _class = getattr(_module, 'Part6')
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

    def togglePauseAnimation(self):
        if self.timer is None:
            return

        if self.timer.is_running():
            self.timer.stop_timer()
            self.pause_button.setText('Resume Animation')
        else:
            self.timer.start_timer()
            self.pause_button.setText('Pause Animation')
        
    def startAnimating(self):
        self.stopAnimating()

        self.timer = MyTimer(block=self.updateScene)
        self.timer.start_timer()
        self.pause_button.setText('Pause Animation')

    def stopAnimating(self):
        if self.timer is not None:
            self.timer.stop_timer()
            self.timer = None
        
    #
    # Button Handlers
    #
    def handlePreviousPartPress(self, state):
        self.transitionToPrevPart()

    def handleNextPartPress(self, state):
        self.transitionToNextPart()

    def handlePreviousChapterPress(self, state):
        self.transitionToPrevChapter()

    def handleNextChapterPress(self, state):
        self.transitionToNextChapter()
    
    def handleRestartAnimationPress(self, state):
        self.restartAnimation()

    def handlePauseAnimationPress(self, state):
        self.togglePauseAnimation()

    def handleFreqChange(self, val):
        self.freq = linear_scale(x1=0.5,
                                 x2=5.0,
                                 y2=1000,
                                 y=val)
        self.restartAnimation()
        self.updateFreqLabel()

    def handlePhaseChange(self, val):
        self.phase_diff_int = val
        self.phase_diff = val * np.pi / 4
        
        self.restartAnimation()
        self.updatePhaseDiffLabel()

    def handleRightCircularPress(self, state):
        self.handlePhaseChange(-2)
        self.phase_diff_slider.setValue(-2)
        
    def handleLeftCircularPress(self, state):
        self.handlePhaseChange(2)
        self.phase_diff_slider.setValue(2)
        
    def handleSaveImagePress(self, state):
        self.canvas.grabFramebuffer().save('images/fileName.png')
    
    def handleDebugActionPress(self, state):
        print(self.canvas.cameraPosition())
        print(self.canvas.opts)

    #
    # Utils
    #
    def updateFreqLabel(self):
        self.freq_label.setText(f'Frequency\n{self.freq}')

    def updatePhaseDiffLabel(self):
        if self.phase_diff_int == 0:
            self.phase_diff_label.setText("Relative Phase\n0")
        else:
            denom = int(np.abs(4 / self.phase_diff_int))
            sign = '' if self.phase_diff_int > 0 else '-'
            self.phase_diff_label.setText(f"Relative Phase\n{sign}\u03c0/{denom}")

        
## build a QApplication before building other widgets
app = pg.mkQApp()

w = BaseWidget()
w.show()


sys.exit(app.exec())  # Start the Qt event loop. This is crucial for the GUI to function.

import sys

from my_widgets import *
import numpy as np

#import pyqt
import pyqtgraph as pg
import pyqtgraph.opengl as gl
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



class Widget(QWidget):
    '''Contains the main window and root layout'''
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ewald Sphere Popout")
        self.resize(500,500)

        self.canvas = gl.GLViewWidget()
        self.canvas.show()


        ## axis
        axes = myGLAxisItem()
        axes.setSize(x=5, y=5, z=5)
        axes.lineplot.setData(width=5.0)
        axes.rotate(-90,0,1,0)
        self.canvas.addItem(axes)

        cnt = 50
        data = np.zeros((cnt,3))
        data[:,2] = np.linspace(0,5,cnt)
        data[:,0] = np.cos(data[:,2])
        
        graph = gl.GLLinePlotItem(parentItem=axes,
                                  pos=data,
                                  color=[1.0,1.0,1.0,1.0],
                                  width=5.0,
                                  antialias=True,
                                  mode='line_strip')
        self.canvas.addItem(graph)
        
        ########################

        vec = myVectorItem(parentItem=axes,
                           end=[5.0,5.0,5.0])

        self.canvas.addItem(vec)

        
        ########################
        opts_layout = QGridLayout()

        l = QLabel("Highlight on Mouse Hover")

        w = QPushButton("Save Image")
        w.clicked.connect(self.handleSaveImagePress)

        opts_layout.addWidget(l, 0, 0)
        opts_layout.addWidget(w, 0, 1)

        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.canvas)
        main_layout.addLayout(opts_layout)
        
        self.setLayout(main_layout)

    def handleSaveImagePress(self, state):
        self.canvas.grabFramebuffer().save('images/fileName.png')

## build a QApplication before building other widgets
app = pg.mkQApp()

w = Widget()
w.show()


sys.exit(app.exec())  # Start the Qt event loop. This is crucial for the GUI to function.

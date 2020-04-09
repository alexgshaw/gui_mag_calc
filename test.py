# import sys
# import time

# import numpy as np

# from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
# if is_pyqt5():
#     from matplotlib.backends.backend_qt5agg import (
#         FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
# else:
#     from matplotlib.backends.backend_qt4agg import (
#         FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
# from matplotlib.figure import Figure


# class ApplicationWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self._main = QtWidgets.QWidget()
#         self.setCentralWidget(self._main)
#         layout = QtWidgets.QVBoxLayout(self._main)

#         static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
#         layout.addWidget(static_canvas)
#         self.addToolBar(NavigationToolbar(static_canvas, self))

#         dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
#         layout.addWidget(dynamic_canvas)
#         self.addToolBar(QtCore.Qt.BottomToolBarArea,
#                         NavigationToolbar(dynamic_canvas, self))

#         self._static_ax = static_canvas.figure.subplots()
#         t = np.linspace(0, 10, 501)
#         self._static_ax.plot(t, np.tan(t), ".")

#         self._dynamic_ax = dynamic_canvas.figure.subplots()
#         self._timer = dynamic_canvas.new_timer(
#             100, [(self._update_canvas, (), {})])
#         self._timer.start()

#     def _update_canvas(self):
#         self._dynamic_ax.clear()
#         t = np.linspace(0, 10, 101)
#         # Shift the sinusoid as a function of time.
#         self._dynamic_ax.plot(t, np.sin(t + time.time()))
#         self._dynamic_ax.figure.canvas.draw()


# if __name__ == "__main__":
#     qapp = QtWidgets.QApplication(sys.argv)
#     app = ApplicationWindow()
#     app.show()
#     qapp.exec_()

import sys
import matplotlib
import numpy as np
matplotlib.use('Qt5Agg')

# from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from plane_canvas import PlaneCanvas
from matplotlib import pyplot as plt


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # sc = MplCanvas(self, width=5, height=4, dpi=100)
        # sc.axes.pcolormesh(np.random.rand(10,10))
        # sc = PlaneCanvas(self)
        # plt.figure(1)
        # plt.pcolormesh(np.random.rand(10,10))

        # # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        # toolbar = NavigationToolbar(sc, self)

        layout = QVBoxLayout()
        # layout.addWidget(toolbar)
        # layout.addWidget(sc)

        self.btn = QPushButton("Browse")
        self.btn.clicked.connect(self.getfiles)

        self.label = QLabel('Hello')

        layout.addWidget(self.label)
        layout.addWidget(self.btn)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.show()

    def getfiles(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        filenames = []

        if dlg.exec_():
            filenames = dlg.selectedFiles()                
            with open(filenames[0], 'r') as f:
                data = f.read()
                self.label.setText(data)


app = QApplication(sys.argv)
w = MainWindow()
app.exec_()
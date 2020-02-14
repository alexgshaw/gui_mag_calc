import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=5, dpi=200):
        fig = plt.figure(1, figsize=(width,height), dpi=dpi)
        super(PlotCanvas, self).__init__(fig)
        self.calc = parent.calc
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot(1, 10, np.array([0,0,1]))

    def plot(self,
             side_length,
             resolution,
             center_point,
             norm_vec=np.array([0,0,1]),
             return_vector=False,
             mask_radius=None):

        plane = self.calc.make_plane(side_length=side_length,
                                            resolution=resolution,
                                            center_point=center_point,
                                            norm_vec=norm_vec,
                                            mask_radius=mask_radius)

        a = np.linspace(-side_length/2, side_length/2, resolution*side_length)
        b = np.linspace(-side_length/2, side_length/2, resolution*side_length)

        plt.figure(1)
        plt.clf()

        plt.pcolormesh(a, b, plane, cmap='Spectral')
        plt.gca().set_aspect('equal')

        cbar = plt.colorbar(orientation='horizontal')
        cbar.set_label('Tesla')

        plt.xlabel('Angstroms')
        plt.ylabel('Angstroms')
        plt.title('Magnetic Field')
        plt.tight_layout()

        self.draw()
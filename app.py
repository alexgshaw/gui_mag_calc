import numpy as np
import os
import sys
import inspect
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from plot_layout import PlotLayout
from field_layout import FieldLayout

plt.style.use('ggplot')

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(1, parentdir)

from mag_calc import MagCalc

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Magnetic Calculator')

        self.calc = self.get_calc()

        plot_layout = PlotLayout(self)
        field_layout = FieldLayout(self)
        layout = QHBoxLayout()

        layout.addLayout(field_layout)
        layout.addLayout(plot_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setGeometry(app.desktop().availableGeometry())
        self.setCentralWidget(widget)

    def get_calc(self):
        spins = np.load('spin_atom_arrays/1_1_1_spins.npy')
        atoms = np.load('spin_atom_arrays/1_1_1_atoms.npy')
        calc = MagCalc(atoms=atoms,
                        spins=spins,
                        g_factor=2,
                        spin=1,
                        magneton='mu_B')
        return calc

if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()

    app.exec_()

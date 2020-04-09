import numpy as np
import os
import sys
import inspect
import matplotlib.pyplot as plt
from plane_canvas import PlaneCanvas
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

plt.style.use('ggplot')

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(1,parentdir)

from mag_calc import MagCalc

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Magnetic Calculator')
        self.calc = self.get_calc()

        self.layout = QVBoxLayout()
        self.coordinates = QHBoxLayout()
        self.buttons = QHBoxLayout()
        self.sliders = QGridLayout()

        self.field_button = QPushButton('Compute Field')
        self.plot_button = QPushButton('Plot Field')
        self.label = QLabel('Field here')
        self.res_slider = QSlider(Qt.Horizontal)
        self.sl_slider = QSlider(Qt.Horizontal)
        self.res_label = QLabel('Resolution: 10')
        self.sl_label = QLabel('Side Length: 10')
        self.x_coord = QLineEdit()
        self.y_coord = QLineEdit()
        self.z_coord = QLineEdit()
        self.plot = PlaneCanvas(self)
        
        self.field_button.clicked.connect(self.on_field_button_clicked)
        self.plot_button.clicked.connect(self.on_plot_button_clicked)
        
        self.label.setText('Enter coordinates for field calculation.')

        self.res_slider.setMinimum(5)
        self.res_slider.setMaximum(100)
        self.res_slider.setValue(10)
        self.res_slider.valueChanged.connect(self.on_res_slider_change)
        # self.res_slider.setTickInterval(2)
        # self.res_slider.setTickPosition(QSlider.TicksBelow)
        self.res_slider.setToolTip(str(self.res_slider.value()))
        self.sl_slider.setMinimum(1)
        self.sl_slider.setMaximum(20)
        self.sl_slider.setValue(10)
        self.sl_slider.valueChanged.connect(self.on_sl_slider_change)
        # self.sl_slider.setTickInterval(1)
        # self.sl_slider.setTickPosition(QSlider.TicksBelow)
        self.sl_slider.setToolTip(str(self.sl_slider.value()))

        self.x_coord.setPlaceholderText('x-coordinate')
        self.y_coord.setPlaceholderText('y-coordinate')
        self.z_coord.setPlaceholderText('z-coordinate')
        self.coordinates.addWidget(self.x_coord)
        self.coordinates.addWidget(self.y_coord)
        self.coordinates.addWidget(self.z_coord)

        self.buttons.addWidget(self.field_button)
        self.buttons.addWidget(self.plot_button)

        self.sliders.addWidget(self.res_label, 0, 0)
        self.sliders.addWidget(self.sl_label, 0, 1)
        self.sliders.addWidget(self.res_slider, 1, 0)
        self.sliders.addWidget(self.sl_slider, 1, 1)

        self.layout.addLayout(self.buttons)
        self.layout.addWidget(self.label)
        self.layout.addLayout(self.coordinates)
        self.layout.addLayout(self.sliders)
        self.layout.addWidget(self.plot)

        widget = QWidget()
        widget.setLayout(self.layout)

        self.setGeometry(app.desktop().availableGeometry())

        self.setCentralWidget(widget)

    def get_location(self):
        try:
            x = float(self.x_coord.text())
            y = float(self.y_coord.text())
            z = float(self.z_coord.text())
            return np.array([x,y,z])
        except ValueError:
            raise ValueError('Please enter x,y,z coordinates.')

    def on_res_slider_change(self):
        self.res_label.setText('Resolution: {}'.format(self.res_slider.value()))

    def on_sl_slider_change(self):
        self.sl_label.setText('Side Length: {}'.format(self.sl_slider.value()))

    def on_field_button_clicked(self):
        try:
            location = self.get_location()
            field = self.calc.calculate_field(location, False)
            self.label.setText(str(round(field, 6)))
        except ValueError as e:
            self.label.setText(e.args[0])


    def on_plot_button_clicked(self):
        try:
            location = self.get_location()
            resolution = self.res_slider.value()
            side_length = self.sl_slider.value()
            self.plot.plot(resolution, side_length, location)
        except ValueError as e:
            self.label.setText(e.args[0])

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

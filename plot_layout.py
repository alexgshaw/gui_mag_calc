from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from plot_canvas import PlotCanvas
import numpy as np

INIT_RES = 20
INIT_SL = 4
RES_MIN = 5
RES_MAX = 100
SL_MIN = 1
SL_MAX = 20
INIT_CENTER = ['0','0','1']
INIT_NORM = ['0','0','1']
INIT_MASK = '8'

class PlotLayout(QVBoxLayout):
    def __init__(self, parent):
        super(PlotLayout, self).__init__()
        
        self.parent = parent
        self.calc = parent.calc

        self.plot_button = QPushButton('PLOT')

        self.center_label = QLabel('Center Point')
        self.normal_label = QLabel('Normal Vector')
        self.mask_label = QLabel('Mask Radius')
        self.res_label = QLabel()
        self.sl_label = QLabel()

        self.center_x_edit = QLineEdit(INIT_CENTER[0])
        self.center_y_edit = QLineEdit(INIT_CENTER[1])
        self.center_z_edit = QLineEdit(INIT_CENTER[2])
        self.normal_x_edit = QLineEdit(INIT_NORM[0])
        self.normal_y_edit = QLineEdit(INIT_NORM[1])
        self.normal_z_edit = QLineEdit(INIT_NORM[2])
        self.mask_edit = QLineEdit(INIT_MASK)

        self.res_slider = QSlider(Qt.Horizontal)
        self.sl_slider = QSlider(Qt.Horizontal)

        self.plot = PlotCanvas(self.parent)
        self.toolbar = NavigationToolbar(self.plot, self.parent)

        center_xyz_layout = QHBoxLayout()
        normal_xyz_layout = QHBoxLayout()
        center_layout = QHBoxLayout()
        normal_layout = QHBoxLayout()
        mask_layout = QHBoxLayout()
        right_layout = QVBoxLayout()
        left_layout = QVBoxLayout()
        top_layout = QHBoxLayout()

        center_xyz_layout.addWidget(self.center_x_edit)
        center_xyz_layout.addWidget(self.center_y_edit)
        center_xyz_layout.addWidget(self.center_z_edit)

        normal_xyz_layout.addWidget(self.normal_x_edit)
        normal_xyz_layout.addWidget(self.normal_y_edit)
        normal_xyz_layout.addWidget(self.normal_z_edit)

        center_layout.addWidget(self.center_label)
        center_layout.addLayout(center_xyz_layout)
        normal_layout.addWidget(self.normal_label)
        normal_layout.addLayout(normal_xyz_layout)
        mask_layout.addWidget(self.mask_label)
        mask_layout.addWidget(self.mask_edit)

        left_layout.addLayout(center_layout)
        left_layout.addLayout(normal_layout)
        left_layout.addWidget(self.res_label)
        left_layout.addWidget(self.res_slider)
        right_layout.addWidget(self.plot_button)
        right_layout.addLayout(mask_layout)
        right_layout.addWidget(self.sl_label)
        right_layout.addWidget(self.sl_slider)

        top_layout.addLayout(left_layout)
        top_layout.addLayout(right_layout)
        
        self.addLayout(top_layout)
        self.addWidget(self.toolbar)
        self.addWidget(self.plot)

        self.sl_slider.valueChanged.connect(self.on_sl_slider_change)
        self.res_slider.valueChanged.connect(self.on_res_slider_change)

        self.plot_button.clicked.connect(self.on_plot_button_clicked)

        self.res_slider.setMinimum(RES_MIN)
        self.res_slider.setMaximum(RES_MAX)
        self.res_slider.setValue(INIT_RES)
        self.sl_slider.setMinimum(SL_MIN)
        self.sl_slider.setMaximum(SL_MAX)
        self.sl_slider.setValue(INIT_SL)

        self.center_x_edit.setPlaceholderText('x-coordinate')
        self.center_y_edit.setPlaceholderText('y-coordinate')
        self.center_z_edit.setPlaceholderText('z-coordinate')
        self.normal_x_edit.setPlaceholderText('x-coordinate')
        self.normal_y_edit.setPlaceholderText('y-coordinate')
        self.normal_z_edit.setPlaceholderText('z-coordinate')
        self.mask_edit.setPlaceholderText('Leave blank no mask')


    def on_res_slider_change(self):
        self.res_label.setText('Resolution: {} (Points per Angstrom)'.format(self.res_slider.value()))

    def on_sl_slider_change(self):
        self.sl_label.setText('Side Length: {} (Angstroms)'.format(self.sl_slider.value()))

    def get_center(self):
        try:
            x = float(self.center_x_edit.text())
            y = float(self.center_y_edit.text())
            z = float(self.center_z_edit.text())
            return np.array([x,y,z])
        except ValueError:
            raise ValueError('Please enter x,y,z coordinates.')

    def get_normal(self):
        try:
            x = float(self.normal_x_edit.text())
            y = float(self.normal_y_edit.text())
            z = float(self.normal_z_edit.text())
            return np.array([x,y,z])
        except ValueError:
            raise ValueError('Please enter x,y,z coordinates.')

    def on_plot_button_clicked(self):
        try:
            center = self.get_center()
            normal = self.get_normal()
            resolution = self.res_slider.value()
            side_length = self.sl_slider.value()
            mask_radius = float(self.mask_edit.text()) if self.mask_edit.text() != '' else None

            self.plot.plot(side_length=side_length,
                           resolution=resolution,
                           center_point=center,
                           norm_vec=normal,
                           mask_radius=mask_radius)

        except ValueError as e:
            alert = QMessageBox()
            alert.setText(e.args[0])
            alert.exec_()
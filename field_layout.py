from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from table_canvas import Table
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import numpy as np

class FieldLayout(QVBoxLayout):
    def __init__(self, parent):
        super(FieldLayout, self).__init__()
        
        self.parent = parent
        self.calc = parent.calc
        
        self.table = Table(self.parent)

        self.file_label = QLabel('Choose a .npy file.')
        self.loc_label = QLabel('Location')
        self.mask_label = QLabel('Mask Radius')

        self.browse_button = QPushButton('Browse')
        self.calc_button = QPushButton('CALCULATE')

        self.browse_button.clicked.connect(self.on_browse_button_clicked)
        self.calc_button.clicked.connect(self.on_calc_button_clicked)

        self.loc_x_edit = QLineEdit()
        self.loc_y_edit = QLineEdit()
        self.loc_z_edit = QLineEdit()
        self.mask_edit = QLineEdit()

        loc_xyz_layout = QHBoxLayout()
        loc_layout = QHBoxLayout()
        mask_layout = QHBoxLayout()
        vec_layout = QHBoxLayout()
        top_layout = QGridLayout()

        loc_xyz_layout.addWidget(self.loc_x_edit)
        loc_xyz_layout.addWidget(self.loc_y_edit)
        loc_xyz_layout.addWidget(self.loc_z_edit)

        loc_layout.addWidget(self.loc_label)
        loc_layout.addLayout(loc_xyz_layout)
        mask_layout.addWidget(self.mask_label)
        mask_layout.addWidget(self.mask_edit)

        top_layout.addWidget(self.browse_button, 0, 0)
        top_layout.addWidget(self.file_label, 1, 0)
        top_layout.addLayout(mask_layout, 2, 0)
        top_layout.addWidget(self.calc_button, 0, 1)
        top_layout.addLayout(loc_layout, 1, 1)

        self.addLayout(top_layout)
        self.addLayout(self.table)


    def get_location(self):
        try:
            x = float(self.loc_x_edit.text())
            y = float(self.loc_y_edit.text())
            z = float(self.loc_z_edit.text())
            return np.array([x,y,z])
        except ValueError:
            # raise ValueError('Please enter x,y,z coordinates.')

        
    def on_calc_button_clicked(self):
        try:
            location = self.get_location()
            self.table.make_table(locations=location, mask_radius=8)
        # except ValueError as e:

        except Exception as e:
            alert = QMessageBox()
            alert.setText(e.args[0])
            alert.exec_()


    def on_browse_button_clicked(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        filenames = []

        if dlg.exec_():
            try:
                filenames = dlg.selectedFiles()
                locations = np.load(filenames[0])
                self.table.init_table(locations=locations)
            except Exception as e:
                alert = QMessageBox()
                alert.setText(e.args[0])
                alert.exec_()

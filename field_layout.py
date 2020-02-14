from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from plot_canvas import PlotCanvas

init_res = 20
init_sl = 4

class FieldLayout(QVBoxLayout):
    def __init__(self, parent):
        super(FieldLayout, self).__init__()
        
        self.parent = parent
        self.calc = parent.calc

        self.file_label = QLabel('Choose a file.')
        self.loc_label = QLabel('Location')
        self.mask_label = QLabel('Mask Radius')
        self.vec_label = QLabel('Vector')

        self.browse_button = QPushButton('Browse')
        self.calc_button = QPushButton('CALCULATE')

        self.loc_x_edit = QLineEdit()
        self.loc_y_edit = QLineEdit()
        self.loc_z_edit = QLineEdit()
        self.mask_edit = QLineEdit()

        self.vec_radio = QRadioButton()

        toolbar_widget = QWidget()
        self.plot = PlotCanvas(self.parent)
        self.toolbar = NavigationToolbar(self.plot, toolbar_widget)
        toolbar_widget.setLayout(QVBoxLayout())
        toolbar_widget.layout().addWidget(self.toolbar)


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
        vec_layout.addWidget(self.vec_label)
        vec_layout.addWidget(self.vec_radio)

        top_layout.addWidget(self.browse_button, 0, 0)
        top_layout.addWidget(self.file_label, 1, 0)
        top_layout.addLayout(mask_layout, 2, 0)
        top_layout.addWidget(self.calc_button, 0, 1)
        top_layout.addLayout(loc_layout, 1, 1)
        top_layout.addLayout(vec_layout, 2, 1)

        self.addLayout(top_layout)
        self.addWidget(toolbar_widget)
        self.addWidget(self.plot)
        

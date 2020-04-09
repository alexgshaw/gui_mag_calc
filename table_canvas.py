import numpy as np 
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# np.set_printoptions(precision=3)

ROWS = 1
COLS = 5
LABELS = ['LOCATION', 'X', 'Y', 'Z', 'MAGNITUDE']
DECIMALS = 3

class Table(QVBoxLayout):
    def __init__(self, parent):
        super(Table, self).__init__()

        self.parent = parent
        self.calc = parent.calc

        self.table = QTableWidget()
        self.table.setColumnCount(COLS)
        self.table.setHorizontalHeaderLabels(LABELS)
        # self.make_table(np.random.rand(3,3), mask_radius=8)
        self.init_table(np.random.rand(3,3))

        header = self.table.horizontalHeader()
        for i in range(COLS):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

        self.addWidget(self.table)


    def init_table(self,
                   locations=None):
        if locations.ndim == 1:
            ROWS = 1
            locations = np.expand_dims(locations, axis=0)
        else:
            ROWS = len(locations)

        self.table.setRowCount(ROWS)
        for i, location in enumerate(locations):
            self.table.setItem(i, 0, QTableWidgetItem(str(tuple(location.round(DECIMALS)))))
            self.table.setItem(i, 1, QTableWidgetItem(''))
            self.table.setItem(i, 2, QTableWidgetItem(''))
            self.table.setItem(i, 3, QTableWidgetItem(''))
            self.table.setItem(i, 4, QTableWidgetItem(''))


    def make_table(self,
                   locations,
                   mask_radius):
        if locations.ndim == 1:
            ROWS = 1
            locations = np.expand_dims(locations, axis=0)
        else:
            ROWS = len(locations)

        fields = self.calc.calculate_field(locations=locations,
                                           return_vector=True,
                                           mask_radius=mask_radius)

        self.table.setRowCount(ROWS)
        for i, (location, field) in enumerate(zip(locations, fields)):
            self.table.setItem(i, 0, QTableWidgetItem(str(tuple(location.round(DECIMALS)))))
            self.table.setItem(i, 1, QTableWidgetItem(str(field[0])))
            self.table.setItem(i, 2, QTableWidgetItem(str(field[1])))
            self.table.setItem(i, 3, QTableWidgetItem(str(field[2])))
            self.table.setItem(i, 4, QTableWidgetItem(str(np.linalg.norm(field))))


        

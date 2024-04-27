# Cache Table class, part of the Cache Simulator
# ECE 1110 Project 2
# Christopher Luk and Dane Krall

from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QTableWidget,
)
from random import randrange

class MemoryTable(object):
    def __init__(self):
        self.table_window = QWidget()
        self.create_layout()
        self.table_window.setLayout(self.layout)

    def create_layout(self):
        self.layout = QGridLayout()

        memory_label = QLabel("Physical Memory")
        self.layout.addWidget(memory_label, 0, 0, 1, 8)
        self.memory_table = QTableWidget()
        self.memory_table.setRowCount(4096)
        self.memory_table.setColumnCount(16)
        self.initialize_column_header()
        self.initialize_row_header()
        self.initialize_data()
        self.layout.addWidget(self.memory_table, 1, 0, 8, 8)

    def initialize_column_header(self):
        header_list = []
        for i in range(self.memory_table.columnCount()):
            header_list.append(str(hex(i)))
        self.memory_table.setHorizontalHeaderLabels(header_list)

    def initialize_row_header(self):
        header_list = []
        for i in range(self.memory_table.rowCount()):
            header_list.append(str(hex(i * 16)))
        self.memory_table.setVerticalHeaderLabels(header_list)

    def initialize_data(self):
        for i in range(self.memory_table.rowCount()):
            for j in range(self.memory_table.columnCount()):
                item_to_insert = QLabel(str(hex(randrange(256))))
                self.memory_table.setCellWidget(i, j, item_to_insert)
# Cache Table class, part of the Cache Simulator
# ECE 1110 Project 2
# Christopher Luk and Dane Krall

from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
    QTableWidget,
)

class CacheTable(object):
    def __init__(self):
        self.table_window = QWidget()
        self.L1_LRU = [[-1]*1 for i in range(1)]
        self.L2_LRU = [[-1]*1 for i in range(1)]
        self.L3_LRU = [[-1]*1 for i in range(1)]
        self.L4_LRU = [[-1]*1 for i in range(1)]
        self.L5_LRU = [[-1]*1 for i in range(1)]
        self.create_layout()
        self.table_window.setLayout(self.layout)

    def build_cache(self, l1_size=1, l2_size=1, l3_size=1, l4_size=1, l5_size=1, blk_size=1, sa1=1, sa2=1, sa3=1, sa4=1, sa5=1):
        self.L1.clear()
        self.L2.clear()
        self.L3.clear()
        self.L4.clear()
        self.L5.clear()
        self.L1.setRowCount(int(l1_size / blk_size))
        self.L2.setRowCount(int(l2_size / blk_size))
        self.L3.setRowCount(int(l3_size / blk_size))
        self.L4.setRowCount(int(l4_size / blk_size))
        self.L5.setRowCount(int(l5_size / blk_size))
        self.L1.setColumnCount(blk_size + 3)
        self.L2.setColumnCount(blk_size + 3)
        self.L3.setColumnCount(blk_size + 3)
        self.L4.setColumnCount(blk_size + 3)
        self.L5.setColumnCount(blk_size + 3)
        self.initialize_column_header()
        self.initialize_row_header(self.L1, sa1)
        self.initialize_row_header(self.L2, sa2)
        self.initialize_row_header(self.L3, sa3)
        self.initialize_row_header(self.L4, sa4)
        self.initialize_row_header(self.L5, sa5)
        self.L1_LRU = [[-1]*(sa1) for i in range(int(l1_size / blk_size / sa1))]
        self.L2_LRU = [[-1]*(sa2) for i in range(int(l2_size / blk_size / sa2))]
        self.L3_LRU = [[-1]*(sa3) for i in range(int(l3_size / blk_size / sa3))]
        self.L4_LRU = [[-1]*(sa4) for i in range(int(l4_size / blk_size / sa4))]
        self.L5_LRU = [[-1]*(sa5) for i in range(int(l5_size / blk_size / sa5))]

    def initialize_column_header(self):
        header_list = ["Valid", "Dirty", "Tag", "Cache Data"]
        self.L1.setHorizontalHeaderLabels(header_list)
        self.L2.setHorizontalHeaderLabels(header_list)
        self.L3.setHorizontalHeaderLabels(header_list)
        self.L4.setHorizontalHeaderLabels(header_list)
        self.L5.setHorizontalHeaderLabels(header_list)

    def initialize_row_header(self, cache = QTableWidget, set_associativity=1):
        header_list = []
        for i in range(cache.rowCount()):
            set_number = int(i / set_associativity)
            block_number = i % set_associativity
            header_list.append("Set " + str(set_number) + ", Block " + str(block_number))
            cache.setCellWidget(i, 0, QLabel("0"))
        cache.setVerticalHeaderLabels(header_list)

    def clear_cache(self):
        self.L1.clearContents()
        self.L2.clearContents()
        self.L3.clearContents()
        self.L4.clearContents()
        self.L5.clearContents()
        for i in range(self.L1.rowCount()):
            self.L1.setCellWidget(i, 0, QLabel("0"))
        for j in range(self.L2.rowCount()):
            self.L2.setCellWidget(j, 0, QLabel("0"))
        for k in range(self.L3.rowCount()):
            self.L3.setCellWidget(k, 0, QLabel("0"))
        for l in range(self.L4.rowCount()):
            self.L4.setCellWidget(l, 0, QLabel("0"))
        for m in range(self.L5.rowCount()):
            self.L5.setCellWidget(m, 0, QLabel("0"))

    def create_layout(self):
        self.layout = QGridLayout()

        L1_label = QLabel("L1 cache:")
        self.layout.addWidget(L1_label, 0, 0, 1, 1)
        self.L1 = QTableWidget()
        self.layout.addWidget(self.L1, 1, 0, 1, 1)
        
        L2_label = QLabel("L2 cache:")
        self.layout.addWidget(L2_label, 0, 1, 1, 1)
        self.L2 = QTableWidget()
        self.layout.addWidget(self.L2, 1, 1, 1, 1)

        L3_label = QLabel("L3 cache:")
        self.layout.addWidget(L3_label, 0, 2, 1, 1)
        self.L3 = QTableWidget()
        self.layout.addWidget(self.L3, 1, 2, 1, 1)

        L4_label = QLabel("L4 cache:")
        self.layout.addWidget(L4_label, 0, 3, 1, 1)
        self.L4 = QTableWidget()
        self.layout.addWidget(self.L4, 1, 3, 1, 1)

        L5_label = QLabel("L5 cache:")
        self.layout.addWidget(L5_label, 0, 4, 1, 1)
        self.L5 = QTableWidget()
        self.layout.addWidget(self.L5, 1, 4, 1, 1)
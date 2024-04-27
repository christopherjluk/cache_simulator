# Cache Simulator
# ECE 1110 Project 2
# Christopher Luk and Dane Krall

import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QComboBox,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableWidget,
)
from PyQt5.QtGui import QIntValidator
from cache_table import CacheTable
from memory_table import MemoryTable

class CacheSimulator(object):
    def main(self):
        app = QApplication(sys.argv)
        self.windows = QWidget()

        # Cache Hits and Cache Misses
        self.L1_hits = 0
        self.L1_misses = 0
        self.L2_hits = 0
        self.L2_misses = 0
        self.L3_hits = 0
        self.L3_misses = 0
        self.L4_hits = 0
        self.L4_misses = 0
        self.L5_hits = 0
        self.L5_misses = 0

        # Cycle Times and Latencies
        self.ind_latency = 0
        self.total_latency = 0
        self.latency_count = 0
        self.avg_latency = 0

        # Window Configuration
        self.window_config()

        # Creating the cache table
        self.cache_table = CacheTable()
        self.layout.addWidget(self.cache_table.table_window, 1, 0, 4, 5)

        # Creating the memory table
        self.memory_table = MemoryTable()
        self.layout.addWidget(self.memory_table.table_window, 1, 6, 11, 8)

        # Change in cache layer size
        self.layer_0_size_box.currentIndexChanged.connect(self.set_associativity_config)
        self.layer_1_size_box.currentIndexChanged.connect(self.set_associativity_config)
        self.layer_2_size_box.currentIndexChanged.connect(self.set_associativity_config)
        self.layer_3_size_box.currentIndexChanged.connect(self.set_associativity_config)
        self.layer_4_size_box.currentIndexChanged.connect(self.set_associativity_config)

        # Change in block size
        self.size_input.currentIndexChanged.connect(self.set_associativity_config)
        self.size_input.currentIndexChanged.connect(self.set_associativity_config)
        self.size_input.currentIndexChanged.connect(self.set_associativity_config)
        self.size_input.currentIndexChanged.connect(self.set_associativity_config)
        self.size_input.currentIndexChanged.connect(self.set_associativity_config)

        # Parameter Functions
        self.apply_button.clicked.connect(self.apply_settings)
        self.reset_button.clicked.connect(self.reset_settings)
        
        # Stream Functions
        self.reset_stream_button.clicked.connect(self.reset_stream)
        self.add_stream_button.clicked.connect(self.add_stream)

        self.windows.show()
        sys.exit(app.exec_())

    def window_config(self):
        self.windows.setWindowTitle("Cache Simulator")
        self.windows.resize(500, 500)
        self.windows.move(100, 100)
        
        self.layout = QGridLayout()

        # Title
        title_label = QLabel("ECE 1110 Cache Simulator (Christopher Luk and Dane Krall)\nUniversity of Pittsburgh: Swanson School of Engineering")
        self.layout.addWidget(title_label, 0, 0, 1, 7)
        
        # Input Stream
        input_label = QLabel("Input Stream")
        self.layout.addWidget(input_label, 1, 5, 1, 1)
        self.input_stream = QLineEdit()
        self.input_stream.setEnabled(False)
        self.layout.addWidget(self.input_stream, 2, 5, 1, 1)
        self.reset_stream_button = QPushButton("Reset Stream")
        self.reset_stream_button.setEnabled(False)
        self.add_stream_button = QPushButton("Add and Continue")
        self.add_stream_button.setEnabled(False)
        self.layout.addWidget(self.reset_stream_button, 3, 5, 1, 1)
        self.layout.addWidget(self.add_stream_button, 4, 5, 1, 1)

        # Number of cache layers
        num_layers_label = QLabel("Number of cache layers:")
        self.layout.addWidget(num_layers_label, 7, 0, 1, 1)
        self.num_layers_box = QComboBox()
        self.num_layers_box.insertItem(0, "1")
        self.num_layers_box.insertItem(1, "2")
        self.num_layers_box.insertItem(2, "3")
        self.num_layers_box.insertItem(3, "4")
        self.num_layers_box.insertItem(4, "5")
        self.layout.addWidget(self.num_layers_box, 8, 0, 1, 1)

        # Cache layer size
        layer_size_label = QLabel("Cache layer sizes:")
        self.layout.addWidget(layer_size_label, 7, 1, 1, 1)
        self.layer_0_size_box = QComboBox()
        self.layer_1_size_box = QComboBox()
        self.layer_2_size_box = QComboBox()
        self.layer_3_size_box = QComboBox()
        self.layer_4_size_box = QComboBox()
        for i in range(20):
            size_var = pow(2, i)
            self.layer_0_size_box.insertItem(i, str(size_var))
            self.layer_1_size_box.insertItem(i, str(size_var))
            self.layer_2_size_box.insertItem(i, str(size_var))
            self.layer_3_size_box.insertItem(i, str(size_var))
            self.layer_4_size_box.insertItem(i, str(size_var))
        self.layout.addWidget(self.layer_0_size_box, 8, 1, 1, 1)
        self.layout.addWidget(self.layer_1_size_box, 9, 1, 1, 1)
        self.layout.addWidget(self.layer_2_size_box, 10, 1, 1, 1)
        self.layout.addWidget(self.layer_3_size_box, 11, 1, 1, 1)
        self.layout.addWidget(self.layer_4_size_box, 12, 1, 1, 1)

        # Access Latency
        access_latency_label = QLabel("Access latencies:")
        self.layout.addWidget(access_latency_label, 7, 2, 1, 1)
        self.latency_validator = QIntValidator()
        self.latency_validator.setRange(1, 100)
        self.access_latency_input_0 = QLineEdit()
        self.layout.addWidget(self.access_latency_input_0, 8, 2, 1, 1)
        self.access_latency_input_1 = QLineEdit()
        self.layout.addWidget(self.access_latency_input_1, 9, 2, 1, 1)
        self.access_latency_input_2 = QLineEdit()
        self.layout.addWidget(self.access_latency_input_2, 10, 2, 1, 1)
        self.access_latency_input_3 = QLineEdit()
        self.layout.addWidget(self.access_latency_input_3, 11, 2, 1, 1)
        self.access_latency_input_4 = QLineEdit()
        self.layout.addWidget(self.access_latency_input_4, 12, 2, 1, 1)

        # Block Size
        self.size_input = QComboBox()
        self.size_input.insertItem(0, "1")
        self.size_input.insertItem(1, "2")
        self.size_input.insertItem(2, "4")
        self.size_input.insertItem(3, "8")
        self.size_input.insertItem(4, "16")
        self.size_input.insertItem(5, "32")
        self.size_input.insertItem(6, "64")
        size_label = QLabel("Block size:")
        self.layout.addWidget(size_label, 7, 3, 1, 1)
        self.layout.addWidget(self.size_input, 8, 3, 1, 1)

        # Set Associativity
        set_associativity_label = QLabel("Set associativities:")
        self.layout.addWidget(set_associativity_label, 7, 4, 1, 1)
        self.set_associativity_box_0 = QComboBox()
        self.set_associativity_box_0.insertItem(0, "1")
        self.layout.addWidget(self.set_associativity_box_0, 8, 4, 1, 1)
        self.set_associativity_box_1 = QComboBox()
        self.set_associativity_box_1.insertItem(0, "1")
        self.layout.addWidget(self.set_associativity_box_1, 9, 4, 1, 1)
        self.set_associativity_box_2 = QComboBox()
        self.set_associativity_box_2.insertItem(0, "1")
        self.layout.addWidget(self.set_associativity_box_2, 10, 4, 1, 1)
        self.set_associativity_box_3 = QComboBox()
        self.set_associativity_box_3.insertItem(0, "1")
        self.layout.addWidget(self.set_associativity_box_3, 11, 4, 1, 1)
        self.set_associativity_box_4 = QComboBox()
        self.set_associativity_box_4.insertItem(0, "1")
        self.layout.addWidget(self.set_associativity_box_4, 12, 4, 1, 1)

        # Write / Allocation Policy
        policy_label = QLabel("Write / allocation policy:")
        self.layout.addWidget(policy_label, 7, 5, 1, 1)
        self.policy_button = QPushButton("Write-back (unclicked)\nWrite-through (clicked)")
        self.policy_button.setCheckable(True)
        self.layout.addWidget(self.policy_button, 8, 5, 1, 1)

        # Reset and apply settings buttons
        self.reset_button = QPushButton("Reset")
        self.apply_button = QPushButton("Apply")
        self.apply_button.setEnabled(False)
        self.layout.addWidget(self.reset_button, 13, 5, 1, 1)
        self.layout.addWidget(self.apply_button, 14, 5, 1, 1)

        # Hits and misses
        self.L1_hit_table = QTableWidget()
        self.L1_hit_table.setRowCount(1)
        self.L1_hit_table.setColumnCount(2)
        self.L1_hit_table.setHorizontalHeaderLabels(["Hits", "Misses"])
        self.L1_hit_table.setVerticalHeaderLabels(["L1"])
        self.L1_hit_table.setCellWidget(0, 0, QLabel(str(self.L1_hits)))
        self.L1_hit_table.setCellWidget(0, 1, QLabel(str(self.L1_misses)))
        self.layout.addWidget(self.L1_hit_table, 5, 0, 1, 1)
        self.L2_hit_table = QTableWidget()
        self.L2_hit_table.setRowCount(1)
        self.L2_hit_table.setColumnCount(2)
        self.L2_hit_table.setHorizontalHeaderLabels(["Hits", "Misses"])
        self.L2_hit_table.setVerticalHeaderLabels(["L2"])
        self.L2_hit_table.setCellWidget(0, 0, QLabel(str(self.L2_hits)))
        self.L2_hit_table.setCellWidget(0, 1, QLabel(str(self.L2_misses)))
        self.layout.addWidget(self.L2_hit_table, 5, 1, 1, 1)
        self.L3_hit_table = QTableWidget()
        self.L3_hit_table.setRowCount(1)
        self.L3_hit_table.setColumnCount(2)
        self.L3_hit_table.setHorizontalHeaderLabels(["Hits", "Misses"])
        self.L3_hit_table.setVerticalHeaderLabels(["L3"])
        self.L3_hit_table.setCellWidget(0, 0, QLabel(str(self.L3_hits)))
        self.L3_hit_table.setCellWidget(0, 1, QLabel(str(self.L3_misses)))
        self.layout.addWidget(self.L3_hit_table, 5, 2, 1, 1)
        self.L4_hit_table = QTableWidget()
        self.L4_hit_table.setRowCount(1)
        self.L4_hit_table.setColumnCount(2)
        self.L4_hit_table.setHorizontalHeaderLabels(["Hits", "Misses"])
        self.L4_hit_table.setVerticalHeaderLabels(["L4"])
        self.L4_hit_table.setCellWidget(0, 0, QLabel(str(self.L4_hits)))
        self.L4_hit_table.setCellWidget(0, 1, QLabel(str(self.L4_misses)))
        self.layout.addWidget(self.L4_hit_table, 5, 3, 1, 1)
        self.L5_hit_table = QTableWidget()
        self.L5_hit_table.setRowCount(1)
        self.L5_hit_table.setColumnCount(2)
        self.L5_hit_table.setHorizontalHeaderLabels(["Hits", "Misses"])
        self.L5_hit_table.setVerticalHeaderLabels(["L5"])
        self.L5_hit_table.setCellWidget(0, 0, QLabel(str(self.L5_hits)))
        self.L5_hit_table.setCellWidget(0, 1, QLabel(str(self.L5_misses)))
        self.layout.addWidget(self.L5_hit_table, 5, 4, 1, 1)

        # Return cycles and latencies
        self.return_cycle = QTableWidget()
        self.return_cycle.setRowCount(1)
        self.return_cycle.setColumnCount(2)
        self.return_cycle.setHorizontalHeaderLabels(["Start Time", "Return Time"])
        self.return_cycle.setVerticalHeaderLabels(["Cycle"])
        self.return_cycle.setCellWidget(0, 0, QLabel("0"))
        self.return_cycle.setCellWidget(0, 1, QLabel("0"))
        self.layout.addWidget(self.return_cycle, 6, 1, 1, 1)
        self.latency_table = QTableWidget()
        self.latency_table.setRowCount(1)
        self.latency_table.setColumnCount(2)
        self.latency_table.setHorizontalHeaderLabels(["Individual Latency", "Average Latency"])
        self.latency_table.setVerticalHeaderLabels(["Latencies"])
        self.latency_table.setCellWidget(0, 0, QLabel(str(self.ind_latency)))
        self.latency_table.setCellWidget(0, 1, QLabel(str(self.avg_latency)))
        self.layout.addWidget(self.latency_table, 6, 3, 1, 1)

        self.windows.setLayout(self.layout)

    def set_associativity_config(self):
        for i in range(self.set_associativity_box_0.count()):
            self.set_associativity_box_0.removeItem(0)
        for i in range(self.set_associativity_box_1.count()):
            self.set_associativity_box_1.removeItem(0)
        for i in range(self.set_associativity_box_2.count()):
            self.set_associativity_box_2.removeItem(0)
        for i in range(self.set_associativity_box_3.count()):
            self.set_associativity_box_3.removeItem(0)
        for i in range(self.set_associativity_box_4.count()):
            self.set_associativity_box_4.removeItem(0)
        block_size = int(self.size_input.currentText())
        max_sa_0 = int(self.layer_0_size_box.currentText()) / block_size
        count = 0
        iter = 1
        while(iter <= max_sa_0):
            self.set_associativity_box_0.insertItem(count, str(iter))
            iter = iter * 2
            count = count + 1
        block_size = int(self.size_input.currentText())
        max_sa_1 = int(self.layer_1_size_box.currentText()) / block_size
        count = 0
        iter = 1
        while(iter <= max_sa_1):
            self.set_associativity_box_1.insertItem(count, str(iter))
            iter = iter * 2
            count = count + 1
        block_size = int(self.size_input.currentText())
        max_sa_2 = int(self.layer_2_size_box.currentText()) / block_size
        count = 0
        iter = 1
        while(iter <= max_sa_2):
            self.set_associativity_box_2.insertItem(count, str(iter))
            iter = iter * 2
            count = count + 1
        block_size = int(self.size_input.currentText())
        max_sa_3 = int(self.layer_3_size_box.currentText()) / block_size
        count = 0
        iter = 1
        while(iter <= max_sa_3):
            self.set_associativity_box_3.insertItem(count, str(iter))
            iter = iter * 2
            count = count + 1
        block_size = int(self.size_input.currentText())
        max_sa_4 = int(self.layer_4_size_box.currentText()) / block_size
        count = 0
        iter = 1
        while(iter <= max_sa_4):
            self.set_associativity_box_4.insertItem(count, str(iter))
            iter = iter * 2
            count = count + 1

    def reset_settings(self):
        self.apply_button.setEnabled(True)
        self.num_layers_box.setCurrentIndex(0)
        self.layer_0_size_box.setCurrentIndex(0)
        self.layer_1_size_box.setCurrentIndex(0)
        self.layer_2_size_box.setCurrentIndex(0)
        self.layer_3_size_box.setCurrentIndex(0)
        self.layer_4_size_box.setCurrentIndex(0)
        self.access_latency_input_0.setText("1")
        self.access_latency_input_1.setText("2")
        self.access_latency_input_2.setText("3")
        self.access_latency_input_3.setText("4")
        self.access_latency_input_4.setText("5")
        self.size_input.setCurrentIndex(0)
        self.set_associativity_box_0.setCurrentIndex(0)
        self.set_associativity_box_1.setCurrentIndex(0)
        self.set_associativity_box_2.setCurrentIndex(0)
        self.set_associativity_box_3.setCurrentIndex(0)
        self.set_associativity_box_4.setCurrentIndex(0)
        self.policy_button.setChecked(False)
        self.apply_settings()

    def apply_settings(self):
        self.input_stream.setEnabled(True)
        self.add_stream_button.setEnabled(True)
        self.reset_stream_button.setEnabled(True)
        self.num_layers = int(self.num_layers_box.currentText())
        self.layer_0_size = int(self.layer_0_size_box.currentText())
        self.layer_1_size = int(self.layer_1_size_box.currentText())
        self.layer_2_size = int(self.layer_2_size_box.currentText())
        self.layer_3_size = int(self.layer_3_size_box.currentText())
        self.layer_4_size = int(self.layer_4_size_box.currentText())
        if(self.access_latency_input_0.hasAcceptableInput()):
            self.access_latency0 = int(self.access_latency_input_0.text())
        else:
            self.access_latency_input_0.setText("1")
            self.access_latency0 = 1
        if(self.access_latency_input_1.hasAcceptableInput()):
            self.access_latency1 = int(self.access_latency_input_1.text())
        else:
            self.access_latency_input_1.setText("2")
            self.access_latency1 = 2
        if(self.access_latency_input_2.hasAcceptableInput()):
            self.access_latency2 = int(self.access_latency_input_2.text())
        else:
            self.access_latency_input_2.setText("3")
            self.access_latency2 = 3
        if(self.access_latency_input_3.hasAcceptableInput()):
            self.access_latency3 = int(self.access_latency_input_3.text())
        else:
            self.access_latency_input_3.setText("4")
            self.access_latency3 = 4
        if(self.access_latency_input_4.hasAcceptableInput()):
            self.access_latency4 = int(self.access_latency_input_4.text())
        else:
            self.access_latency_input_4.setText("5")
            self.access_latency4 = 5
        self.block_size = int(self.size_input.currentText())
        if(self.set_associativity_box_0.currentIndex() >= 0):
            self.set_associativity_0 = int(self.set_associativity_box_0.currentText())
        else:
            self.set_associativity_0 = 1
        if(self.set_associativity_box_1.currentIndex() >= 0):
            self.set_associativity_1 = int(self.set_associativity_box_1.currentText())
        else:
            self.set_associativity_1 = 1
        if(self.set_associativity_box_2.currentIndex() >= 0):
            self.set_associativity_2 = int(self.set_associativity_box_2.currentText())
        else:
            self.set_associativity_2 = 1
        if(self.set_associativity_box_3.currentIndex() >= 0):
            self.set_associativity_3 = int(self.set_associativity_box_3.currentText())
        else:
            self.set_associativity_3 = 1
        if(self.set_associativity_box_4.currentIndex() >= 0):
            self.set_associativity_4 = int(self.set_associativity_box_4.currentText())
        else:
            self.set_associativity_4 = 1
        if(self.policy_button.isChecked()):
            self.write_through = True
        else:
            self.write_through = False
        conditional_0 = ((self.layer_0_size >= self.block_size) and (int(self.layer_0_size / self.block_size) >= self.set_associativity_0))
        conditional_1 = ((self.layer_1_size >= self.block_size) and (int(self.layer_1_size / self.block_size) >= self.set_associativity_1)) or (self.num_layers < 2)
        conditional_2 = ((self.layer_2_size >= self.block_size) and (int(self.layer_2_size / self.block_size) >= self.set_associativity_2)) or (self.num_layers < 3)
        conditional_3 = ((self.layer_3_size >= self.block_size) and (int(self.layer_3_size / self.block_size) >= self.set_associativity_3)) or (self.num_layers < 4)
        conditional_4 = ((self.layer_4_size >= self.block_size) and (int(self.layer_4_size / self.block_size) >= self.set_associativity_4)) or (self.num_layers < 5)
        conditional_5 = not((self.set_associativity_0 == 0) or ((self.set_associativity_1 == 0) and (self.num_layers > 1)) or ((self.set_associativity_2 == 0) and (self.num_layers > 2)) or ((self.set_associativity_3 == 0) and (self.num_layers > 3)) or ((self.set_associativity_4 == 0) and (self.num_layers > 4)))
        conditional_6 = not(((self.layer_0_size >= self.layer_1_size) and (self.num_layers > 1)) or ((self.layer_1_size >= self.layer_2_size) and (self.num_layers > 2)) or ((self.layer_2_size >= self.layer_3_size) and (self.num_layers > 3)) or ((self.layer_3_size >= self.layer_4_size) and (self.num_layers > 4)))
        conditional_7 = not(((self.access_latency0 >= self.access_latency1) and (self.num_layers > 1)) or ((self.access_latency1 >= self.access_latency2) and (self.num_layers > 2)) or ((self.access_latency2 >= self.access_latency3) and (self.num_layers > 3)) or ((self.access_latency3 >= self.access_latency4) and (self.num_layers > 4)))
        if(conditional_0 and conditional_1 and conditional_2 and conditional_3 and conditional_4 and conditional_5 and conditional_6 and conditional_7):
            self.input_stream.setEnabled(True)
            self.add_stream_button.setEnabled(True)
            self.reset_stream_button.setEnabled(True)
        else:
            self.input_stream.setEnabled(False)
            self.reset_stream_button.setEnabled(False)
            self.add_stream_button.setEnabled(False)
        self.cache_table.build_cache(
            l1_size=self.layer_0_size,
            l2_size=self.layer_1_size,
            l3_size=self.layer_2_size,
            l4_size=self.layer_3_size,
            l5_size=self.layer_4_size,
            blk_size=self.block_size,
            sa1=self.set_associativity_0,
            sa2=self.set_associativity_1,
            sa3=self.set_associativity_2,
            sa4=self.set_associativity_3,
            sa5=self.set_associativity_4,
        )
        self.reset_stream()

    def enable_parameters(self):
        self.num_layers_box.setEnabled(True)
        self.layer_0_size_box.setEnabled(True)
        self.layer_1_size_box.setEnabled(True)
        self.layer_2_size_box.setEnabled(True)
        self.layer_3_size_box.setEnabled(True)
        self.layer_4_size_box.setEnabled(True)
        self.access_latency_input_0.setEnabled(True)
        self.access_latency_input_1.setEnabled(True)
        self.access_latency_input_2.setEnabled(True)
        self.access_latency_input_3.setEnabled(True)
        self.access_latency_input_4.setEnabled(True)
        self.size_input.setEnabled(True)
        self.set_associativity_box_0.setEnabled(True)
        self.set_associativity_box_1.setEnabled(True)
        self.set_associativity_box_2.setEnabled(True)
        self.set_associativity_box_3.setEnabled(True)
        self.set_associativity_box_4.setEnabled(True)
        self.policy_button.setEnabled(True)
        self.reset_button.setEnabled(True)
        self.apply_button.setEnabled(True)
    
    def disable_parameters(self):
        self.num_layers_box.setEnabled(False)
        self.layer_0_size_box.setEnabled(False)
        self.layer_1_size_box.setEnabled(False)
        self.layer_2_size_box.setEnabled(False)
        self.layer_3_size_box.setEnabled(False)
        self.layer_4_size_box.setEnabled(False)
        self.access_latency_input_0.setEnabled(False)
        self.access_latency_input_1.setEnabled(False)
        self.access_latency_input_2.setEnabled(False)
        self.access_latency_input_3.setEnabled(False)
        self.access_latency_input_4.setEnabled(False)
        self.size_input.setEnabled(False)
        self.set_associativity_box_0.setEnabled(False)
        self.set_associativity_box_1.setEnabled(False)
        self.set_associativity_box_2.setEnabled(False)
        self.set_associativity_box_3.setEnabled(False)
        self.set_associativity_box_4.setEnabled(False)
        self.policy_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        self.apply_button.setEnabled(False)

    def reset_stream(self):
        self.input_stream.clear()
        self.enable_parameters()
        self.L1_hits = 0
        self.L1_misses = 0
        self.L2_hits = 0
        self.L2_misses = 0
        self.L3_hits = 0
        self.L3_misses = 0
        self.L4_hits = 0
        self.L4_misses = 0
        self.L5_hits = 0
        self.L5_misses = 0
        self.L1_hit_table.setCellWidget(0, 0, QLabel(str(self.L1_hits)))
        self.L1_hit_table.setCellWidget(0, 1, QLabel(str(self.L1_misses)))
        self.L2_hit_table.setCellWidget(0, 0, QLabel(str(self.L2_hits)))
        self.L2_hit_table.setCellWidget(0, 1, QLabel(str(self.L2_misses)))
        self.L3_hit_table.setCellWidget(0, 0, QLabel(str(self.L3_hits)))
        self.L3_hit_table.setCellWidget(0, 1, QLabel(str(self.L3_misses)))
        self.L4_hit_table.setCellWidget(0, 0, QLabel(str(self.L4_hits)))
        self.L4_hit_table.setCellWidget(0, 1, QLabel(str(self.L4_misses)))
        self.L5_hit_table.setCellWidget(0, 0, QLabel(str(self.L5_hits)))
        self.L5_hit_table.setCellWidget(0, 1, QLabel(str(self.L5_misses)))
        self.cache_table.clear_cache()
        self.cache_table.L1_LRU = [[-1]*(self.set_associativity_0) for i in range(int(self.layer_0_size / self.block_size / self.set_associativity_0))]
        self.cache_table.L2_LRU = [[-1]*(self.set_associativity_1) for i in range(int(self.layer_1_size / self.block_size / self.set_associativity_1))]
        self.cache_table.L3_LRU = [[-1]*(self.set_associativity_2) for i in range(int(self.layer_2_size / self.block_size / self.set_associativity_2))]
        self.cache_table.L4_LRU = [[-1]*(self.set_associativity_3) for i in range(int(self.layer_3_size / self.block_size / self.set_associativity_3))]
        self.cache_table.L5_LRU = [[-1]*(self.set_associativity_4) for i in range(int(self.layer_4_size / self.block_size / self.set_associativity_4))]
        self.ind_latency = 0
        self.avg_latency = 0
        self.return_cycle.setCellWidget(0, 0, QLabel("0"))
        self.return_cycle.setCellWidget(0, 1, QLabel("0"))
        self.ind_latency = 0
        self.total_latency = 0
        self.latency_count = 0
        self.avg_latency = 0
        self.latency_table.setCellWidget(0, 0, QLabel(str(self.ind_latency)))
        self.latency_table.setCellWidget(0, 1, QLabel(str(self.avg_latency)))

    def add_stream(self):
        self.input_stream.setEnabled(False)
        self.disable_parameters()
        op = ((self.input_stream.text()).split(" "))[0]
        addr = int(((self.input_stream.text()).split(" "))[1])
        arr_time = int(((self.input_stream.text()).split(" "))[2])
        if(op == 'w'):
            write = int(((self.input_stream.text()).split(" "))[3])
        else:
            write = 0
        self.update_cache(op, addr, arr_time, write)
        # TODO : Print outputs
        self.input_stream.clear()
        self.input_stream.setEnabled(True)

    def update_cache(self, op='r', addr=0, arr_time=0, write=0):
        if(op == 'r'):
            self.read_cache(addr=addr, arr_time=arr_time)
        elif(op == 'w'):
            self.write_cache(addr=addr, arr_time=arr_time, write=write)

    def read_cache(self, addr=0, arr_time=0):
        read_done = False
        conditional1 = False
        conditional2 = False
        conditional3 = False
        conditional4 = False
        conditional5 = False
        for set_iter in range(int((self.layer_0_size / self.block_size) / self.set_associativity_0)):
            if(read_done):
                break
            for block_iter in range(self.set_associativity_0):
                if(set_iter == (int(addr / self.block_size) % int(self.layer_0_size / self.block_size / self.set_associativity_0))):
                    if(int(self.cache_table.L1.cellWidget((set_iter * self.set_associativity_0) + block_iter, 0).text()) == 0):
                        self.L1_misses = self.L1_misses + 1
                        self.L1_hit_table.setCellWidget(0, 1, QLabel(str(self.L1_misses)))
                        for LRU_iter in range(self.set_associativity_0):
                            if(LRU_iter == (self.set_associativity_0 - 1)):
                                self.cache_table.L1_LRU[set_iter][LRU_iter] = block_iter
                            else:
                                self.cache_table.L1_LRU[set_iter][LRU_iter] = self.cache_table.L1_LRU[set_iter][LRU_iter+1]
                        self.cache_table.L1.setCellWidget((set_iter * self.set_associativity_0) + block_iter, 0, QLabel(str(1)))
                        self.cache_table.L1.setCellWidget((set_iter * self.set_associativity_0) + block_iter, 1, QLabel(str(0)))
                        self.cache_table.L1.setCellWidget((set_iter * self.set_associativity_0) + block_iter, 2, QLabel(str(int(addr / (self.set_associativity_0 * self.block_size)))))
                        starting_addr = int(addr / self.block_size) * self.block_size
                        for data_iter in range(self.block_size):
                            dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                            self.cache_table.L1.setCellWidget((set_iter * self.set_associativity_0) + block_iter, 3 + data_iter, QLabel(dataToInsert))
                        read_done = True
                        break
                    elif(int(self.cache_table.L1.cellWidget((set_iter * self.set_associativity_0) + block_iter, 2).text()) == int(addr / (self.set_associativity_0 * self.block_size))):
                        self.L1_hits = self.L1_hits + 1
                        self.L1_hit_table.setCellWidget(0, 0, QLabel(str(self.L1_hits)))
                        conditional1 = True
                        block_out = self.cache_table.L1_LRU[set_iter].index(block_iter)
                        for LRU_iter in range(self.set_associativity_0 - block_out):
                            if(LRU_iter == (self.set_associativity_0 - block_out - 1)):
                                self.cache_table.L1_LRU[set_iter][LRU_iter + block_out] = block_iter
                            else:
                                self.cache_table.L1_LRU[set_iter][LRU_iter + block_out] = self.cache_table.L1_LRU[set_iter][LRU_iter+block_out+1]
                        read_done = True
                        break
                    elif(block_iter == (self.set_associativity_0 - 1)):
                        self.L1_misses = self.L1_misses + 1
                        self.L1_hit_table.setCellWidget(0, 1, QLabel(str(self.L1_misses)))
                        block_out = self.cache_table.L1_LRU[set_iter][0]
                        for LRU_iter in range(self.set_associativity_0):
                            if(LRU_iter == (self.set_associativity_0 - 1)):
                                self.cache_table.L1_LRU[set_iter][LRU_iter] = block_out
                            else:
                                self.cache_table.L1_LRU[set_iter][LRU_iter] = self.cache_table.L1_LRU[set_iter][LRU_iter+1]
                        tag = int(self.cache_table.L1.cellWidget((set_iter * self.set_associativity_0) + block_out, 2).text())
                        starting_mem = int(tag * (self.layer_0_size / self.set_associativity_0))
                        for memory_iter in range(self.block_size):
                            dataToMemory = self.cache_table.L1.cellWidget((set_iter * self.set_associativity_0) + block_out, 3 + memory_iter).text()
                            self.memory_table.memory_table.setCellWidget(int(starting_mem / 16), (int(starting_mem / 8) % 2) + memory_iter, QLabel(dataToMemory))
                        self.cache_table.L1.setCellWidget((set_iter * self.set_associativity_0) + block_out, 2, QLabel(str(int(addr / (self.set_associativity_0 * self.block_size)))))
                        self.cache_table.L1.setCellWidget((set_iter * self.set_associativity_0) + block_out, 1, QLabel(str(0)))
                        starting_addr = int(addr / self.block_size) * self.block_size
                        for data_iter in range(self.block_size):
                            dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                            self.cache_table.L1.setCellWidget((set_iter * self.set_associativity_0) + block_out, 3 + data_iter, QLabel(dataToInsert))
                        read_done = True
                        break
        if(self.num_layers >= 2):
            read_done = False
            for set_iter in range(int((self.layer_1_size / self.block_size) / self.set_associativity_1)):
                if(read_done):
                    break
                for block_iter in range(self.set_associativity_1):
                    if(set_iter == (int(addr / self.block_size) % int(self.layer_1_size / self.block_size / self.set_associativity_1))):
                        if(int(self.cache_table.L2.cellWidget((set_iter * self.set_associativity_1) + block_iter, 0).text()) == 0):
                            self.L2_misses = self.L2_misses + 1
                            self.L2_hit_table.setCellWidget(0, 1, QLabel(str(self.L2_misses)))
                            for LRU_iter in range(self.set_associativity_1):
                                if(LRU_iter == (self.set_associativity_1 - 1)):
                                    self.cache_table.L2_LRU[set_iter][LRU_iter] = block_iter
                                else:
                                    self.cache_table.L2_LRU[set_iter][LRU_iter] = self.cache_table.L2_LRU[set_iter][LRU_iter+1]
                            self.cache_table.L2.setCellWidget((set_iter * self.set_associativity_1) + block_iter, 0, QLabel(str(1)))
                            self.cache_table.L2.setCellWidget((set_iter * self.set_associativity_1) + block_iter, 1, QLabel(str(0)))
                            self.cache_table.L2.setCellWidget((set_iter * self.set_associativity_1) + block_iter, 2, QLabel(str(int(addr / (self.set_associativity_1 * self.block_size)))))
                            starting_addr = int(addr / self.block_size) * self.block_size
                            for data_iter in range(self.block_size):
                                dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                                self.cache_table.L2.setCellWidget((set_iter * self.set_associativity_1) + block_iter, 3 + data_iter, QLabel(dataToInsert))
                            read_done = True
                            break
                        elif(int(self.cache_table.L2.cellWidget((set_iter * self.set_associativity_1) + block_iter, 2).text()) == int(addr / (self.set_associativity_1 * self.block_size))):
                            self.L2_hits = self.L2_hits + 1
                            self.L2_hit_table.setCellWidget(0, 0, QLabel(str(self.L2_hits)))
                            conditional2 = True
                            block_out = self.cache_table.L2_LRU[set_iter].index(block_iter)
                            for LRU_iter in range(self.set_associativity_1 - block_out):
                                if(LRU_iter == (self.set_associativity_1 - block_out - 1)):
                                    self.cache_table.L2_LRU[set_iter][LRU_iter + block_out] = block_iter
                                else:
                                    self.cache_table.L2_LRU[set_iter][LRU_iter + block_out] = self.cache_table.L2_LRU[set_iter][LRU_iter+block_out+1]
                            read_done = True
                            break
                        elif(block_iter == (self.set_associativity_1 - 1)):
                            self.L2_misses = self.L2_misses + 1
                            self.L2_hit_table.setCellWidget(0, 1, QLabel(str(self.L2_misses)))
                            block_out = self.cache_table.L2_LRU[set_iter][0]
                            for LRU_iter in range(self.set_associativity_1):
                                if(LRU_iter == (self.set_associativity_1 - 1)):
                                    self.cache_table.L2_LRU[set_iter][LRU_iter] = block_out
                                else:
                                    self.cache_table.L2_LRU[set_iter][LRU_iter] = self.cache_table.L2_LRU[set_iter][LRU_iter+1]
                            tag = int(self.cache_table.L2.cellWidget((set_iter * self.set_associativity_1) + block_out, 2).text())
                            starting_mem = int(tag * (self.layer_1_size / self.set_associativity_1))
                            for memory_iter in range(self.block_size):
                                dataToMemory = self.cache_table.L2.cellWidget((set_iter * self.set_associativity_1) + block_out, 3 + memory_iter).text()
                                self.memory_table.memory_table.setCellWidget(int(starting_mem / 16), (int(starting_mem / 8) % 2) + memory_iter, QLabel(dataToMemory))
                            self.cache_table.L2.setCellWidget((set_iter * self.set_associativity_1) + block_out, 2, QLabel(str(int(addr / (self.set_associativity_1 * self.block_size)))))
                            self.cache_table.L2.setCellWidget((set_iter * self.set_associativity_1) + block_out, 1, QLabel(str(0)))
                            starting_addr = int(addr / self.block_size) * self.block_size
                            for data_iter in range(self.block_size):
                                dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                                self.cache_table.L2.setCellWidget((set_iter * self.set_associativity_1) + block_out, 3 + data_iter, QLabel(dataToInsert))
                            read_done = True
                            break
        if(self.num_layers >= 3):
            read_done = False
            for set_iter in range(int((self.layer_2_size / self.block_size) / self.set_associativity_2)):
                if(read_done):
                    break
                for block_iter in range(self.set_associativity_2):
                    if(set_iter == (int(addr / self.block_size) % int(self.layer_2_size / self.block_size / self.set_associativity_2))):
                        if(int(self.cache_table.L3.cellWidget((set_iter * self.set_associativity_2) + block_iter, 0).text()) == 0):
                            self.L3_misses = self.L3_misses + 1
                            self.L3_hit_table.setCellWidget(0, 1, QLabel(str(self.L3_misses)))
                            for LRU_iter in range(self.set_associativity_2):
                                if(LRU_iter == (self.set_associativity_2 - 1)):
                                    self.cache_table.L3_LRU[set_iter][LRU_iter] = block_iter
                                else:
                                    self.cache_table.L3_LRU[set_iter][LRU_iter] = self.cache_table.L3_LRU[set_iter][LRU_iter+1]
                            self.cache_table.L3.setCellWidget((set_iter * self.set_associativity_2) + block_iter, 0, QLabel(str(1)))
                            self.cache_table.L3.setCellWidget((set_iter * self.set_associativity_2) + block_iter, 1, QLabel(str(0)))
                            self.cache_table.L3.setCellWidget((set_iter * self.set_associativity_2) + block_iter, 2, QLabel(str(int(addr / (self.set_associativity_2 * self.block_size)))))
                            starting_addr = int(addr / self.block_size) * self.block_size
                            for data_iter in range(self.block_size):
                                dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                                self.cache_table.L3.setCellWidget((set_iter * self.set_associativity_2) + block_iter, 3 + data_iter, QLabel(dataToInsert))
                            read_done = True
                            break
                        elif(int(self.cache_table.L3.cellWidget((set_iter * self.set_associativity_2) + block_iter, 2).text()) == int(addr / (self.set_associativity_2 * self.block_size))):
                            self.L3_hits = self.L3_hits + 1
                            self.L3_hit_table.setCellWidget(0, 0, QLabel(str(self.L3_hits)))
                            conditional3 = True
                            block_out = self.cache_table.L3_LRU[set_iter].index(block_iter)
                            for LRU_iter in range(self.set_associativity_2 - block_out):
                                if(LRU_iter == (self.set_associativity_2 - block_out - 1)):
                                    self.cache_table.L3_LRU[set_iter][LRU_iter + block_out] = block_iter
                                else:
                                    self.cache_table.L3_LRU[set_iter][LRU_iter + block_out] = self.cache_table.L3_LRU[set_iter][LRU_iter+block_out+1]
                            read_done = True
                            break
                        elif(block_iter == (self.set_associativity_2 - 1)):
                            self.L3_misses = self.L3_misses + 1
                            self.L3_hit_table.setCellWidget(0, 1, QLabel(str(self.L3_misses)))
                            block_out = self.cache_table.L3_LRU[set_iter][0]
                            for LRU_iter in range(self.set_associativity_2):
                                if(LRU_iter == (self.set_associativity_2 - 1)):
                                    self.cache_table.L3_LRU[set_iter][LRU_iter] = block_out
                                else:
                                    self.cache_table.L3_LRU[set_iter][LRU_iter] = self.cache_table.L3_LRU[set_iter][LRU_iter+1]
                            tag = int(self.cache_table.L3.cellWidget((set_iter * self.set_associativity_2) + block_out, 2).text())
                            starting_mem = int(tag * (self.layer_2_size / self.set_associativity_2))
                            for memory_iter in range(self.block_size):
                                dataToMemory = self.cache_table.L3.cellWidget((set_iter * self.set_associativity_2) + block_out, 3 + memory_iter).text()
                                self.memory_table.memory_table.setCellWidget(int(starting_mem / 16), (int(starting_mem / 8) % 2) + memory_iter, QLabel(dataToMemory))
                            self.cache_table.L3.setCellWidget((set_iter * self.set_associativity_2) + block_out, 2, QLabel(str(int(addr / (self.set_associativity_2 * self.block_size)))))
                            self.cache_table.L3.setCellWidget((set_iter * self.set_associativity_2) + block_out, 1, QLabel(str(0)))
                            starting_addr = int(addr / self.block_size) * self.block_size
                            for data_iter in range(self.block_size):
                                dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                                self.cache_table.L3.setCellWidget((set_iter * self.set_associativity_2) + block_out, 3 + data_iter, QLabel(dataToInsert))
                            read_done = True
                            break
        if(self.num_layers >= 4):
            read_done = False
            for set_iter in range(int((self.layer_3_size / self.block_size) / self.set_associativity_3)):
                if(read_done):
                    break
                for block_iter in range(self.set_associativity_3):
                    if(set_iter == (int(addr / self.block_size) % int(self.layer_3_size / self.block_size / self.set_associativity_3))):
                        if(int(self.cache_table.L4.cellWidget((set_iter * self.set_associativity_3) + block_iter, 0).text()) == 0):
                            self.L4_misses = self.L4_misses + 1
                            self.L4_hit_table.setCellWidget(0, 1, QLabel(str(self.L4_misses)))
                            for LRU_iter in range(self.set_associativity_3):
                                if(LRU_iter == (self.set_associativity_3 - 1)):
                                    self.cache_table.L4_LRU[set_iter][LRU_iter] = block_iter
                                else:
                                    self.cache_table.L4_LRU[set_iter][LRU_iter] = self.cache_table.L4_LRU[set_iter][LRU_iter+1]
                            self.cache_table.L4.setCellWidget((set_iter * self.set_associativity_3) + block_iter, 0, QLabel(str(1)))
                            self.cache_table.L4.setCellWidget((set_iter * self.set_associativity_3) + block_iter, 1, QLabel(str(0)))
                            self.cache_table.L4.setCellWidget((set_iter * self.set_associativity_3) + block_iter, 2, QLabel(str(int(addr / (self.set_associativity_3 * self.block_size)))))
                            starting_addr = int(addr / self.block_size) * self.block_size
                            for data_iter in range(self.block_size):
                                dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                                self.cache_table.L4.setCellWidget((set_iter * self.set_associativity_3) + block_iter, 3 + data_iter, QLabel(dataToInsert))
                            read_done = True
                            break
                        elif(int(self.cache_table.L4.cellWidget((set_iter * self.set_associativity_3) + block_iter, 2).text()) == int(addr / (self.set_associativity_3 * self.block_size))):
                            self.L4_hits = self.L4_hits + 1
                            self.L4_hit_table.setCellWidget(0, 0, QLabel(str(self.L4_hits)))
                            conditional4 = True
                            block_out = self.cache_table.L4_LRU[set_iter].index(block_iter)
                            for LRU_iter in range(self.set_associativity_3 - block_out):
                                if(LRU_iter == (self.set_associativity_3 - block_out - 1)):
                                    self.cache_table.L4_LRU[set_iter][LRU_iter + block_out] = block_iter
                                else:
                                    self.cache_table.L4_LRU[set_iter][LRU_iter + block_out] = self.cache_table.L4_LRU[set_iter][LRU_iter+block_out+1]
                            read_done = True
                            break
                        elif(block_iter == (self.set_associativity_3 - 1)):
                            self.L4_misses = self.L4_misses + 1
                            self.L4_hit_table.setCellWidget(0, 1, QLabel(str(self.L4_misses)))
                            block_out = self.cache_table.L4_LRU[set_iter][0]
                            for LRU_iter in range(self.set_associativity_3):
                                if(LRU_iter == (self.set_associativity_3 - 1)):
                                    self.cache_table.L4_LRU[set_iter][LRU_iter] = block_out
                                else:
                                    self.cache_table.L4_LRU[set_iter][LRU_iter] = self.cache_table.L4_LRU[set_iter][LRU_iter+1]
                            tag = int(self.cache_table.L4.cellWidget((set_iter * self.set_associativity_3) + block_out, 2).text())
                            starting_mem = int(tag * (self.layer_3_size / self.set_associativity_3))
                            for memory_iter in range(self.block_size):
                                dataToMemory = self.cache_table.L4.cellWidget((set_iter * self.set_associativity_3) + block_out, 3 + memory_iter).text()
                                self.memory_table.memory_table.setCellWidget(int(starting_mem / 16), (int(starting_mem / 8) % 2) + memory_iter, QLabel(dataToMemory))
                            self.cache_table.L4.setCellWidget((set_iter * self.set_associativity_3) + block_out, 2, QLabel(str(int(addr / (self.set_associativity_3 * self.block_size)))))
                            self.cache_table.L4.setCellWidget((set_iter * self.set_associativity_3) + block_out, 1, QLabel(str(0)))
                            starting_addr = int(addr / self.block_size) * self.block_size
                            for data_iter in range(self.block_size):
                                dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                                self.cache_table.L4.setCellWidget((set_iter * self.set_associativity_3) + block_out, 3 + data_iter, QLabel(dataToInsert))
                            read_done = True
                            break
        if(self.num_layers >= 5):
            read_done = False
            for set_iter in range(int((self.layer_4_size / self.block_size) / self.set_associativity_4)):
                if(read_done):
                    break
                for block_iter in range(self.set_associativity_4):
                    if(set_iter == (int(addr / self.block_size) % int(self.layer_4_size / self.block_size / self.set_associativity_4))):
                        if(int(self.cache_table.L5.cellWidget((set_iter * self.set_associativity_4) + block_iter, 0).text()) == 0):
                            self.L5_misses = self.L5_misses + 1
                            self.L5_hit_table.setCellWidget(0, 1, QLabel(str(self.L5_misses)))
                            for LRU_iter in range(self.set_associativity_4):
                                if(LRU_iter == (self.set_associativity_4 - 1)):
                                    self.cache_table.L5_LRU[set_iter][LRU_iter] = block_iter
                                else:
                                    self.cache_table.L5_LRU[set_iter][LRU_iter] = self.cache_table.L5_LRU[set_iter][LRU_iter+1]
                            self.cache_table.L5.setCellWidget((set_iter * self.set_associativity_4) + block_iter, 0, QLabel(str(1)))
                            self.cache_table.L5.setCellWidget((set_iter * self.set_associativity_4) + block_iter, 1, QLabel(str(0)))
                            self.cache_table.L5.setCellWidget((set_iter * self.set_associativity_4) + block_iter, 2, QLabel(str(int(addr / (self.set_associativity_4 * self.block_size)))))
                            starting_addr = int(addr / self.block_size) * self.block_size
                            for data_iter in range(self.block_size):
                                dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                                self.cache_table.L5.setCellWidget((set_iter * self.set_associativity_4) + block_iter, 3 + data_iter, QLabel(dataToInsert))
                            read_done = True
                            break
                        elif(int(self.cache_table.L5.cellWidget((set_iter * self.set_associativity_4) + block_iter, 2).text()) == int(addr / (self.set_associativity_4 * self.block_size))):
                            self.L5_hits = self.L5_hits + 1
                            self.L5_hit_table.setCellWidget(0, 0, QLabel(str(self.L5_hits)))
                            conditional5 = True
                            block_out = self.cache_table.L5_LRU[set_iter].index(block_iter)
                            for LRU_iter in range(self.set_associativity_4 - block_out):
                                if(LRU_iter == (self.set_associativity_4 - block_out - 1)):
                                    self.cache_table.L5_LRU[set_iter][LRU_iter + block_out] = block_iter
                                else:
                                    self.cache_table.L5_LRU[set_iter][LRU_iter + block_out] = self.cache_table.L5_LRU[set_iter][LRU_iter+block_out+1]
                            read_done = True
                            break
                        elif(block_iter == (self.set_associativity_4 - 1)):
                            self.L5_misses = self.L5_misses + 1
                            self.L5_hit_table.setCellWidget(0, 1, QLabel(str(self.L5_misses)))
                            block_out = self.cache_table.L5_LRU[set_iter][0]
                            for LRU_iter in range(self.set_associativity_4):
                                if(LRU_iter == (self.set_associativity_4 - 1)):
                                    self.cache_table.L5_LRU[set_iter][LRU_iter] = block_out
                                else:
                                    self.cache_table.L5_LRU[set_iter][LRU_iter] = self.cache_table.L5_LRU[set_iter][LRU_iter+1]
                            tag = int(self.cache_table.L5.cellWidget((set_iter * self.set_associativity_4) + block_out, 2).text())
                            starting_mem = int(tag * (self.layer_4_size / self.set_associativity_4))
                            for memory_iter in range(self.block_size):
                                dataToMemory = self.cache_table.L5.cellWidget((set_iter * self.set_associativity_4) + block_out, 3 + memory_iter).text()
                                self.memory_table.memory_table.setCellWidget(int(starting_mem / 16), (int(starting_mem / 8) % 2) + memory_iter, QLabel(dataToMemory))
                            self.cache_table.L5.setCellWidget((set_iter * self.set_associativity_4) + block_out, 2, QLabel(str(int(addr / (self.set_associativity_4 * self.block_size)))))
                            self.cache_table.L5.setCellWidget((set_iter * self.set_associativity_4) + block_out, 1, QLabel(str(0)))
                            starting_addr = int(addr / self.block_size) * self.block_size
                            for data_iter in range(self.block_size):
                                dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                                self.cache_table.L5.setCellWidget((set_iter * self.set_associativity_4) + block_out, 3 + data_iter, QLabel(dataToInsert))
                            read_done = True
                            break
        if(conditional1):
            self.ind_latency = self.access_latency0
        elif(conditional2):
            self.ind_latency = self.access_latency1
        elif(conditional3):
            self.ind_latency = self.access_latency2
        elif(conditional4):
            self.ind_latency = self.access_latency3
        elif(conditional5):
            self.ind_latency = self.access_latency4
        else:
            self.ind_latency = 100
        self.total_latency = self.total_latency + self.ind_latency
        self.latency_count = self.latency_count + 1
        self.avg_latency = self.total_latency / self.latency_count
        self.return_cycle.setCellWidget(0, 0, QLabel(str(arr_time)))
        self.return_cycle.setCellWidget(0, 1, QLabel(str(arr_time + self.ind_latency)))
        self.latency_table.setCellWidget(0, 0, QLabel(str(self.ind_latency)))
        self.latency_table.setCellWidget(0, 1, QLabel(str(self.avg_latency)))
    
    def write_cache(self, addr=0, arr_time=0, write=0):
        if(self.write_through == True):
            self.write_with_write_through(addr=addr, arr_time=arr_time, write=write)
        else:
            self.write_with_write_back(addr=addr, arr_time=arr_time, write=write)

    def write_with_write_through(self, addr=0, arr_time=0, write=0):
        conditional1 = False
        conditional2 = False
        conditional3 = False
        conditional4 = False
        conditional5 = False
        self.memory_table.memory_table.setCellWidget(int(addr / 16), addr % 16, QLabel(str(hex(write))))
        to_write = False
        for set_iter in range(int((self.layer_0_size / self.block_size) / self.set_associativity_0)):
            if(to_write):
                break
            for block_iter in range(self.set_associativity_0):
                if(set_iter == (int(addr / self.block_size) % int(self.layer_0_size / self.block_size / self.set_associativity_0))):
                    if ((self.cache_table.L1.cellWidget((set_iter * self.set_associativity_0) + block_iter, 2) is not None) and (int(self.cache_table.L1.cellWidget((set_iter * self.set_associativity_0) + block_iter, 2).text()) == int(addr / (self.set_associativity_0 * self.block_size)))):
                        conditional1 = True
                        to_write = True
                        self.cache_table.L1.setCellWidget((set_iter * self.set_associativity_0) + block_iter, 3 + (addr % self.block_size), QLabel(str(hex(write))))
                        block_out = self.cache_table.L1_LRU[set_iter].index(block_iter)
                        for LRU_iter in range(self.set_associativity_0 - block_out):
                            if(LRU_iter == (self.set_associativity_0 - block_out - 1)):
                                self.cache_table.L1_LRU[set_iter][LRU_iter + block_out] = block_iter
                            else:
                                self.cache_table.L1_LRU[set_iter][LRU_iter + block_out] = self.cache_table.L1_LRU[set_iter][LRU_iter+block_out+1]
                        self.L1_hits = self.L1_hits + 1
                        self.L1_hit_table.setCellWidget(0, 0, QLabel(str(self.L1_hits)))
        if(not to_write):
            self.L1_misses = self.L1_misses + 1
            self.L1_hit_table.setCellWidget(0, 1, QLabel(str(self.L1_misses)))
        if(self.num_layers >= 2):
            to_write = False
            for set_iter in range(int((self.layer_1_size / self.block_size) / self.set_associativity_1)):
                if(to_write):
                    break
                for block_iter in range(self.set_associativity_1):
                    if(set_iter == (int(addr / self.block_size) % int(self.layer_1_size / self.block_size / self.set_associativity_1))):
                        if ((self.cache_table.L2.cellWidget((set_iter * self.set_associativity_1) + block_iter, 2) is not None) and (int(self.cache_table.L2.cellWidget((set_iter * self.set_associativity_1) + block_iter, 2).text()) == int(addr / (self.set_associativity_1 * self.block_size)))):
                            conditional2 = True
                            to_write = True
                            self.cache_table.L2.setCellWidget((set_iter * self.set_associativity_1) + block_iter, addr % self.block_size, QLabel(str(hex(write))))
                            block_out = self.cache_table.L2_LRU[set_iter].index(block_iter)
                            for LRU_iter in range(self.set_associativity_1 - block_out):
                                if(LRU_iter == (self.set_associativity_1 - block_out - 1)):
                                    self.cache_table.L2_LRU[set_iter][LRU_iter + block_out] = block_iter
                                else:
                                    self.cache_table.L2_LRU[set_iter][LRU_iter + block_out] = self.cache_table.L2_LRU[set_iter][LRU_iter+block_out+1]    
                            self.L2_hits = self.L2_hits + 1
                            self.L2_hit_table.setCellWidget(0, 0, QLabel(str(self.L2_hits)))
            if(not to_write):
                self.L2_misses = self.L2_misses + 1
                self.L2_hit_table.setCellWidget(0, 1, QLabel(str(self.L2_misses)))
        if(self.num_layers >= 3):
            to_write = False
            for set_iter in range(int((self.layer_2_size / self.block_size) / self.set_associativity_2)):
                if(to_write):
                    break
                for block_iter in range(self.set_associativity_2):
                    if(set_iter == (int(addr / self.block_size) % int(self.layer_2_size / self.block_size / self.set_associativity_2))):
                        if ((self.cache_table.L3.cellWidget((set_iter * self.set_associativity_2) + block_iter, 2) is not None) and (int(self.cache_table.L3.cellWidget((set_iter * self.set_associativity_2) + block_iter, 2).text()) == int(addr / (self.set_associativity_2 * self.block_size)))):
                            conditional3 = True
                            to_write = True
                            self.cache_table.L3.setCellWidget((set_iter * self.set_associativity_2) + block_iter, addr % self.block_size, QLabel(str(hex(write))))
                            block_out = self.cache_table.L3_LRU[set_iter].index(block_iter)
                            for LRU_iter in range(self.set_associativity_2 - block_out):
                                if(LRU_iter == (self.set_associativity_2 - block_out - 1)):
                                    self.cache_table.L3_LRU[set_iter][LRU_iter + block_out] = block_iter
                                else:
                                    self.cache_table.L3_LRU[set_iter][LRU_iter + block_out] = self.cache_table.L3_LRU[set_iter][LRU_iter+block_out+1]
                            self.L3_hits = self.L3_hits + 1
                            self.L3_hit_table.setCellWidget(0, 0, QLabel(str(self.L3_hits)))
            if(not to_write):
                self.L3_misses = self.L3_misses + 1
                self.L3_hit_table.setCellWidget(0, 1, QLabel(str(self.L3_misses)))
        if(self.num_layers >= 4):
            to_write = False
            for set_iter in range(int((self.layer_3_size / self.block_size) / self.set_associativity_3)):
                if(to_write):
                    break
                for block_iter in range(self.set_associativity_3):
                    if(set_iter == (int(addr / self.block_size) % int(self.layer_3_size / self.block_size / self.set_associativity_3))):
                        if ((self.cache_table.L4.cellWidget((set_iter * self.set_associativity_3) + block_iter, 2) is not None) and (int(self.cache_table.L4.cellWidget((set_iter * self.set_associativity_3) + block_iter, 2).text()) == int(addr / (self.set_associativity_3 * self.block_size)))):
                            conditional4 = True
                            to_write = True
                            self.cache_table.L4.setCellWidget((set_iter * self.set_associativity_3) + block_iter, addr % self.block_size, QLabel(str(hex(write))))
                            block_out = self.cache_table.L4_LRU[set_iter].index(block_iter)
                            for LRU_iter in range(self.set_associativity_3 - block_out):
                                if(LRU_iter == (self.set_associativity_3 - block_out - 1)):
                                    self.cache_table.L4_LRU[set_iter][LRU_iter + block_out] = block_iter
                                else:
                                    self.cache_table.L4_LRU[set_iter][LRU_iter + block_out] = self.cache_table.L4_LRU[set_iter][LRU_iter+block_out+1]
                            self.L4_hits = self.L4_hits + 1
                            self.L4_hit_table.setCellWidget(0, 0, QLabel(str(self.L4_hits)))
            if(not to_write):
                self.L4_misses = self.L4_misses + 1
                self.L4_hit_table.setCellWidget(0, 1, QLabel(str(self.L4_misses)))
        if(self.num_layers >= 5):
            to_write = False
            for set_iter in range(int((self.layer_4_size / self.block_size) / self.set_associativity_4)):
                if(to_write):
                    break
                for block_iter in range(self.set_associativity_4):
                    if(set_iter == (int(addr / self.block_size) % int(self.layer_4_size / self.block_size / self.set_associativity_4))):
                        if ((self.cache_table.L5.cellWidget((set_iter * self.set_associativity_4) + block_iter, 2) is not None) and (int(self.cache_table.L5.cellWidget((set_iter * self.set_associativity_4) + block_iter, 2).text()) == int(addr / (self.set_associativity_4 * self.block_size)))):
                            conditional5 = True
                            to_write = True
                            self.cache_table.L5.setCellWidget((set_iter * self.set_associativity_4) + block_iter, addr % self.block_size, QLabel(str(hex(write))))
                            block_out = self.cache_table.L5_LRU[set_iter].index(block_iter)
                            for LRU_iter in range(self.set_associativity_4 - block_out):
                                if(LRU_iter == (self.set_associativity_4 - block_out - 1)):
                                    self.cache_table.L5_LRU[set_iter][LRU_iter + block_out] = block_iter
                                else:
                                    self.cache_table.L5_LRU[set_iter][LRU_iter + block_out] = self.cache_table.L5_LRU[set_iter][LRU_iter+block_out+1]
                            self.L5_hits = self.L5_hits + 1
                            self.L5_hit_table.setCellWidget(0, 0, QLabel(str(self.L5_hits)))
            if(not to_write):
                self.L5_misses = self.L5_misses + 1
                self.L5_hit_table.setCellWidget(0, 1, QLabel(str(self.L5_misses)))
        if(conditional1):
            self.ind_latency = self.access_latency0
        elif(conditional2):
            self.ind_latency = self.access_latency1
        elif(conditional3):
            self.ind_latency = self.access_latency2
        elif(conditional4):
            self.ind_latency = self.access_latency3
        elif(conditional5):
            self.ind_latency = self.access_latency4
        else:
            self.ind_latency = 100
        self.total_latency = self.total_latency + self.ind_latency
        self.latency_count = self.latency_count + 1
        self.avg_latency = self.total_latency / self.latency_count
        self.return_cycle.setCellWidget(0, 0, QLabel(str(arr_time)))
        self.return_cycle.setCellWidget(0, 1, QLabel(str(arr_time + self.ind_latency)))
        self.latency_table.setCellWidget(0, 0, QLabel(str(self.ind_latency)))
        self.latency_table.setCellWidget(0, 1, QLabel(str(self.avg_latency)))

    def write_with_write_back(self, addr=0, arr_time=0, write=0):
        conditional1 = False
        conditional2 = False
        conditional3 = False
        conditional4 = False
        conditional5 = False
        to_write = False
        for set_iter in range(int((self.layer_0_size / self.block_size) / self.set_associativity_0)):
            if(to_write):
                break
            for block_iter in range(self.set_associativity_0):
                if(set_iter == (int(addr / self.block_size) % int(self.layer_0_size / self.block_size / self.set_associativity_0))):
                    if(int(self.cache_table.L1.cellWidget((set_iter * self.set_associativity_0) + block_iter, 0).text()) == 0):
                        self.L1_misses = self.L1_misses + 1
                        self.L1_hit_table.setCellWidget(0, 1, QLabel(str(self.L1_misses)))
                        for LRU_iter in range(self.set_associativity_0):
                            if(LRU_iter == (self.set_associativity_0 - 1)):
                                self.cache_table.L1_LRU[set_iter][LRU_iter] = block_iter
                            else:
                                self.cache_table.L1_LRU[set_iter][LRU_iter] = self.cache_table.L1_LRU[set_iter][LRU_iter+1]
                        self.cache_table.L1.setCellWidget((set_iter * self.set_associativity_0) + block_iter, 0, QLabel(str(1)))
                        self.cache_table.L1.setCellWidget((set_iter * self.set_associativity_0) + block_iter, 1, QLabel(str(1)))
                        self.cache_table.L1.setCellWidget((set_iter * self.set_associativity_0) + block_iter, 2, QLabel(str(int(addr / (self.set_associativity_0 * self.block_size)))))
                        starting_addr = int(addr / self.block_size) * self.block_size
                        for data_iter in range(self.block_size):
                            if(data_iter == (addr % self.block_size)):
                                self.cache_table.L1.setCellWidget((set_iter * self.set_associativity_0) + block_iter, 3 + data_iter, QLabel(str(hex(write))))
                            else:
                                dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                                self.cache_table.L1.setCellWidget((set_iter * self.set_associativity_0) + block_iter, 3 + data_iter, QLabel(dataToInsert))
                        to_write = True
                        break
                    elif(int(self.cache_table.L1.cellWidget((set_iter * self.set_associativity_0) + block_iter, 2).text()) == int(addr / (self.set_associativity_0 * self.block_size))):
                        self.L1_hits = self.L1_hits + 1
                        self.L1_hit_table.setCellWidget(0, 0, QLabel(str(self.L1_hits)))
                        conditional1 = True
                        block_out = self.cache_table.L1_LRU[set_iter].index(block_iter)
                        for LRU_iter in range(self.set_associativity_0 - block_out):
                            if(LRU_iter == (self.set_associativity_0 - block_out - 1)):
                                self.cache_table.L1_LRU[set_iter][LRU_iter + block_out] = block_iter
                            else:
                                self.cache_table.L1_LRU[set_iter][LRU_iter + block_out] = self.cache_table.L1_LRU[set_iter][LRU_iter+block_out+1]
                        self.cache_table.L1.setCellWidget((set_iter * self.set_associativity_0) + block_iter, 1, QLabel(str(1)))
                        self.cache_table.L1.setCellWidget((set_iter * self.set_associativity_0) + block_iter, 3 + (addr % self.block_size), QLabel(str(hex(write))))
                        to_write = True
                        break
                    elif(block_iter == (self.set_associativity_0 - 1)):
                        self.L1_misses = self.L1_misses + 1
                        self.L1_hit_table.setCellWidget(0, 1, QLabel(str(self.L1_misses)))
                        block_out = self.cache_table.L1_LRU[set_iter][0]
                        for LRU_iter in range(self.set_associativity_0):
                            if(LRU_iter == (self.set_associativity_0 - 1)):
                                self.cache_table.L1_LRU[set_iter][LRU_iter] = block_out
                            else:
                                self.cache_table.L1_LRU[set_iter][LRU_iter] = self.cache_table.L1_LRU[set_iter][LRU_iter+1]
                        tag = int(self.cache_table.L1.cellWidget((set_iter * self.set_associativity_0) + block_out, 2).text())
                        starting_mem = int(tag * (self.layer_0_size / self.set_associativity_0))
                        for memory_iter in range(self.block_size):
                            dataToMemory = self.cache_table.L1.cellWidget((set_iter * self.set_associativity_0) + block_out, 3 + memory_iter).text()
                            self.memory_table.memory_table.setCellWidget(int(starting_mem / 16), (int(starting_mem / 8) % 2) + memory_iter, QLabel(dataToMemory))
                        self.cache_table.L1.setCellWidget((set_iter * self.set_associativity_0) + block_out, 2, QLabel(str(int(addr / (self.set_associativity_0 * self.block_size)))))
                        self.cache_table.L1.setCellWidget((set_iter * self.set_associativity_0) + block_out, 1, QLabel(str(1)))
                        starting_addr = int(addr / self.block_size) * self.block_size
                        for data_iter in range(self.block_size):
                            if(data_iter == (addr % self.block_size)):
                                self.cache_table.L1.setCellWidget((set_iter * self.set_associativity_0) + block_out, 3 + data_iter, QLabel(str(hex(write))))
                            else:
                                dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                                self.cache_table.L1.setCellWidget((set_iter * self.set_associativity_0) + block_out, 3 + data_iter, QLabel(dataToInsert))
                        to_write = True
                        break
        if(self.num_layers >= 2):
            to_write = False
            for set_iter in range(int((self.layer_1_size / self.block_size) / self.set_associativity_1)):
                if(to_write):
                    break
                for block_iter in range(self.set_associativity_1):
                    if(set_iter == (int(addr / self.block_size) % int(self.layer_1_size / self.block_size / self.set_associativity_1))):
                        if(int(self.cache_table.L2.cellWidget((set_iter * self.set_associativity_1) + block_iter, 0).text()) == 0):
                            self.L2_misses = self.L2_misses + 1
                            self.L2_hit_table.setCellWidget(0, 1, QLabel(str(self.L2_misses)))
                            for LRU_iter in range(self.set_associativity_1):
                                if(LRU_iter == (self.set_associativity_1 - 1)):
                                    self.cache_table.L2_LRU[set_iter][LRU_iter] = block_iter
                                else:
                                    self.cache_table.L2_LRU[set_iter][LRU_iter] = self.cache_table.L2_LRU[set_iter][LRU_iter+1]
                            self.cache_table.L2.setCellWidget((set_iter * self.set_associativity_1) + block_iter, 0, QLabel(str(1)))
                            self.cache_table.L2.setCellWidget((set_iter * self.set_associativity_1) + block_iter, 1, QLabel(str(1)))
                            self.cache_table.L2.setCellWidget((set_iter * self.set_associativity_1) + block_iter, 2, QLabel(str(int(addr / (self.set_associativity_1 * self.block_size)))))
                            starting_addr = int(addr / self.block_size) * self.block_size
                            for data_iter in range(self.block_size):
                                if(data_iter == (addr % self.block_size)):
                                    self.cache_table.L2.setCellWidget((set_iter * self.set_associativity_1) + block_iter, 3 + data_iter, QLabel(str(hex(write))))
                                else:
                                    dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                                    self.cache_table.L2.setCellWidget((set_iter * self.set_associativity_1) + block_iter, 3 + data_iter, QLabel(dataToInsert))
                            to_write = True
                            break
                        elif(int(self.cache_table.L2.cellWidget((set_iter * self.set_associativity_1) + block_iter, 2).text()) == int(addr / (self.set_associativity_1 * self.block_size))):
                            self.L2_hits = self.L2_hits + 1
                            self.L2_hit_table.setCellWidget(0, 0, QLabel(str(self.L2_hits)))
                            conditional2 = True
                            block_out = self.cache_table.L2_LRU[set_iter].index(block_iter)
                            for LRU_iter in range(self.set_associativity_1 - block_out):
                                if(LRU_iter == (self.set_associativity_1 - block_out - 1)):
                                    self.cache_table.L2_LRU[set_iter][LRU_iter + block_out] = block_iter
                                else:
                                    self.cache_table.L2_LRU[set_iter][LRU_iter + block_out] = self.cache_table.L2_LRU[set_iter][LRU_iter+block_out+1]
                            self.cache_table.L2.setCellWidget((set_iter * self.set_associativity_1) + block_iter, 1, QLabel(str(1)))
                            self.cache_table.L2.setCellWidget((set_iter * self.set_associativity_1) + block_iter, 3 + (addr % self.block_size), QLabel(str(hex(write))))
                            to_write = True
                            break
                        elif(block_iter == (self.set_associativity_1 - 1)):
                            self.L2_misses = self.L2_misses + 1
                            self.L2_hit_table.setCellWidget(0, 1, QLabel(str(self.L2_misses)))
                            block_out = self.cache_table.L2_LRU[set_iter][0]
                            for LRU_iter in range(self.set_associativity_1):
                                if(LRU_iter == (self.set_associativity_1 - 1)):
                                    self.cache_table.L2_LRU[set_iter][LRU_iter] = block_out
                                else:
                                    self.cache_table.L2_LRU[set_iter][LRU_iter] = self.cache_table.L2_LRU[set_iter][LRU_iter+1]
                            tag = int(self.cache_table.L2.cellWidget((set_iter * self.set_associativity_1) + block_out, 2).text())
                            starting_mem = int(tag * (self.layer_1_size / self.set_associativity_1))
                            for memory_iter in range(self.block_size):
                                dataToMemory = self.cache_table.L2.cellWidget((set_iter * self.set_associativity_1) + block_out, 3 + memory_iter).text()
                                self.memory_table.memory_table.setCellWidget(int(starting_mem / 16), (int(starting_mem / 8) % 2) + memory_iter, QLabel(dataToMemory))
                            self.cache_table.L2.setCellWidget((set_iter * self.set_associativity_1) + block_out, 2, QLabel(str(int(addr / (self.set_associativity_1 * self.block_size)))))
                            self.cache_table.L2.setCellWidget((set_iter * self.set_associativity_1) + block_out, 1, QLabel(str(1)))
                            starting_addr = int(addr / self.block_size) * self.block_size
                            for data_iter in range(self.block_size):
                                if(data_iter == (addr % self.block_size)):
                                    self.cache_table.L2.setCellWidget((set_iter * self.set_associativity_1) + block_out, 3 + data_iter, QLabel(str(hex(write))))
                                else:
                                    dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                                    self.cache_table.L2.setCellWidget((set_iter * self.set_associativity_1) + block_out, 3 + data_iter, QLabel(dataToInsert))
                            to_write = True
                            break
        if(self.num_layers >= 3):
            to_write = False
            for set_iter in range(int((self.layer_2_size / self.block_size) / self.set_associativity_2)):
                if(to_write):
                    break
                for block_iter in range(self.set_associativity_2):
                    if(set_iter == (int(addr / self.block_size) % int(self.layer_2_size / self.block_size / self.set_associativity_2))):
                        if(int(self.cache_table.L3.cellWidget((set_iter * self.set_associativity_2) + block_iter, 0).text()) == 0):
                            self.L3_misses = self.L3_misses + 1
                            self.L3_hit_table.setCellWidget(0, 1, QLabel(str(self.L3_misses)))
                            for LRU_iter in range(self.set_associativity_2):
                                if(LRU_iter == (self.set_associativity_2 - 1)):
                                    self.cache_table.L3_LRU[set_iter][LRU_iter] = block_iter
                                else:
                                    self.cache_table.L3_LRU[set_iter][LRU_iter] = self.cache_table.L3_LRU[set_iter][LRU_iter+1]
                            self.cache_table.L3.setCellWidget((set_iter * self.set_associativity_2) + block_iter, 0, QLabel(str(1)))
                            self.cache_table.L3.setCellWidget((set_iter * self.set_associativity_2) + block_iter, 1, QLabel(str(1)))
                            self.cache_table.L3.setCellWidget((set_iter * self.set_associativity_2) + block_iter, 2, QLabel(str(int(addr / (self.set_associativity_2 * self.block_size)))))
                            starting_addr = int(addr / self.block_size) * self.block_size
                            for data_iter in range(self.block_size):
                                if(data_iter == (addr % self.block_size)):
                                    self.cache_table.L3.setCellWidget((set_iter * self.set_associativity_2) + block_iter, 3 + data_iter, QLabel(str(hex(write))))
                                else:
                                    dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                                    self.cache_table.L3.setCellWidget((set_iter * self.set_associativity_2) + block_iter, 3 + data_iter, QLabel(dataToInsert))
                            to_write = True
                            break
                        elif(int(self.cache_table.L3.cellWidget((set_iter * self.set_associativity_2) + block_iter, 2).text()) == int(addr / (self.set_associativity_2 * self.block_size))):
                            self.L3_hits = self.L3_hits + 1
                            self.L3_hit_table.setCellWidget(0, 0, QLabel(str(self.L3_hits)))
                            conditional3 = True
                            block_out = self.cache_table.L3_LRU[set_iter].index(block_iter)
                            for LRU_iter in range(self.set_associativity_2 - block_out):
                                if(LRU_iter == (self.set_associativity_2 - block_out - 1)):
                                    self.cache_table.L3_LRU[set_iter][LRU_iter + block_out] = block_iter
                                else:
                                    self.cache_table.L3_LRU[set_iter][LRU_iter + block_out] = self.cache_table.L3_LRU[set_iter][LRU_iter+block_out+1]
                            self.cache_table.L3.setCellWidget((set_iter * self.set_associativity_2) + block_iter, 1, QLabel(str(1)))
                            self.cache_table.L3.setCellWidget((set_iter * self.set_associativity_2) + block_iter, 3 + (addr % self.block_size), QLabel(str(hex(write))))
                            to_write = True
                            break
                        elif(block_iter == (self.set_associativity_2 - 1)):
                            self.L3_misses = self.L3_misses + 1
                            self.L3_hit_table.setCellWidget(0, 1, QLabel(str(self.L3_misses)))
                            block_out = self.cache_table.L3_LRU[set_iter][0]
                            for LRU_iter in range(self.set_associativity_2):
                                if(LRU_iter == (self.set_associativity_2 - 1)):
                                    self.cache_table.L3_LRU[set_iter][LRU_iter] = block_out
                                else:
                                    self.cache_table.L3_LRU[set_iter][LRU_iter] = self.cache_table.L3_LRU[set_iter][LRU_iter+1]
                            tag = int(self.cache_table.L3.cellWidget((set_iter * self.set_associativity_2) + block_out, 2).text())
                            starting_mem = int(tag * (self.layer_2_size / self.set_associativity_2))
                            for memory_iter in range(self.block_size):
                                dataToMemory = self.cache_table.L3.cellWidget((set_iter * self.set_associativity_2) + block_out, 3 + memory_iter).text()
                                self.memory_table.memory_table.setCellWidget(int(starting_mem / 16), (int(starting_mem / 8) % 2) + memory_iter, QLabel(dataToMemory))
                            self.cache_table.L3.setCellWidget((set_iter * self.set_associativity_2) + block_out, 2, QLabel(str(int(addr / (self.set_associativity_2 * self.block_size)))))
                            self.cache_table.L3.setCellWidget((set_iter * self.set_associativity_2) + block_out, 1, QLabel(str(1)))
                            starting_addr = int(addr / self.block_size) * self.block_size
                            for data_iter in range(self.block_size):
                                if(data_iter == (addr % self.block_size)):
                                    self.cache_table.L3.setCellWidget((set_iter * self.set_associativity_2) + block_out, 3 + data_iter, QLabel(str(hex(write))))
                                else:
                                    dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                                    self.cache_table.L3.setCellWidget((set_iter * self.set_associativity_2) + block_out, 3 + data_iter, QLabel(dataToInsert))
                            to_write = True
                            break
        if(self.num_layers >= 4):
            to_write = False
            for set_iter in range(int((self.layer_3_size / self.block_size) / self.set_associativity_3)):
                if(to_write):
                    break
                for block_iter in range(self.set_associativity_3):
                    if(set_iter == (int(addr / self.block_size) % int(self.layer_3_size / self.block_size / self.set_associativity_3))):
                        if(int(self.cache_table.L4.cellWidget((set_iter * self.set_associativity_3) + block_iter, 0).text()) == 0):
                            self.L4_misses = self.L4_misses + 1
                            self.L4_hit_table.setCellWidget(0, 1, QLabel(str(self.L4_misses)))
                            for LRU_iter in range(self.set_associativity_3):
                                if(LRU_iter == (self.set_associativity_3 - 1)):
                                    self.cache_table.L4_LRU[set_iter][LRU_iter] = block_iter
                                else:
                                    self.cache_table.L4_LRU[set_iter][LRU_iter] = self.cache_table.L4_LRU[set_iter][LRU_iter+1]
                            self.cache_table.L4.setCellWidget((set_iter * self.set_associativity_3) + block_iter, 0, QLabel(str(1)))
                            self.cache_table.L4.setCellWidget((set_iter * self.set_associativity_3) + block_iter, 1, QLabel(str(1)))
                            self.cache_table.L4.setCellWidget((set_iter * self.set_associativity_3) + block_iter, 2, QLabel(str(int(addr / (self.set_associativity_3 * self.block_size)))))
                            starting_addr = int(addr / self.block_size) * self.block_size
                            for data_iter in range(self.block_size):
                                if(data_iter == (addr % self.block_size)):
                                    self.cache_table.L4.setCellWidget((set_iter * self.set_associativity_3) + block_iter, 3 + data_iter, QLabel(str(hex(write))))
                                else:
                                    dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                                    self.cache_table.L4.setCellWidget((set_iter * self.set_associativity_3) + block_iter, 3 + data_iter, QLabel(dataToInsert))
                            to_write = True
                            break
                        elif(int(self.cache_table.L4.cellWidget((set_iter * self.set_associativity_3) + block_iter, 2).text()) == int(addr / (self.set_associativity_3 * self.block_size))):
                            self.L4_hits = self.L4_hits + 1
                            self.L4_hit_table.setCellWidget(0, 0, QLabel(str(self.L4_hits)))
                            conditional4 = True
                            block_out = self.cache_table.L4_LRU[set_iter].index(block_iter)
                            for LRU_iter in range(self.set_associativity_3 - block_out):
                                if(LRU_iter == (self.set_associativity_3 - block_out - 1)):
                                    self.cache_table.L4_LRU[set_iter][LRU_iter + block_out] = block_iter
                                else:
                                    self.cache_table.L4_LRU[set_iter][LRU_iter + block_out] = self.cache_table.L4_LRU[set_iter][LRU_iter+block_out+1]
                            self.cache_table.L4.setCellWidget((set_iter * self.set_associativity_3) + block_iter, 1, QLabel(str(1)))
                            self.cache_table.L4.setCellWidget((set_iter * self.set_associativity_3) + block_iter, 3 + (addr % self.block_size), QLabel(str(hex(write))))
                            to_write = True
                            break
                        elif(block_iter == (self.set_associativity_3 - 1)):
                            self.L4_misses = self.L4_misses + 1
                            self.L4_hit_table.setCellWidget(0, 1, QLabel(str(self.L4_misses)))
                            block_out = self.cache_table.L4_LRU[set_iter][0]
                            for LRU_iter in range(self.set_associativity_3):
                                if(LRU_iter == (self.set_associativity_3 - 1)):
                                    self.cache_table.L4_LRU[set_iter][LRU_iter] = block_out
                                else:
                                    self.cache_table.L4_LRU[set_iter][LRU_iter] = self.cache_table.L4_LRU[set_iter][LRU_iter+1]
                            tag = int(self.cache_table.L4.cellWidget((set_iter * self.set_associativity_3) + block_out, 2).text())
                            starting_mem = int(tag * (self.layer_3_size / self.set_associativity_3))
                            for memory_iter in range(self.block_size):
                                dataToMemory = self.cache_table.L4.cellWidget((set_iter * self.set_associativity_3) + block_out, 3 + memory_iter).text()
                                self.memory_table.memory_table.setCellWidget(int(starting_mem / 16), (int(starting_mem / 8) % 2) + memory_iter, QLabel(dataToMemory))
                            self.cache_table.L4.setCellWidget((set_iter * self.set_associativity_3) + block_out, 2, QLabel(str(int(addr / (self.set_associativity_3 * self.block_size)))))
                            self.cache_table.L4.setCellWidget((set_iter * self.set_associativity_3) + block_out, 1, QLabel(str(1)))
                            starting_addr = int(addr / self.block_size) * self.block_size
                            for data_iter in range(self.block_size):
                                if(data_iter == (addr % self.block_size)):
                                    self.cache_table.L4.setCellWidget((set_iter * self.set_associativity_3) + block_out, 3 + data_iter, QLabel(str(hex(write))))
                                else:
                                    dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                                    self.cache_table.L4.setCellWidget((set_iter * self.set_associativity_3) + block_out, 3 + data_iter, QLabel(dataToInsert))
                            to_write = True
                            break
        if(self.num_layers >= 5):
            to_write = False
            for set_iter in range(int((self.layer_4_size / self.block_size) / self.set_associativity_4)):
                if(to_write):
                    break
                for block_iter in range(self.set_associativity_4):
                    if(set_iter == (int(addr / self.block_size) % int(self.layer_4_size / self.block_size / self.set_associativity_4))):
                        if(int(self.cache_table.L5.cellWidget((set_iter * self.set_associativity_4) + block_iter, 0).text()) == 0):
                            self.L5_misses = self.L5_misses + 1
                            self.L5_hit_table.setCellWidget(0, 1, QLabel(str(self.L5_misses)))
                            for LRU_iter in range(self.set_associativity_4):
                                if(LRU_iter == (self.set_associativity_4 - 1)):
                                    self.cache_table.L5_LRU[set_iter][LRU_iter] = block_iter
                                else:
                                    self.cache_table.L5_LRU[set_iter][LRU_iter] = self.cache_table.L5_LRU[set_iter][LRU_iter+1]
                            tag = int(self.cache_table.L5.cellWidget((set_iter * self.set_associativity_4) + block_out, 2).text())
                            starting_mem = int(tag * (self.layer_4_size / self.set_associativity_4))
                            for memory_iter in range(self.block_size):
                                dataToMemory = self.cache_table.L5.cellWidget((set_iter * self.set_associativity_4) + block_out, 3 + memory_iter).text()
                                self.memory_table.memory_table.setCellWidget(int(starting_mem / 16), (int(starting_mem / 8) % 2) + memory_iter, QLabel(dataToMemory))
                            self.cache_table.L5.setCellWidget((set_iter * self.set_associativity_4) + block_iter, 0, QLabel(str(1)))
                            self.cache_table.L5.setCellWidget((set_iter * self.set_associativity_4) + block_iter, 1, QLabel(str(1)))
                            self.cache_table.L5.setCellWidget((set_iter * self.set_associativity_4) + block_iter, 2, QLabel(str(int(addr / (self.set_associativity_4 * self.block_size)))))
                            starting_addr = int(addr / self.block_size) * self.block_size
                            for data_iter in range(self.block_size):
                                if(data_iter == (addr % self.block_size)):
                                    self.cache_table.L5.setCellWidget((set_iter * self.set_associativity_4) + block_iter, 3 + data_iter, QLabel(str(hex(write))))
                                else:
                                    dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                                    self.cache_table.L5.setCellWidget((set_iter * self.set_associativity_4) + block_iter, 3 + data_iter, QLabel(dataToInsert))
                            to_write = True
                            break
                        elif(int(self.cache_table.L5.cellWidget((set_iter * self.set_associativity_4) + block_iter, 2).text()) == int(addr / (self.set_associativity_4 * self.block_size))):
                            self.L5_hits = self.L5_hits + 1
                            self.L5_hit_table.setCellWidget(0, 0, QLabel(str(self.L5_hits)))
                            conditional5 = True
                            block_out = self.cache_table.L5_LRU[set_iter].index(block_iter)
                            for LRU_iter in range(self.set_associativity_4 - block_out):
                                if(LRU_iter == (self.set_associativity_4 - block_out - 1)):
                                    self.cache_table.L5_LRU[set_iter][LRU_iter + block_out] = block_iter
                                else:
                                    self.cache_table.L5_LRU[set_iter][LRU_iter + block_out] = self.cache_table.L5_LRU[set_iter][LRU_iter+block_out+1]
                            self.cache_table.L5.setCellWidget((set_iter * self.set_associativity_4) + block_iter, 1, QLabel(str(1)))
                            self.cache_table.L5.setCellWidget((set_iter * self.set_associativity_4) + block_iter, 3 + (addr % self.block_size), QLabel(str(hex(write))))
                            to_write = True
                            break
                        elif(block_iter == (self.set_associativity_4 - 1)):
                            self.L5_misses = self.L5_misses + 1
                            self.L5_hit_table.setCellWidget(0, 1, QLabel(str(self.L5_misses)))
                            block_out = self.cache_table.L5_LRU[set_iter][0]
                            for LRU_iter in range(self.set_associativity_4):
                                if(LRU_iter == (self.set_associativity_4 - 1)):
                                    self.cache_table.L5_LRU[set_iter][LRU_iter] = block_out
                                else:
                                    self.cache_table.L5_LRU[set_iter][LRU_iter] = self.cache_table.L5_LRU[set_iter][LRU_iter+1]
                            self.cache_table.L5.setCellWidget((set_iter * self.set_associativity_4) + block_out, 2, QLabel(str(int(addr / (self.set_associativity_4 * self.block_size)))))
                            self.cache_table.L5.setCellWidget((set_iter * self.set_associativity_4) + block_out, 1, QLabel(str(1)))
                            starting_addr = int(addr / self.block_size) * self.block_size
                            for data_iter in range(self.block_size):
                                if(data_iter == (addr % self.block_size)):
                                    self.cache_table.L5.setCellWidget((set_iter * self.set_associativity_4) + block_out, 3 + data_iter, QLabel(str(hex(write))))
                                else:
                                    dataToInsert = self.memory_table.memory_table.cellWidget(int(starting_addr / 16), (int(starting_addr / 8) % 2) + data_iter).text()
                                    self.cache_table.L5.setCellWidget((set_iter * self.set_associativity_4) + block_out, 3 + data_iter, QLabel(dataToInsert))
                            to_write = True
                            break
        if(conditional1):
            self.ind_latency = self.access_latency0
        elif(conditional2):
            self.ind_latency = self.access_latency1
        elif(conditional3):
            self.ind_latency = self.access_latency2
        elif(conditional4):
            self.ind_latency = self.access_latency3
        elif(conditional5):
            self.ind_latency = self.access_latency4
        else:
            self.ind_latency = 100
        self.total_latency = self.total_latency + self.ind_latency
        self.latency_count = self.latency_count + 1
        self.avg_latency = self.total_latency / self.latency_count
        self.return_cycle.setCellWidget(0, 0, QLabel(str(arr_time)))
        self.return_cycle.setCellWidget(0, 1, QLabel(str(arr_time + self.ind_latency)))
        self.latency_table.setCellWidget(0, 0, QLabel(str(self.ind_latency)))
        self.latency_table.setCellWidget(0, 1, QLabel(str(self.avg_latency)))

if __name__ == "__main__":
    CacheSimulator().main()
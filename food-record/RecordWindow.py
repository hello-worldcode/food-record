import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPalette, QBrush#用来显示窗口背景
from PyQt5.QtCore import pyqtSignal

class RecordWindow(QWidget):
    return_to_main_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('记录功能界面')
        self.setGeometry(720, 300,500, 500)

        layout = QVBoxLayout(self)
        label = QLabel('这是记录功能界面', self)
        layout.addWidget(label)

        back_button = QPushButton('返回', self)
        back_button.clicked.connect(self.return_to_main_signal.emit)
        layout.addWidget(back_button)
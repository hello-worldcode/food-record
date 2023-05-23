import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal
from RouletteWidget import RouletteWidget

class SelectWindow(QWidget):
    return_to_main_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('选择功能界面')
        self.setGeometry(720, 300, 500, 500)

        layout = QVBoxLayout(self)

        back_button = QPushButton('返回', self)
        back_button.clicked.connect(self.return_to_main_signal.emit)
        layout.addWidget(back_button)

        button = QPushButton('选择', self)
        button.clicked.connect(self.show_roulette)
        layout.addWidget(button)

        self.roulette_window = RouletteWidget(self)  # 创建转盘窗口，并将选择窗口作为父窗口
        self.roulette_window.hide()  # 隐藏转盘窗口

    def show_roulette(self):
        self.hide()  # 隐藏选择窗口
        self.roulette_window.show()  # 显示转盘窗口

    def return_to_main(self):
        self.show()  # 返回选择窗口
        self.roulette_window.hide()  # 隐藏转盘窗口

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SelectWindow()
    win.show()
    sys.exit(app.exec())

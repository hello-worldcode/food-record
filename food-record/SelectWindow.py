import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap, QPalette, QBrush#用来显示窗口背景
from RandomSelectWindow import RouletteWidget
from WinSelect import WinSelect
from PyQt5.QtCore import Qt


class SelectWindow(QWidget):
    return_to_main_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('选择功能界面')
        self.setGeometry(720, 300, 500, 500)

        layout = QVBoxLayout(self)
        background_image = QPixmap('background.jpg')
        backgroud_brush = QBrush(background_image)
        palette = self.palette()
        palette.setBrush(QPalette.Background, backgroud_brush)
        self.setPalette(palette)


        back_button = QPushButton('返回', self)
        back_button.setStyleSheet("QPushButton { font-weight: bold; font-size: 16px; padding: 5px; }")  # 设置按钮样式
        layout.addWidget(back_button, alignment=Qt.AlignTop | Qt.AlignLeft)
        back_button.clicked.connect(self.return_to_main_signal.emit)

        button = QPushButton('饭菜选择', self)
        button.clicked.connect(self.show_roulette)  # 连接到打开转盘界面的槽函数
        layout.addWidget(button)

        button1 = QPushButton('窗口选择', self)
        button1.clicked.connect(self.show_win_select)  # 连接到打开转盘界面的槽函数
        layout.addWidget(button1)


    def show_roulette(self):
        self.hide()  # 隐藏主界面
        self.roulette_window = RouletteWidget()  # 创建记录界面，并将选择窗口作为父窗口
        self.roulette_window.return_to_main_signal.connect(self.return_to_main)
        self.roulette_window.show()

    def show_win_select(self):
        self.hide()
        self.win_select=WinSelect()
        self.win_select.return_to_main_signal.connect(self.return_to_main1)
        self.win_select.show()

    def return_to_main(self):
        if self.roulette_window.isVisible():
            self.roulette_window.hide()
        self.show()  # 返回主界面

    def return_to_main1(self):
        if self.win_select.isVisible():
            self.win_select.hide()
        self.show()  # 返回主界面

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SelectWindow()
    win.show()
    sys.exit(app.exec())

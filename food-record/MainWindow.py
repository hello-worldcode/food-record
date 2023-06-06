import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPalette, QBrush#用来显示窗口背景
from PyQt5.QtCore import pyqtSignal
from SelectWindow import SelectWindow
from RecordWindow import RecordWindow


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('食记')
        self.setGeometry(720, 300, 500, 500)

        background_image = QPixmap('background.jpg')
        backgroud_brush = QBrush(background_image)
        palette = self.palette()
        palette.setBrush(QPalette.Background, backgroud_brush)
        self.setPalette(palette)

        layout = QVBoxLayout(self)
        self.label = QLabel(self)
        layout.addWidget(self.label)

        self.button = QPushButton('记录功能', self)
        self.button.clicked.connect(self.show_record_page)
        layout.addWidget(self.button)

        self.button1 = QPushButton('选择功能', self)
        self.button1.clicked.connect(self.show_select_page)
        layout.addWidget(self.button1)


        self.record_window = None
        self.select_window = None
        self.expense_records=None

    def show_record_page(self):
        self.hide()  # 隐藏主界面
        self.record_window = RecordWindow()  # 创建记录界面
        self.record_window.return_to_main_signal.connect(self.return_to_main)
        self.record_window.show()

    def show_select_page(self):
        self.hide()  # 隐藏主界面
        self.select_window = SelectWindow()  # 创建选择界面
        self.select_window.return_to_main_signal.connect(self.return_to_main)
        self.select_window.show()



    def return_to_main(self):
        if self.record_window and self.record_window.isVisible():
            self.record_window.hide()  # 隐藏记录界面
        if self.select_window and self.select_window.isVisible():
            self.select_window.hide()  # 隐藏选择界面
        self.show()  # 显示主界面


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())







import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget,QVBoxLayout
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap, QPainterPath
from PyQt5.QtCore import Qt, QPoint, QTimer, pyqtSignal


class RouletteWidget(QWidget):
    return_to_main_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setGeometry(720, 300, 500, 500)

        self.angle = 0
        self.rotation_speed = 5
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_rotation)
        self.start_button.setGeometry(170, 450, 100, 30)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_rotation)
        self.stop_button.setGeometry(250, 450, 100, 30)

        layout = QVBoxLayout(self)
        back_button = QPushButton('back', self)
        back_button.clicked.connect(self.return_to_main_signal.emit)
        back_button.setStyleSheet("QPushButton { font-weight: bold; font-size: 16px; padding: 5px; }")  # 设置按钮样式
        layout.addWidget(back_button, alignment=Qt.AlignTop | Qt.AlignLeft)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制转盘背景
        painter.setBrush(Qt.lightGray)
        painter.drawEllipse(100, 100, 300, 300)

        # 绘制转盘标记
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        painter.drawLine(250, 100, 250, 400)
        painter.drawLine(100, 250, 400, 250)

        # 绘制转盘指针
        painter.setBrush(Qt.red)
        painter.save()
        painter.translate(250, 250)
        painter.rotate(self.angle)
        painter.drawPolygon(
            [QPoint(-10, -170), QPoint(10, -170), QPoint(0, -190)]
        )
        painter.restore()

    def rotate(self):
        self.angle += self.rotation_speed
        self.update()

    def start_rotation(self):
        self.timer.start(50)

    def stop_rotation(self):
        self.timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    roulette_widget = RouletteWidget()
    roulette_widget.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
import mysql.connector
import random
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QPalette, QBrush

class RouletteWidget(QMainWindow):
    return_to_main_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Roulette Widget")
        self.setGeometry(720, 300, 500, 500)

        background_image = QPixmap('background.jpg')
        backgroud_brush = QBrush(background_image)
        palette = self.palette()
        palette.setBrush(QPalette.Background, backgroud_brush)
        self.setPalette(palette)


        self.back_button = QPushButton('返回', self)
        self.back_button.setStyleSheet("QPushButton { font-weight: bold; font-size: 16px; padding: 5px; }")
        self.back_button.clicked.connect(self.return_to_main_signal.emit)

        self.recommend_button = QPushButton("随机推荐", self)
        self.recommend_button.setGeometry(28, 460, 440, 30)
        self.recommend_button.clicked.connect(self.random_recommendation)

        self.recommendation_label = QLabel(self)
        self.recommendation_label.setGeometry(50, 100, 300, 30)
        self.recommendation_label.setStyleSheet("QLabel { color: white; font-size: 16px; }")  # 设置文本颜色为白色和字体大小
        #self.recommendation_label.setAlignment(Qt.AlignCenter)

        # 创建数据库连接
        self.cnx = mysql.connector.connect(
            user='root',
            password='12345',
            host='localhost',
            database='dining_info',
            raise_on_warnings=True
        )

    def random_recommendation(self):
        try:
            cursor = self.cnx.cursor()
            query = "SELECT window_info FROM dining_info"
            cursor.execute(query)
            window_info_list = cursor.fetchall()
            cursor.close()

            if window_info_list:
                recommended_window_info = random.choice(window_info_list)
                self.recommendation_label.setText("推荐就餐窗口食物：" + recommended_window_info[0])
            else:
                self.recommendation_label.setText("没有就餐窗口食物数据")

        except mysql.connector.Error as err:
            print(f"数据库错误: {err}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    roulette_widget = RouletteWidget()
    roulette_widget.show()
    sys.exit(app.exec_())

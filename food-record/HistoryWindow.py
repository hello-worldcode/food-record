import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
import mysql.connector
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import warnings
from PyQt5.QtWidgets import QLabel
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


warnings.filterwarnings('ignore', category=UserWarning)



class HistoryWindow(QMainWindow):
    return_to_main_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("历史消费记录")
        self.setGeometry(720, 300, 500, 500)

        layout = QVBoxLayout(self)

        self.plot_button = QPushButton('绘制折线图', self)
        self.plot_button.clicked.connect(self.plot_chart)
        layout.addWidget(self.plot_button, alignment=Qt.AlignCenter)

        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)

        self.ax.set_xlabel('日期')
        self.ax.set_ylabel('金额')
        self.ax.set_title('一周内消费记录')
        self.ax.grid(True)

        # 创建数据库连接
        self.cnx = mysql.connector.connect(
            user='root',
            password='12345',
            host='localhost',
            database='dining_info',
            raise_on_warnings=True
        )


    def plot_chart(self):
        # 获取一周内的日期范围
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=1)

        # 查询数据库中的消费记录
        try:
            cursor = self.cnx.cursor()
            query = f"SELECT dining_date, price FROM dining_info WHERE dining_date >= '{start_date}' AND dining_date <= '{end_date}'"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()

            # 解析查询结果
            dates = []
            amounts = []
            for date, amount in results:
                dates.append(date.strftime('%Y-%m-%d'))
                amounts.append(amount)


            # 绘制折线图
            self.ax.clear()
            self.ax.plot(dates, amounts, marker='o')
            self.ax.set_xticks(dates)
            self.ax.set_xlabel('日期')
            self.ax.set_ylabel('金额')
            self.ax.set_title('一周内消费记录')
            self.ax.grid(True)
            self.canvas.draw()


        except mysql.connector.Error as err:
            print(f"数据库错误: {err}")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HistoryWindow()
    window.show()
    sys.exit(app.exec_())

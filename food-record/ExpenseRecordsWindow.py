import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from pyecharts import options as opts
from pyecharts.charts import Line, Pie, Bar
from pyecharts.globals import ThemeType
import mysql.connector


class ExpenseWindow(QWidget):
    return_to_main_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('消费记录界面')
        self.setGeometry(720, 300, 500, 500)

        self.label = QLabel(self)

        layout = QVBoxLayout(self)
        background_image = QPixmap('background.jpg')
        background_brush = QBrush(background_image)
        palette = self.palette()
        palette.setBrush(QPalette.Background, background_brush)
        self.setPalette(palette)

        back_button = QPushButton('返回', self)
        back_button.setStyleSheet("QPushButton { font-weight: bold; font-size: 16px; padding: 5px; }")
        layout.addWidget(back_button, alignment=Qt.AlignTop | Qt.AlignLeft)
        back_button.clicked.connect(self.return_to_main_signal.emit)

        self.cnx = mysql.connector.connect(
            user='root',
            password='12345',
            host='localhost',
            database='dining_info',
            raise_on_warnings=True
        )

        self.display_expense_records()
        self.display_window_visit_ratio()
        self.display_window_queue_times()

    def display_expense_records(self):
        try:
            cursor = self.cnx.cursor()
            query = "SELECT dining_date, SUM(price) FROM dining_info GROUP BY dining_date"
            cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()

            if records:
                dates = []
                prices = []
                for record in records:
                    if len(record) >= 2:
                        dates.append(record[0])
                        prices.append(record[1])

                line = (
                    Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
                    .add_xaxis(dates)
                    .add_yaxis("每天消费总额", prices)
                    .set_global_opts(title_opts=opts.TitleOpts(title="每天消费总额折线图"))
                    .render("每日消费金额记录.html")
                )

                self.label.setText("已生成消费记录")
                self.label.setGeometry(100, 200, 300, 30)
                self.label.setStyleSheet("QLabel { color: black; font-size: 20px; }")

            else:
                self.label.setText("没有消费记录")

        except mysql.connector.Error as err:
            print(f"数据库错误: {err}")

    def display_window_visit_ratio(self):
        try:
            cursor = self.cnx.cursor()
            query = "SELECT window_info, COUNT(*) FROM dining_info GROUP BY window_info"
            cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()

            if records:
                window_labels = []
                visit_counts = []
                for record in records:
                    if len(record) >= 2:
                        window_labels.append(record[0])
                        visit_counts.append(record[1])

                pie = (
                    Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
                    .add("", [list(z) for z in zip(window_labels, visit_counts)])
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
                    .render("窗口访问次数比例.html")
                )

        except mysql.connector.Error as err:
            print(f"数据库错误: {err}")

    def display_window_queue_times(self):
        try:
            cursor = self.cnx.cursor()
            query = "SELECT window_info, AVG(queue_duration) FROM dining_info GROUP BY window_info"
            cursor.execute(query)
            records = cursor.fetchall()
            cursor.close()

            if records:
                window_labels = []
                queue_times = []
                for record in records:
                    if len(record) >= 2:
                        window_labels.append(record[0])
                        queue_times.append(record[1])

                # 根据排队时长对数据进行排序
                sorted_data = sorted(zip(queue_times, window_labels))
                sorted_queue_times, sorted_window_labels = zip(*sorted_data)

                bar = (
                    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
                    .add_xaxis(sorted_window_labels)
                    .add_yaxis("平均排队时长", sorted_queue_times)
                    .set_global_opts(
                        title_opts=opts.TitleOpts(title="不同窗口平均排队时长"),
                        datazoom_opts=[opts.DataZoomOpts()],
                    )
                    .set_series_opts(label_opts=opts.LabelOpts(formatter="{c}分钟"))
                    .render("窗口平均排队时长.html")
                )

        except mysql.connector.Error as err:
            print(f"数据库错误: {err}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ExpenseWindow()
    win.show()
    sys.exit(app.exec())

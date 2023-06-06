import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QInputDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt
import mysql.connector
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from ExpenseRecordsWindow import ExpenseWindow

class RecordWindow(QWidget):
    return_to_main_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('选择功能界面')
        self.setGeometry(720, 300, 500, 500)

        background_image = QPixmap('background.jpg')
        backgroud_brush = QBrush(background_image)
        palette = self.palette()
        palette.setBrush(QPalette.Background, backgroud_brush)
        self.setPalette(palette)

        layout = QVBoxLayout(self)

        back_button = QPushButton('返回', self)
        back_button.setStyleSheet("QPushButton { font-weight: bold; font-size: 16px; padding: 5px; }")
        layout.addWidget(back_button, alignment=Qt.AlignTop | Qt.AlignLeft)
        back_button.clicked.connect(self.return_to_main_signal.emit)

        add_button = QPushButton('添加就餐信息', self)
        add_button.clicked.connect(self.add_dining_info)
        layout.addWidget(add_button)

        self.button2 = QPushButton('消费记录', self)
        self.button2.clicked.connect(self.show_expense_records)
        layout.addWidget(self.button2)


    def show_expense_records(self):
        # TODO: 添加显示消费记录的逻辑
        self.hide()
        self.expense_records_window=ExpenseWindow()
        self.expense_records_window.return_to_main_signal.connect(self.return_to_main)
        self.expense_records_window.show()

    def add_dining_info(self):
        meal_type, ok = QInputDialog.getText(self, '添加就餐信息', '请输入饭菜名称:')
        if ok and meal_type:
            queue_duration, ok = QInputDialog.getInt(self, '添加就餐信息', '请输入排队时长（分钟）:')
            if ok:
                price, ok = QInputDialog.getDouble(self, '添加就餐信息', '请输入价格:')
                if ok:
                    try:
                        cnx = mysql.connector.connect(
                            user='root',
                            password='12345',
                            host='localhost',
                            database='dining_info',
                            raise_on_warnings=True
                        )
                        cursor = cnx.cursor()

                        # 构造 SQL 插入语句
                        insert_query = "INSERT INTO dining_info (window_info, meal_type, queue_duration, price, dining_date) VALUES (%s, %s, %s, %s, CURDATE())"

                        # 获取就餐窗口信息
                        window_info, ok = QInputDialog.getText(self, '添加就餐信息', '请输入就餐窗口名称:')
                        if ok and window_info:
                            # 执行 SQL 插入操作
                            cursor.execute(insert_query, (window_info, meal_type, queue_duration, price))
                            cnx.commit()

                            QMessageBox.information(self, '添加成功', '就餐信息已成功添加到数据库！')
                        else:
                            QMessageBox.warning(self, '错误', '未提供就餐窗口信息，请重试！')

                        cursor.close()
                        cnx.close()
                    except mysql.connector.Error as err:
                        QMessageBox.critical(self, '错误', f'数据库错误: {err}')

    def return_to_main(self):
        if self.expense_records_window and self.expense_records_window.isVisible():
            self.expense_records_window.hide()
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = RecordWindow()
    win.show()
    sys.exit(app.exec())


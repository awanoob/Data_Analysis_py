import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"测试程序 - 版本 1.1.0")
        self.setGeometry(300, 300, 250, 150)

        # 显示版本号
        label = QLabel('当前版本：1.1.0', self)
        label.move(50, 50)

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = MyApp()
    sys.exit(app.exec())

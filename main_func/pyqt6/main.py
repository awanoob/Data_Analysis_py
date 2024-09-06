import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog
from ui_mainwindow import Ui_MainWindow  # 导入生成的UI类

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()  # 创建UI实例
        self.ui.setupUi(self)  # 设置UI

        # 绑定菜单动作到openFile方法
        self.ui.actiontest_file.triggered.connect(self.openFiles)
        self.ui.actiontrue_file.triggered.connect(self.openFile)

    # 定义文件打开逻辑，支持多选文件
    def openFiles(self):
        file_names, _ = QFileDialog.getOpenFileNames(self, "打开文件", "", "All Files (*)")
        if file_names:
            print(f"选择的文件路径: {file_names}")
    def openFile(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "All Files (*)")
        if file_name:
            print(f"选择的文件路径: {file_name}")



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

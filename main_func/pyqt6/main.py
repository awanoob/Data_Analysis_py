import os
import sys
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem, QComboBox, QCheckBox, QMenu
from ui_mainwindow import Ui_MainWindow  # 导入你原来的UI类

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()  # 创建UI实例
        self.ui.setupUi(self)  # 设置UI

        # 绑定菜单动作到openFile方法
        self.ui.action_file.triggered.connect(self.open_files)

        # 设置表格
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(["文件名", "文件格式", "频率", "真值文件"])

        # 启用右键菜单
        self.ui.tableWidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.tableWidget.customContextMenuRequested.connect(self.show_context_menu)

        self.file_data = []  # 用于存储文件数据

    def open_files(self):
        filepaths, _ = QFileDialog.getOpenFileNames(self, "打开文件", "", "All Files (*)")
        if filepaths:
            self.display_file_paths(filepaths, is_true_value=False)


    def display_file_paths(self, file_paths, is_true_value):
        for file_path in file_paths:
            row_position = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row_position)

            # 文件名
            self.ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(os.path.basename(file_path)))

            # 文件格式
            format_combo = QComboBox()
            format_combo.addItems(["navplot", "GPCHC"])
            self.ui.tableWidget.setCellWidget(row_position, 1, format_combo)

            # 频率
            freq_combo = QComboBox()
            freq_combo.addItems(["1Hz", "5Hz", "20Hz", "100Hz"])
            self.ui.tableWidget.setCellWidget(row_position, 2, freq_combo)

            # 真值文件
            checkbox = QCheckBox()
            checkbox.setChecked(is_true_value)
            checkbox.setStyleSheet("margin-left:50%; margin-right:50%;")
            self.ui.tableWidget.setCellWidget(row_position, 3, checkbox)

            # 存储文件数据
            self.file_data.append({
                'path': file_path,
                'format': format_combo,
                'frequency': freq_combo,
                'is_true_value': checkbox
            })

        self.ui.tableWidget.resizeColumnsToContents()

    def show_context_menu(self, position):
        context_menu = QMenu()
        delete_action = context_menu.addAction("删除")
        action = context_menu.exec(self.ui.tableWidget.mapToGlobal(position))
        if action == delete_action:
            self.delete_selected_rows()

    def delete_selected_rows(self):
        rows = sorted(set(index.row() for index in self.ui.tableWidget.selectedIndexes()), reverse=True)
        for row in rows:
            self.ui.tableWidget.removeRow(row)
            del self.file_data[row]

    def get_file_data(self):
        data = []
        for row, file_info in enumerate(self.file_data):
            data.append({
                'path': file_info['path'],
                'format': file_info['format'].currentText(),
                'frequency': file_info['frequency'].currentText(),
                'is_true_value': file_info['is_true_value'].isChecked()
            })
        return data

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
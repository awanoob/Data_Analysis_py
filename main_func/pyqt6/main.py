import os
import sys
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem, QComboBox, QCheckBox, QMenu
from ui_mainwindow import Ui_MainWindow  # 导入你的UI类

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 绑定菜单动作
        self.ui.action_file.triggered.connect(self.open_files)

        # 设置右键菜单
        self.setup_context_menu()

        # 连接信号
        self.ui.tableWidget_2.itemChanged.connect(self.on_tableWidget_2_item_changed)
        self.ui.tableWidget.itemChanged.connect(self.on_tableWidget_item_changed)

        # 连接计算误差按钮
        self.ui.pushButton.clicked.connect(self.calculate_error)

        self.file_data = []
        self.time_data = self.get_tableWidget_2_data()

    def on_tableWidget_2_item_changed(self):
        self.time_data = self.get_tableWidget_2_data()
        print("当前tableWidget_2中的数据：", self.time_data)

    def on_tableWidget_item_changed(self):
        self.file_data = self.get_tableWidget_data()
        print("当前tableWidget中的数据：", self.file_data)

    def open_files(self):
        filepaths, _ = QFileDialog.getOpenFileNames(self, "打开文件", "", "All Files (*)")
        if filepaths:
            self.display_file_paths(filepaths, is_true_value=False)

    def display_file_paths(self, file_paths, is_true_value):
        for file_path in file_paths:
            row_position = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row_position)

            self.ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(os.path.basename(file_path)))

            format_combo = QComboBox()
            format_combo.addItems(["navplot", "GPCHC"])
            self.ui.tableWidget.setCellWidget(row_position, 1, format_combo)

            freq_combo = QComboBox()
            freq_combo.addItems(["1Hz", "5Hz", "20Hz", "100Hz"])
            self.ui.tableWidget.setCellWidget(row_position, 2, freq_combo)

            checkbox = QCheckBox()
            checkbox.setChecked(is_true_value)
            checkbox.setStyleSheet("margin-left:50%; margin-right:50%;")
            self.ui.tableWidget.setCellWidget(row_position, 3, checkbox)

            self.file_data.append({
                'path': file_path,
                'format': format_combo,
                'frequency': freq_combo,
                'is_true_value': checkbox
            })

    def get_tableWidget_2_data(self):
        return self.get_table_data(self.ui.tableWidget_2)

    def get_tableWidget_data(self):
        return self.get_table_data(self.ui.tableWidget)

    def get_table_data(self, table_widget):
        table_data = []
        for row in range(table_widget.rowCount()):
            row_data = []
            for column in range(table_widget.columnCount()):
                cell_widget = table_widget.cellWidget(row, column)
                if isinstance(cell_widget, QComboBox):
                    row_data.append(cell_widget.currentText())
                elif isinstance(cell_widget, QCheckBox):
                    row_data.append(cell_widget.isChecked())
                else:
                    item = table_widget.item(row, column)
                    row_data.append(item.text() if item else '')
            table_data.append(row_data)
        return table_data

    def setup_context_menu(self):
        self.ui.tableWidget.customContextMenuRequested.connect(self.show_tableWidget_context_menu)
        self.ui.tableWidget_2.customContextMenuRequested.connect(self.show_tableWidget_2_context_menu)

    def show_tableWidget_context_menu(self, position):
        menu = QMenu()
        delete_action = menu.addAction("删除")
        action = menu.exec(self.ui.tableWidget.mapToGlobal(position))
        if action == delete_action:
            self.delete_selected_rows(self.ui.tableWidget)

    def show_tableWidget_2_context_menu(self, position):
        menu = QMenu()
        add_action = menu.addAction("添加行")
        delete_action = menu.addAction("删除")
        action = menu.exec(self.ui.tableWidget_2.mapToGlobal(position))
        if action == add_action:
            self.add_new_row(self.ui.tableWidget_2)
        elif action == delete_action:
            self.delete_selected_rows(self.ui.tableWidget_2)

    def delete_selected_rows(self, table_widget):
        rows = sorted(set(index.row() for index in table_widget.selectedIndexes()), reverse=True)
        for row in rows:
            table_widget.removeRow(row)
            if table_widget == self.ui.tableWidget:
                del self.file_data[row]

    def add_new_row(self, table_widget):
        row_position = table_widget.rowCount()
        table_widget.insertRow(row_position)
        for column in range(table_widget.columnCount()):
            table_widget.setItem(row_position, column, QTableWidgetItem(""))

    def calculate_error(self):
        # 这里添加计算误差的逻辑
        print("计算误差")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
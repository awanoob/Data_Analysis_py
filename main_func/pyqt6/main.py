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

        # 设置tableWidget的列数和表头
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(["文件名", "文件格式", "频率", "真值文件"])

        # 设置tableWidget_2的列数和表头
        self.ui.tableWidget_2.setColumnCount(3)
        self.ui.tableWidget_2.setHorizontalHeaderLabels(["场景", "开始时间", "结束时间"])
        self.ui.tableWidget_2.setRowCount(3)  # 初始化三行

        # 设置右键菜单
        self.setup_context_menu()

        # 允许用户直接在tableWidget_2表格中编辑数据
        self.ui.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers)

        # 当tableWidget_2的内容改变时，触发on_tableWidget_2_item_changed函数
        self.ui.tableWidget_2.itemChanged.connect(self.on_tableWidget_2_item_changed)

        # 当tableWidget的内容改变时，触发on_tableWidget_item_changed函数
        self.ui.tableWidget.itemChanged.connect(self.on_tableWidget_item_changed)

        self.file_data = []  # 用于存储文件数据

        # 打印初始的表格数据
        self.time_data = self.get_tableWidget_2_data()
        print(self.time_data)

    def on_tableWidget_2_item_changed(self):
        """当tableWidget_2的单元格内容更改时触发"""
        self.time_data = self.get_tableWidget_2_data()
        print("当前tableWidget_2中的数据：")
        for row in self.time_data:
            print(row)

    def on_tableWidget_item_changed(self):
        """当tableWidget的单元格内容更改时触发"""
        self.file_data = self.get_tableWidget_data()
        print("当前tableWidget中的数据：")
        for row in self.file_data:
            print(row)

    def open_files(self):
        filepaths, _ = QFileDialog.getOpenFileNames(self, "打开文件", "", "All Files (*)")
        if filepaths:
            self.display_file_paths(filepaths, is_true_value=False)

    def display_file_paths(self, file_paths, is_true_value):
        """这个函数用来展示表格1中的数据, 并且将数据存储到self.file_data中"""
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

    def get_tableWidget_2_data(self):
        """获取tableWidget_2的数据"""
        table_data = []
        row_count = self.ui.tableWidget_2.rowCount()
        column_count = self.ui.tableWidget_2.columnCount()

        for row in range(row_count):
            row_data = []
            for column in range(column_count):
                item = self.ui.tableWidget_2.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append('')  # 如果单元格为空，存储空字符串
            table_data.append(row_data)

        return table_data

    def get_tableWidget_data(self):
        """获取tableWidget的数据，包括QComboBox和QCheckBox的值"""
        table_data = []
        row_count = self.ui.tableWidget.rowCount()
        column_count = self.ui.tableWidget.columnCount()

        for row in range(row_count):
            row_data = []
            for column in range(column_count):
                # 检查单元格是否有小部件（例如QComboBox或QCheckBox）
                cell_widget = self.ui.tableWidget.cellWidget(row, column)

                if isinstance(cell_widget, QComboBox):  # 如果是QComboBox
                    row_data.append(cell_widget.currentText())
                elif isinstance(cell_widget, QCheckBox):  # 如果是QCheckBox
                    row_data.append(cell_widget.isChecked())
                else:
                    item = self.ui.tableWidget.item(row, column)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append('')  # 如果单元格为空，存储空字符串
            table_data.append(row_data)

        return table_data

    def setup_context_menu(self):
        # 启用右键菜单
        self.ui.tableWidget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.tableWidget_2.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)

        # 连接右键菜单请求信号到槽函数
        self.ui.tableWidget.customContextMenuRequested.connect(self.show_tableWidget_context_menu)
        self.ui.tableWidget_2.customContextMenuRequested.connect(self.show_tableWidget_2_context_menu)

    def show_tableWidget_context_menu(self, position):
        # 创建tableWidget的右键菜单
        menu = QMenu()
        delete_action = menu.addAction("删除")
        action = menu.exec(self.ui.tableWidget.mapToGlobal(position))

        if action == delete_action:
            self.delete_selected_rows(self.ui.tableWidget)

    def show_tableWidget_2_context_menu(self, position):
        # 创建tableWidget_2的右键菜单
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
        # 获取当前行数
        row_position = table_widget.rowCount()

        # 在最后一行添加新行
        table_widget.insertRow(row_position)

        if table_widget == self.ui.tableWidget_2:
            # 可选：为新行设置默认的单元格内容
            table_widget.setItem(row_position, 0, QTableWidgetItem(""))
            table_widget.setItem(row_position, 1, QTableWidgetItem(""))
            table_widget.setItem(row_position, 2, QTableWidgetItem(""))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


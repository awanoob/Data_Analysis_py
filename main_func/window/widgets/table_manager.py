# widgets/table_manager.py
from PyQt6.QtWidgets import (QTableWidgetItem, QComboBox, QMenu, QHeaderView,
                             QMessageBox, QFileDialog)
from window.widgets.custom_widgets import CenteredCheckBox
import logging
from PyQt6.QtGui import QAction


class TableManager:
    def __init__(self, main_window):
        self.main_window = main_window  # 保存主窗口引用
        self.setup_tables()
        self.setup_context_menus()
        self.file_data = []

    def setup_tables(self):
        # 使用 self.main_window.ui 来访问 UI 元素
        table1 = self.main_window.ui.tableWidget
        table2 = self.main_window.ui.tableWidget_2

        # 设置表格1的列宽
        table1.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        table1.setColumnWidth(0, 400)
        for i in range(1, 5):
            table1.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)

        # 设置表格2的列宽
        table2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def setup_context_menus(self):
        self.main_window.ui.tableWidget.customContextMenuRequested.connect(self.show_tableWidget_context_menu)
        self.main_window.ui.tableWidget_2.customContextMenuRequested.connect(self.show_tableWidget_2_context_menu)

    # # original code
    # def show_tableWidget_context_menu(self, position):
    #     menu = QMenu()
    #     delete_action = menu.addAction("删除")
    #     action = menu.exec(self.main_window.ui.tableWidget.mapToGlobal(position))
    #     if action == delete_action:
    #         self.delete_selected_rows(self.main_window.ui.tableWidget)

    # # original code
    # def show_tableWidget_2_context_menu(self, position):
    #     menu = QMenu()
    #     add_action = menu.addAction("添加行")
    #     delete_action = menu.addAction("删除")
    #     action = menu.exec(self.main_window.ui.tableWidget_2.mapToGlobal(position))
    #     if action == add_action:
    #         self.add_new_row(self.main_window.ui.tableWidget_2)
    #     elif action == delete_action:
    #         self.delete_selected_rows(self.main_window.ui.tableWidget_2)

    # # original code
    # def delete_selected_rows(self, table_widget):
    #     rows = sorted(set(index.row() for index in table_widget.selectedIndexes()), reverse=True)
    #     for row in rows:
    #         table_widget.removeRow(row)
    #         if table_widget == self.main_window.ui.tableWidget:
    #             del self.file_data[row]

    # # original code
    # def add_new_row(self, table_widget):
    #     row_position = table_widget.rowCount()
    #     table_widget.insertRow(row_position)
    #     for column in range(table_widget.columnCount()):
    #         table_widget.setItem(row_position, column, QTableWidgetItem(""))

    def create_table_controls(self, row_position, data=None):
        """创建表格控件的辅助函数"""
        table1 = self.main_window.ui.tableWidget

        if data:
            table1.setItem(row_position, 0, QTableWidgetItem(data.get('data_path', '')))
            table1.setItem(row_position, 1, QTableWidgetItem(data.get('dev_name', '')))

        # 创建格式下拉框
        format_combo = QComboBox()
        format_combo.addItems(["navplot", "GPCHC", "zqcz_agg"])
        if data and 'data_format' in data:
            index = format_combo.findText(data['data_format'])
            if index >= 0:
                format_combo.setCurrentIndex(index)
        table1.setCellWidget(row_position, 2, format_combo)

        # 创建频率下拉框
        freq_combo = QComboBox()
        freq_combo.addItems(["1Hz", "5Hz", "20Hz", "100Hz"])
        if data and 'data_frq' in data:
            index = freq_combo.findText(data['data_frq'])
            if index >= 0:
                freq_combo.setCurrentIndex(index)
        table1.setCellWidget(row_position, 3, freq_combo)

        # 创建复选框
        is_checked = False
        if data and 'is_bchmk' in data:
            is_checked = data['is_bchmk']
        centered_checkbox = CenteredCheckBox(is_checked)
        table1.setCellWidget(row_position, 4, centered_checkbox)

    def get_table1_data(self):
        """获取表格1的数据"""
        table1 = self.main_window.ui.tableWidget
        table_data = []

        for row in range(table1.rowCount()):
            table_data.append({
                'data_path': table1.item(row, 0).text(),
                'dev_name': table1.item(row, 1).text() if table1.item(row, 1) else '',
                'data_format': table1.cellWidget(row, 2).currentText(),
                'data_frq': table1.cellWidget(row, 3).currentText(),
                'is_bchmk': table1.cellWidget(row, 4).checkbox.isChecked()
            })
        return table_data

    def get_table2_data(self):
        """获取表格2的数据"""
        table2 = self.main_window.ui.tableWidget_2
        table_data = []

        for row in range(table2.rowCount()):
            table_data.append({
                'scene': table2.item(row, 0).text() if table2.item(row, 0) else '',
                'era_start': table2.item(row, 1).text() if table2.item(row, 1) else '',
                'era_end': table2.item(row, 2).text() if table2.item(row, 2) else ''
            })
        return table_data

    def add_data_files(self):
        """添加数据文件"""
        filepaths, _ = QFileDialog.getOpenFileNames(self.main_window, "打开文件", "", "All Files (*)")
        if filepaths:
            table1 = self.main_window.ui.tableWidget
            for file_path in filepaths:
                row_position = table1.rowCount()
                table1.insertRow(row_position)
                table1.setItem(row_position, 0, QTableWidgetItem(file_path))
                self.create_table_controls(row_position)

    # test for show_tableWidget_context_menu
    def show_tableWidget_context_menu(self, position):
        # 获取点击位置的单元格
        index = self.main_window.ui.tableWidget.indexAt(position)
        # 判断是否点击在表格区域内
        if index.isValid():
            # 在表格内右键点击
            self.show_table_context_menu(position, index)
        else:
            # 在表格外右键点击
            self.show_empty_space_context_menu(position)

    def show_table_context_menu(self, position, index):
        # 获取右键菜单
        menu = QMenu()

        # 添加删除选中行的菜单项
        delete_action = QAction("删除行")
        delete_action.triggered.connect(lambda: self.delete_row(index.row(), self.main_window.ui.tableWidget))
        menu.addAction(delete_action)

        # 显示菜单
        menu.exec(self.main_window.ui.tableWidget.mapToGlobal(position))

    def show_empty_space_context_menu(self, position):
        # 获取右键菜单
        menu = QMenu()

        # 删除最后一行的菜单项
        delete_last_row_action = QAction("删除行")
        delete_last_row_action.triggered.connect(lambda: self.delete_row(self.main_window.ui.tableWidget.rowCount() - 1, self.main_window.ui.tableWidget))
        menu.addAction(delete_last_row_action)

        # 显示菜单
        menu.exec(self.main_window.ui.tableWidget.mapToGlobal(position))

    # test for show_tableWidget_2_context_menu
    def show_tableWidget_2_context_menu(self, position):
        # 获取点击位置的单元格
        index = self.main_window.ui.tableWidget_2.indexAt(position)
        # 判断是否点击在表格区域内
        if index.isValid():
            # 在表格内右键点击
            self.show_table_context_menu_2(position, index)
        else:
            # 在表格外右键点击
            self.show_empty_space_context_menu_2(position)

    def show_table_context_menu_2(self, position, index):
        # 获取右键菜单
        menu = QMenu()

        # 添加删除选中行的菜单项
        delete_action = QAction("删除行")
        delete_action.triggered.connect(lambda: self.delete_row(index.row(), self.main_window.ui.tableWidget_2))
        menu.addAction(delete_action)

        # 在选中行上方添加一行的菜单项
        add_above_action = QAction("在上方插入行")
        add_above_action.triggered.connect(lambda: self.add_row(index.row(), self.main_window.ui.tableWidget_2))
        menu.addAction(add_above_action)

        # 在选中行下方添加一行的菜单项
        add_below_action = QAction("在下方插入行")
        add_below_action.triggered.connect(lambda: self.add_row(index.row() + 1, self.main_window.ui.tableWidget_2))
        menu.addAction(add_below_action)

        # 显示菜单
        menu.exec(self.main_window.ui.tableWidget_2.mapToGlobal(position))

    def show_empty_space_context_menu_2(self, position):
        # 获取右键菜单
        menu = QMenu()

        # 删除最后一行的菜单项
        delete_last_row_action = QAction("删除行")
        delete_last_row_action.triggered.connect(lambda: self.delete_row(self.main_window.ui.tableWidget_2.rowCount() - 1, self.main_window.ui.tableWidget_2))
        menu.addAction(delete_last_row_action)

        # 在最后一行下方添加一行的菜单项
        add_last_row_below_action = QAction("在下方插入行")
        add_last_row_below_action.triggered.connect(lambda: self.add_row(self.main_window.ui.tableWidget_2.rowCount(), self.main_window.ui.tableWidget_2))
        menu.addAction(add_last_row_below_action)

        # 显示菜单
        menu.exec(self.main_window.ui.tableWidget_2.mapToGlobal(position))

    # test for delete_selected_rows
    def delete_row(self, row, table_widget):
        if row >= 0:
            # 删除指定行
            table_widget.removeRow(row)
        else:
            return

    # test for add_row
    def add_row(self, row, table_widget):
        # 在指定行位置添加一行
        table_widget.insertRow(row)
        # 可以为新行填充默认数据
        for column in range(table_widget.columnCount()):
            table_widget.setItem(row, column, QTableWidgetItem(""))

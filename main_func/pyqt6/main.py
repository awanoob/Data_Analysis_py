import os
import sys
import logging
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem, QComboBox, QCheckBox, QMenu, QWidget, QHBoxLayout, \
    QHeaderView, QProgressBar
from PyQt6.QtCore import Qt
from ui_mainwindow import Ui_MainWindow
from ui_selectreport import Ui_SelectReport


class QTextEditLogger(logging.Handler):
    def __init__(self, log_text_edit):
        super().__init__()
        self.log_text_edit = log_text_edit

    def emit(self, record):
        log_message = self.format(record)
        self.log_text_edit.append(log_message)  # 在文本框中追加日志消息


class CenteredCheckBox(QWidget):
    def __init__(self, is_checked=False, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(is_checked)
        layout.addWidget(self.checkbox)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

from PyQt6.QtWidgets import QDialog

class SelectReportDialog(QDialog):
    def __init__(self, parent=None):
        super(SelectReportDialog, self).__init__(parent)
        self.ui = Ui_SelectReport()  # 这里实例化的是 Ui_SelectReport
        self.ui.setupUi(self)  # 使用 setupUi 来加载设计的界面布局

def open_select_report_dialog(self):
    dialog = SelectReportDialog(self)  # 创建 SelectReportDialog 实例
    dialog.exec()  # 以模态方式打开子界面




class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 加载样式表
        self.load_stylesheet()

        # 初始化日志处理器
        self.setup_logging()

        # 绑定菜单动作
        self.ui.action_open.triggered.connect(self.open_files)

        # 设置右键菜单
        self.setup_context_menu()

        # 绑定生成报告动作
        self.ui.action_generate_report.triggered.connect(self.open_select_report_dialog)

        # 连接信号
        self.ui.tableWidget_2.itemChanged.connect(self.on_tableWidget_2_item_changed)
        self.ui.tableWidget.itemChanged.connect(self.on_tableWidget_item_changed)

        # 设置表格的列宽
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # 连接计算误差按钮
        self.ui.pushButton.clicked.connect(self.calculate_error_with_progress)

        self.file_data = []
        self.time_data = self.get_tableWidget_2_data()

    def open_select_report_dialog(self):
        dialog = SelectReportDialog(self)  # 实例化子界面
        dialog.exec()  # 显示子界面

    def load_stylesheet(self):
        """加载样式表"""
        with open('qt6_style.qss', 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def setup_logging(self):
        """设置日志记录器，将日志输出到 logTextEdit"""
        text_edit_logger = QTextEditLogger(self.ui.logTextEdit)  # 假设 logTextEdit 是你的 QTextEdit 名称
        text_edit_logger.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(text_edit_logger)  # 添加处理器到根记录器
        logging.getLogger().setLevel(logging.INFO)  # 设置日志级别

    def on_tableWidget_2_item_changed(self):
        """tableWidget_2中的数据发生变化时触发"""
        self.time_data = self.get_tableWidget_2_data()
        logging.info("当前tableWidget_2中的数据：%s", self.time_data)

    def on_tableWidget_item_changed(self):
        """tableWidget中的数据发生变化时触发"""
        self.file_data = self.get_tableWidget_data()
        logging.info("当前tableWidget中的数据：%s", self.file_data)

    def open_files(self):
        """打开文件"""
        filepaths, _ = QFileDialog.getOpenFileNames(self, "打开文件", "", "All Files (*)")
        if filepaths:
            self.display_file_paths(filepaths, is_true_value=False)

    def display_file_paths(self, file_paths, is_true_value):
        """显示文件路径，并添加到表格中"""
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

            centered_checkbox = CenteredCheckBox(is_true_value)
            self.ui.tableWidget.setCellWidget(row_position, 3, centered_checkbox)

            self.file_data.append({
                'path': file_path,
                'format': format_combo,
                'frequency': freq_combo,
                'is_true_value': centered_checkbox.checkbox
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
                elif isinstance(cell_widget, CenteredCheckBox):
                    row_data.append(cell_widget.checkbox.isChecked())
                else:
                    item = table_widget.item(row, column)
                    row_data.append(item.text() if item else '')
            table_data.append(row_data)
        return table_data

    def setup_context_menu(self):
        """设置右键菜单"""
        self.ui.tableWidget.customContextMenuRequested.connect(self.show_tableWidget_context_menu)
        self.ui.tableWidget_2.customContextMenuRequested.connect(self.show_tableWidget_2_context_menu)

    def show_tableWidget_context_menu(self, position):
        """显示右键菜单"""
        menu = QMenu()
        delete_action = menu.addAction("删除")
        action = menu.exec(self.ui.tableWidget.mapToGlobal(position))
        if action == delete_action:
            self.delete_selected_rows(self.ui.tableWidget)

    def show_tableWidget_2_context_menu(self, position):
        """显示右键菜单"""
        menu = QMenu()
        add_action = menu.addAction("添加行")
        delete_action = menu.addAction("删除")
        action = menu.exec(self.ui.tableWidget_2.mapToGlobal(position))
        if action == add_action:
            self.add_new_row(self.ui.tableWidget_2)
        elif action == delete_action:
            self.delete_selected_rows(self.ui.tableWidget_2)

    def delete_selected_rows(self, table_widget):
        """删除选中的行"""
        rows = sorted(set(index.row() for index in table_widget.selectedIndexes()), reverse=True)
        for row in rows:
            table_widget.removeRow(row)
            if table_widget == self.ui.tableWidget:
                del self.file_data[row]

    def add_new_row(self, table_widget):
        """添加新行"""
        row_position = table_widget.rowCount()
        table_widget.insertRow(row_position)
        for column in range(table_widget.columnCount()):
            table_widget.setItem(row_position, column, QTableWidgetItem(""))

    def calculate_error(self):
        # 假设这是一个计算误差的逻辑
        logging.info("开始计算误差...")
        # 计算逻辑
        error_result = "误差结果"  # 假设的结果
        logging.info("误差计算完成：%s", error_result)
        return error_result

    def calculate_error_with_progress(self):
        # 添加进度条
        progress_bar = self.ui.progressBar

        # 模拟计算过程并更新进度
        for i in range(101):
            QtCore.QThread.msleep(20)  # 模拟处理时间
            progress_bar.setValue(i)
            QtWidgets.QApplication.processEvents()

        # 完成计算
        result = self.calculate_error()
        logging.info("计算结果：%s", result)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

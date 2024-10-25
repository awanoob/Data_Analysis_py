import sys
import os
import logging
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
from ui_mainwindow import Ui_MainWindow
from ui_selectreport import Ui_SelectReport
from utils.logger import setup_logging
from utils.updater import UpdateManager
from utils.project_manager import ProjectManager
from widgets.table_manager import TableManager


class SelectReportDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SelectReportDialog, self).__init__(parent)
        self.ui = Ui_SelectReport()
        self.ui.setupUi(self)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 初始化UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.centralwidget.hide()

        # 加载样式表
        self.load_stylesheet()

        # 初始化各个管理器
        self.project_manager = ProjectManager(self)
        self.table_manager = TableManager(self)
        self.update_manager = UpdateManager(self)

        # 设置日志输出
        setup_logging(self.ui.logTextEdit)

        # 设置信号连接
        self.setup_connections()

        # 检查更新
        self.update_manager.check_for_updates()

        self.current_project_file = None
        self.unsaved_changes = None

    def load_stylesheet(self):
        # 从外部文件加载样式表
        try:
            with open('qt6_style.qss', 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            logging.error(f"加载样式表失败: {e}")

    def setup_connections(self):
        # 连接菜单动作
        self.ui.action_new_project.triggered.connect(self.project_manager.new_project)
        self.ui.action_open_project.triggered.connect(self.project_manager.open_project)
        self.ui.action_save_project.triggered.connect(self.project_manager.save_project)
        self.ui.action_add_data.triggered.connect(self.table_manager.add_data_files)
        self.ui.action_generate_report.triggered.connect(self.open_select_report_dialog)

        # 连接计算按钮
        self.ui.pushButton.clicked.connect(self.calculate_error_with_progress)


    def open_select_report_dialog(self):
        # 打开报告选择对话框
        dialog = SelectReportDialog(self)
        dialog.exec()

    def calculate_error_with_progress(self):
        """执行误差计算并显示进度"""
        # 获取当前数据
        self.project_manager.project_config['data'] = self.table_manager.get_table1_data()
        self.project_manager.project_config['era_list'] = self.table_manager.get_table2_data()

        # 保存项目
        if self.project_manager.current_project_file:
            self.project_manager.save_project()

        # 显示进度
        progress_bar = self.ui.progressBar
        for i in range(101):
            QtCore.QThread.msleep(20)
            progress_bar.setValue(i)
            QtWidgets.QApplication.processEvents()

        # 计算结果
        result = self.calculate_error()
        logging.info("计算结果：%s", result)

    def calculate_error(self):
        logging.info("开始计算误差...")
        error_result = "误差结果"  # 这里替换为实际的计算逻辑
        logging.info("误差计算完成：%s", error_result)
        return error_result

    def update_ui_from_project_config(self, project_config):
        """根据项目配置更新UI"""
        # 清空表格
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget_2.setRowCount(0)

        # 更新数据表格
        for data in project_config['data']:
            row_position = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row_position)
            self.table_manager.create_table_controls(row_position, data)

        # 更新时间段表格
        for era in project_config['era_list']:
            row_position = self.ui.tableWidget_2.rowCount()
            self.ui.tableWidget_2.insertRow(row_position)
            self.ui.tableWidget_2.setItem(row_position, 0, QtWidgets.QTableWidgetItem(era['scene']))
            self.ui.tableWidget_2.setItem(row_position, 1, QtWidgets.QTableWidgetItem(era['era_start']))
            self.ui.tableWidget_2.setItem(row_position, 2, QtWidgets.QTableWidgetItem(era['era_end']))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
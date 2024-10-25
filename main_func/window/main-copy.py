import json
import os
import sys
import logging
from urllib.parse import urlparse
import yaml
import certifi
import requests
import urllib3
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem, QComboBox, QCheckBox, QMenu, QWidget, QHBoxLayout, QHeaderView, QProgressBar, QMessageBox, QProgressDialog
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QDateTime

from ui_mainwindow import Ui_MainWindow
from ui_selectreport import Ui_SelectReport

CURRENT_VERSION = "1.0.0"  # 设置当前软件版本
GITHUB_API_URL = "https://api.github.com/repos/awanoob/Data_Analysis_py/releases/latest"  # GitHub API URL

class QTextEditLogger(logging.Handler):
    def __init__(self, log_text_edit):
        super().__init__()
        self.log_text_edit = log_text_edit

    def emit(self, record):
        log_message = self.format(record)
        self.log_text_edit.append(log_message)

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

class SelectReportDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SelectReportDialog, self).__init__(parent)
        self.ui = Ui_SelectReport()
        self.ui.setupUi(self)

class DownloadThread(QThread):
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(str)

    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path

    def run(self):
        response = requests.get(self.url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        wrote = 0

        with open(self.save_path, 'wb') as f:
            for data in response.iter_content(block_size):
                wrote += len(data)
                f.write(data)
                progress = int(100 * wrote / total_size)
                self.progress_signal.emit(progress)

        self.finished_signal.emit(self.save_path)


class MainWindow(QtWidgets.QMainWindow):
    # 项目配置定义
    project_config = {
        'path_proj': '',
        'data': [],
        'era_list': [],
        'cvrt2navplot': True,
        'out2car_coor': False,
        'era_auto_all': False,
        'output_cep': False,
        'output_fig': True,
        'output_multi_fig': True,
        'usr_def_syserr_x': -3,
        'usr_def_syserr_y': -3,
        'usr_def_syserr_z': -3,
        'usr_def_syserr_r': -3,
        'usr_def_syserr_p': -3,
        'usr_def_syserr_h': -3,
        'usr_def_syserr_list': [],
        'cal_pos_syserr': 2,
        'cal_alt_syserr': 2,
        'cal_att_syserr': 2
    }
    def __init__(self):
        super(MainWindow, self).__init__()
        self.current_project_file = None
        self.unsaved_changes = None


        # 加载 UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.centralwidget.hide()
        # 加载样式表
        self.load_stylesheet()
        # 设置日志输出
        self.setup_logging()
        # 设置项目配置
        self.setup_context_menu()
        # 设置菜单栏
        self.ui.action_new_project.triggered.connect(self.new_project)
        self.ui.action_open_project.triggered.connect(self.open_project)
        self.ui.action_save_project.triggered.connect(self.save_project)
        self.ui.action_add_data.triggered.connect(self.add_data)

        self.ui.action_generate_report.triggered.connect(self.open_select_report_dialog)
        # self.ui.tableWidget_2.itemChanged.connect(self.on_tableWidget_2_item_changed)
        # self.ui.tableWidget.itemChanged.connect(self.on_tableWidget_item_changed)

        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.ui.tableWidget.setColumnWidth(0, 400)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)



        self.ui.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.pushButton.clicked.connect(self.calculate_error_with_progress)

        self.check_for_updates()

        self.file_data = []
        # self.time_data = self.get_tableWidget_2_data()

    def load_stylesheet(self):
        # 从外部文件加载样式表
        with open('qt6_style.qss', 'r', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def setup_logging(self):
        # 将日志输出到 QTextEdit
        text_edit_logger = QTextEditLogger(self.ui.logTextEdit)
        text_edit_logger.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(text_edit_logger)
        logging.getLogger().setLevel(logging.INFO)

    def open_select_report_dialog(self):
        # 打开报告选择对话框
        dialog = SelectReportDialog(self)
        dialog.exec()

    # def on_tableWidget_item_changed(self):
    #     self.file_data = self.get_tableWidget_data()
    #     logging.info("当前tableWidget中的数据：%s", self.file_data)
    # def on_tableWidget_2_item_changed(self):
    #     self.time_data = self.get_tableWidget_2_data()
    #     logging.info("当前tableWidget_2中的数据：%s", self.time_data)

    def new_project(self):
        """新建一个项目"""
        # 检查是否有未保存的更改
        if self.check_unsaved_changes():
            reply = QMessageBox.question(
                self, "保存更改", "是否要保存当前项目的更改？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.save_project()
            elif reply == QMessageBox.StandardButton.Cancel:
                return

        # 选择保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            self, "新建项目", self.get_last_directory(), "YAML Files (*.yaml);;All Files (*)"
        )
        # 创建项目文件
        if file_path:
            if not file_path.endswith('.yaml'):
                file_path += '.yaml'
            try:
                # 创建一个空的项目配置文件

                project_config = self.project_config
                project_config['path_proj'] = file_path
                with open(file_path, 'w') as f:
                    yaml.dump(project_config, f, allow_unicode=True)

                self.ui.centralwidget.show()
                self.unsaved_changes = False  # 重置未保存标记


                self.set_last_directory(os.path.dirname(file_path))  # 保存最后的目录路径


                QMessageBox.information(self, "成功", "项目创建成功！")
                self.project_config['path_proj'] = file_path  # 记录当前项目路径
                self.update_ui_from_project_config(project_config)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"创建项目文件失败：{str(e)}")



    def open_project(self):
        """打开项目配置文件"""
        if self.check_unsaved_changes():
            reply = QMessageBox.question(
                self, "保存更改", "是否要保存当前项目的更改？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.save_project()
            elif reply == QMessageBox.StandardButton.Cancel:
                return

        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开工程", self.get_last_directory(), "YAML Files (*.yaml);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    project_config = yaml.safe_load(f)

                # 根据打开的项目文件内容更新界面状态...
                self.update_ui_from_project_config(project_config)

                self.ui.centralwidget.show()
                self.unsaved_changes = False  # 重置未保存标记
                self.set_last_directory(os.path.dirname(file_path))  # 保存最后的目录路径
            except Exception as e:
                QMessageBox.critical(self, "错误", f"打开项目文件失败：{str(e)}")

    def save_project(self):
        """保存项目配置到文件"""
        try:
            if not hasattr(self, 'current_project_file') or not self.current_project_file:
                file_path, _ = QFileDialog.getSaveFileName(
                    self, "保存项目", self.get_last_directory(), "YAML Files (*.yaml);;All Files (*)"
                )
                if file_path:
                    if not file_path.endswith('.yaml'):
                        file_path += '.yaml'
                    self.project_config['path_proj'] = file_path
                else:
                    QMessageBox.warning(self, "警告", "请先创建或打开一个项目。")
                    return

            with open(self.current_project_file, 'w') as f:
                yaml.dump(self.project_config, f, allow_unicode=True)

            QMessageBox.information(self, "成功", "项目保存成功！")
            self.unsaved_changes = False  # 重置未保存标记
            self.set_last_directory(os.path.dirname(self.current_project_file))  # 保存最后的目录路径

        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存项目文件失败：{str(e)}")

    def update_ui_from_project_config(self, project_config):
        """根据当前的项目配置更新UI控件"""
        # 清空表格
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget_2.setRowCount(0)

        # 更新数据表格
        for data in project_config['data']:
            row_position = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row_position)

            # 使用函数创建控件,并传入数据
            self.create_table_controls(row_position, data)

        # 更新时间段表格
        for era in project_config['era_list']:
            row_position = self.ui.tableWidget_2.rowCount()
            self.ui.tableWidget_2.insertRow(row_position)
            self.ui.tableWidget_2.setItem(row_position, 0, QTableWidgetItem(era['scene']))
            self.ui.tableWidget_2.setItem(row_position, 1, QTableWidgetItem(era['era_start']))
            self.ui.tableWidget_2.setItem(row_position, 2, QTableWidgetItem(era['era_end']))



        # 更新设备名称列表等其他项目配置
        # 你可以在这里根据具体的配置内容更新其他UI组件


    def check_unsaved_changes(self):
        """检查是否有未保存的更改"""
        if hasattr(self, 'unsaved_changes') and self.unsaved_changes:
            return True
        return False

    def set_last_directory(self, path):
        """保存最后访问的目录"""
        self.last_directory = path

    def get_last_directory(self):
        """获取最后访问的目录"""
        return getattr(self, 'last_directory', '')

    def add_data(self):
        """添加数据文件"""
        filepaths, _ = QFileDialog.getOpenFileNames(self, "打开文件", "", "All Files (*)")
        if filepaths:
            for file_path in filepaths:
                row_position = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(row_position)
                self.ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(file_path))
                self.create_table_controls(row_position)


    def create_table_controls(self, row_position, data=None):
        """
        创建表格控件的辅助函数

        Args:
            row_position: 行位置
            data: 可选的初始数据字典,包含格式、频率和是否为基准值的信息
        """
        # 文件路径列保持不变,使用 QTableWidgetItem
        if data:
            self.ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(data.get('data_path', '')))

        # 创建格式下拉框
        format_combo = QComboBox()
        format_combo.addItems(["navplot", "GPCHC"])
        if data and 'data_format' in data:
            index = format_combo.findText(data['data_format'])
            if index >= 0:
                format_combo.setCurrentIndex(index)
        self.ui.tableWidget.setCellWidget(row_position, 2, format_combo)

        # 创建频率下拉框
        freq_combo = QComboBox()
        freq_combo.addItems(["1Hz", "5Hz", "20Hz", "100Hz"])
        if data and 'data_frq' in data:
            index = freq_combo.findText(data['data_frq'])
            if index >= 0:
                freq_combo.setCurrentIndex(index)
        self.ui.tableWidget.setCellWidget(row_position, 3, freq_combo)

        # 创建复选框
        is_checked = False
        if data and 'is_bchmk' in data:
            is_checked = data['is_bchmk'].lower() == 'true'
        centered_checkbox = CenteredCheckBox(is_checked)
        self.ui.tableWidget.setCellWidget(row_position, 4, centered_checkbox)

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
        logging.info("开始计算误差...")
        error_result = "误差结果"
        logging.info("误差计算完成：%s", error_result)
        return error_result

    def get_table1_data(self, table_widget):
        table_data = []
        for row in range(table_widget.rowCount()):
            table_data.append({
                'data_path': table_widget.item(row, 0).text(),
                'dev_name': table_widget.item(row, 1).text(),
                'data_format': table_widget.cellWidget(row, 2).currentText(),
                'data_frq': table_widget.cellWidget(row, 3).currentText(),
                'is_bchmk': table_widget.cellWidget(row, 4).checkbox.isChecked()
            })
        return table_data

    def get_table2_data(self, table_widget):
        table_data = []
        for row in range(table_widget.rowCount()):
            table_data.append({
                'scene': table_widget.item(row, 0).text(),
                'era_start': table_widget.item(row, 1).text(),
                'era_end': table_widget.item(row, 2).text()
            })
        return table_data


    def calculate_error_with_progress(self):
        """
        获取当前界面两个表格的数据，把数据保存到.yaml文件中，然后计算误差
        """
        project_config = self.project_config
        project_config['data'] = self.get_table1_data(self.ui.tableWidget)
        project_config['era_list'] = self.get_table2_data(self.ui.tableWidget_2)
        project_config['path_proj'] = self.current_project_file

        with open(self.current_project_file, 'w') as f:
            yaml.dump(project_config, f, allow_unicode=True)

        progress_bar = self.ui.progressBar
        for i in range(101):
            QtCore.QThread.msleep(20)
            progress_bar.setValue(i)
            QtWidgets.QApplication.processEvents()

        result = self.calculate_error()
        logging.info("计算结果：%s", result)






    def get_proxy_settings(self):
        """从配置文件或环境变量中读取代理设置"""
        proxy_settings = {}
        try:
            with open('proxy_config.json', 'r') as f:
                proxy_settings = json.load(f)
        except FileNotFoundError:
            http_proxy = os.environ.get('HTTP_PROXY')
            https_proxy = os.environ.get('HTTPS_PROXY')
            if http_proxy:
                proxy_settings['http'] = http_proxy
            if https_proxy:
                proxy_settings['https'] = https_proxy
        return proxy_settings

    def check_for_updates(self):
        """检查 GitHub 上是否有新版本，支持 HTTPS 代理设置"""
        try:
            proxy_settings = self.get_proxy_settings()

            if proxy_settings and 'https' in proxy_settings:
                proxy_url = proxy_settings['https']
                proxy_parts = urlparse(proxy_url)
                proxy_host = proxy_parts.hostname
                proxy_port = proxy_parts.port

                # 创建代理管理器
                https = urllib3.ProxyManager(
                    proxy_url,
                    cert_reqs='CERT_REQUIRED',
                    ca_certs=certifi.where(),
                    server_hostname=urlparse(GITHUB_API_URL).hostname
                )
            else:
                # 如果没有代理，使用普通的 PoolManager
                https = urllib3.PoolManager(
                    cert_reqs='CERT_REQUIRED',
                    ca_certs=certifi.where()
                )

            response = https.request('GET', GITHUB_API_URL, timeout=10.0)

            if response.status == 200:
                data = json.loads(response.data.decode('utf-8'))
                latest_version = data["tag_name"]
                if self.is_new_version(latest_version):
                    self.prompt_update(latest_version)
                else:
                    logging.info("当前版本已是最新版本。")
            else:
                logging.warning("无法检查更新，GitHub API 响应错误。")
        except Exception as e:
            logging.error(f"检查更新时出错: {e}")
            QMessageBox.warning(self, "更新检查失败",
                                "无法连接到更新服务器。请检查您的网络连接或代理设置。")

    def is_new_version(self, latest_version):
        return latest_version > CURRENT_VERSION

    def prompt_update(self, latest_version):
        update_msg = f"检测到新版本: {latest_version}，当前版本: {CURRENT_VERSION}。\n是否立即更新？"
        reply = QMessageBox.question(self, "软件更新", update_msg, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.download_update(latest_version)

    def download_update(self, version):
        url = f"https://github.com/awanoob/Data_Analysis_py/releases/download/{version}/DataAnalysis.exe"
        save_path = os.path.join(os.path.dirname(sys.executable), "DataAnalysis_new.exe")

        self.progress_dialog = QProgressDialog("正在下载更新...", "取消", 0, 100, self)
        self.progress_dialog.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.show()

        self.download_thread = DownloadThread(url, save_path)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.finished_signal.connect(self.update_finished)
        self.download_thread.start()

    def update_progress(self, value):
        self.progress_dialog.setValue(value)

    def update_finished(self, save_path):
        self.progress_dialog.close()
        reply = QMessageBox.question(self, "更新完成", "新版本已下载完成，是否立即安装？\n(将重启应用)",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.install_update(save_path)

    def install_update(self, new_exe_path):
        current_exe = sys.executable
        update_script = f"""
import os
import sys
import time

def replace_exe():
    current_exe = "{current_exe}"
    new_exe = "{new_exe_path}"
    backup_exe = current_exe + ".bak"

    # 等待原程序退出
    time.sleep(1)

    # 备份当前exe
    os.rename(current_exe, backup_exe)

    # 替换为新exe
    os.rename(new_exe, current_exe)

    # 删除备份
    os.remove(backup_exe)

    # 启动新版本
    os.startfile(current_exe)

if __name__ == '__main__':
    replace_exe()
"""
        with open("update_script.py", "w") as f:
            f.write(update_script)

        # 启动更新脚本并退出当前程序
        os.startfile("update_script.py")
        sys.exit()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
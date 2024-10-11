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
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.centralwidget.hide()
        self.load_stylesheet()
        self.setup_logging()
        self.setup_context_menu()


        self.ui.action_new_project.triggered.connect(self.new_project)
        self.ui.action_open_project.triggered.connect(self.open_project)




        self.ui.action_generate_report.triggered.connect(self.open_select_report_dialog)
        self.ui.tableWidget_2.itemChanged.connect(self.on_tableWidget_2_item_changed)
        self.ui.tableWidget.itemChanged.connect(self.on_tableWidget_item_changed)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.pushButton.clicked.connect(self.calculate_error_with_progress)

        self.check_for_updates()

        self.file_data = []
        self.time_data = self.get_tableWidget_2_data()

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


    def on_tableWidget_item_changed(self):
        self.file_data = self.get_tableWidget_data()
        logging.info("当前tableWidget中的数据：%s", self.file_data)
    def on_tableWidget_2_item_changed(self):
        self.time_data = self.get_tableWidget_2_data()
        logging.info("当前tableWidget_2中的数据：%s", self.time_data)




    def new_project(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "新建项目", "", "YAML Files (*.yaml);;All Files (*)"
        )

        if file_path:
            if not file_path.endswith('.yaml'):
                file_path += '.yaml'
            try:
                project_config = {
                    'path_proj': os.path.dirname(file_path),
                    'path_in_list': [],
                    'path_truth': '',
                    'path_eracsv': '',
                    'data_agg_list': [],
                    'data_agg_truth': '',
                    'data_frq': [],
                    'data_frq_truth': '',
                    'dev_name_list': [],
                    'era_list':{'Scene':[], 'start_time':[], 'end_time':[]},
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

                with open(file_path, 'w') as f:
                    yaml.dump(project_config, f)

                QMessageBox.information(self, "成功", "项目创建成功！")
                self.ui.centralwidget.show()
            except Exception as e:
                QMessageBox.critical(self, "错误", f"创建项目文件失败：{str(e)}")


    def open_project(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "打开工程", "", "YAML Files (*.yaml);;All Files (*)")
        if filepath:
            with open(filepath, 'r') as f:
                project_config = yaml.safe_load(f)
            self.ui.centralwidget.show()



    def add_data(self):
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

    def calculate_error_with_progress(self):
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
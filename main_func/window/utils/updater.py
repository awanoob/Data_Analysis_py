import os
import sys
import json
import urllib3
import certifi
import requests
from urllib.parse import urlparse
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QMessageBox, QProgressDialog
from PyQt6.QtCore import Qt
from main_func.window.config.settings import CURRENT_VERSION, GITHUB_API_URL

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

class UpdateManager:
    def __init__(self, main_window):
        self.main_window = main_window

    def get_proxy_settings(self):
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
        try:
            proxy_settings = self.get_proxy_settings()

            if proxy_settings and 'https' in proxy_settings:
                proxy_url = proxy_settings['https']
                https = urllib3.ProxyManager(
                    proxy_url,
                    cert_reqs='CERT_REQUIRED',
                    ca_certs=certifi.where(),
                    server_hostname=urlparse(GITHUB_API_URL).hostname
                )
            else:
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
            QMessageBox.warning(self.main_window, "更新检查失败",
                              "无法连接到更新服务器。请检查您的网络连接或代理设置。")

    def is_new_version(self, latest_version):
        return latest_version > CURRENT_VERSION

    def prompt_update(self, latest_version):
        update_msg = f"检测到新版本: {latest_version}，当前版本: {CURRENT_VERSION}。\n是否立即更新？"
        reply = QMessageBox.question(self.main_window, "软件更新", update_msg,
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.download_update(latest_version)

    def download_update(self, version):
        url = f"https://github.com/awanoob/Data_Analysis_py/releases/download/{version}/DataAnalysis.exe"
        save_path = os.path.join(os.path.dirname(sys.executable), "DataAnalysis_new.exe")

        self.progress_dialog = QProgressDialog("正在下载更新...", "取消", 0, 100, self.main_window)
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.show()

        self.download_thread = DownloadThread(url, save_path)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.finished_signal.connect(self.update_finished)
        self.download_thread.start()

    def update_progress(self, value):
        self.progress_dialog.setValue(value)

    def update_finished(self, save_path):
        try:
            self.progress_dialog.close()
        finally:
            self.progress_dialog.deleteLater()
            self.progress_dialog = None
        reply = QMessageBox.question(self.main_window, "更新完成", "新版本已下载完成，是否立即安装？\n(将重启应用)",
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

    time.sleep(1)

    os.rename(current_exe, backup_exe)
    os.rename(new_exe, current_exe)
    os.remove(backup_exe)
    os.startfile(current_exe)

if __name__ == '__main__':
    replace_exe()
"""
        with open("update_script.py", "w") as f:
            f.write(update_script)

        os.startfile("update_script.py")
        sys.exit()
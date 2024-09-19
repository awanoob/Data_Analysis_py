import sys
import requests
from PyQt6.QtWidgets import QApplication, QMessageBox, QWidget
from PyQt6.QtCore import QThread, pyqtSignal


class UpdateCheckerThread(QThread):
    # 信号用于在检查完成后通知主线程
    update_available = pyqtSignal(str, str)  # 参数为最新版本号和下载链接

    def __init__(self, current_version):
        super().__init__()
        self.current_version = current_version

    def run(self):
        try:
            # 请求 GitHub API 获取最新发布版本信息
            response = requests.get('https://api.github.com/repos/awanoob/Data_Analysis_py/releases/latest')
            latest_release = response.json()
            latest_version = latest_release['tag_name']
            download_url = latest_release['assets'][0]['browser_download_url']  # 获取下载链接

            if self.current_version < latest_version:
                self.update_available.emit(latest_version, download_url)
        except Exception as e:
            print(f"Error checking for updates: {e}")


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.current_version = "1.0.0"  # 这里设置当前的程序版本
        self.init_ui()

        # 启动更新检查线程
        self.update_checker = UpdateCheckerThread(self.current_version)
        self.update_checker.update_available.connect(self.show_update_dialog)
        self.update_checker.start()

    def init_ui(self):
        self.setWindowTitle("自动更新检查示例")
        self.setGeometry(300, 300, 250, 150)
        self.show()

    def show_update_dialog(self, latest_version, download_url):
        reply = QMessageBox.question(self, '更新可用',
                                     f'新版本 {latest_version} 可用，是否现在下载？',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.Yes)

        if reply == QMessageBox.StandardButton.Yes:
            # 打开下载链接
            import webbrowser
            webbrowser.open(download_url)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = MyApp()
    sys.exit(app.exec())

import os
import yaml
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from main_func.window.config.settings import DEFAULT_PROJECT_CONFIG

class ProjectManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.current_project_file = None
        self.unsaved_changes = False
        self.last_directory = ''
        self.project_config = DEFAULT_PROJECT_CONFIG.copy()

    def new_project(self):
        if self.check_unsaved_changes():
            reply = QMessageBox.question(
                self.main_window, "保存更改", "是否要保存当前项目的更改？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.save_project()
            elif reply == QMessageBox.StandardButton.Cancel:
                return

        file_path, _ = QFileDialog.getSaveFileName(
            self.main_window, "新建项目", self.last_directory, "YAML Files (*.yaml);;All Files (*)"
        )

        if file_path:
            if not file_path.endswith('.yaml'):
                file_path += '.yaml'
            try:
                self.project_config['path_proj'] = file_path
                with open(file_path, 'w') as f:
                    yaml.dump(self.project_config, f, allow_unicode=True)

                self.current_project_file = file_path
                self.main_window.ui.centralwidget.show()
                self.unsaved_changes = False
                self.last_directory = os.path.dirname(file_path)

                QMessageBox.information(self.main_window, "成功", "项目创建成功！")
                self.main_window.update_ui_from_project_config(self.project_config)
            except Exception as e:
                QMessageBox.critical(self.main_window, "错误", f"创建项目文件失败：{str(e)}")

    def open_project(self):
        if self.check_unsaved_changes():
            reply = QMessageBox.question(
                self.main_window, "保存更改", "是否要保存当前项目的更改？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.save_project()
            elif reply == QMessageBox.StandardButton.Cancel:
                return

        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window, "打开工程", self.last_directory, "YAML Files (*.yaml);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.project_config = yaml.safe_load(f)

                self.current_project_file = file_path
                self.main_window.ui.centralwidget.show()
                self.unsaved_changes = False
                self.last_directory = os.path.dirname(file_path)
                self.main_window.update_ui_from_project_config(self.project_config)
            except Exception as e:
                QMessageBox.critical(self.main_window, "错误", f"打开项目文件失败：{str(e)}")

    def save_project(self):
        try:
            if not self.current_project_file:
                file_path, _ = QFileDialog.getSaveFileName(
                    self.main_window, "保存项目", self.last_directory, "YAML Files (*.yaml);;All Files (*)"
                )
                if file_path:
                    if not file_path.endswith('.yaml'):
                        file_path += '.yaml'
                    self.current_project_file = file_path
                else:
                    return

            with open(self.current_project_file, 'w') as f:
                yaml.dump(self.project_config, f, allow_unicode=True)

            QMessageBox.information(self.main_window, "成功", "项目保存成功！")
            self.unsaved_changes = False
            self.last_directory = os.path.dirname(self.current_project_file)

        except Exception as e:
            QMessageBox.critical(self.main_window, "错误", f"保存项目文件失败：{str(e)}")

    def check_unsaved_changes(self):
        return self.unsaved_changes

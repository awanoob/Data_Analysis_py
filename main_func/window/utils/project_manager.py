import os
import yaml
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from window.config.settings import DEFAULT_PROJECT_CONFIG
# from main_func.window.ui_configdialog import ConfigDialog
from window.ui_configdialog import ConfigDialog

class ProjectManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.current_project_file = None
        self.unsaved_changes = False
        self.last_directory = ''
        self.project_config = DEFAULT_PROJECT_CONFIG.copy()

    def open_config_dialog(self):
        """打开配置选项对话框"""
        dialog = ConfigDialog(self.main_window)
        if dialog.exec():  # exec() 运行对话框并等待用户交互
            # 在这里处理用户选择的配置
            selected_options = dialog.get_selected_options()
            # 可以根据需求将结果保存到某个配置文件或应用到当前逻辑
            self.project_config['output_cep'] = selected_options['isCEP']

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
                self.project_config['path_proj'] = os.path.dirname(file_path)
                with open(file_path, 'w') as f:
                    yaml.dump(self.project_config, f, allow_unicode=True)

                self.current_project_file = file_path
                self.main_window.ui.centralwidget.show()
                self.unsaved_changes = False
                self.last_directory = os.path.dirname(file_path)

                QMessageBox.information(self.main_window, "成功", "项目创建成功！")
                self.update_ui_from_project_config(self.project_config)
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
                with open(file_path, 'r') as f:
                    self.project_config = yaml.safe_load(f)

                self.current_project_file = file_path
                self.main_window.ui.centralwidget.show()
                self.unsaved_changes = False
                self.last_directory = os.path.dirname(file_path)
                self.update_ui_from_project_config(self.project_config)
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

            with open(self.current_project_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.project_config, f, allow_unicode=True)

            QMessageBox.information(self.main_window, "成功", "项目保存成功！")
            self.unsaved_changes = False
            self.last_directory = os.path.dirname(self.current_project_file)

        except Exception as e:
            QMessageBox.critical(self.main_window, "错误", f"保存项目文件失败：{str(e)}")

    def check_unsaved_changes(self):
        return self.unsaved_changes

    def update_ui_from_project_config(self, project_config):
        """根据项目配置更新UI"""
        # 清空表格
        self.main_window.ui.tableWidget.setRowCount(0)
        self.main_window.ui.tableWidget_2.setRowCount(0)

        # 更新数据表格
        for data in project_config['data']:
            row_position = self.main_window.ui.tableWidget.rowCount()
            self.main_window.ui.tableWidget.insertRow(row_position)
            self.main_window.table_manager.create_table_controls(row_position, data)

        # 更新时间段表格
        for era in project_config['era_list']:
            row_position = self.main_window.ui.tableWidget_2.rowCount()
            self.main_window.ui.tableWidget_2.insertRow(row_position)
            self.main_window.ui.tableWidget_2.setItem(row_position, 0, QtWidgets.QTableWidgetItem(era['scene']))
            self.main_window.ui.tableWidget_2.setItem(row_position, 1, QtWidgets.QTableWidgetItem(era['era_start']))
            self.main_window.ui.tableWidget_2.setItem(row_position, 2, QtWidgets.QTableWidgetItem(era['era_end']))

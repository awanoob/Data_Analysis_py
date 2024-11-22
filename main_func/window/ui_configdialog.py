from PyQt6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QPushButton

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("配置选项")
        self.resize(300, 200)

        # 布局
        layout = QVBoxLayout()

        # 添加多个选项
        self.checkbox1 = QCheckBox("输出CEP统计量")
        self.checkbox2 = QCheckBox("启用选项 B")
        self.checkbox3 = QCheckBox("启用选项 C")
        layout.addWidget(self.checkbox1)
        layout.addWidget(self.checkbox2)
        layout.addWidget(self.checkbox3)

        # 确认按钮
        self.confirm_button = QPushButton("确认")
        self.confirm_button.clicked.connect(self.accept)  # accept() 会关闭对话框
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def get_selected_options(self):
        """返回用户勾选的选项"""
        return {
            "isCEP": self.checkbox1.isChecked(),
            "option_b": self.checkbox2.isChecked(),
            "option_c": self.checkbox3.isChecked(),
        }

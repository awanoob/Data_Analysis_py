from PyQt6.QtWidgets import QWidget, QHBoxLayout, QCheckBox
from PyQt6.QtCore import Qt

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
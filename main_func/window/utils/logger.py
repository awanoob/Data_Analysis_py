from PyQt6.QtWidgets import QTextEdit
import logging

class QTextEditLogger(logging.Handler):
    def __init__(self, log_text_edit):
        super().__init__()
        self.log_text_edit = log_text_edit

    def emit(self, record):
        log_message = self.format(record)
        self.log_text_edit.append(log_message)

def setup_logging(text_edit):
    text_edit_logger = QTextEditLogger(text_edit)
    text_edit_logger.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(text_edit_logger)
    logging.getLogger().setLevel(logging.INFO)
from PyQt6.QtGui import QTextCharFormat, QFont, QTextCursor
from PyQt6.QtWidgets import QApplication, QTextEdit
from logger_setup import logger
from typing import Callable, Any
from formatters.text_format_setup import BaseTextFormatter


class SubScriptTextFormatter(BaseTextFormatter):

    def make_subscript(self, fmt, current_format):
        # Set the vertical alignment to Subscript for the format
        fmt.setVerticalAlignment(QTextCharFormat.VerticalAlignment.AlignSubScript)
    
    # This method can be used to directly apply this formatting
    def apply(self):
        self.apply_current_text_format(self.format_text)
        
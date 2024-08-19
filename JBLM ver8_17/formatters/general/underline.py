from PyQt6.QtGui import QTextCharFormat, QFont, QTextCursor
from PyQt6.QtWidgets import QApplication, QTextEdit
from logger_setup import logger
from typing import Callable, Any
from formatters.text_format_setup import BaseTextFormatter


class UnderlineTextFormatter(BaseTextFormatter):

    def make_underline(self, fmt, current_format):
        fmt.setFontUnderline(not current_format.font().underline())
    
    # This method can be used to directly apply this formatting
    def apply(self):
        self.apply_current_text_format(self.format_text)
        
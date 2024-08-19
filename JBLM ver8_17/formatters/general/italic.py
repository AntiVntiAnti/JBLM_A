from PyQt6.QtGui import QTextCharFormat, QFont, QTextCursor
from PyQt6.QtWidgets import QApplication, QTextEdit
from logger_setup import logger
from typing import Callable, Any
from formatters.text_format_setup import BaseTextFormatter


class ItalicTextFormatter(BaseTextFormatter):
    """
    A text formatter that applies italic formatting to text.
    """

    def make_italic(self, fmt, current_format):
        """
        Toggles the italic formatting of the given text format.

        Args:
            fmt (QTextCharFormat): The text format to modify.
            current_format (QTextCharFormat): The current text format.

        Returns:
            None
        """
        fmt.setFontItalic(not current_format.font().italic())
    
    def apply(self):
        """
        Applies the italic formatting to the current text format.

        Returns:
            None
        """
        self.apply_current_text_format(self.format_text)
        
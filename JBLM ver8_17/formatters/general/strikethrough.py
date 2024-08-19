from PyQt6.QtGui import QTextCharFormat, QFont, QTextCursor
from PyQt6.QtWidgets import QApplication, QTextEdit
from logger_setup import logger
from typing import Callable, Any
from formatters.text_format_setup import BaseTextFormatter


class StrikeTextFormatter(BaseTextFormatter):
    """
    A text formatter for applying strikethrough formatting to text.
    """

    def make_strikethrough(self, fmt, current_format):
        """
        Toggles the strikethrough formatting for the given text format.

        Args:
            fmt (QTextCharFormat): The text format to modify.
            current_format (QTextCharFormat): The current text format.

        Returns:
            None
        """
        fmt.setFontStrikeOut(not current_format.font().strikeOut())
    
    def apply(self):
        """
        Applies the strikethrough formatting to the current text.

        Returns:
            None
        """
        self.apply_current_text_format(self.format_text)
        
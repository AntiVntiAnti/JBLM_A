from PyQt6.QtGui import QTextCharFormat, QFont, QTextCursor
from PyQt6.QtWidgets import QApplication, QTextEdit
from logger_setup import logger
from typing import Callable, Any
from formatters.text_format_setup import BaseTextFormatter


class IncreaseFontSizeFormatter(BaseTextFormatter):
    """
    A formatter class for increasing the font size of text.

    This class provides methods to adjust the font size of a given text format,
    increase the font size by 1 point, and apply the formatting to the text.

    Attributes:
        None

    Methods:
        adjust_font_size(fmt, current_format, increase=True):
            Adjusts the font size of the given text format.

        increase_font_size(fmt, current_format):
            Increases the font size of the given text format by 1 point.

        apply():
            Applies the current text format to the text.

    Usage:
        formatter = IncreaseFontSizeFormatter()
        formatter.increase_font_size(fmt, current_format)
        formatter.apply()
    """

    def adjust_font_size(self, fmt, current_format, increase=True):
        """
        Adjusts the font size of the given text format.

        Args:
            fmt (QTextCharFormat): The text format to adjust.
            current_format (QTextCharFormat): The current text format.
            increase (bool, optional): Whether to increase the font size. Defaults to True.

        Returns:
            None
        """
        # Get the DEC 23 JOURNJOURN(previously codejourn) font size
        current_font_size = current_format.fontPointSize()

        # Use a default font size if the DEC 23 JOURNJOURN(previously codejourn) font size is not valid
        default_font_size = 12
        if current_font_size <= 0:
            current_font_size = default_font_size

        # Increase or decrease the font size by 1 point
        new_font_size = current_font_size + 1 if increase else current_font_size - 1
        new_font_size = max(new_font_size, 1)  # Ensure font size is always positive

        # Set the new font size
        fmt.setFontPointSize(new_font_size)

    def increase_font_size(self, fmt, current_format):
        """
        Increases the font size of the given text format by 1 point.

        Args:
            fmt (QTextCharFormat): The text format to adjust.
            current_format (QTextCharFormat): The current text format.

        Returns:
            None
        """
        self.adjust_font_size(fmt, current_format, increase=True)
    
    def apply(self):
        """
        Applies the current text format to the text.

        Args:
            None

        Returns:
            None
        """
        self.apply_current_text_format(self.format_text)
        
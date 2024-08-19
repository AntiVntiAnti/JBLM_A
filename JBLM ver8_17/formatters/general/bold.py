from PyQt6.QtGui import QTextCharFormat, QFont, QTextCursor
from PyQt6.QtWidgets import QApplication, QTextEdit
from logger_setup import logger
from typing import Callable, Any
from formatters.text_format_setup import BaseTextFormatter


class BoldTextFormatter(BaseTextFormatter):
    """
    A text formatter that toggles the bold state of the font in a QTextCharFormat.
    """

    def make_bold(self, fmt: QTextCharFormat, current_format: QTextCharFormat) -> None:
        """
        Toggles the bold state of the font in the given QTextCharFormat.

        :param fmt: The QTextCharFormat to modify.
        :param current_format: The current QTextCharFormat of the text, used to check if it's already bold.
        """
        try:
            # Toggle bold state based on the current state
            fmt.setFontWeight(
                QFont.Weight.Bold if not current_format.font().bold() else QFont.Weight.Normal)
        except Exception as e:
            logger.error(f"Error making bold text format: {e}", exc_info=True)

    # This method can be used to directly apply this formatting
    def apply(self):
        self.apply_current_text_format(self.format_text)
        
from PyQt6.QtGui import QTextCharFormat
from PyQt6.QtWidgets import QApplication, QTextEdit
from logger_setup import logger


class BaseTextFormatter:
    """
    Base class for text formatters.

    This class provides methods to apply text formatting to a QTextEdit widget.

    Attributes:
        None

    Methods:
        apply_text_format: Applies the specified text format to the given QTextEdit widget.
        apply_current_text_format: Applies the specified text format to the currently focused QTextEdit widget.
    """

    try:
        def apply_text_format(self, note_widget: QTextEdit, format_func):
            """
            Applies the specified text format to the given QTextEdit widget.

            Args:
                note_widget (QTextEdit): The QTextEdit widget to apply the text format to.
                format_func (function): The function that defines the text format to apply.

            Returns:
                None
            """
            fmt = QTextCharFormat()
            format_func(fmt, note_widget.currentCharFormat())
            cursor = note_widget.textCursor()
            cursor.mergeCharFormat(fmt)
    except Exception as e:
        logger.error(f"Failed to apply text format: {e}")

    def apply_current_text_format(self, format_func):
        """
        Applies the specified text format to the currently focused QTextEdit widget.

        Args:
            format_func (function): The function that defines the text format to apply.

        Returns:
            None
        """
        try:
            focused_widget = QApplication.instance().focusWidget()
            if isinstance(focused_widget, QTextEdit):
                self.apply_text_format(focused_widget, format_func)
        except Exception as e:
            logger.error(f"Failed to apply text format: {e}")
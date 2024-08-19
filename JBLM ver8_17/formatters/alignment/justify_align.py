from PyQt6.QtGui import QTextCursor, QTextBlockFormat
from PyQt6.QtWidgets import QApplication, QTextEdit
from PyQt6.QtCore import Qt
from formatters.text_alignment_setup import BaseAlignmentFormatter
from logger_setup import logger


class JustifyAlignFormatter(BaseAlignmentFormatter):
    """
    A formatter class for justifying text alignment.

    This class provides methods to justify text alignment to center.
    It inherits from the BaseAlignmentFormatter class.

    Attributes:
        None

    Methods:
        justify_text(cursor): Justifies the text alignment to center.
        apply(): Applies the current text format.
    """

    def justify_text(self, cursor):
        """
        Justifies the text alignment to center.

        Args:
            cursor: The QTextCursor object representing the text cursor.
        """
        try:
            # Create a QTextBlockFormat object for block (paragraph) formatting
            block_format = QTextBlockFormat()
            # Set the alignment to Center
            block_format.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # Apply the block format to the cursor selection or current block
            cursor.mergeBlockFormat(block_format)
        except Exception as e:
            logger.error(f"error when trying to justify the selected text {e}", exc_info=True)
    
    # This method can be used to directly apply this formatting
    def apply(self):
        """
        Applies the current text format.
        """
        try:
            self.apply_current_text_format(self.format_text)
        except Exception as e:
            logger.error(f"error apply_current_text_format {e}", exc_info=True)
            
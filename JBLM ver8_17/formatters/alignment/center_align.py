from PyQt6.QtGui import QTextCursor, QTextBlockFormat
from PyQt6.QtWidgets import QApplication, QTextEdit
from PyQt6.QtCore import Qt
from formatters.text_alignment_setup import BaseAlignmentFormatter


class CenterAlignFormatter(BaseAlignmentFormatter):
    """
    A formatter class for center alignment of text.
    """

    def center_text(self, cursor):
        """
        Centers the text at the current cursor position.

        Args:
            cursor: The QTextCursor object representing the current cursor position.
        """
        # Create a QTextBlockFormat object for block (paragraph) formatting
        block_format = QTextBlockFormat()
        # Set the alignment to Center
        block_format.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Apply the block format to the cursor selection or current block
        cursor.mergeBlockFormat(block_format)
    
    # This method can be used to directly apply this formatting
    def __init__(self):
        """
        Initializes the CenterAlignFormatter class.
        """
        self.format_text = None

    def apply(self):
        """
        Applies the center alignment formatting to the current text.
        """
        self.apply_current_text_format(self.format_text)

    def apply_current_text_format(self, format_text):
        """
        Applies the current text format to the given text.

        Args:
            format_text: The text to apply the format to.
        """
        # Implement the logic to apply the current text format
        pass
        
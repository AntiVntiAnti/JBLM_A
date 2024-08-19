from PyQt6.QtGui import QTextCursor, QTextBlockFormat
from PyQt6.QtWidgets import QApplication, QTextEdit
from PyQt6.QtCore import Qt
from formatters.text_alignment_setup import BaseAlignmentFormatter


class RightAlignFormatter(BaseAlignmentFormatter):
    """
    A formatter class for right-aligning text.
    """

    def right_align_text(self, cursor):
        """
        Right-aligns the text at the current cursor position.

        Args:
            cursor: The QTextCursor object representing the current cursor position.
        """
        # Create a QTextBlockFormat object for block (paragraph) formatting
        block_format = QTextBlockFormat()
        # Set the alignment to Right
        block_format.setAlignment(Qt.AlignmentFlag.AlignRight)
        # Apply the block format to the cursor selection or current block
        cursor.mergeBlockFormat(block_format)
    
    def apply(self):
        """
        Applies the right alignment formatting to the current text.
        """
        self.apply_current_text_format(self.format_text)
        
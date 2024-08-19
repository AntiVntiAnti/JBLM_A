from PyQt6.QtGui import QTextCursor, QTextBlockFormat
from PyQt6.QtWidgets import QApplication, QTextEdit
from PyQt6.QtCore import Qt
from formatters.text_alignment_setup import BaseAlignmentFormatter


class LeftAlignFormatter(BaseAlignmentFormatter):
    """
    A formatter class for left-aligning text.
    """

    def left_align_text(self, cursor):
        """
        Left-aligns the text at the current cursor position.

        Args:
            cursor: The QTextCursor object representing the current cursor position.
        """
        # Create a QTextBlockFormat object for block (paragraph) formatting
        block_format = QTextBlockFormat()
        # Set the alignment to Left
        block_format.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # Apply the block format to the cursor selection or current block
        cursor.mergeBlockFormat(block_format)
    
    def apply(self):
        """
        Applies the left alignment formatting to the current text format.
        """
        self.apply_current_text_format(self.format_text)
        
from PyQt6.QtGui import QTextCursor, QTextBlockFormat
from PyQt6.QtWidgets import QApplication, QTextEdit
from PyQt6.QtCore import Qt
from logger_setup import logger


class BaseAlignmentFormatter:
    def apply_text_alignment(self, note_widget, alignment_func):
        try:
            cursor = note_widget.textCursor()
            alignment_func(cursor)  # Apply the alignment function to the cursor
        except Exception as e:
            logger.error(f"error applying text formatting in base module {e}", exc_info=True)

    def apply_current_text_alignment(self, alignment_func):
        try:
            focused_widget = QApplication.instance().focusWidget()
            if isinstance(focused_widget, QTextEdit):
                self.apply_text_alignment(focused_widget, alignment_func)
        except Exception as e:
            logger.error(f"apply_current_text_alignment failed in base module {e}", exc_info=True)
            
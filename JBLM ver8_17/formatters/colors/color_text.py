from PyQt6.QtWidgets import QColorDialog
from formatters.text_format_setup import BaseTextFormatter


class ColorTextFormatter(BaseTextFormatter):
    """
    A text formatter that applies font color to the text.
    """

    def font_color(self, fmt, current_format):
        """
        Prompts the user to select a color and applies it as the font color.

        Args:
            fmt (QTextCharFormat): The text character format to modify.
            current_format (QTextCharFormat): The current text character format.

        Returns:
            None
        """
        color = QColorDialog.getColor()
        fmt.setForeground(color)
        
    def apply(self):
        """
        Applies the current text format to the text.

        Returns:
            None
        """
        self.apply_current_text_format(self.format_text)
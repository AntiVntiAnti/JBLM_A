from PyQt6.QtWidgets import QColorDialog
from formatters.text_format_setup import BaseTextFormatter


class HighlightColorFormatter(BaseTextFormatter):
    """
    A class that represents a text formatter for highlighting text with a color.

    This formatter allows the user to select a color using QColorDialog and apply it as the background color
    for the formatted text.

    Attributes:
        None

    Methods:
        format_text(fmt, current_format): Formats the text by setting the background color based on the selected color.
        apply(): Applies the formatting by calling the format_text method.

    Example usage:
        formatter = HighlightColorFormatter()
        formatter.apply()
    """

    def format_text(self, fmt, current_format):
        """
        Formats the text by setting the background color based on the selected color.

        Args:
            fmt (QTextCharFormat): The text format to be modified.
            current_format (QTextCharFormat): The current format of the text.

        Returns:
            None
        """
        color = QColorDialog.getColor()
        if color.isValid():
            fmt.setBackground(color)
        else:
            # Handle the case where no color is selected (optional)
            pass

    def apply(self):
        """
        Applies the formatting by calling the format_text method.

        Args:
            None

        Returns:
            None
        """
        self.apply_current_text_format(self.format_text)
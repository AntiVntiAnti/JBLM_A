from PyQt6.QtCore import QSettings, QDate, QTime
from PyQt6.QtWidgets import QDateEdit, QTextEdit
import tracker_config as tkc
from logger_setup import logger


class SettingsManagerAgendaFriday:
    """
    A class that manages the settings for the Friday agenda in the application.
    """

    def __init__(self):
        self.settings = QSettings(tkc.ORGANIZATION_NAME, tkc.APPLICATION_NAME)

    def save_fri_journal(self, fri_date: QDateEdit, fri_note_one: QTextEdit, ):
        """
        Saves the Friday journal settings.

        Args:
            fri_date (QDateEdit): The QDateEdit widget for the Friday date.
            fri_note_one (QTextEdit): The QTextEdit widget for the Friday note.

        Returns:
            None
        """
        try:
            self.settings.setValue('fri_date', fri_date.date())
            self.settings.setValue('fri_note_one', fri_note_one.toHtml())
        except Exception as e:
            logger.error(f"Error saving Friday journal settings: {str(e)}")

    def restore_fri_journal(self, fri_date: QDateEdit, fri_note_one: QTextEdit, ):
        """
        Restores the Friday journal settings.

        Args:
            fri_date (QDateEdit): The QDateEdit widget for the Friday date.
            fri_note_one (QTextEdit): The QTextEdit widget for the Friday note.

        Returns:
            None
        """
        try:
            fri_date.setDate(self.settings.value('fri_date', QDate.currentDate()))
            fri_note_one.setHtml(self.settings.value('fri_note_one', "", type=str))
        except Exception as e:
            logger.error(f"Error restoring Friday journal settings: {str(e)}")

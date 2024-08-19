from PyQt6.QtCore import QSettings, QDate, QTime
from PyQt6.QtWidgets import QDateEdit, QTextEdit
import tracker_config as tkc
from logger_setup import logger

class SettingsManagerAgendaThursday:
    """
    A class that manages the settings for Thursday's agenda in a journal application.
    """

    def __init__(self):
        self.settings = QSettings(tkc.ORGANIZATION_NAME, tkc.APPLICATION_NAME)

    def save_thurs_journal(self, thurs_date: QDateEdit, thurs_note_one: QTextEdit, ):
        """
        Saves the Thursday journal settings.

        Args:
            thurs_date (QDateEdit): The QDateEdit widget for Thursday's date.
            thurs_note_one (QTextEdit): The QTextEdit widget for Thursday's note.

        Raises:
            Exception: If there is an error while saving the settings.
        """
        try:
            self.settings.setValue('thurs_date', thurs_date.date())
            self.settings.setValue('thurs_note_one', thurs_note_one.toHtml())
        except Exception as e:
            logger.error(f"Error saving Thursday journal: {str(e)}")

    def restore_thurs_journal(self, thurs_date: QDateEdit, thurs_note_one: QTextEdit, ):
        """
        Restores the Thursday journal settings.

        Args:
            thurs_date (QDateEdit): The QDateEdit widget for Thursday's date.
            thurs_note_one (QTextEdit): The QTextEdit widget for Thursday's note.

        Raises:
            Exception: If there is an error while restoring the settings.
        """
        try:
            thurs_date.setDate(self.settings.value('thurs_date', QDate.currentDate()))
            thurs_note_one.setHtml(self.settings.value('thurs_note_one', "", type=str))
        except Exception as e:
            logger.error(f"Error restoring Thursday journal: {str(e)}")

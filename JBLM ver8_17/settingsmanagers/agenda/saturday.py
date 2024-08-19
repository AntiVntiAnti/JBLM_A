from PyQt6.QtCore import QSettings, QDate, QTime
from PyQt6.QtWidgets import QDateEdit, QTextEdit
import tracker_config as tkc
from logger_setup import logger

class SettingsManagerAgendaSaturday:
    """
    A class that manages the settings for Saturday agenda in a journal application.
    """

    def __init__(self):
        self.settings = QSettings(tkc.ORGANIZATION_NAME, tkc.APPLICATION_NAME)

    def save_sat_journal(self, sat_date: QDateEdit, sat_note_one: QTextEdit, ):
        """
        Saves the Saturday journal settings.

        Args:
            sat_date (QDateEdit): The QDateEdit widget for the Saturday date.
            sat_note_one (QTextEdit): The QTextEdit widget for the Saturday note.

        Raises:
            Exception: If an error occurs while saving the Saturday journal settings.
        """
        try:
            self.settings.setValue('sat_date', sat_date.date())
            self.settings.setValue('sat_note_one', sat_note_one.toHtml())
        except Exception as e:
            logger.error(f"Error occurred while saving Saturday journal: {str(e)}")

    def restore_sat_journal(self, sat_date: QDateEdit, sat_note_one: QTextEdit, ):
        """
        Restores the Saturday journal settings.

        Args:
            sat_date (QDateEdit): The QDateEdit widget for the Saturday date.
            sat_note_one (QTextEdit): The QTextEdit widget for the Saturday note.

        Raises:
            Exception: If an error occurs while restoring the Saturday journal settings.
        """
        try:
            sat_date.setDate(self.settings.value('sat_date', QDate.currentDate()))
            sat_note_one.setHtml(self.settings.value('sat_note_one', "", type=str))
        except Exception as e:
            logger.error(f"Error occurred while restoring Saturday journal: {str(e)}")

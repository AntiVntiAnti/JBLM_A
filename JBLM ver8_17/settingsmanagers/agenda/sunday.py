from PyQt6.QtCore import QSettings, QDate, QTime
from PyQt6.QtWidgets import QDateEdit, QTextEdit
import tracker_config as tkc
from logger_setup import logger


class SettingsManagerAgendaSunday:
    """
    A class that manages the settings for the Sunday agenda in a journal application.
    """

    def __init__(self):
        self.settings = QSettings(tkc.ORGANIZATION_NAME, tkc.APPLICATION_NAME)

    def save_sun_journal(self, sun_date: QDateEdit, sun_note_one: QTextEdit, ):
        """
        Saves the Sunday journal settings.

        Args:
            sun_date (QDateEdit): The date of the Sunday journal.
            sun_note_one (QTextEdit): The content of the Sunday journal.

        Raises:
            Exception: If an error occurs while saving the settings.
        """
        try:
            self.settings.setValue('sun_date', sun_date.date())
            self.settings.setValue('sun_note_one', sun_note_one.toHtml())
        except Exception as e:
            logger.error(f"Error occurred while saving sun journal: {str(e)}")

    def restore_sun_journal(self, sun_date: QDateEdit, sun_note_one: QTextEdit, ):
        """
        Restores the Sunday journal settings.

        Args:
            sun_date (QDateEdit): The date of the Sunday journal.
            sun_note_one (QTextEdit): The content of the Sunday journal.

        Raises:
            Exception: If an error occurs while restoring the settings.
        """
        try:
            sun_date.setDate(self.settings.value('sun_date', QDate.currentDate()))
            sun_note_one.setHtml(self.settings.value('sun_note_one', "", type=str))
        except Exception as e:
            logger.error(f"Error occurred while restoring sun journal: {str(e)}")

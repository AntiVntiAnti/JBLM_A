from PyQt6.QtCore import QSettings, QDate, QTime
from PyQt6.QtWidgets import QDateEdit, QTextEdit
import tracker_config as tkc
from logger_setup import logger


class SettingsManagerAgendaWednesday:
    """
    Manages the settings related to the Wednesday agenda in the application.
    """

    def __init__(self):
        self.settings = QSettings(tkc.ORGANIZATION_NAME, tkc.APPLICATION_NAME)

    def save_wed_journal(self, wed_date: QDateEdit, wed_note_one: QTextEdit, ):
        """
        Saves the Wednesday journal entry.

        Args:
            wed_date (QDateEdit): The QDateEdit widget containing the date of the journal entry.
            wed_note_one (QTextEdit): The QTextEdit widget containing the journal entry.

        Raises:
            Exception: If there is an error while saving the journal entry.

        Returns:
            None
        """
        try:
            self.settings.setValue('wed_date', wed_date.date())
            self.settings.setValue('wed_note_one', wed_note_one.toHtml())
        except Exception as e:
            logger.error(f"Failed to save Wednesday journal: {str(e)}")

    def restore_wed_journal(self, wed_date: QDateEdit, wed_note_one: QTextEdit, ):
        """
        Restores the Wednesday journal entry.

        Args:
            wed_date (QDateEdit): The QDateEdit widget to set the restored date.
            wed_note_one (QTextEdit): The QTextEdit widget to set the restored journal entry.

        Raises:
            Exception: If there is an error while restoring the journal entry.

        Returns:
            None
        """
        try:
            wed_date.setDate(self.settings.value('wed_date', QDate.currentDate()))
            wed_note_one.setHtml(self.settings.value('wed_note_one', "", type=str))
        except Exception as e:
            logger.error(f"Failed to restore Wednesday journal: {str(e)}")

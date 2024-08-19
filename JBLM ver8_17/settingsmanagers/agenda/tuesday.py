from PyQt6.QtCore import QSettings, QDate, QTime
from PyQt6.QtWidgets import QDateEdit, QTextEdit
import tracker_config as tkc
from logger_setup import logger

class SettingsManagerAgendaTuesday:
    """
    A class that manages the settings for Tuesday's agenda in the application.
    """

    def __init__(self):
        self.settings = QSettings(tkc.ORGANIZATION_NAME, tkc.APPLICATION_NAME)

    def save_tues_journal(self, tues_date: QDateEdit, tues_note_one: QTextEdit):
        """
        Saves the Tuesday's journal settings.

        Args:
            tues_date (QDateEdit): The QDateEdit widget for Tuesday's date.
            tues_note_one (QTextEdit): The QTextEdit widget for Tuesday's note.

        Raises:
            Exception: If there is an error while saving the settings.
        """
        try:
            self.settings.setValue('tues_date', tues_date.date())
            self.settings.setValue('tues_note_one', tues_note_one.toHtml())
        except Exception as e:
            logger.error(f"Failed to save Tuesday's journal: {str(e)}")

    def restore_tues_journal(self, tues_date: QDateEdit, tues_note_one: QTextEdit,):
        """
        Restores the Tuesday's journal settings.

        Args:
            tues_date (QDateEdit): The QDateEdit widget for Tuesday's date.
            tues_note_one (QTextEdit): The QTextEdit widget for Tuesday's note.

        Raises:
            Exception: If there is an error while restoring the settings.
        """
        try:
            tues_date.setDate(self.settings.value('tues_date', QDate.currentDate()))
            tues_note_one.setHtml(self.settings.value('tues_note_one', "", type=str))
        except Exception as e:
            logger.error(f"Failed to restore Tuesday's journal: {str(e)}")

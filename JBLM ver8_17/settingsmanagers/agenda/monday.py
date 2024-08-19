from PyQt6.QtCore import QSettings, QDate, QTime
import tracker_config as tkc
from PyQt6.QtWidgets import QDateEdit, QTextEdit
from logger_setup import logger

class SettingsManagerAgendaMonday:
    """
    A class that manages the settings for Monday in the agenda.

    This class provides methods to save and restore the Monday journal settings.
    """

    def __init__(self):
        self.settings = QSettings(tkc.ORGANIZATION_NAME, tkc.APPLICATION_NAME)

    def save_mon_journal(self, mon_date: QDateEdit, mon_note_one: QTextEdit, ):
        """
        Save the Monday journal settings.

        Args:
            mon_date (QDateEdit): The QDateEdit widget for the Monday date.
            mon_note_one (QTextEdit): The QTextEdit widget for the Monday note.

        Raises:
            Exception: If an error occurs while saving the Monday journal.
        """
        try:
            self.settings.setValue('mon_date', mon_date.date())
            self.settings.setValue('mon_note_one', mon_note_one.toHtml())
        except Exception as e:
            logger.error(f"Error occurred while saving Monday journal: {str(e)}")

    def restore_mon_journal(self, mon_date: QDateEdit, mon_note_one: QTextEdit, ):
        """
        Restore the Monday journal settings.

        Args:
            mon_date (QDateEdit): The QDateEdit widget for the Monday date.
            mon_note_one (QTextEdit): The QTextEdit widget for the Monday note.

        Raises:
            Exception: If an error occurs while restoring the Monday journal.
        """
        try:
            mon_date.setDate(self.settings.value('mon_date', QDate.currentDate()))
            mon_note_one.setHtml(self.settings.value('mon_note_one', "", type=str))
        except Exception as e:
            logger.error(f"Error occurred while restoring Monday journal: {str(e)}")

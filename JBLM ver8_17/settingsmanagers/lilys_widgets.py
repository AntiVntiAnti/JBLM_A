from PyQt6.QtCore import QSettings, QDate, QTime
from PyQt6.QtWidgets import QDateEdit, QTextEdit, QSlider, QSpinBox
import tracker_config as tkc
from logger_setup import logger


class SettingsManagerLilysWidgets:
    """
    A class that manages the settings for Tuesday's agenda in the application.
    """
    
    def __init__(self):
        self.settings = QSettings(tkc.ORGANIZATION_NAME, tkc.APPLICATION_NAME)
    
    def save_lilys_widget_states(
        self,
        lily_time_in_room_slider: QSlider,
        lily_mood_slider: QSlider,
        lily_mood_activity_slider: QSlider,
        lily_energy_slider: QSlider,
        lily_time_in_room: QSlider,
        lily_mood: QSpinBox,
        lily_activity: QSpinBox,
        lily_energy: QSpinBox,
        lily_notes: QTextEdit,
    ):
        try:
            self.settings.setValue('lily_time_in_room_slider', lily_time_in_room_slider.value())
            self.settings.setValue('lily_mood_slider', lily_mood_slider.value())
            self.settings.setValue('lily_mood_activity_slider', lily_mood_activity_slider.value())
            self.settings.setValue('lily_energy_slider', lily_energy_slider.value())
            self.settings.setValue('lily_time_in_room', lily_time_in_room.value())
            self.settings.setValue('lily_mood', lily_mood.value())
            self.settings.setValue('lily_activity', lily_activity.value())
            self.settings.setValue('lily_energy', lily_energy.value())
            self.settings.setValue('lily_notes', lily_notes.toHtml())
        except Exception as e:
            logger.error(f"Failed to save Tuesday's journal: {str(e)}")
    
    def restore_lilys_widget_states(
        self,
        lily_time_in_room_slider: QSlider,
        lily_mood_slider: QSlider,
        lily_mood_activity_slider: QSlider,
        lily_energy_slider: QSlider,
        lily_time_in_room: QSlider,
        lily_mood: QSpinBox,
        lily_activity: QSpinBox,
        lily_energy: QSpinBox,
        lily_notes: QTextEdit, ):
        try:
            lily_time_in_room_slider.setValue(self.settings.value('lily_time_in_room_slider',
                                                                  0,
                                                                  type=int))
            lily_mood_slider.setValue(self.settings.value('lily_mood_slider', 0, type=int))
            lily_mood_activity_slider.setValue(self.settings.value('lily_mood_activity_slider',
                                                                   0,
                                                                   type=int))
            lily_energy_slider.setValue(self.settings.value('lily_energy_slider', 0, type=int))
            lily_time_in_room.setValue(self.settings.value('lily_time_in_room', 0, type=int))
            lily_mood.setValue(self.settings.value('lily_mood', 0, type=int))
            lily_activity.setValue(self.settings.value('lily_activity', 0, type=int))
            lily_energy.setValue(self.settings.value('lily_energy', 0, type=int))
            lily_notes.setHtml(self.settings.value('lily_notes', "", type=str))
        except Exception as e:
            logger.error(f"Failed to restore Tuesday's journal: {str(e)}")

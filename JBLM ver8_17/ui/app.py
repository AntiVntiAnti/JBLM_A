import datetime
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QDate, QSettings, QTime, Qt, QByteArray, QDateTime
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QApplication, QTextEdit, QPushButton, QDialog, QFormLayout, QLineEdit
from PyQt6.QtPrintSupport import QPrintDialog

# ############################################################################
# UI
# ############################################################################
from ui.main_ui.gui import Ui_MainWindow

# ############################################################################
# LOGGER
# ############################################################################
import tracker_config as tkc
from logger_setup import logger

# ############################################################################
# NAVIGATION
# ############################################################################
from navigation.master_navigation import (
    change_mainStack, change_alpha_stack_page,
    change_agenda_stack_page, )

# ############################################################################
# UTILITY
# ############################################################################
from utility.app_operations.diet_calc import (
    calculate_calories)
from utility.app_operations.save_generic import (
    TextEditSaver)
from utility.widgets_set_widgets.slider_spinbox_connections import (
    connect_slider_spinbox)
from utility.app_operations.frameless_window import (
    FramelessWindow)
from utility.app_operations.window_controls import (
    WindowController)
from utility.app_operations.current_date_highlighter import (
    DateHighlighter)
from utility.widgets_set_widgets.line_connections import (
    line_edit_times)
from utility.widgets_set_widgets.slider_timers import (
    connect_slider_timeedits)
from utility.widgets_set_widgets.buttons_set_time import (
    btn_times)
from utility.app_operations.show_hide import (
    toggle_views)
from utility.widgets_set_widgets.buttons_set_time import (
    btn_times)

# #############################################################################
# DATABASE Magicks 
# #############################################################################
from database.database_manager import (
    DataManager)
# Delete Records
from database.database_utility.delete_records import (
    delete_selected_rows)
# setup Models
from database.database_utility.model_setup import (
    create_and_set_model)
# add data modules
from database.add_data.basics_mod.basics_shower import add_shower_data
from database.add_data.basics_mod.basics_exercise import add_exercise_data
from database.add_data.basics_mod.basics_teethbrushing import add_teethbrush_data
from database.add_data.diet_mod.diet_hydration import add_hydration_data
from database.add_data.diet_mod.diet import add_diet_data
from database.add_data.lily_mod.lily_walk_notes import add_lily_walk_notes
from database.add_data.lily_mod.lily_diet import add_lily_diet_data
from database.add_data.lily_mod.lily_walks import add_lily_walk_data
from database.add_data.lily_mod.lily_time_in_room import add_time_in_room_data
from database.add_data.lily_mod.lily_mood import add_lily_mood_data
from database.add_data.lily_mod.lily_notes import add_lily_note_data
from database.add_data.sleep_mod.sleep_quality import add_sleep_quality_data
from database.add_data.sleep_mod.sleep_total_hours_slept import add_total_hours_slept_data
from database.add_data.sleep_mod.sleep_woke_up_like import add_woke_up_like_data
from database.add_data.sleep_mod.sleep import add_sleep_data
from database.add_data.mental.wefe import add_wefe_data
from database.add_data.mental.mmdmr import add_mentalsolo_data
from database.add_data.mental.cspr import add_cspr_data
# add agenda days sorted below
from database.add_data.agenda.sunday import (
    agenda_data_sunday)
from database.add_data.agenda.monday import (
    agenda_data_monday)
from database.add_data.agenda.tuesday import (
    agenda_data_tuesday)
from database.add_data.agenda.wednesday import (
    agenda_data_wednesday)
from database.add_data.agenda.thursday import (
    agenda_data_thursday)
from database.add_data.agenda.friday import (
    agenda_data_friday)
from database.add_data.agenda.saturday import (
    agenda_data_saturday)

#############################################################################
#                                      QSettings Situation
#############################################################################

from settingsmanagers.agenda.sunday import (
    SettingsManagerAgendaSunday)  # SUNDAY
from settingsmanagers.agenda.monday import (
    SettingsManagerAgendaMonday)  # MONDAY
from settingsmanagers.agenda.tuesday import (
    SettingsManagerAgendaTuesday)  # TUESDAY
from settingsmanagers.agenda.wednesday import (
    SettingsManagerAgendaWednesday)  # WEDNESDAY
from settingsmanagers.agenda.thursday import (
    SettingsManagerAgendaThursday)  # THURSDAY
from settingsmanagers.agenda.friday import (
    SettingsManagerAgendaFriday)  # FRIDAY
from settingsmanagers.agenda.saturday import (
    SettingsManagerAgendaSaturday)  # SATURDAY
from settingsmanagers.lilys_widgets import SettingsManagerLilysWidgets
# Formatters
from formatters.colors.highlight import HighlightColorFormatter
from formatters.colors.color_text import ColorTextFormatter
from formatters.general.bold import BoldTextFormatter
from formatters.general.italic import ItalicTextFormatter
from formatters.general.superscript import SuperScriptTextFormatter
from formatters.general.subscript import SubScriptTextFormatter
from formatters.general.decrease_size import DecreaseFontSizeFormatter
from formatters.general.increase_size import IncreaseFontSizeFormatter
from formatters.general.strikethrough import StrikeTextFormatter
from formatters.general.underline import UnderlineTextFormatter
from formatters.alignment.right_align import RightAlignFormatter
from formatters.alignment.center_align import CenterAlignFormatter
from formatters.alignment.justify_align import JustifyAlignFormatter
from formatters.alignment.left_align import LeftAlignFormatter


class TableInputDialog(QDialog):
    """
    Dialog window for inputting table dimensions.

    This dialog allows the user to input the amount rows and columns for a table.

    Attributes:
        rows_input (QLineEdit): Input field for the amount rows.
        columns_input (QLineEdit): Input field for the amount columns.
        ok_button (QPushButton): OK button for accepting the input.
        cancel_button (QPushButton): Cancel button for rejecting the input.
    """
    
    def __init__(self,
                 parent=None):
        super().__init__(parent)
        self.setWindowTitle('Table Dimensions')
        layout = QFormLayout(self)
        
        # Input fields for rows and columns
        self.rows_input = QLineEdit(self)
        self.columns_input = QLineEdit(self)
        layout.addRow('Rows:', self.rows_input)
        layout.addRow('Columns:', self.columns_input)
        
        # OK and Cancel buttons
        self.ok_button = QPushButton('OK', self)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.reject)
        layout.addRow(self.ok_button, self.cancel_button)
    
    def get_dimensions(self):
        """
        Get the dimensions entered by the user.

        Returns:
            tuple: A tuple containing the amount rows and columns entered by the user.
        """
        return self.rows_input.text(), self.columns_input.text()


class MainWindow(FramelessWindow, QtWidgets.QMainWindow, Ui_MainWindow):
    """
    The main window of the application.

    This class represents the main window of the application. It inherits from FramelessWindow,
    QtWidgets.QMainWindow, and Ui_MainWindow. It contains various models, setup functions,
    and operations related to the application.

    Attributes:
    - exercise_model: The exercise model.
    - tooth_model: The tooth model.
    - shower_model: The shower model.
    - hydro_model: The hydro model.
    - diet_model: The diet model.
    - lily_walk_note_model: The lily walk note model.
    - lily_note_model: The lily note model.
    - lily_room_model: The lily room model.
    - lily_walk_model: The lily walk model.
    - lily_mood_model: The lily mood model.
    - lily_diet_model: The lily diet model.
    - mmdmr_model: The mmdmr model.
    - cspr_model: The cspr model.
    - wefe_model: The wefe model.
    - btn_times: The button times.
    - sleep_quality_model: The sleep quality model.
    - woke_up_like_model: The woke up like model.
    - sleep_model: The sleep model.
    - total_hours_slept_model: The total hours slept model.
    - total_hrs_slept: The total hours slept.
    - basics_model: The basics model.
    - ui: The UI object.
    - db_manager: The database manager.
    - settings: The QSettings object.
    - window_controller: The WindowController object.

    Methods:
    - __init__: Initializes the MainWindow object.
    - commits_setup: Sets up the commits.
    - slider_set_spinbox: Connects sliders to spinboxes.
    - update_time: Updates the time displayed on the time_label widget.
    - update_beck_summary: Updates the averages of the sliders in the wellbeing and pain module.
    - init_hydration_tracker: Initializes the hydration tracker buttons.
    - switch_bds_page: Switches to the bds page.
    - switch_sleep_data_page: Switches to the sleep data page.
    - switch_to_diet_data_page: Switches to the diet data page.
    - switch_to_basics_data_page: Switches to the basics data page.
    - switch_to_mmdm_measures: Switches to the mmdm measures page.
    - switch_to_wefe_measures: Switches to the wefe measures page.
    - cspr_measures: Switches to the cspr measures page.
    - mmwefecspr_datapage: Switches to the mmwefecspr datapage.
    - switch_lilys_mod: Switches to the lilys mod page.
    - switch_to_lilys_dataviews: Switches to the lilys dataviews page.
    - auto_date_setters: Automatically sets the date for various widgets.
    - auto_time_setters: Automatically sets the time for various widgets.
    - app_operations: Performs various operations related to the application.
    """
    
    def __init__(self,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.sat_model = None
        self.fri_model = None
        self.wed_model = None
        self.thurs_model = None
        self.mon_model = None
        self.tues_model = None
        self.sun_model = None
        self.date_widgets = None
        self.date_highlighter = None
        self.day_buttons = None
        self.mmdmr_model = None
        self.cspr_model = None
        self.wefe_model = None
        self.context_menu = None
        self.exercise_model = None
        self.tooth_model = None
        self.shower_model = None
        self.hydro_model = None
        self.diet_model = None
        self.lily_walk_note_model = None
        self.lily_note_model = None
        self.lily_room_model = None
        self.lily_walk_model = None
        self.lily_mood_model = None
        self.lily_diet_model = None
        self.btn_times = None
        self.sleep_quality_model = None
        self.woke_up_like_model = None
        self.sleep_model = None
        self.total_hours_slept_model = None
        self.total_hrs_slept = None
        self.basics_model = None
        self.settings_manager_sunday = SettingsManagerAgendaSunday()
        self.settings_manager_monday = SettingsManagerAgendaMonday()
        self.settings_manager_tuesday = SettingsManagerAgendaTuesday()
        self.settings_manager_wednesday = SettingsManagerAgendaWednesday()
        self.settings_manager_thursday = SettingsManagerAgendaThursday()
        self.settings_manager_friday = SettingsManagerAgendaFriday()
        self.settings_manager_saturday = SettingsManagerAgendaSaturday()
        self.settings_manager_lilys_widgets = SettingsManagerLilysWidgets()
        self.text_formatter_color = ColorTextFormatter()
        self.text_formatter_bold = BoldTextFormatter()
        self.text_formatter_strikethrough = StrikeTextFormatter()
        self.text_formatter_decrease_font_size = DecreaseFontSizeFormatter()
        self.text_formatter_increase_font = IncreaseFontSizeFormatter()
        self.text_formatter_highlight = HighlightColorFormatter()
        self.text_formatter_italic = ItalicTextFormatter()
        self.text_formatter_underline = UnderlineTextFormatter()
        self.text_formatter_subscript = SubScriptTextFormatter()
        self.text_formatter_superscript = SuperScriptTextFormatter()
        # setup alignment formatters
        self.TextFormatCenter = CenterAlignFormatter()
        self.TextFormatRightAlign = RightAlignFormatter()
        self.TextFormatAlignLeft = LeftAlignFormatter()
        self.TextFormatJustify = JustifyAlignFormatter()
        # setup saving method for textedits
        self.text_edit_saver = TextEditSaver()
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.settings = QSettings(tkc.ORGANIZATION_NAME, tkc.APPLICATION_NAME)
        self.window_controller = WindowController()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.db_manager = DataManager()
        self.switch_page_view_setup()
        self.switch_page_agenda_view_setup()
        self.setup_models()
        self.restore_state()
        self.app_operations()
        self.commits_setup()
        self.delete_actions()
        self.sort_tables_by_date_desc()
        self.agendas_navigation()
        self.stack_navigation()
        self.hide_check_frame.setVisible(False)
        self.using_actions_checks_buttons()
        self.setup_formatting_actions()
        self.open_to_date()
        self.highlight_current_date()
        self.restore_visibility_state()
        self.auto_date_time_widgets()
        
        self.calculate_total_hours_slept()
        
        self.init_hydration_tracker()
        
        self.slider_set_spinbox()
    
    def sort_tables_by_date_desc(self):
        table_views = [self.wefe_tableview, self.cspr_tableview, self.mdmmr_tableview,
                       self.sleep_tableview, self.total_hours_slept_tableview,
                       self.woke_up_like_tableview, self.sleep_quality_tableview, self.shower_table,
                       self.teethbrushed_table, self.yoga_table, self.diet_table,
                       self.hydration_table, self.lily_diet_table, self.lily_mood_table,
                       self.lily_walk_table, self.time_in_room_table, self.lily_notes_table,
                       self.lily_walk_note_table]
        
        # Column index for the date column
        date_column_index = 1  # Adjust this to the correct column index for your date column
        for table_view in table_views:
            table_view.setSortingEnabled(True)
            table_view.sortByColumn(date_column_index, Qt.SortOrder.DescendingOrder)
    
    def commits_setup(self):
        """
        Sets up the methods with their buttons/actions to commit data relevant to the module. 
        
        This method calls several other methods to set up commits for different activities,
        such as sleep, total hours, woke up like, sleep quality, diet data, shower, exercise,
        teethbrush, lily diet data, lily mood data, lily walk, lily in room, lily notes data,
        lily walk notes data, mmdmr table, cspr table, wefe table, and slider set spinbox.
        """
        self.add_cspr_data()
        self.add_diet_data()
        self.add_exercise_data()
        self.add_lily_diet_data()
        self.add_lily_mood_data()
        self.add_lily_notes_data()
        self.add_lily_walk_notes_data()
        self.add_lily_walk_data()
        self.add_lily_time_in_room_data()
        self.add_mmdmr_data()
        self.add_shower_data()
        self.add_sleep_data()
        self.add_sleep_quality_data()
        self.add_wefe_data()
        self.add_woke_up_like_data()
        self.add_teethbrushing_data()
        self.add_total_hours_data()
        self.add_sunday_data()
        self.add_monday_data()
        self.add_tuesday_data()
        self.add_wednesday_data()
        self.add_thursday_data()
        self.add_friday_data()
        self.add_saturday_data()
    
    ##########################################################################################
    # APP-OPERATIONS setup
    ##########################################################################################
    def app_operations(self):
        """
        Performs the necessary operations for setting up the application.

        This method connects the currentChanged signal of the mainStack to the on_page_changed slot,
        hides the check frame, connects the triggered signal of the actionTotalHours to the
        calculate_total_hours_slept slot, and sets the current index of the mainStack based on the
        last saved index.

        Raises:
            Exception: If an error occurs while setting up the app_operations.

        """
        try:
            self.actionInjectDate.triggered.connect(self.inject_date)
            self.actionInjectTime.triggered.connect(self.inject_time)
            
            self.actionSave.triggered.connect(self.save_current_text)
            self.actionPrint.triggered.connect(self.print_current_textedit)
            self.agendaStack.currentChanged.connect(self.on_page_changed)
            self.actionInjectTable.triggered.connect(self.inject_table)
            self.actionToggleWeekBar.triggered.connect(lambda: toggle_views(
                self.week_frame))
            self.actionTotalHours.triggered.connect(self.calculate_total_hours_slept)
            self.actionExit.triggered.connect(self.close_app)
        except Exception as e:
            logger.error(f"Error in app_operation block : {e}", exc_info=True)
    
    def on_page_changed(self,
                        index):
        """
        Callback method triggered when the page is changed in the UI.

        Args:
            index (int): The index of the new page.
        """
        try:
            self.settings.setValue("lastPageIndex", index)
        except Exception as e:
            logger.error(f"An error occurred in on_page_changed {e}", exc_info=True)
    
    def close_app(self):
        self.close()
    
    def save_visibility_state(self,
                              key,
                              state):
        """
        Save the visibility state of a widget.

        Parameters:
            key (str): The key to identify the widget.
            state (bool): The visibility state of the widget.

        Returns:
            None
        """
        settings = QSettings(tkc.ORGANIZATION_NAME, tkc.APPLICATION_NAME)
        settings.setValue(key, state)
    
    def restore_visibility_state(self):
        """
        Restores the visibility state of various UI elements based on the saved settings.

        The visibility state of the following UI elements will be restored:
        - week_frame

        The visibility state is retrieved from the saved settings using QSettings.

        Returns:
            None
        """
        
        self.week_frame.setVisible(
            self.settings.value(
                'week_frame',
                False,
                type=bool
            )
        )
    
    #########################################################################
    # highlight_current_date DATE MAPPING METHOD
    #########################################################################
    def highlight_current_date(self) -> None:
        """
        Highlights the current date in the date widgets.

        This method initializes a dictionary of date widgets and creates a DateHighlighter object
        to highlight the current date in the UI.

        Raises:
            Exception: If an error occurs while highlighting the current date.

        Returns:
            None
        """
        try:
            self.date_widgets = {
                "sun_date": self.sun_date,
                "mon_date": self.mon_date,
                "tues_date": self.tues_date,
                "wed_date": self.wed_date,
                "thurs_date": self.thurs_date,
                "fri_date": self.fri_date,
                "sat_date": self.sat_date,
            }
            self.date_highlighter = DateHighlighter(self.date_widgets)
        except Exception as e:
            logger.exception(f"Error occurred when using highlight_current_date {e}",
                             exc_info=True)
    
    ##########################################################################
    # FORMATTER ACTIONS
    ##########################################################################
    def setup_formatting_actions(self) -> None:
        """
        Connects formatting operations to the respective actions.

        This method sets up the connections between various formatting actions and their
        corresponding formatting operations.
        It connects the actions to the appropriate methods of the text formatters, allowing the
        user to apply formatting
        to the text in the main window.

        Raises:
            Exception: If an error occurs during the formatting operations.

        Returns:
            None
        """
        try:
            # general formatting
            self.actionTextSubscript.triggered.connect(
                lambda: self.text_formatter_subscript.apply_current_text_format(
                    self.text_formatter_subscript.make_subscript
                )
            )
            self.actionTextSuperScript.triggered.connect(
                lambda: self.text_formatter_superscript.apply_current_text_format(
                    self.text_formatter_superscript.make_superscript
                )
            )
            self.actionTextBold.triggered.connect(
                lambda: self.text_formatter_bold.apply_current_text_format(
                    self.text_formatter_bold.make_bold
                )
            )
            self.actionTextItalic.triggered.connect(
                lambda: self.text_formatter_italic.apply_current_text_format(
                    self.text_formatter_italic.make_italic
                )
            )
            self.actionTextUnderline.triggered.connect(
                lambda: self.text_formatter_underline.apply_current_text_format(
                    self.text_formatter_underline.make_underline
                )
            )
            self.actionTextStrike.triggered.connect(
                lambda: self.text_formatter_strikethrough.apply_current_text_format(
                    self.text_formatter_strikethrough.make_strikethrough
                )
            )
            # colors
            self.actionTextHighlight.triggered.connect(
                lambda: self.text_formatter_highlight.apply_current_text_format(
                    self.text_formatter_highlight.format_text
                )
            )
            self.actionTextColor.triggered.connect(
                lambda: self.text_formatter_color.apply_current_text_format(
                    self.text_formatter_color.font_color
                )
            )
            # inc dec font size
            self.actionTextIncrease.triggered.connect(
                lambda: self.text_formatter_increase_font.apply_current_text_format(
                    self.text_formatter_increase_font.increase_font_size
                )
            )
            self.actionTextDecrease.triggered.connect(
                lambda: self.text_formatter_decrease_font_size.apply_current_text_format(
                    self.text_formatter_decrease_font_size.decrease_font_size
                )
            )
            # alignment
            self.actionTextAlignCenter.triggered.connect(
                lambda: self.TextFormatCenter.apply_current_text_alignment(
                    self.TextFormatCenter.center_text
                )
            )
            self.actionTextAlignRight.triggered.connect(
                lambda: self.TextFormatRightAlign.apply_current_text_alignment(
                    self.TextFormatRightAlign.right_align_text
                )
            )
            self.actionTextAlignLeft.triggered.connect(
                lambda: self.TextFormatAlignLeft.apply_current_text_alignment(
                    self.TextFormatAlignLeft.left_align_text
                )
            )
            self.actionTextAlignJustify.triggered.connect(
                lambda: self.TextFormatJustify.apply_current_text_alignment(
                    self.TextFormatJustify.justify_text
                )
            )
        
        except Exception as e:
            logger.error(f"Error occurred during formatting operations, {e}", exc_info=True)
    
    #########################################################################
    # Agenda_stack will open to current day in the Journal Mod
    #########################################################################
    def open_to_date(self):
        """
        Opens the agenda module to the current date.

        This method sets the current day in the agenda and agenda data stacks, maps the buttons
        to the current day,
        and checks the corresponding day buttons.

        Raises:
            AttributeError: If an attribute error occurs when setting up actions.

        """
        try:
            # get DEC 23 dec24JournJourn(previously codejourn) day
            current_day = datetime.datetime.today().weekday()
            # Adjust the value to match your setup
            if current_day == 6:  # if today is Sunday
                current_day = 0
            else:
                current_day += 1  # shift other days by +1
            self.agenda_journal_stack.setCurrentIndex(current_day)
            self.agenda_data_stack.setCurrentIndex(current_day)
            self.map_buttons_to_days()
            self.day_buttons[current_day].setChecked(True)
        
        except AttributeError as e:
            logger.exception(f"Error occurred when setting up actions:{e}", exc_info=True)
    
    #########################################################################
    # map_buttons_to_days
    #########################################################################
    def map_buttons_to_days(self) -> None:
        """
        Maps buttons to days.

        This method maps the day buttons to their corresponding days of the week.
        It creates a dictionary where the keys represent the day index (0-6) and the values
        represent the corresponding button object.

        Returns:
            None
        """
        try:
            self.day_buttons = {
                0: self.sun_journal_nav_btn, 1: self.mon_journal_nav_btn,
                2: self.tues_journal_nav_btn, 3: self.wed_journal_nav_btn,
                4: self.thurs_journal_nav_btn, 5: self.fri_journal_nav_btn,
                6: self.sat_journal_nav_btn,
            }
        
        except Exception as e:
            logger.error(f"An error in the map_buttons_to_days check it out! {e}",
                         exc_info=True)
    
    #########################################################################
    # Save CURRENT text setup to save[export] the current working Textedit
    #########################################################################
    def save_current_text(self) -> None:
        """
        Save the current text by updating the current text edit and then
        saving the current text edit.

        Raises:
            Exception: If there is an error while saving the current text.
        """
        try:
            self.update_current_text_edit()
            self.text_edit_saver.save_current_text()
        except Exception as e:
            logger.error(f"Error saving current text: {e}", exc_info=True)
    
    def inject_time(self):
        """
        Injects the current time into the focused QTextEdit widget.

        This method retrieves the currently focused widget and checks if it is an instance of QTextEdit.
        If it is, the current time is get and inserted into the QTextEdit widget using HTML formatting.

        Raises:
            Exception: If an error occurs during the injection process.

        """
        try:
            focused_widget = QApplication.instance().focusWidget()
            if isinstance(focused_widget, QTextEdit):
                text_edit = focused_widget
                current_time = QDateTime.currentDateTime().toString("h:mm AP")
                cursor = text_edit.textCursor()
                cursor.insertHtml(f"""
                                <strong><sup>it.is</sup></strong>{current_time}
                                """)
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
    
    def inject_date(self):
        """
        Injects text into the currently focused QTextEdit widget.

        This method retrieves the currently focused widget using QApplication.instance().focusWidget().
        If the focused widget is an instance of QTextEdit, it retrieves the text edit object and inserts
        the predefined text from the tkc.COURSEWORK variable at the current cursor position.

        Raises:
            Exception: If any error occurs during the injection process.

        """
        try:
            focused_widget = QApplication.instance().focusWidget()
            if isinstance(focused_widget, QTextEdit):
                text_edit = focused_widget
                current_date = QDate.currentDate().toString("MMM dd, yyyy")
                cursor = text_edit.textCursor()
                cursor.insertHtml(f"""
                                    <h3 style="font:12pt 'Helvetica-Neue'; letter-spacing:2px;">{current_date}</h3>
                                    """)
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
    
    def generate_table_html(self,
                            rows,
                            columns):
        """
        Generate an HTML table with the specified amount rows and columns.

        Args:
            rows (int): The several rows in the table.
            columns (int): The number of columns in the table.

        Returns:
            str: The HTML code for the generated table.

        Raises:
            Exception: If an error occurs while generating the table.

        """
        try:
            table_html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8">
            <title>Day at a Glance</title>
            <style>
                td {
                    border: 1px solid rgba(111,111,111, 0.34);
                    text-align: left;
                    padding:4px;
                }
            </style>
            </head>
            <body>
            """
            # table_html += f'Table of {rows} rows x {columns} columns'
            table_html += '<table>'
            for _ in range(rows):
                table_html += '<tr>'
                for _ in range(columns):
                    table_html += '<td></td>'
                table_html += '</tr>'
            table_html += '</table>'
            return table_html
        except Exception as e:
            logger.error(f"{e}")
    
    #########################################################################
    # Print support
    #########################################################################
    def update_current_text_edit(self):
        """
        Updates the current text edit.

        This method is responsible for updating the current text edit widget in the main window.
        It retrieves the currently focused widget using QApplication.instance().focusWidget() and
        checks if it is an instance of QTextEdit.
        If it is, it sets the current text edit using self.text_edit_saver.set_current_text_edit(
        focused_widget).
        Finally, it logs the update operation with the widget name.

        Raises:
            Exception: If there is an error updating the current text edit.
        """
        try:
            focused_widget = QApplication.instance().focusWidget()
            
            if isinstance(focused_widget, QTextEdit):
                self.text_edit_saver.set_current_text_edit(focused_widget)
                widget_name = (focused_widget.objectName() or "Unnamed QTextEdit")
                
                logger.debug(f"Current text edit updated for {widget_name}")
        except Exception as e:
            logger.error(f"Error updating current text edit: {e}", exc_info=True)
    
    #########################################################################
    # print_current_textedit support
    #########################################################################
    @staticmethod
    def print_current_textedit():
        """
        A method to print the content of the current QTextEdit widget,
        including logging the name of the QTextEdit being printed.

        This method retrieves the currently focused widget and checks if it is
        an instance of QTextEdit. If it is, it retrieves the widget's object name
        or uses a placeholder if the object name is not set. It then logs a debug
        message indicating that the current text edit is being printed for the
        specific widget.

        It creates a QPrintDialog to allow the user to select a printer and
        configure print settings. If the dialog is accepted, it prints the content
        of the focused QTextEdit widget using the selected printer. Finally, it
        logs a debug message indicating that the current text edit has been
        successfully printed.

        If any exception occurs during the process, an error message is logged
        along with the exception details.

        Raises:
            Exception: If an error occurs while printing the current text edit.
        """
        try:
            focused_widget = QApplication.instance().focusWidget()
            if isinstance(focused_widget, QTextEdit):
                # Attempt to retrieve the widget's object name, or use a
                # placeholder
                widget_name = (focused_widget.objectName() or "Unnamed QTextEdit")
                logger.debug(f"Printing current text edit for {widget_name}")
                
                dlg = QPrintDialog()
                if dlg.exec():
                    focused_widget.print(dlg.printer())
                    logger.debug(f"""Current text edit printed for
                                {widget_name}""")
        except Exception as e:
            logger.error(f"Error printing current text edit: {e}", exc_info=True)
    
    #########################################################################
    # Actions Check Buttons
    #########################################################################
    def using_actions_checks_buttons(self):
        """
        Connects each action to its corresponding button.

        This method creates a dictionary mapping action triggers to their corresponding buttons.
        It then loops through the dictionary and connects each action to its button using the
        `triggered` signal. When an action is triggered, the corresponding button will be checked.

        Returns:
            None
        """
        try:
            # A dictionary mapping action triggers to their corresponding button.
            action_to_button = {
                self.actionViewJournalSun: self.sun_journal_nav_btn,
                self.actionViewJournalMon: self.mon_journal_nav_btn,
                self.actionViewJournalTues: self.tues_journal_nav_btn,
                self.actionViewJournalWed: self.wed_journal_nav_btn,
                self.actionViewJournalThurs: self.thurs_journal_nav_btn,
                self.actionViewJournalFri: self.fri_journal_nav_btn,
                self.actionViewJournalSat: self.sat_journal_nav_btn,
            }
            
            # Loop through the dictionary and connect each action to its button.
            for action, button in action_to_button.items():
                action.triggered.connect(lambda checked, b=button: b.setChecked(True))
        except Exception as e:
            logger.error(f"An error occurred when using actions checks buttons {e}",
                         exc_info=True)
    
    #############################################################################################
    # Agenda Journal Navigation
    #############################################################################################
    def agendas_navigation(self):
        """
        Sets up the agenda navigation for the journal.

        This method connects actions and buttons to stack page indices for the agenda journal.
        It also sets up the pain rate sliders and connects them to the update_pain_sliders
        method.

        Raises:
            Exception: If an error occurs during the setup process.
        """
        try:
            # Mapping actions and buttons to stack page indices for the agenda journal
            action_to_page = {
                self.actionViewJournalSun: 0, self.actionViewJournalMon: 1,
                self.actionViewJournalTues: 2,
                self.actionViewJournalWed: 3, self.actionViewJournalThurs: 4,
                self.actionViewJournalFri: 5,
                self.actionViewJournalSat: 6,
            }
            
            agenda_navigation_btn = {
                self.sun_journal_nav_btn: 0, self.mon_journal_nav_btn: 1,
                self.tues_journal_nav_btn: 2, self.wed_journal_nav_btn: 3,
                self.thurs_journal_nav_btn: 4, self.fri_journal_nav_btn: 5,
                self.sat_journal_nav_btn: 6,
            }
            
            action_to_data_page = {
                self.actionViewJournalSun: 0, self.actionViewJournalMon: 1,
                self.actionViewJournalTues: 2,
                self.actionViewJournalWed: 3, self.actionViewJournalThurs: 4,
                self.actionViewJournalFri: 5,
                self.actionViewJournalSat: 6
            }
            
            alpha_stack_navigation_actions = {
                self.action_input_view_agenda: 0, self.action_data_view_agenda: 1,
            }
            try:
                # Main Stack Navigation
                for action, page in alpha_stack_navigation_actions.items():
                    action.triggered.connect(
                        lambda _, p=page: change_alpha_stack_page(self.agendaStack, p))
            except Exception as e:
                logger.error(f"An error occurred when setting up stack navigation {e}",
                             exc_info=True)
            # ACTIONS to change pages in the agenda module
            # cmd + 1-7, 1 being sunday, 7 being saturday :D
            for action, page in action_to_page.items():
                action.triggered.connect(
                    lambda _, p=page: change_agenda_stack_page(self.agenda_journal_stack, p))
            
            # BUTTONS for Agenda's SideBar
            # option + 1-7 (1 being sunday, this changes the data stack as below)
            for button, page in agenda_navigation_btn.items():
                button.clicked.connect(
                    lambda _, p=page: change_agenda_stack_page(self.agenda_journal_stack, p))
            # ACTION for DATA page
            for action, page in action_to_data_page.items():
                action.triggered.connect(
                    lambda _, p=page: change_agenda_stack_page(self.agenda_data_stack, p))
        
        except Exception as e:
            logger.error(f"An error has occurred: Navigation \n : {e}", exc_info=True)
    
    #########################################################################
    # UPDATE TIME support
    #########################################################################
    @staticmethod
    def update_time(state,
                    time_label):
        """
        Update the time displayed on the time_label widget based on the given state.

        Parameters:
        - state (int): The state of the time_label widget. If state is 2, the time_label will be
        updated.
        - time_label (QLabel): The QLabel widget to update with the current time.

        Returns:
        None

        Raises:
        None
        """
        try:
            if state == 2:  # checked state
                current_time = QTime.currentTime()
                time_label.setTime(current_time)
        except Exception as e:
            logger.error(f"Error updating time. {e}", exc_info=True)
    
    def init_hydration_tracker(self):
        """
        Initializes the hydration tracker buttons.

        This method connects the click events of the hydration tracker buttons
        to the `commit_hydration` method with the corresponding hydration amount.

        Raises:
            Exception: If there is an error initializing the hydration tracker buttons.

        """
        try:
            self.eight_ounce_cup.clicked.connect(
                lambda: self.commit_hydration(8)
            )
            self.sixteen_ounce_cup.clicked.connect(
                lambda: self.commit_hydration(16)
            )
            self.twenty_four_ounce_cup.clicked.connect(
                lambda: self.commit_hydration(24)
            )
            self.thirty_two_ounce_cup.clicked.connect(
                lambda: self.commit_hydration(32)
            )
        except Exception as e:
            logger.error(f"Error initializing hydration tracker buttons: {e}", exc_info=True)
    
    # ////////////////////////////////////////////////////////////////////////////////////////
    # SLIDER UPDATES SPINBOX/VICE VERSA SETUP
    # ////////////////////////////////////////////////////////////////////////////////////////
    def slider_set_spinbox(self):
        """
        Connects sliders to their corresponding spinboxes.

        This method establishes a connection between sliders and spinboxes
        by mapping each slider to its corresponding spinbox. It then calls
        the `connect_slider_spinbox` function to establish the connection.

        Returns:
            None
        """
        connect_slider_to_spinbox = {
            self.lily_time_in_room_slider: self.lily_time_in_room,
            self.lily_mood_slider: self.lily_mood,
            self.lily_mood_activity_slider: self.lily_activity,
            self.lily_gait_slider: self.lily_gait,
            self.lily_behavior_slider: self.lily_behavior,
            self.lily_energy_slider: self.lily_energy,
            self.woke_up_like_slider: self.woke_up_like,
            self.sleep_quality_slider: self.sleep_quality,
            self.wellbeing_slider: self.wellbeing_spinbox,
            self.excite_slider: self.excite_spinbox,
            self.focus_slider: self.focus_spinbox,
            self.energy_slider: self.energy_spinbox,
            self.mood_slider: self.mood,
            self.mania_slider: self.mania,
            self.depression_slider: self.depression,
            self.mixed_risk_slider: self.mixed_risk,
            self.calm_slider: self.calm_spinbox,
            self.stress_slider: self.stress_spinbox,
            self.rage_slider: self.rage_spinbox,
            self.pain_slider: self.pain_spinbox,
        }
        
        for slider, spinbox in connect_slider_to_spinbox.items():
            connect_slider_spinbox(slider, spinbox)
    
    # ####################################################################################
    # SWITCH PAGE METHODS
    # ####################################################################################
    
    def switch_page2(self,
                     page_widget,
                     width,
                     height):
        try:
            self.agendaStack.setCurrentWidget(page_widget)
            self.setFixedSize(width, height)
        except Exception as e:
            logger.error(f"{e}", exc_info=True)

    def switch_page(self,
                    page_widget,
                    width,
                    height):
        try:
            self.mainStack.setCurrentWidget(page_widget)
            self.setFixedSize(width, height)
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
            
    def switch_to_agenda_page(self):
        try:
            self.switch_page2(
                self.agendaInputPage,
                580, 480
            )
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
            
    def switch_agenda_size_large(self):
        try:
            self.switch_page2(
                self.agendaInputPage,
                720,
                840
            )
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
            
    def switch_agenda_size_medium(self):
        self.switch_page2(
            self.agendaInputPage,
            480, 360
        )
        
    def switch_agenda_size_small(self):
        self.switch_page2(
            self.agendaInputPage,
            360, 480
        )
        
    def switch_to_agenda_data_page(self):
        self.switch_page2(
            self.agendaJournsDataViewPage,
            400,
            600
        )
    
    def switch_bds_page(self):
        self.switch_page(
            self.bds_page,
            290,
            320
        )
    
    def switch_lilys_mod(self):
        self.switch_page(
            self.lilys_mod,
            290,
            320
        )
    
    def switch_to_mental_page(self):
        self.switch_page(
            self.mentalpage,
            290,
            330
        )
    
    def switch_to_mental_data_page(self):
        self.switch_page(
            self.mentaldatapage,
            745,
            540
        )
    
    def switch_sleep_data_page(self):
        self.switch_page(
            self.sleep_data_page,
            540,
            540
        )
    
    def switch_to_diet_data_page(self):
        self.switch_page(
            self.diet_data_page,
            800,
            540
        )
    
    def switch_to_basics_data_page(self):
        self.switch_page(
            self.basics_data_page,
            540,
            540
        )
    
    def switch_to_lilys_dataviews(self):
        self.switch_page(
            self.lilys_dataviews,
            860,
            456
        )
    
    def switch_page_agenda_view_setup(self):
        try:
            agenda_switch = {
                self.action_input_view_agenda: self.switch_to_agenda_page,
                self.action_data_view_agenda: self.switch_to_agenda_data_page,
                self.actionAgendaLarge: self.switch_agenda_size_large,
                self.actionAgendaMedium: self.switch_agenda_size_medium,
                self.actionAgendaSmall: self.switch_agenda_size_small
                # todo need to affix these to only transform the Agenda page.
            }
            
            for action, switchpage in agenda_switch.items():
                action.triggered.connect(switchpage)
                # TODO better exceptions
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
    
    def switch_page_view_setup(self):
        try:
            view_switch = {
                self.actionBDSInput: self.switch_bds_page,
                self.actionSleepDataView: self.switch_sleep_data_page,
                self.actionDietDataView: self.switch_to_diet_data_page,
                self.actionBasicsDataView: self.switch_to_basics_data_page,
                self.actionLilysPage: self.switch_lilys_mod,
                self.actionLilyDataView: self.switch_to_lilys_dataviews,
                self.actionMentalModsView: self.switch_to_mental_page,
                self.actionMentalDataView: self.switch_to_mental_data_page,
            }
            
            for action, switchview in view_switch.items():
                action.triggered.connect(switchview)
        
        except Exception as e:
            logger.error(f"{e}")
    
    def auto_date_time_widgets(self):
        """
        Initializes date and time widgets with current date and time values.
        """
        try:
            widget_date_edit = [
                self.mmdmr_date,
                self.wefe_date,
                self.cspr_date,
                self.diet_date,
                self.sleep_date,
                self.basics_date,
                self.lily_date,
            ]
            
            widget_time_edit = [
                self.mmdmr_time,
                self.wefe_time,
                self.cspr_time,
                self.diet_time,
                self.sleep_time,
                self.basics_time,
                self.lily_time,
            ]
            
            for widget in widget_date_edit:
                widget.setDate(QDate.currentDate())
            
            for widget in widget_time_edit:
                widget.setTime(QTime.currentTime())
        except Exception as e:
            logger.error(f"{e}")
    
    def commits_set_times(self):
        """
        Sets the times for various buttons in the UI.

        The times are stored in a dictionary where the keys are the buttons and the values are the corresponding times.
        The buttons and times are connected using the `btn_times` dictionary.

        Example:
            self.btn_times = {
                self.shower_c: self.basics_time,
                self.add_exercise_data: self.basics_time,
                self.add_teethbrushing_data: self.basics_time,
            }

        The lineEdits are then connected to the centralized function `btn_times` using a for loop.

        Returns:
            None
        """
        self.btn_times = {
            self.shower_c: self.basics_time,
            self.add_exercise_data: self.basics_time,
            self.add_teethbrushing_data: self.basics_time,
        }
        
        # Connect lineEdits to the centralized function
        for app_btns, times_edit in self.btn_times.items():
            btn_times(app_btns, times_edit)
    
    def calculate_total_hours_slept(self) -> None:
        """
        Calculates the total hours slept based on the awake time and asleep time.

        This method calculates the total hours slept by subtracting the awake time from the
        asleep time.
        If the time spans past midnight, it adds 24 hours worth of minutes to the total.
        The result is then converted to hours and minutes and displayed in the
        total_hours_slept_lineedit.

        Raises:
            Exception: If an error occurs while calculating the total hours slept.

        """
        
        try:
            time_asleep = self.time_awake.time()
            time_awake = self.time_asleep.time()
            
            # Convert time to total minutes since the start of the day
            minutes_asleep = (time_asleep.hour() * 60 + time_asleep.minute())
            minutes_awake = (time_awake.hour() * 60 + time_awake.minute())
            
            # Calculate the difference in minutes
            total_minutes = minutes_asleep - minutes_awake
            
            # Handle case where the time spans past midnight
            if total_minutes < 0:
                total_minutes += (24 * 60)  # Add 24 hours worth of minutes
            
            # Convert back to hours and minutes
            hours = total_minutes // 60
            minutes = total_minutes % 60
            
            # Create the total_hours_slept string in HH:mm format
            self.total_hrs_slept = f"{hours:02}:{minutes:02}"
            
            # Update the lineEdit with the total hours slept
            self.total_hours_slept.setText(self.total_hrs_slept)
        
        except Exception as e:
            logger.error(f"Error occurred while calculating total hours slept {e}", exc_info=True)
    
    def inject_table(self):
        """
        Opens a dialog to input table dimensions and inserts an HTML table into the focused QTextEdit widget.

        Raises:
            Exception: If an error occurs during the table injection process.
        """
        try:
            dialog = TableInputDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                rows, columns = map(int, dialog.get_dimensions())
                html = self.generate_table_html(rows, columns)
                focused_widget = QApplication.instance().focusWidget()
                if focused_widget and isinstance(focused_widget, QTextEdit):
                    text_edit = focused_widget
                    cursor = text_edit.textCursor()
                    cursor.insertHtml(html)
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
    
    def stack_navigation(self):
        """
        Handles the stack navigation for the main window.

        This method maps actions and buttons to stack page indices for the agenda journal.
        It connects the actions to the corresponding pages in the stack.

        Raises:
            Exception: If an error occurs during the stack navigation.

        """
        try:
            # Mapping actions and buttons to stack page indices for the agenda journal
            mainStackNavvy = {
                self.action_input_view_agenda: 0,
                self.actionBDSInput: 1,
                self.actionLilysPage: 2,
                self.actionMentalModsView: 3,
                self.actionSleepDataView: 4,
                self.actionDietDataView: 5,
                self.actionBasicsDataView: 6,
                self.actionLilyDataView: 7,
                self.actionMentalDataView: 8,
            }
            
            # Main Stack Navigation
            for action, page in mainStackNavvy.items():
                action.triggered.connect(
                    lambda _, p=page: change_mainStack(self.mainStack, p))
        
        except Exception as e:
            logger.error(f"An error has occurred: {e}", exc_info=True)
    
    # ##########################################################################################
    # ##########################################################################################
    #           COMMITS COMMITS COMMITS COMMITS COMMITS COMMITS COMMITS COMMITS COMMITS
    # ##########################################################################################
    # ##########################################################################################
    def add_sunday_data(self):
        """
        Connects the 'triggered' signal of actionSunday to the agenda_data_sunday function with the necessary arguments.
        """
        try:
            self.actionSunday.triggered.connect(lambda: agenda_data_sunday(self, {
                "sun_date": "sun_date", "sun_note_one": "sun_note_one", "model": "sun_model",
            },
                                                                           self.db_manager.insert_into_sunday_table))
        except Exception as e:
            logger.error(f"Unable to commit Sunday's Journ, sunday forfeits!{e}", exc_info=True)
    
    def add_monday_data(self):
        try:
            self.actionMonday.triggered.connect(lambda: agenda_data_monday(self, {
                "mon_date": "mon_date", "mon_note_one": "mon_note_one", "model": "mon_model",
            },
                                                                           self.db_manager.insert_into_monday_table, ))
        except Exception as e:
            logger.error(f"Unable to commit Monday's Journ, monday forfeits! {e}",
                         exc_info=True)
    
    def add_tuesday_data(self):
        try:
            self.actionTuesday.triggered.connect(lambda: agenda_data_tuesday(self, {
                "tues_date": "tues_date", "tues_note_one": "tues_note_one",
                "model": "tues_model",
            }, self.db_manager.insert_into_tuesday_table))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def add_wednesday_data(self):
        try:
            self.actionWednesday.triggered.connect(lambda: agenda_data_wednesday(self, {
                "wed_date": "wed_date", "wed_note_one": "wed_note_one", "model": "wed_model",
            }, self.db_manager.insert_into_wednesday_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def add_thursday_data(self):
        try:
            self.actionThursday.triggered.connect(lambda: agenda_data_thursday(self, {
                "thurs_date": "thurs_date", "thurs_note_one": "thurs_note_one",
                "model": "thurs_model",
            }, self.db_manager.insert_into_thursday_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def add_friday_data(self):
        try:
            self.actionFriday.triggered.connect(lambda: agenda_data_friday(self, {
                "fri_date": "fri_date", "fri_note_one": "fri_note_one", "model": "fri_model",
            }, self.db_manager.insert_into_friday_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def add_saturday_data(self):
        try:
            self.actionSaturday.triggered.connect(lambda: agenda_data_saturday(self, {
                "sat_date": "sat_date", "sat_note_one": "sat_note_one", "model": "sat_model",
            }, self.db_manager.insert_into_saturday_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def add_sleep_data(self):
        """
        Connects the 'Commit Sleep' action to the 'add_sleep_data' function and inserts the sleep data into the sleep table.

        Raises:
            Exception: If an error occurs during the connection or insertion process.
        """
        try:
            self.actionCommitSleep.triggered.connect(lambda: add_sleep_data(self, {
                "sleep_date": "sleep_date",
                "time_asleep": "time_asleep",
                "time_awake": "time_awake",
                "model": "sleep_model",
            }, self.db_manager.insert_into_sleep_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def add_total_hours_data(self):
        """
        Connects the 'CommitSleep' action to the 'add_total_hours_slept_data' function and inserts data into the 
        'total_hours_slept_table' in the database.

        Raises:
            Exception: If an error occurs during the execution of the method.

        """
        try:
            self.actionCommitSleep.triggered.connect(lambda: add_total_hours_slept_data(self, {
                "sleep_date": "sleep_date", "total_hours_slept": "total_hours_slept", "model":
                    "total_hours_slept_model",
            }, self.db_manager.insert_into_total_hours_slept_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def add_woke_up_like_data(self):
        """
        Connects the 'Commit Sleep' action to the 'add_woke_up_like_data' function.

        This method connects the 'triggered' signal of the 'actionCommitSleep' QAction to the 'add_woke_up_like_data'
        function. It passes the necessary parameters to the function and inserts the data into the 'woke_up_like' table
        using the 'db_manager' object.

        Raises:
            Exception: If an error occurs during the connection or data insertion, an exception is raised.

        """
        try:
            self.actionCommitSleep.triggered.connect(lambda: add_woke_up_like_data(self, {
                "sleep_date": "sleep_date",
                "woke_up_like": "woke_up_like",
                "model": "woke_up_like_model",
            }, self.db_manager.insert_woke_up_like_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def add_sleep_quality_data(self):
        """
        Connects the 'Commit Sleep' action to the 'add_sleep_quality_data' function and inserts the sleep quality data
        into the sleep quality table in the database.

        Raises:
            Exception: If an error occurs during the execution of the method.

        """
        try:
            self.actionCommitSleep.triggered.connect(lambda: add_sleep_quality_data(self, {
                "sleep_date": "sleep_date", "sleep_quality": "sleep_quality", "model":
                    "sleep_quality_model",
            },
                                                                                    self.db_manager.insert_into_sleep_quality_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def add_diet_data(self):
        """
        Connects the 'Commit Diet' action to the 'add_diet_data' function and inserts the diet data into the database.

        Raises:
            Exception: If an error occurs during the process.

        """
        try:
            self.actionCommitDiet.triggered.connect(lambda: add_diet_data(self, {
                "diet_date": "diet_date", "diet_time": "diet_time", "food_eaten": "food_eaten",
                "calories": "calories", "model": "diet_model",
            }, self.db_manager.insert_into_diet_table, ))
        except Exception as e:
            logger.error(f"An error has occurred: {e}", exc_info=True)
    
    def commit_hydration(self,
                         amount):
        """
        Commits the hydration data to the database.

        Args:
            amount (int): The amount of water in ounces.

        Raises:
            Exception: If an error occurs while committing the hydration data.

        Returns:
            None
        """
        try:
            date = QDate.currentDate().toString("yyyy-MM-dd")
            time = QTime.currentTime().toString("hh:mm:ss")
            self.db_manager.insert_into_hydration_table(date, time, amount)
            logger.info(f"Committed {amount} oz of water at {date} {time}")
            self.hydro_model.select()
        except Exception as e:
            logger.error(f"Error committing hydration data: {e}", exc_info=True)
    
    def add_shower_data(self):
        """
        Connects the 'clicked' signal of the 'shower_c' button to the 'add_shower_data' function,
        passing the necessary parameters and calling the 'insert_into_shower_table' method of the 'db_manager' object.

        Raises:
            Exception: If an error occurs during the process.

        """
        try:
            self.shower_c.clicked.connect(lambda: add_shower_data(self, {
                "basics_date": "basics_date", "basics_time": "basics_time",
                "shower_check": "shower_check", "model": "shower_model",
            },
                                                                  self.db_manager.insert_into_shower_table, ))
        except Exception as e:
            logger.error(f"An error occurred: {e}", exc_info=True)
    
    def add_exercise_data(self):
        """
        Connects the `yoga_commit` button to the `add_exercise_data` function with the specified arguments.

        This method is responsible for setting up the connection between the `yoga_commit` button and the `add_exercise_data` function.
        It passes the necessary arguments to the `add_exercise_data` function, which is responsible for inserting exercise data into the exercise table.

        Args:
            self: The instance of the class.

        Returns:
            None
        """
        self.yoga_commit.clicked.connect(lambda: add_exercise_data(self, {
            "basics_date": "basics_date", "basics_time": "basics_time",
            "exerc_check": "exerc_check", "model": "exercise_model",
        }, self.db_manager.insert_into_exercise_table, ))
    
    def add_teethbrushing_data(self):
        """
        Connects the `clicked` signal of the `teeth_commit` button to the `add_teethbrush_data` function.

        The `add_teethbrush_data` function is called with the following parameters:
        - `self`: The instance of the main window class.
        - A dictionary containing the data to be passed to the `add_teethbrush_data` function.
        - `self.db_manager.insert_into_tooth_table`: The method to be called when inserting data into the tooth table.

        This method is responsible for handling the commit action when the `teeth_commit` button is clicked.
        """
        self.teeth_commit.clicked.connect(lambda: add_teethbrush_data(self, {
            "basics_date": "basics_date", "basics_time": "basics_time",
            "tooth_check": "tooth_check", "model": "tooth_model",
        }, self.db_manager.insert_into_tooth_table, ))
    
    def add_lily_diet_data(self):
        """
        Connects the `lily_ate_check` button click event to the `add_lily_diet_data` function.

        The `add_lily_diet_data` function is called with the following parameters:
        - `self`: The current instance of the class.
        - A dictionary containing the data to be passed to the `add_lily_diet_data` function:
            - "lily_date": The value of the "lily_date" attribute.
            - "lily_time": The value of the "lily_time" attribute.
            - "model": The value of the "lily_diet_model" attribute.
        - `self.db_manager.insert_into_lily_diet_table`: The function to be called when the button is clicked.

        Raises:
            Exception: If an error occurs during the execution of the method.

        """
        try:
            self.lily_ate_check.clicked.connect(lambda: add_lily_diet_data(self, {
                "lily_date": "lily_date", "lily_time": "lily_time",
                "model": "lily_diet_model",
            }, self.db_manager.insert_into_lily_diet_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def add_lily_mood_data(self):
        """
        Connects the 'commit_mood' action to the 'add_lily_mood_data' function and passes the necessary data to it.

        This method connects the 'commit_mood' action to the 'add_lily_mood_data' function, which is responsible for inserting
        Lily's mood data into the database. It sets up the necessary data and connects the action to the function using a lambda
        function. The lambda function passes the required data and the function to be called when the action is triggered.

        Parameters:
            self (MainWindow): The instance of the main window.

        Returns:
            None
        """
        try:
            self.actionCommitLilyMood.triggered.connect(lambda: add_lily_mood_data(self, {
                "lily_date": "lily_date",
                "lily_time": "lily_time",
                "lily_mood_slider": "lily_mood_slider",
                "lily_energy_slider": "lily_energy_slider",
                "lily_mood_activity_slider": "lily_mood_activity_slider",
                "model": "lily_mood_model",
            }, self.db_manager.insert_into_lily_mood_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def add_lily_notes_data(self):
        """
        Connects the 'commit_lily_notes' action to the 'add_lily_note_data' function.

        This method connects the 'commit_lily_notes' action to the 'add_lily_note_data' function,
        passing the necessary parameters. It handles any exceptions that occur and logs an error message.

        Parameters:
        - self: The instance of the main window.

        Returns:
        - None
        """
        try:
            self.lily_note_commit_btn.clicked.connect(lambda: add_lily_note_data(self, {
                "lily_date": "lily_date", "lily_time": "lily_time",
                "lily_notes": "lily_notes",
                "model": "lily_note_model",
            }, self.db_manager.insert_into_lily_notes_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def add_lily_walk_data(self):
        """
        Connects the `lily_walk_btn` button to the `add_lily_walk_data` function with specified arguments.

        This method is responsible for setting up the connection between the `lily_walk_btn` button and the `add_lily_walk_data` function.
        It passes a dictionary of data and a callback function to the `add_lily_walk_data` function.

        Args:
            self: The instance of the class.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the connection setup.

        """
        try:
            self.lily_walk_btn.clicked.connect(lambda: add_lily_walk_data(self, {
                "lily_date": "lily_date", "lily_time": "lily_time",
                "lily_behavior_slider": "lily_behavior_slider",
                "lily_gait_slider": "lily_gait_slider",
                "model": "lily_walk_model"
            }, self.db_manager.insert_into_wiggles_walks_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def add_lily_time_in_room_data(self):
        """
        Connects the 'commit_room_time' action to the 'add_time_in_room_data' function,
        passing the necessary parameters and inserting the data into the time in room table.

        Raises:
            Exception: If an error occurs during the commit process.

        """
        try:
            self.actionCommitLilysTimeInRoom.triggered.connect(lambda: add_time_in_room_data(self, {
                "lily_date": "lily_date", "lily_time": "lily_time", "lily_time_in_room_slider":
                    "lily_time_in_room_slider", "model": "lily_room_model"
            }, self.db_manager.insert_into_time_in_room_table))
        except Exception as e:
            logger.error(f"Error occurring during in_room commit main_window.py loc. {e}",
                         exc_info=True)
    
    def add_lily_walk_notes_data(self):
        """
        Connects the `lily_walk_btn` button to the `add_lily_walk_notes` function with specified
        arguments.

        This method sets up the connection between the `lily_walk_btn` button and the
        `add_lily_walk_notes` function.
        When the button is clicked, it calls the `add_lily_walk_notes` function with the provided
        arguments.

        Args:
            self: The instance of the main window class.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the connection setup.

        """
        try:
            self.lily_walk_note_commit_btn.clicked.connect(lambda: add_lily_walk_notes(self, {
                "lily_date": "lily_date", "lily_time": "lily_time",
                "lily_walk_note": "lily_walk_note", "model": "lily_walk_note_model"
            }, self.db_manager.insert_into_lily_walk_notes_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def add_mmdmr_data(self) -> None:
        """
        Connects the 'commit' action to the 'add_mentalsolo_data' function and inserts data into
        the mmdmr_table.

        This method connects the 'commit' action to the 'add_mentalsolo_data' function, which is
        responsible for inserting data into the mmdmr_table. It sets up the connection using the
        `triggered.connect()` method and passes the necessary data to the `add_mentalsolo_data`
        function.

        Raises:
            Exception: If an error occurs during the process.
        """
        try:
            self.actionCommitMMDMr.triggered.connect(
                lambda: add_mentalsolo_data(
                    self, {
                        "mmdmr_date": "mmdmr_date",
                        "mmdmr_time": "mmdmr_time",
                        "mood_slider": "mood_slider",
                        "mania_slider": "mania_slider",
                        "depression_slider": "depression_slider",
                        "mixed_risk_slider": "mixed_risk_slider",
                        "model": "mmdmr_model"
                    },
                    self.db_manager.insert_into_mmdmr_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def add_cspr_data(self) -> None:
        """
        Connects the 'Commit CSPR' action to the 'add_cspr_data' function and inserts the CSPR exam
        data into the database.

        Raises:
            Exception: If an error occurs during the execution of the method.
        """
        try:
            self.actionCommitCSPR.triggered.connect(
                lambda: add_cspr_data(
                    self, {
                        "cspr_date": "cspr_date",
                        "cspr_time": "cspr_time",
                        "calm_slider": "calm_slider",
                        "stress_slider": "stress_slider",
                        "pain_slider": "pain_slider",
                        "rage_slider": "rage_slider",
                        "model": "cspr_model"
                    },
                    self.db_manager.insert_into_cspr_exam, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def add_wefe_data(self) -> None:
        """
        Connects the actionCommitWEFE signal to the add_wefe_data function with the specified parameters.
        Inserts the WEFE data into the WEFE table using the db_manager.

        Raises:
            Exception: If an error occurs during the execution of the method.
        """
        try:
            self.actionCommitWEFE.triggered.connect(
                lambda: add_wefe_data(
                    self, {
                        "wefe_date": "wefe_date",
                        "wefe_time": "wefe_time",
                        "wellbeing_slider": "wellbeing_slider",
                        "excite_slider": "excite_slider",
                        "focus_slider": "focus_slider",
                        "energy_slider": "energy_slider",
                        "model": "wefe_model"
                    },
                    self.db_manager.insert_into_wefe_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def setup_models(self) -> None:
        """
        Set up models for various tables in the main window.

        This method creates and sets models for different tables in the main window.
        It uses the `create_and_set_model` function to create and set the models.

        Raises:
            Exception: If there is an error setting up the models.

        """
        try:
            self.wefe_model = create_and_set_model(
                "wefe_table",
                self.wefe_tableview
            )
            
            self.cspr_model = create_and_set_model(
                "cspr_table",
                self.cspr_tableview
            )
            
            self.mmdmr_model = create_and_set_model(
                "mmdmr_table",
                self.mdmmr_tableview
            )
            
            self.sleep_model = create_and_set_model(
                "sleep_table",
                self.sleep_tableview
            )
            
            self.total_hours_slept_model = create_and_set_model(
                "total_hours_slept_table",
                self.total_hours_slept_tableview
            )
            
            self.woke_up_like_model = create_and_set_model(
                "woke_up_like_table",
                self.woke_up_like_tableview)
            
            self.sleep_quality_model = create_and_set_model(
                "sleep_quality_table",
                self.sleep_quality_tableview)
            
            self.shower_model = create_and_set_model(
                "shower_table",
                self.shower_table
            )
            # SLEEP: model creates and set
            
            self.tooth_model = create_and_set_model(
                "tooth_table",
                self.teethbrushed_table
            )
            
            self.exercise_model = create_and_set_model(
                "exercise_table",
                self.yoga_table
            )
            
            self.diet_model = create_and_set_model(
                "diet_table",
                self.diet_table
            )
            
            self.hydro_model = create_and_set_model(
                "hydration_table",
                self.hydration_table
            )
            
            self.lily_diet_model = create_and_set_model(
                "lily_diet_table",
                self.lily_diet_table
            )
            
            self.lily_mood_model = create_and_set_model(
                "lily_mood_table",
                self.lily_mood_table
            )
            
            self.lily_walk_model = create_and_set_model(
                "lily_walk_table",
                self.lily_walk_table
            )
            
            self.lily_room_model = create_and_set_model(
                "lily_in_room_table",
                self.time_in_room_table
            )
            
            self.lily_note_model = create_and_set_model(
                "lily_notes_table",
                self.lily_notes_table
            )
            
            self.lily_walk_note_model = create_and_set_model(
                "lily_walk_notes_table",
                self.lily_walk_note_table
            )
            self.sun_model = create_and_set_model(
                "sunday_table",
                self.sun_table
            )
            self.mon_model = create_and_set_model(
                "monday_table",
                self.mon_table
            )
            self.tues_model = create_and_set_model(
                "tuesday_table",
                self.tues_table
            )
            self.wed_model = create_and_set_model(
                "wednesday_table",
                self.wed_table
            )
            self.thurs_model = create_and_set_model(
                "thursday_table",
                self.thurs_table
            )
            self.fri_model = create_and_set_model(
                "friday_table",
                self.fri_table
            )
            self.sat_model = create_and_set_model(
                "saturday_table",
                self.sat_table
            )
        except Exception as e:
            logger.error(f"Error setting up models: {e}", exc_info=True)
    
    def delete_actions(self):
        """
        Connects the `actionDelete` trigger to multiple `delete_selected_rows` functions for different tables and models.
        """
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'wefe_tableview',
                    'wefe_model'
                )
            )
        except Exception as e:
            logger.error(f"Error deleting wefe records: {e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'cspr_tableview',
                    'cspr_model'
                )
            )
        except Exception as e:
            logger.error(f"Error deleting cspr records: {e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'mdmmr_tableview',
                    'mmdmr_model'
                )
            )
        except Exception as e:
            logger.error(f"Error deleting sleep records: {e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'sleep_tableview',
                    'sleep_model'
                )
            )
        except Exception as e:
            logger.error(f"Error deleting total hours slept records: {e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'total_hours_slept_tableview',
                    'total_hours_slept_model'
                )
            )
        except Exception as e:
            logger.error(f"Error deleting total hours slept records: {e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'woke_up_like_tableview',
                    'woke_up_like_model'
                )
            )
        except Exception as e:
            logger.error(f"Error deleting woke up like records : {e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'sleep_quality_tableview',
                    'sleep_quality_model'
                )
            )
        except Exception as e:
            logger.error(f"Error deleting sleep quality records : {e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'shower_table',
                    'shower_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'teethbrushed_table',
                    'tooth_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'yoga_table',
                    'exercise_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'diet_table',
                    'diet_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'hydration_table',
                    'hydro_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'lily_walk_table',
                    'lily_walk_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'lily_diet_table',
                    'lily_diet_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'lily_mood_table',
                    'lily_mood_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'time_in_room_table',
                    'lily_room_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'lily_notes_table',
                    'lily_note_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'lily_walk_note_table',
                    'lily_walk_note_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'sun_table',
                    'sun_model'
                )
            )
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'mon_table',
                    'mon_model'
                )
            )
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'tues_table',
                    'tues_model'
                )
            )
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'wed_table',
                    'wed_model'
                )
            )
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'thurs_table',
                    'thurs_model'
                )
            )
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'fri_table',
                    'fri_model'
                )
            )
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
            
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'sat_table',
                    'sat_model'
                )
            )
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
            
    def save_state(self):
        """
        Saves the state of the main window.

        This method saves the values of various sliders, inputs, and other UI elements
        as well as the window geometry and state to the application settings.

        Raises:
            Exception: If there is an error while saving the state.

        """
        try:
            self.settings_manager_sunday.save_sun_journal(
                self.sun_date,
                self.sun_note_one
            )
            
            self.settings_manager_monday.save_mon_journal(
                self.mon_date,
                self.mon_note_one,
            )
            
            self.settings_manager_tuesday.save_tues_journal(
                self.tues_date,
                self.tues_note_one,
            )
            
            self.settings_manager_wednesday.save_wed_journal(
                self.wed_date,
                self.wed_note_one
            )
            
            self.settings_manager_thursday.save_thurs_journal(
                self.thurs_date,
                self.thurs_note_one,
            )
            
            self.settings_manager_friday.save_fri_journal(
                self.fri_date,
                self.fri_note_one,
            )
            
            self.settings_manager_saturday.save_sat_journal(
                self.sat_date,
                self.sat_note_one,
            )
            
            self.settings_manager_lilys_widgets.save_lilys_widget_states(
                self.lily_time_in_room_slider,
                self.lily_mood_slider,
                self.lily_mood_activity_slider,
                self.lily_energy_slider,
                self.lily_time_in_room,
                self.lily_mood,
                self.lily_activity,
                self.lily_energy,
                self.lily_notes,
            )
            
            self.settings.setValue(
                "geometry",
                self.saveGeometry())
            
            self.settings.setValue(
                "windowState",
                self.saveState())
            
        except Exception as e:
            logger.error(f"Geometry not good fail. {e}", exc_info=True)
    
    def restore_state(self) -> None:
        """
        Restores the state of the main window by retrieving values from the settings.

        This method restores the values of various sliders, text fields, and window geometry
        from the settings. If an error occurs during the restoration process, it is logged
        with the corresponding exception.

        Returns:
            None
        """
        try:
            self.settings_manager_sunday.restore_sun_journal(
                self.sun_date,
                self.sun_note_one,
            )
            self.settings_manager_monday.restore_mon_journal(
                self.mon_date,
                self.mon_note_one,
            )
            self.settings_manager_tuesday.restore_tues_journal(
                self.tues_date,
                self.tues_note_one,
            )
            self.settings_manager_wednesday.restore_wed_journal(
                self.wed_date,
                self.wed_note_one,
            )
            self.settings_manager_thursday.restore_thurs_journal(
                self.thurs_date,
                self.thurs_note_one
            )
            self.settings_manager_friday.restore_fri_journal(
                self.fri_date,
                self.fri_note_one,
            )
            self.settings_manager_saturday.restore_sat_journal(
                self.sat_date,
                self.sat_note_one,
            )
            self.settings_manager_lilys_widgets.restore_lilys_widget_states(
                self.lily_time_in_room_slider,
                self.lily_mood_slider,
                self.lily_mood_activity_slider,
                self.lily_energy_slider,
                self.lily_time_in_room,
                self.lily_mood,
                self.lily_activity,
                self.lily_energy,
                self.lily_notes,
            )
            # # TODO: AGAIN PLACE THESE IN A SEPARATE MANAGER KKthx self.
            # # RESTORE LILYS MODULE
            # self.lily_time_in_room_slider.setValue(
            #     self.settings.value('lily_time_in_room_slider', 0, type=int))
            #
            # self.lily_mood_slider.setValue(
            #     self.settings.value('lily_mood_slider', 0, type=int))
            #
            # self.lily_mood_activity_slider.setValue(
            #     self.settings.value('lily_mood_activity_slider', 0, type=int))
            #
            # self.lily_energy_slider.setValue(
            #     self.settings.value('lily_energy_slider', 0, type=int))
            #
            # self.lily_time_in_room.setValue(
            #     self.settings.value('lily_time_in_room', 0, type=int))
            #
            # self.lily_mood.setValue(
            #     self.settings.value('lily_mood', 0, type=int))
            #
            # self.lily_activity.setValue(
            #     self.settings.value('lily_activity', 0, type=int))
            #
            # self.lily_energy.setValue(
            #     self.settings.value('lily_energy', 0, type=int))
            #
            # self.lily_notes.setHtml(
            #     self.settings.value('lily_notes', "", type=str))
            #
            # restore window geometry state
            self.restoreGeometry(
                self.settings.value("geometry", QByteArray()))
            
            self.restoreState(
                self.settings.value("windowState", QByteArray()))
        except Exception as e:
            logger.error(f"Error restoring WINDOW STATE {e}", exc_info=True)
    
    def closeEvent(self,
                   event: QCloseEvent) -> None:
        """
        Event handler for the close event of the main window.

        This method is called when the user tries to close the main window.
        It saves the state of the application before closing.

        Args:
            event (QCloseEvent): The close event object.

        Returns:
            None
        """
        try:
            try:
                self.save_visibility_state(
                    'week_frame',
                    self.week_frame.isVisible()
                )
            except Exception as e:
                logger.error(f"Error saving visibility state for week_frame: {e}", exc_info=True)
            self.save_state()
        except Exception as e:
            logger.error(f"error saving state during closure: {e}", exc_info=True)

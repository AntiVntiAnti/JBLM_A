from PyQt6.QtCore import QDate
from logger_setup import logger


def agenda_data_thursday(main_window_instance, widget_names, db_insert_method):
    """
    Generates the data to be inserted into the database for the Thursday agenda.

    Parameters:
    - main_window_instance: The instance of the main window.
    - widget_names: A dictionary containing the names of the widgets.
    - db_insert_method: The method used to insert data into the database.

    Returns:
    None
    """
    try:
        # Get the date for this week'
        widget_methods = {
            widget_names['thurs_date']: (None, 'date', 'dd-MM-yyyy'),
            widget_names['thurs_note_one']: (widget_names['thurs_note_one'], 'toPlainText', ""),
        }

        data_to_insert = []
        for widget_name, (widget_attr, method, format_type) in widget_methods.items():
            widget = getattr(main_window_instance, widget_name)
            value = getattr(widget, method)()
            if format_type:
                value = value.toString(format_type)
            data_to_insert.append(value)

        db_insert_method(*data_to_insert)
        reset_agenda_thurs(main_window_instance, widget_names)
    except Exception as e:
        logger.error(f"Error: adding thursdays data to database {e}", exc_info=True)

def reset_agenda_thurs(main_window_instance, widget_names):
    """
    Reset the agenda for Thursday.

    Parameters:
    - main_window_instance: The instance of the main window.
    - widget_names: A dictionary containing the names of the widgets.

    Returns:
    None
    """
    try:
        getattr(main_window_instance, widget_names['thurs_date']).setDate(QDate.currentDate())
        getattr(main_window_instance, widget_names['thurs_note_one']).clear()

        # Assuming there is a model for each day
        getattr(main_window_instance, widget_names['model']).select()
    except Exception as e:
        logger.error(f"Error: resetting thursdays agenda {e}", exc_info=True)
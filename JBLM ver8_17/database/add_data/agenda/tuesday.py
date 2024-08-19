from PyQt6.QtCore import QDate
from logger_setup import logger


def agenda_data_tuesday(main_window_instance, widget_names, db_insert_method):
    """
    Generate the agenda data for Tuesday.

    Args:
        main_window_instance (MainWidget): An instance of the main window.
        widget_names (dict): A dictionary containing the names of the widgets.
        db_insert_method (function): A function to insert data into the database.

    Returns:
        None

    Description:
        This function generates the agenda data for Tuesday based on the provided
        main window instance, widget names, and database insert method. It retrieves
        the values from the specified widgets, formats them if necessary, and appends
        them to a data list. Finally, it calls the database insert method with the
        generated data and resets the agenda for Tuesday.

    Usage:
        agenda_data_tuesday(main_window_instance, widget_names, db_insert_method)
    """

    try:
        widget_methods = {
            widget_names['tues_date']: (None, 'date', 'dd-MM-yyyy'),
            widget_names['tues_note_one']: (widget_names['tues_note_one'], 'toPlainText', ""),
        }

        data_to_insert = []
        for widget_name, (widget_attr, method, format_type) in widget_methods.items():
            widget = getattr(main_window_instance, widget_name)
            value = getattr(widget, method)()
            if format_type:
                value = value.toString(format_type)
            data_to_insert.append(value)

        db_insert_method(*data_to_insert)
        reset_agenda_tues(main_window_instance, widget_names)

    except Exception as e:
        logger.error(f"error occurred while adding tuesdays agenda data: {e}", exc_info=True)

def reset_agenda_tues(main_window_instance, widget_names):
    """
    Resets the agenda for Tuesday.

    Parameters:
    - main_window_instance: The instance of the main window.
    - widget_names: A dictionary containing the names of the widgets.

    Returns:
    None
    """
    try:
        
        getattr(main_window_instance, widget_names['tues_date']).setDate(QDate.currentDate())
        getattr(main_window_instance, widget_names['tues_note_one']).clear()

        # Assuming there is a model for each day
        getattr(main_window_instance, widget_names['model']).select()

    except Exception as e:
        logger.error(f"error occurred while resetting tuesdays agenda data: {e}", exc_info=True)
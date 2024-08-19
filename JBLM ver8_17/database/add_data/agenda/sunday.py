from PyQt6.QtCore import QDate
from logger_setup import logger

def agenda_data_sunday(main_window_instance, widget_names, db_insert_method):
    """
    Generate the agenda data for Sunday.

    Parameters:
    - main_window_instance: The instance of the main window.
    - widget_names: A dictionary of widget names.
    - db_insert_method: The method to insert data into the database.

    Returns:
    None
    """
    try:
        widget_methods = {
            widget_names['sun_date']: (None, 'date', 'dd-MM-yyyy'),
            widget_names['sun_note_one']: (widget_names['sun_note_one'], 'toPlainText', ""),
        }

        data_to_insert = []
        for widget_name, (widget_attr, method, format_type) in widget_methods.items():
            widget = getattr(main_window_instance, widget_name)
            value = getattr(widget, method)()
            if format_type:
                value = value.toString(format_type)
            data_to_insert.append(value)

        db_insert_method(*data_to_insert)
        reset_agenda_sun(main_window_instance, widget_names)
    except Exception as e:
        logger.exception(f"Error occurred: adding Sunday data {e}", exc_info=True)

def reset_agenda_sun(main_window_instance, widget_names):
    """
    Reset the agenda for the sun.

    Parameters:
        main_window_instance (QMainWindow): The main window instance.
        widget_names (dict): A dictionary containing the names of the widgets.

    Returns:
        None
    """
    try:
        getattr(main_window_instance, widget_names['sun_date']).setDate(QDate.currentDate())
        getattr(main_window_instance, widget_names['sun_note_one']).clear()

        # Assuming there is a model for each day
        getattr(main_window_instance, widget_names['model']).select()
    except Exception as e:
        logger.exception(f"Error occurred: resetting Sunday data {e}", exc_info=True)

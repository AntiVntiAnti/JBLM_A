from PyQt6.QtCore import QDate
from logger_setup import logger


def agenda_data_saturday(main_window_instance, widget_names, db_insert_method):
    """
        Extracts data from Saturday widget methods and inserts it into the database.

        Args:
            main_window_instance: The instance of the main window.
            widget_names: A dictionary that maps widget names to their corresponding attribute names.
            db_insert_method: The method used to insert data into the database.

        Returns:
            None
    """
    try:
        widget_methods = {
            widget_names['sat_date']: (None, 'date', 'dd-MM-yyyy'),
            widget_names['sat_note_one']: (widget_names['sat_note_one'], 'toPlainText', ""),
        }

        data_to_insert = []
        for widget_name, (widget_attr, method, format_type) in widget_methods.items():
            widget = getattr(main_window_instance, widget_name)
            value = getattr(widget, method)()
            if format_type:
                value = value.toString(format_type)
            data_to_insert.append(value)

        db_insert_method(*data_to_insert)
        reset_agenda_sat(main_window_instance, widget_names)
    except Exception as e:
        logger.error(f"Error occurred while inserting data: {e}", exc_info=True)


def reset_agenda_sat(main_window_instance, widget_names):
    """
    Reset the agenda for Saturday.

    Parameters:
    - main_window_instance (object): An instance of the main window.
    - widget_names (dict): A dictionary containing the names of the widgets.

    Returns:
    None
    """
    try:
        # Clear all entries and set date back
        getattr(main_window_instance, widget_names['sat_date']).setDate(QDate.currentDate())
        getattr(main_window_instance, widget_names['sat_note_one']).clear()

        # Assuming there is a model for each day
        getattr(main_window_instance, widget_names['model']).select()
    except Exception as e:
        logger.error(f"Error occurred while resetting saturdays agenda: {e}", exc_info=True)

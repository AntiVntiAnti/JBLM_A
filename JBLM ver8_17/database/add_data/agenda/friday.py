from PyQt6.QtCore import QDate
# from sexy_logger import logger
from logger_setup import logger


def agenda_data_friday(main_window_instance, widget_names, db_insert_method):
    """
    Add data to the agenda for Friday.

    Args:
        main_window_instance (object): An instance of the main window.
        widget_names (dict): A dictionary containing the names of the widgets.
        db_insert_method (function): The method used to insert data into the database.

    Returns:
        None

    Raises:
        Exception: If an error occurs while adding data.

    """
    try:
        widget_methods = {
            widget_names['fri_date']: (None, 'date', 'dd-MM-yyyy'),
            widget_names['fri_note_one']: (widget_names['fri_note_one'], 'toPlainText', ""),
        }

        data_to_insert = []
        for widget_name, (widget_attr, method, format_type) in widget_methods.items():
            widget = getattr(main_window_instance, widget_name)
            value = getattr(widget, method)()
            if format_type:
                value = value.toString(format_type)
            data_to_insert.append(value)

        db_insert_method(*data_to_insert)
        reset_agenda_fri(main_window_instance, widget_names)
    except Exception as e:
        logger.info(f"Error adding data agenda_data_friday: {e}", exc_info=True)
        
        
def reset_agenda_fri(main_window_instance, widget_names):
    """
    Reset the agenda for Friday by clearing the date and note fields and selecting the model.

    Args:
        main_window_instance (object): An instance of the main window.
        widget_names (dict): A dictionary containing the names of the widgets.

    Raises:
        Exception: If an error occurs while resetting the agenda.

    Returns:
        None

    """
    try:
        getattr(main_window_instance, widget_names['fri_date']).setDate(QDate.currentDate())
        getattr(main_window_instance, widget_names['fri_note_one']).clear()

        # Assuming there is a model for each day
        getattr(main_window_instance, widget_names['model']).select()
    except Exception as e:
        logger.error(f"Error resetting friday agenda: {e}", exc_info=True)
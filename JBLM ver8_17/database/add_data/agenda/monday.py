from PyQt6.QtCore import QDate
from logger_setup import logger


def agenda_data_monday(main_window_instance, widget_names, db_insert_method):
    """
    Generate the agenda data for Monday.

    Args:
        main_window_instance: An instance of the main window.
        widget_names: A dictionary of widget names.
        db_insert_method: The method to insert data into the database.

    Returns:
        None
    """
    try:
        widget_methods = {
            widget_names['mon_date']: (None, 'date', 'dd-MM-yyyy'),
            widget_names['mon_note_one']: (widget_names['mon_note_one'], 'toPlainText', ""),
            }
    
        data_to_insert = []
        for widget_name, (widget_attr, method, format_type) in widget_methods.items():
            widget = getattr(main_window_instance, widget_name)
            value = getattr(widget, method)()
            if format_type:
                value = value.toString(format_type)
            data_to_insert.append(value)
    
        db_insert_method(*data_to_insert)
        reset_agenda_mon(main_window_instance, widget_names)
    except Exception as e:
        logger.error(f"Error inserting data into agenda_mon: {e},",
                     exc_info=True)

def reset_agenda_mon(main_window_instance, widget_names):
    """
    Resets the agenda for Monday by clearing the note and setting the date to the current date.

    Args:
        main_window_instance: An instance of the main window.
        widget_names: A dictionary containing the names of the widgets.

    Raises:
        Exception: If there is an error resetting the agenda_mon.

    """
    try:
        getattr(main_window_instance, widget_names['mon_date']).setDate(QDate.currentDate())
        getattr(main_window_instance, widget_names['mon_note_one']).clear()
    
        # Assuming there is a model for each day
        getattr(main_window_instance, widget_names['model']).select()
    except Exception as e:
        logger.error(f"Error resetting agenda_mon: {e}", exc_info=True)
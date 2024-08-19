from PyQt6.QtCore import QDate
from logger_setup import logger


def agenda_data_wednesday(main_window_instance, widget_names, db_insert_method):
    """
    Generate the data to be inserted into the database for Wednesday's agenda.

    Parameters:
        main_window_instance (MainWindow): An instance of the main window.
        widget_names (dict): A dictionary containing the names of the widgets.
        db_insert_method (function): The method used to insert data into the database.

    Returns:
        None
    """
    try:
        widget_methods = {
            widget_names['wed_date']: (None, 'date', 'dd-MM-yyyy'),
            widget_names['wed_note_one']: (widget_names['wed_note_one'], 'toPlainText', ""),
        }

        data_to_insert = []
        for widget_name, (widget_attr, method, format_type) in widget_methods.items():
            widget = getattr(main_window_instance, widget_name)
            value = getattr(widget, method)()
            if format_type:
                value = value.toString(format_type)
            data_to_insert.append(value)

        db_insert_method(*data_to_insert)
        reset_agenda_wed(main_window_instance, widget_names)
    except Exception as e:
        logger.error(f"Error occurred: inserting data for Wednesday's agenda.{e}", exc_info=True)


def reset_agenda_wed(main_window_instance, widget_names):
    """
    Reset the agenda for Wednesday.

    :param main_window_instance: The instance of the main window.
    :param widget_names: A dictionary of widget names.
    :return: None
    """
    try:
        getattr(main_window_instance, widget_names['wed_date']).setDate(QDate.currentDate())
        getattr(main_window_instance, widget_names['wed_note_one']).clear()

        # Assuming there is a model for each day
        getattr(main_window_instance, widget_names['model']).select()
    except Exception as e:
        logger.error(f"Error occurred: resetting the agenda for Wednesday. {e}", exc_info=True)
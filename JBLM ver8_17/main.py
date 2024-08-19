from PyQt6.QtWidgets import QApplication
from ui.app import MainWindow
import sys
from logger_setup import logger
from ui.main_ui import res
# pyrcc5 resources.qrc -o resources.py  I am almost 100% with the not forgetting this :D
# from system_tray_magicks import wizardz


def run_app():
    """
    Runs the application.

    This function initializes the application, creates the main window,
    and starts the event loop.

    Raises:
        Exception: If an error occurs during the execution of the application.
    """
    logger.debug("Entry Point bega'th")
    try:
        app = QApplication(sys.argv)
        
        # Initialize the system tray
        # tray = wizardz()
        
        # window = MainWindow(tray)  # Pass the tray object if needed
        window = MainWindow()
        window.show()
        window.setFixedSize(640, 640)
        sys.exit(app.exec())
    except (ValueError, TypeError) as e:
        logger.error(f"Value or Type error occurred {e}", exc_info=True)
    except ImportError as e:
        logger.error(f"Import error occurred {e}", exc_info=True)
    except OSError as e:
        logger.error(f"OS error occurred {e}", exc_info=True)
    except Exception as e:
        logger.error(f"Unexpected error occurred {e}", exc_info=True)


if __name__ == '__main__':
    run_app()

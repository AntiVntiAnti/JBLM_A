from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PyQt6.QtGui import QIcon, QAction
import sys

class SystemTray:
    def __init__(self):
        self.tray = QSystemTrayIcon()
        self.menu = QMenu()

        # Create actions
        self.show_action = QAction("Show")
        self.quit_action = QAction("Quit")

        # Add actions to the menu
        self.menu.addAction(self.show_action)
        self.menu.addAction(self.quit_action)

        # Set the menu to the tray icon
        self.tray.setContextMenu(self.menu)

        # Set an icon (using text as an icon)
        self.tray.setIcon(QIcon.fromTheme("text-icon"))

        # Show the tray icon
        self.tray.show()

    def set_icon(self, icon_path):
        self.tray.setIcon(QIcon(icon_path))

    def set_tooltip(self, tooltip):
        self.tray.setToolTip(tooltip)

def wizardz():
    return SystemTray()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tray = SystemTray()
    sys.exit(app.exec())

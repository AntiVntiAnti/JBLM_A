import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QFileDialog
from PyQt6.QtGui import QImage, QTextCursor
from PyQt6.QtCore import QSettings, Qt, QBuffer, QByteArray
import sqlite3


class ImageTextEdit(QTextEdit):
    
    def __init__(self,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
    
    def dragEnterEvent(self,
                       event):
        if event.mimeData().hasImage():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)
    
    def dropEvent(self,
                  event):
        if event.mimeData().hasImage():
            image = event.mimeData().imageData()
            self.insert_image(image)
            event.acceptProposedAction()
        else:
            super().dropEvent(event)
    
    def insert_image(self,
                     image):
        cursor = self.textCursor()
        document = self.document()
        cursor.insertImage(image)
        
        # Save the image to the SQLite3 database
        self.save_image_to_db(image)
    
    def save_image_to_db(self,
                         image):
        buffer = QBuffer()
        buffer.open(QBuffer.OpenModeFlag.ReadWrite)
        image.save(buffer, "PNG")
        binary_data = buffer.data()
        connection = sqlite3.connect('images.db')
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, image BLOB)")
        cursor.execute("INSERT INTO images (image) VALUES (?)", (binary_data,))
        connection.commit()
        connection.close()


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.text_edit = ImageTextEdit()
        self.settings = QSettings("MyCompany", "ImageEditor")
        
        self.init_ui()
        self.load_last_document()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.setWindowTitle("Image Editor with SQLite3")
        self.resize(800, 600)
        
        self.text_edit.textChanged.connect(self.save_document_state)
    
    def load_last_document(self):
        last_file = self.settings.value("last_file", "")
        if last_file and os.path.exists(last_file):
            with open(last_file, 'r') as f:
                self.text_edit.setText(f.read())
    
    def save_document_state(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Document")
        if file_name:
            with open(file_name, 'w') as f:
                f.write(self.text_edit.toHtml())
            self.settings.setValue("last_file", file_name)


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

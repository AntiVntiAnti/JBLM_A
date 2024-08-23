import sys
import os
from PyQt6.QtWidgets import QApplication, \
    QMainWindow, \
    QWidget, \
    QVBoxLayout, \
    QSpinBox, \
    QPushButton, \
    QTableView, \
    QTabWidget, \
    QMessageBox
from PyQt6.QtCore import QDateTime, Qt
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Mood Tracker")
        self.setGeometry(100, 100, 600, 400)
        
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        
        self.create_tabs()
        self.setup_database()
        self.show()
    
    def create_tabs(self):
        # Tab 1: Input
        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        
        self.mood_spinbox = QSpinBox()
        self.mood_spinbox.setRange(0, 10)
        self.mood_spinbox.setPrefix("Mood: ")
        
        self.mania_spinbox = QSpinBox()
        self.mania_spinbox.setRange(0, 10)
        self.mania_spinbox.setPrefix("Mania: ")
        
        self.depression_spinbox = QSpinBox()
        self.depression_spinbox.setRange(0, 10)
        self.depression_spinbox.setPrefix("Depression: ")
        
        commit_button = QPushButton("Commit")
        commit_button.clicked.connect(self.commit_record)
        
        tab1_layout.addWidget(self.mood_spinbox)
        tab1_layout.addWidget(self.mania_spinbox)
        tab1_layout.addWidget(self.depression_spinbox)
        tab1_layout.addWidget(commit_button)
        
        tab1.setLayout(tab1_layout)
        
        # Tab 2: Table View
        tab2 = QWidget()
        tab2_layout = QVBoxLayout()
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QTableView.SelectionMode.MultiSelection)
        delete_button = QPushButton("Delete Selected Records")
        delete_button.clicked.connect(self.delete_records)
        tab2_layout.addWidget(self.table_view)
        tab2_layout.addWidget(delete_button)
        tab2.setLayout(tab2_layout)
        
        tab3 = QWidget()
        tab3_layout = QVBoxLayout()
        self.moodTableView = QTableView()
        self.moodTableView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.moodTableView.setSelectionMode(QTableView.SelectionMode.MultiSelection)
        delete_button3 = QPushButton("Delete Selected Records")
        delete_button3.clicked.connect(self.delete_records3)
        tab3_layout.addWidget(self.moodTableView)
        tab3_layout.addWidget(delete_button3)
        tab3.setLayout(tab3_layout)
        
        tab4 = QWidget()
        tab4_layout = QVBoxLayout()
        self.maniaTableView = QTableView()
        self.maniaTableView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.maniaTableView.setSelectionMode(QTableView.SelectionMode.MultiSelection)
        delete_button3 = QPushButton("Delete Selected Records")
        delete_button3.clicked.connect(self.delete_records3)
        tab4_layout.addWidget(self.maniaTableView)
        tab4_layout.addWidget(delete_button3)
        tab4.setLayout(tab4_layout)
        
        tab5 = QWidget()
        tab5_layout = QVBoxLayout()
        self.depressionTableView = QTableView()
        self.depressionTableView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.depressionTableView.setSelectionMode(QTableView.SelectionMode.MultiSelection)
        delete_button4 = QPushButton("Delete Selected Records")
        delete_button4.clicked.connect(self.delete_records4)
        tab5_layout.addWidget(self.depressionTableView)
        tab5_layout.addWidget(delete_button4)
        tab5.setLayout(tab5_layout)
        
        self.tab_widget.addTab(tab1, "Input")
        self.tab_widget.addTab(tab2, "Records")
        self.tab_widget.addTab(tab3, "Mood")
        self.tab_widget.addTab(tab4, "Mania")
        self.tab_widget.addTab(tab5, "Depression")
    
    def setup_database(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        home_dir = os.path.expanduser("~")
        db_path = os.path.join(home_dir, "mood_tracker.db")
        self.db.setDatabaseName(db_path)
        if not self.db.open():
            QMessageBox.critical(None, "Database Error", self.db.lastError().text())
        
        query = QSqlQuery()
        query.exec(
            """
            CREATE TABLE IF NOT EXISTS datetime_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                time TEXT
            )
        """
        )
        query.exec(
            """
            CREATE TABLE IF NOT EXISTS mood (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime_id INTEGER,
                mood INTEGER,
                FOREIGN KEY(datetime_id) REFERENCES datetime_table(id)
            )
        """
        )
        query.exec(
            """
            CREATE TABLE IF NOT EXISTS mania (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime_id INTEGER,
                mania INTEGER,
                FOREIGN KEY(datetime_id) REFERENCES datetime_table(id)
            )
        """
        )
        query.exec(
            """
            CREATE TABLE IF NOT EXISTS depression (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datetime_id INTEGER,
                depression INTEGER,
                FOREIGN KEY(datetime_id) REFERENCES datetime_table(id)
            )
        """
        )
        
        self.model = QSqlTableModel()
        self.model.setTable("datetime_table")
        self.model.select()
        
        self.table_view.setModel(self.model)
        
        self.modelMood = QSqlTableModel()
        self.modelMood.setTable("mood")
        self.modelMood.select()
        # TODO : make moodTableView and set up and place
        self.moodTableView.setModel(self.modelMood)
        
        self.modelMania = QSqlTableModel()
        self.modelMania.setTable("mania")
        self.modelMania.select()
        # TODO : make moodTableView and set up and place
        self.maniaTableView.setModel(self.modelMania)
        
        self.modelDepression = QSqlTableModel()
        self.modelDepression.setTable("depression")
        self.modelDepression.select()
        # TODO : make moodTableView and set up and place
        self.depressionTableView.setModel(self.modelDepression)
    
    def commit_record(self):
        date_time = QDateTime.currentDateTime()
        date = date_time.toString("yyyy-MM-dd")
        time = date_time.toString("HH:mm:ss")
        
        query = QSqlQuery()
        query.prepare("INSERT INTO datetime_table (date, time) VALUES (?, ?)")
        query.addBindValue(date)
        query.addBindValue(time)
        if not query.exec():
            QMessageBox.critical(None, "Database Error", query.lastError().text())
        
        datetime_id = query.lastInsertId()
        
        mood = self.mood_spinbox.value()
        query.prepare("INSERT INTO mood (datetime_id, mood) VALUES (?, ?)")
        query.addBindValue(datetime_id)
        query.addBindValue(mood)
        if not query.exec():
            QMessageBox.critical(None, "Database Error", query.lastError().text())
        
        mania = self.mania_spinbox.value()
        query.prepare("INSERT INTO mania (datetime_id, mania) VALUES (?, ?)")
        query.addBindValue(datetime_id)
        query.addBindValue(mania)
        self.modelMania.select()
        if not query.exec():
            QMessageBox.critical(None, "Database Error", query.lastError().text())
        
        depression = self.depression_spinbox.value()
        query.prepare("INSERT INTO depression (datetime_id, depression) VALUES (?, ?)")
        query.addBindValue(datetime_id)
        query.addBindValue(depression)
        self.modelDepression.select()
        if not query.exec():
            QMessageBox.critical(None, "Database Error", query.lastError().text())
        
        self.modelMood.select()
        self.modelMania.select()
        self.modelDepression.select()
        self.model.select()
    
    def delete_records(self):
        selected_rows = self.table_view.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(None, "No Selection", "Please select records to delete.")
            return
        
        ids = [self.model.data(index) for index in selected_rows]
        query = QSqlQuery()
        query.prepare("DELETE FROM datetime_table WHERE id = ?")
        for record_id in ids:
            query.addBindValue(record_id)
            if not query.exec():
                QMessageBox.critical(None, "Database Error", query.lastError().text())
        
        self.model.select()
    
    def delete_records2(self):
        selected_rows = self.table_view.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(None, "No Selection", "Please select records to delete.")
            return
        
        ids = [self.model.data(index) for index in selected_rows]
        query = QSqlQuery()
        query.prepare("DELETE FROM mood_table WHERE id = ?")
        for record_id in ids:
            query.addBindValue(record_id)
            if not query.exec():
                QMessageBox.critical(None, "Database Error", query.lastError().text())
        
        self.model.select()
    
    def delete_records3(self):
        selected_rows = self.table_view.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(None, "No Selection", "Please select records to delete.")
            return
        
        ids = [self.model.data(index) for index in selected_rows]
        query = QSqlQuery()
        query.prepare("DELETE FROM mania_table WHERE id = ?")
        for record_id in ids:
            query.addBindValue(record_id)
            if not query.exec():
                QMessageBox.critical(None, "Database Error", query.lastError().text())
        
        self.model.select()
    
    def delete_records4(self):
        selected_rows = self.table_view.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(None, "No Selection", "Please select records to delete.")
            return
        
        ids = [self.model.data(index) for index in selected_rows]
        query = QSqlQuery()
        query.prepare("DELETE FROM depression_table WHERE id = ?")
        for record_id in ids:
            query.addBindValue(record_id)
            if not query.exec():
                QMessageBox.critical(None, "Database Error", query.lastError().text())
        
        self.model.select()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

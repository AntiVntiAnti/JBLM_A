# utils.py or helpers.py
from PyQt6.QtCore import Qt


def apply_sorting(table_view, column_index):
    table_view.setSortingEnabled(True)
    table_view.sortByColumn(column_index, Qt.SortOrder.DescendingOrder)

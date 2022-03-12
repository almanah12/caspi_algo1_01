"""
File containing utility functions for the GUI.
"""

from datetime import datetime
from typing import List

from PyQt5 import QtGui
from PyQt5.QtGui import QColorConstants
from PyQt5.QtWidgets import QComboBox, QDialog, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QTableView)

from delegats import ButtonEditorDelegate, ButtonDeleteDelegate


def create_popup(parent, msg: str, title='Warning'):
    """
    Creates a popup with message provided.
    :param parent: Parent object to create popup on.
    :param title: Title for message box. By default, it is warning.
    :param msg: Message provided.
    """
    QMessageBox.about(parent, title, msg)


def open_from_msg_box(text: str, title: str):
    """
    Create a message box with an open/close dialog with text and title provided and return true or false depending
    on whether the user wants to open it or not.
    :param text: Text to put in message box.
    :param title: Title to put in message box.
    """
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText(text)
    msg_box.setWindowTitle(title)
    msg_box.setStandardButtons(QMessageBox.Open | QMessageBox.Close)
    return msg_box.exec_() == QMessageBox.Open


def get_elements_from_combobox(combobox: QComboBox) -> List[str]:
    """
    Returns all elements from combobox provided in a list.
    :param combobox: Combobox to get list of elements from.
    :return: List of elements from combobox.
    """
    return [combobox.itemText(i) for i in range(combobox.count())]


def show_and_bring_window_to_front(window: QDialog):
    """
    This will bring the window provided to the very front of the screen.
    :param window: Window object to bring to front.
    """
    # window.show()
    # window.activateWindow()
    # window.raise_()
    window.exec_()


def add_to_table_widget(table, data: list, color,  insertDate=True):
    """
    Function that will add specified data to a provided table.
    :param color:
    :param insertDate: Boolean to add date to 0th index of data or not.
    :param table: Table we will add data to.
    :param data: Data we will add to table.
    """
    row_position = table.rowCount()
    columns = table.columnCount()

    if insertDate:
        data.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if len(data) != columns:
        raise ValueError('/Data needs to have the same amount of columns as table.')

    table.insertRow(row_position)
    for column in range(0, columns):
        value = data[column]
        if type(value) not in (int, float):
            item = QTableWidgetItem(str(value))
        else:
            item = QTableWidgetItem()
            item.setData(Qt.DisplayRole, value)
        table.setItem(row_position, column, item)
        if color == 1:
            table.item(row_position, column).setBackground(QColorConstants.Svg.palegreen)
        elif color == 2:
            table.item(row_position, column).setBackground(QColorConstants.Svg.lightsalmon)
        elif color == 3:
            table.item(row_position, column).setBackground(QColorConstants.Svg.yellow)
        elif color == 4:
            table.item(row_position, column).setBackground(QColorConstants.Svg.greenyellow)


def add_to_data_table_view(self, model, name_table, table: QTableView):
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    header = table.horizontalHeader()

    table.setHorizontalHeader(header)
    table.setModel(model)
    if name_table == 'permanent_table':
        editor_delegate = ButtonEditorDelegate(self)  # Была ошибка, передал self и проблема решилась
        delete_delegate = ButtonDeleteDelegate(self)

        table.setItemDelegateForColumn(0, editor_delegate)
        table.setItemDelegateForColumn(1, delete_delegate)

    model.setTable(name_table)
    model.select()

    # После долгих попыток получилось изменить ширину столбца табл.
    # Нужно было поставить setColumnWidth в конце метода
    # header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
    # header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

    # Подгон равзмера столбца по содержанию
    table.resizeColumnsToContents()


def add_to_data_table_temp(self, model, name_table, table: QTableView):
    table.setSelectionBehavior(QAbstractItemView.SelectRows)

    # table.setHorizontalHeader(header)
    table.setModel(model)

    model.setTable(name_table)
    model.select()


def clear_table(table: QTableWidget):
    """
    Sets table row count to 0.
    :param table: Table which is to be cleared.
    """
    table.setRowCount(0)



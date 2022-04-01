"""
File containing utility functions for the GUI.
"""

from datetime import datetime
from typing import List

from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QColorConstants
from PyQt5.QtWidgets import QComboBox, QDialog, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QTableView)

from caspi_pars.delegats import ButtonEditorDelegate, ButtonDeleteDelegate
from caspi_pars.helpers import logger

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


# class ColumnSwapProxy(QtCore.QSortFilterProxyModel):
#     def data(self, index, role=QtCore.Qt.DisplayRole):
#         logger.debug(index)
#         return super().data(index.sibling(index.row(), index.column() + 1), role)
#
#     def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
#         if orientation == QtCore.Qt.Horizontal and (section==10 or section==12):
#             section += 1
#         return super().headerData(section, orientation, role)


def add_to_data_table_view(parent, model, name_table, table: QTableView):
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    header = table.horizontalHeader()

    table.setHorizontalHeader(header)
    # proxy = ColumnSwapProxy()
    # proxy.setSourceModel(model)
    table.setModel(model)
    if name_table == 'permanent_table':
        editor_delegate = ButtonEditorDelegate(parent)  # Была ошибка, передал self и проблема решилась
        delete_delegate = ButtonDeleteDelegate(parent)

        table.setItemDelegateForColumn(0, editor_delegate)
        table.setItemDelegateForColumn(1, delete_delegate)

    model.setTable(name_table)
    model.select()
    # Подгон размера столбца по содержанию
    table.resizeColumnsToContents()
    # После долгих попыток получилось изменить ширину столбца табл.
    # Нужно было поставить setColumn
    # Width в конце метода

    # Показывать данные остальных городов
    if parent.comboBox_show_data_other_city.currentText() == '1':
        # Город 2
        table.setColumnWidth(14, 0)
        table.setColumnWidth(15, 0)
        table.setColumnWidth(16, 0)  # Скрывает столбец
        table.setColumnWidth(17, 0)
        table.setColumnWidth(19, 0)
        table.setColumnWidth(21, 0)
        # Город 3
        table.setColumnWidth(22, 0)
        table.setColumnWidth(23, 0)
        table.setColumnWidth(24, 0)
        table.setColumnWidth(25, 0)
        table.setColumnWidth(27, 0)
        table.setColumnWidth(29, 0)
        # Город 4
        table.setColumnWidth(30, 0)
        table.setColumnWidth(31, 0)
        table.setColumnWidth(32, 0)
        table.setColumnWidth(33, 0)
        table.setColumnWidth(35, 0)
        table.setColumnWidth(37, 0)
    elif parent.comboBox_show_data_other_city.currentText() == '2':
        # Город 3
        table.setColumnWidth(22, 0)
        table.setColumnWidth(23, 0)
        table.setColumnWidth(24, 0)
        table.setColumnWidth(25, 0)
        table.setColumnWidth(27, 0)
        table.setColumnWidth(29, 0)
        # Город 4
        table.setColumnWidth(30, 0)
        table.setColumnWidth(31, 0)
        table.setColumnWidth(32, 0)
        table.setColumnWidth(33, 0)
        table.setColumnWidth(35, 0)
        table.setColumnWidth(37, 0)
    elif parent.comboBox_show_data_other_city.currentText() == '3':
        # Город 4
        table.setColumnWidth(30, 0)
        table.setColumnWidth(31, 0)
        table.setColumnWidth(32, 0)
        table.setColumnWidth(33, 0)
        table.setColumnWidth(35, 0)
        table.setColumnWidth(37, 0)

    else:
        table.resizeColumnsToContents()

    if name_table == 'permanent_table':
        table.setColumnWidth(4, 0)
        table.setColumnWidth(5, 0)
        table.setColumnWidth(10, 0)  # Скрывает столбец
        table.setColumnWidth(12, 0)
        table.setColumnWidth(18, 0)
        table.setColumnWidth(20, 0)
        table.setColumnWidth(26, 0)
        table.setColumnWidth(28, 0)
        table.setColumnWidth(34, 0)
        table.setColumnWidth(36, 0)
        table.setColumnWidth(38, 0)


def clear_table(table: QTableWidget):
    """
    Sets table row count to 0.
    :param table: Table which is to be cleared.
    """
    table.setRowCount(0)



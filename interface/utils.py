"""
File containing utility functions for the GUI.
"""

from datetime import datetime
from typing import List

from PyQt5.QtGui import QColorConstants
from PyQt5.QtWidgets import QComboBox, QDialog, QMessageBox, QTableWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QTableView)

from caspi_pars.other_func.check_data_fill import ch_dt_fill_for_tableview, active_goods_table

from caspi_pars.delegats import ButtonEditorDelegate, ButtonDeleteDelegate, ReadOnlyDelegate


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


def add_to_data_table_view(parent, model, name_table, table: QTableView):
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    # headmodel = QStandardItemModel()
    # headmodel.setHorizontalHeaderLabels(['q1', 'q2', 'q3', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13', 'q14', 'q15', 'q16', 'q17', 'q18', 'q19'])
    #
    # headview1 = QHeaderView(Qt.Horizontal)
    # headview1.setModel(headmodel)
    # headview1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    header = table.horizontalHeader()
    #
    table.setHorizontalHeader(header)

    table.setModel(model)
    if name_table == 'permanent_table':
        active_goods_table()
        editor_delegate = ButtonEditorDelegate(parent)  # Была ошибка, передал self и проблема решилась
        delete_delegate = ButtonDeleteDelegate(parent)
        read_only = ReadOnlyDelegate(parent)

        table.setItemDelegateForColumn(0, editor_delegate)
        table.setItemDelegateForColumn(1, delete_delegate)
        for column in range(2, 43):
            table.setItemDelegateForColumn(column, read_only)
    model.setTable(name_table)
    model.select()
    # Подгон размера столбца по содержанию
    table.resizeColumnsToContents()

    # Показывать данные остальных городов
    if name_table == 'permanent_table':
        if parent.comboBox_show_data_other_city.currentText() == '1':
            # Город 2
            ch_dt_fill_for_tableview(parent)
            list_column_1 = [14, 15, 16, 17, 19, 21, 22, 23, 24, 25, 27, 29, 30, 31, 32, 33, 35, 37]
            for colum in list_column_1:
                table.setColumnWidth(colum, 0)

        elif parent.comboBox_show_data_other_city.currentText() == '2':
            ch_dt_fill_for_tableview(parent)

            list_column_2 = [22, 23, 24, 25, 27, 29, 30, 31, 32, 33, 35, 37]
            for colum in list_column_2:
                table.setColumnWidth(colum, 0)

        elif parent.comboBox_show_data_other_city.currentText() == '3':
            ch_dt_fill_for_tableview(parent)

            list_column_3 = [30, 31, 32, 33, 35, 37]
            for colum in list_column_3:
                table.setColumnWidth(colum, 0)

        else:
            ch_dt_fill_for_tableview(parent)

            table.resizeColumnsToContents()

        # Скрывает столбец
        list_column = [4, 5, 10, 12, 18, 20, 26, 28, 34, 36, 38]
        for colum in list_column:
            table.setColumnWidth(colum, 0)

        # if parent.filter_comboBox.currentText() == 'Товары без данных':
        #     model.setFilter(filter_for_goods_without_data)
        #
        # elif parent.filter_comboBox.currentText() == 'Товары с данными':
        #     model.setFilter(filter_for_goods_with_data)
        #
        # else:
        #     model.setFilter(filter_all_data)

    return table


def clear_table(table: QTableWidget):
    """
    Sets table row count to 0.
    :param table: Table which is to be cleared.
    """
    table.setRowCount(0)



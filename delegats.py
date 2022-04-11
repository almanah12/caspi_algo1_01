from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QStyleOptionButton, QStyledItemDelegate, QStyle, QMainWindow, QMessageBox)
from PyQt5.QtCore import QSize

from caspi_pars.db_QSqlDatabase import model_perm
from caspi_pars.helpers import resource_path
from caspi_pars.interface.add_base_data import Add_Base_Data
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets


class ButtonEditorDelegate(QStyledItemDelegate):
    buttonClicked = QtCore.pyqtSignal(int, int)

    def __init__(self, parent=QMainWindow):
        super().__init__(parent)
        self.parent = parent
        self._pressed = None
        self._buttonTxt = QIcon(resource_path(r"icons_delegate/edit.png"))

    def paint(self, painter, option, index):
        painter.save()
        opt = QStyleOptionButton()

        opt.icon = self._buttonTxt
        opt.iconSize = QSize(50, 50)

        opt.rect = option.rect
        # opt.palette = option.palette

        if self._pressed and self._pressed == (index.row(), index.column()):
            opt.state = QStyle.State_Enabled | QStyle.State_Sunken
        else:
            opt.state = QStyle.State_Enabled | QStyle.State_Raised
        QtWidgets.QApplication.style().drawControl(QStyle.CE_PushButton, opt, painter)
        painter.restore()

    def editorEvent(self, event, model, option, index):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            # store the position that is clicked
            self._pressed = (index.row(), index.column())
            return True
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            if self._pressed == (index.row(), index.column()):
                self.buttonClicked.emit(*self._pressed)
                self.add_base_data = Add_Base_Data(self.parent)
                self.add_base_data.init_delegate(index.row())
                self.add_base_data.exec_()

                self.add_base_data.activateWindow()
                self.add_base_data.raise_()

            self._pressed = None
            return True

        return False

    def createEditor(self, parent, option, index):
        """ Disable the createEditor or you'll lose your button on a double-click """
        return None

    def setEditorData(self, item, index):
        """ We don't change what's in the button so disable this event also """
        return None


class ButtonDeleteDelegate(QStyledItemDelegate):

    buttonClicked = QtCore.pyqtSignal(int, int)

    def __init__(self, parent=QMainWindow):
        super().__init__(parent)
        self.parent = parent
        self._pressed = None
        self._buttonTxt = QIcon(resource_path(r"icons_delegate/delete.png"))

    def paint(self, painter, option, index):
        painter.save()
        opt = QStyleOptionButton()

        opt.icon = self._buttonTxt
        opt.iconSize = QSize(50, 50)

        opt.rect = option.rect
        # opt.palette = option.palette
        #opt.rect.setBottom(20)

        if self._pressed and self._pressed == (index.row(), index.column()):
            opt.state = QStyle.State_Enabled | QStyle.State_Sunken
        else:
            opt.state = QStyle.State_Enabled | QStyle.State_Raised
        QtWidgets.QApplication.style().drawControl(QStyle.CE_PushButton, opt, painter)
        painter.restore()

    def editorEvent(self, event, model, option, index):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            # store the position that is clicked
            self._pressed = (index.row(), index.column())
            return True
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            if self._pressed == (index.row(), index.column()):
                self.buttonClicked.emit(*self._pressed)
                reply = QMessageBox.question(self.parent, 'Message',
                                             "Вы уверены что хотите удалить строку данных?", QMessageBox.Yes |
                                             QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    model_perm.removeRows(index.row(), 1)
                    event.accept()
                else:
                    event.ignore()

            self._pressed = None
            return True

        return False


class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, insex):
        return
# class ColorDelegate(QtWidgets.QStyledItemDelegate):
#     def paint(self, painter, option, index):
#         if index.column() in (4, 5):
#             model = index.model()
#             r = index.row()
#             color = calculate_color(model, r)
#             if color != index.data(QtCore.Qt.BackgroundRole):
#                 for i in range(model.columnCount()):
#                     model.setData(model.index(r, i), color, QtCore.Qt.BackgroundRole)
#         super(ColorDelegate, self).paint(painter, option, index)
#
#
# def calculate_color(model, row):
#     max_value = int(model.index(row, 2).data())
#     current_value = int(model.index(row, 3).data())
#     if current_value == 0:
#         return QtGui.QBrush(QtCore.Qt.white)
#     elif max_value == current_value:
#         return QtGui.QBrush(QtCore.Qt.green)
#     else:
#         return QtGui.QBrush(QtCore.Qt.yellow)
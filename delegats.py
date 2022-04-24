from PyQt5 import QtCore, Qt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QStyleOptionButton, QStyledItemDelegate, QStyle, QMainWindow, QMessageBox, QApplication,
                             QItemDelegate, QCheckBox, QStyleOptionViewItem)
from PyQt5.QtCore import QSize, QPoint, QRect, QEvent


from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionButton, QStyle, QApplication

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
                self.add_base_data.filter_data(self.parent.search_table_articul_lineEdit.text())
                self.add_base_data.init_delegate(index.row())
                self.add_base_data.exec_()

                self.add_base_data.activateWindow()
                self.add_base_data.raise_()

            self._pressed = None
            return True

        return False

    # def createEditor(self, parent, option, index):
    #     """ Disable the createEditor or you'll lose your button on a double-click """
    #     return None
    #
    # def setEditorData(self, item, index):
    #     """ We don't change what's in the button so disable this event also """
    #     return None


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

# class CheckBoxDelegate(QStyledItemDelegate):
#     """
#     A delegate that places a fully functioning QCheckBox in every
#     cell of the column to which it's applied
#     """
#     def __init__(self, parent):
#         QItemDelegate.__init__(self, parent)
#
#     def createEditor(self, parent, option, index):
#         '''
#         Important, otherwise an editor is created if the user clicks in this cell.
#         ** Need to hook up a signal to the model
#         '''
#         return None
#
#     def paint(self, painter, option, index):
#         '''
#         Paint a checkbox without the label.
#         '''
#
#         checked = index.data()
#         check_box_style_option = QStyleOptionButton()
#
#         if int(index.flags() & QtCore.Qt.ItemIsEditable) > 0:
#             check_box_style_option.state |= QStyle.State_Enabled
#         else:
#             check_box_style_option.state |= QStyle.State_ReadOnly
#
#         if checked:
#             check_box_style_option.state |= QStyle.State_On
#         else:
#             check_box_style_option.state |= QStyle.State_Off
#
#         check_box_style_option.rect = option.rect
#
#         # this will not run - hasFlag does not exist
#         #if not index.model().hasFlag(index, QtCore.Qt.ItemIsEditable):
#             #check_box_style_option.state |= QtGui.QStyle.State_ReadOnly
#
#         check_box_style_option.state |= QStyle.State_Enabled
#
#         QApplication.style().drawControl(QStyle.CE_CheckBox, check_box_style_option, painter)


class CheckBoxDelegate(QtWidgets.QItemDelegate):
    """
    A delegate that places a fully functioning QCheckBox cell of the column to which it's applied.
    """
    def __init__(self, parent=QMainWindow):
        super().__init__(parent)
        self.parent = parent
        self._buttonTxt = QIcon(resource_path(r"icons_delegate/delete.png"))

    def createEditor(self, parent, option, index):
        """
        Important, otherwise an editor is created if the user clicks in this cell.
        """
        return None

    def paint(self, painter, option, index):
        """
        Paint a checkbox without the label.
        """
        painter.save()
        self.drawCheck(painter, option, option.rect, QtCore.Qt.Unchecked if int(index.data()) == 0 else QtCore.Qt.Checked)
        painter.restore()

    def editorEvent(self, event, model, option, index):
        '''
        Change the data in the model and the state of the checkbox
        if the user presses the left mousebutton and this cell is editable. Otherwise do nothing.
        '''
        if not int(index.flags() & QtCore.Qt.ItemIsEditable) > 0:
            return False

        if event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.LeftButton:
            # Change the checkbox-state
            self.setModelData(None, model, index)
            model.submit()

            return True

        return False

    def setModelData (self, editor, model, index):
        '''
        The user wanted to change the old state in the opposite.
        '''
        model.setData(index, 1 if int(index.data()) == 0 else 0, QtCore.Qt.EditRole)


    # def createEditor(self, parent, options, index):
    #     if not index.isValid():
    #         return None
    #     editor = QtWidgets.QCheckBox(parent)
    #     return editor
    #
    #
    # def setEditorData(self, editor, index):
    #     if not index.isValid():
    #         return None
    #     CHval = (index.model().data(index, QtCore.Qt.EditRole))
    #     if CHval == 0:
    #         editor.setCheckState(QtCore.Qt.Unchecked)
    #     else:
    #         editor.setCheckState(QtCore.Qt.Checked)
    #
    # def updateEditorGeometry(self, editor, options, index):
    #     if not index.isValid():
    #         return None
    #     editor.setGeometry(options.rect)
    #
    # def setModelData(self, editor, model, index):
    #     if not index.isValid():
    #         return None
    #     UNval = editor.checkState()
    #     if UNval == QtCore.Qt.Unchecked:
    #         modelVal = 0
    #     else:
    #         modelVal = 1
    #     model.setData(index, modelVal, QtCore.Qt.EditRole)


class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, insex):
        return

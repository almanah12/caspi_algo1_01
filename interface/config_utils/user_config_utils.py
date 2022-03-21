"""
Saving, loading, and copying settings helper functions for configuration.py can be found here.
"""

import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QCompleter
from qtpy import QtCore

from helpers import resource_path


def getOpenFilesAndDirs(parent=None, caption='', directory='',
                        filter='', initialFilter='', options=None):
    def updateText():
        # Обновить содержимое виджета редактирования строки выбранными файлами
        selected = []
        for index in view.selectionModel().selectedRows():
            selected.append('"{}"'.format(index.data()))
        lineEdit.setText(' '.join(selected))

    dialog = QtWidgets.QFileDialog(parent, windowTitle=caption)
    dialog.setFileMode(dialog.ExistingFiles)
    if options:
        dialog.setOptions(options)
    dialog.setOption(dialog.DontUseNativeDialog, True)  # !!!
    if directory:
        dialog.setDirectory(directory)
    if filter:
        dialog.setNameFilter(filter)
        if initialFilter:
            dialog.selectNameFilter(initialFilter)

    # по умолчанию, если каталог открыт в режиме списка файлов,
    # QFileDialog.accept() показывает содержимое этого каталога,
    # но нам нужно иметь возможность "открывать" и каталоги, как мы можем делать с файлами,
    # поэтому мы просто переопределяем `accept()` с реализацией QDialog по умолчанию,
    # которая просто вернет `dialog.selectedFiles()`

    dialog.accept = lambda: QtWidgets.QDialog.accept(dialog)

    # в неродном диалоге есть много представлений элементов,
    # но те, которые отображают фактическое содержимое, создаются внутри QStackedWidget;
    # это QTreeView и QListView, и дерево используется только тогда,
    # когда viewMode установлен на QFileDialog.Details, что не в этом случае.

    stackedWidget = dialog.findChild(QtWidgets.QStackedWidget)
    view = stackedWidget.findChild(QtWidgets.QListView)
    view.selectionModel().selectionChanged.connect(updateText)

    lineEdit = dialog.findChild(QtWidgets.QLineEdit)
    # очищаем содержимое строки редактирования всякий раз, когда изменяется текущий каталог
    dialog.directoryEntered.connect(lambda: lineEdit.setText(''))

    dialog.exec_()
    return dialog.selectedFiles()


def list_proxy_folder(gui, typeFile, widget):
    selected_files = QFileDialog.getOpenFileName(gui, 'Select files', '', typeFile)
    if selected_files[0]:
        path = selected_files[0]
        widget.setText(path)
        widget.setToolTip(path.split('/')[-1])

    else:
        QtWidgets.QMessageBox.information(gui, 'Message', 'Вы ничего не выбрали.')


def list_proxy_folder1(gui, typeFile, widget):
    dialog = QFileDialog()
    dialog.setDirectory(resource_path(r'data_files/data_goods'))
    selected_files = QFileDialog.getOpenFileName(gui, 'Select files', '', typeFile)

    if selected_files[0]:
        path = selected_files[0]
        widget.setText(path)
        widget.setToolTip(path.split('/')[-1])

    else:
        QtWidgets.QMessageBox.information(gui, 'Message', 'Вы ничего не выбрали.')


def search_line_comboBox(word_list, widget, i=True):
    """ Autocompletion of sender and subject """
    word_set = set(word_list)
    completer = QCompleter(word_set)
    if i:
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
    else:
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitive)
    widget.setCompleter(completer)


def get_list_comboBox(file, list):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return sorted(f.read().strip().split('\n'))
    else:
        # with open(file, 'r') as f:
        #     return sorted(f.write(f'{list}\n'))
        return sorted(list)


def add_comboBox(file, comboBox, list):
    nameable = [comboBox.currentText()]
    if nameable[0] not in get_list_comboBox(file, list) and nameable[0] != '':
        comboBox.addItems(nameable)
    save_comboBox(file, comboBox)
    search_line_comboBox(get_list_comboBox(file, list), comboBox)


def save_comboBox(file, comboBox):
    with open(file, 'w') as f:
        for i in range(comboBox.count()):
            it = comboBox.itemData(i, 0)
            f.write(f'{it}\n')


def delete_comboBox(file, comboBox):
    comboBox.removeItem(comboBox.currentIndex())
    save_comboBox(file, comboBox)

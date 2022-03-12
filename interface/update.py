"""
Configuration window.
"""
import os
import sys
import threading
import time

import gdown
import win32api
from PyQt5 import uic
from PyQt5.QtWidgets import (QDialog, QMainWindow, QApplication)
from py7zr import py7zr

from helpers import resource_path

app = QApplication(sys.argv)


class Update(QDialog):
    """
    Configuration window.
    """

    # def __init__(self, parent: QMainWindow, *args, **kwargs):
    #     super(Configuration, self).__init__(parent, *args, **kwargs)
    #     self.setupUi(self)
    def __init__(self, parent: QMainWindow):

        super(Update, self).__init__(parent)  # Initializing object

        uic.loadUi(resource_path(r'UI/update.ui'), self)  # Loading the main UI
        self.parent = parent
        self.thread()
        self.pushButton_install_app.clicked.connect(self.install_update)

    def install_update(self):
        win32api.ShellExecute(0, 'open', resource_path(r'data_files/data_update_app/alashPars.exe'), None, None, 10)
        self.destroy()
        self.parent.destroy()
        sys.exit(app.exec_())

    def thread(self):
        t1 = threading.Thread(target=self.download_app_exe)
        t1.start()

    def download_app_exe(self):
        self.progressBar_download_app.setMaximum(0)
        self.label_update_text.setText('Идет загрузка exe файла')
        self.pushButton_install_app.setEnabled(False)

        try:
            url = "https://drive.google.com/uc?export=download&id=1_DTat-JPa0O6UDPpgUPTLXJg2JFiPxP8"
            output = "data_files/data_update_app/alashPars.7z"
            gdown.download(url, output)

            py7zr.SevenZipFile(resource_path(r'data_files/data_update_app/alashPars.7z'))\
                .extractall(resource_path(r'data_files/data_update_app/'))
            os.remove(resource_path(r'data_files/data_update_app/alashPars.7z'))

            self.progressBar_download_app.setMaximum(100)
            # self.progressBar_download_app.setValue(100)
            self.label_update_text.setText('Загрузка завершена. Нажмите на кнопку "Установить"')
            self.pushButton_install_app.setEnabled(True)

        except Exception as ex:
            print(ex)
            self.label_update_text.setText(f'{ex}')

        # with gdown.download(url, output) as r:
        #     print('count ', int(r.headers.get('Content-Length')))
        #     self.progressBar_download_app['maximum'] = int(r.headers.get('Content-Length'))
        #     r.raise_for_status()
        #     with open(resource_path(r'data_files/test.exe'), 'wb') as f:
        #         for chunk in r.iter_content(chunk_size=4096):
        #             if chunk:  # filter out keep-alive new chunks
        #                 f.write(chunk)
        #                 self.progressBar_download_app.setValue(chunk)

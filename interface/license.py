"""
Configuration window.
"""
import threading
from datetime import datetime
import sys
import telepot
from PyQt5 import uic
from PyQt5.QtCore import QSettings, QTime
from PyQt5.QtWidgets import (QDialog, QMainWindow, QApplication)
from interface.resources_qtdesigner import license_rs

from enums import curr_uuid, token, channel_id
from helpers import resource_path, logger

app = QApplication(sys.argv)


class License(QDialog):
    """
    license window.
    """

    def __init__(self, parent: QMainWindow):
        license_rs.qInitResources()
        super(License, self).__init__(parent)  # Initializing object

        uic.loadUi(resource_path(r'UI/license.ui'), self)  # Loading the main UI
        self.parent = parent
        self.setting_variables = QSettings(resource_path(r'data_shop/config.ini'), QSettings.IniFormat)
        self.lineEdit_key_app.setText(self.setting_variables.value('key_app'))
        # self.thread()
        self.pushButton_send_request_key.clicked.connect(self.thread)
        self.pushButton_save_key.clicked.connect(self.safe_key)

    def send_request(self):
        try:
            bot = telepot.Bot(token)
            bot.sendMessage(channel_id, curr_uuid)  # send a activation message to telegram receiver id
            self.timeEdit.setTime(QTime.currentTime())
            self.pushButton_send_request_key.setEnabled(False)
            self.label_error_text.setText('Запрос отправлен, свяжитесь с админом для получения ключа ')
            self.label_error_text.setStyleSheet("color:green")
        except Exception as ex:
            logger.error(ex)
            self.label_error_text.setText(f'{ex}')
            self.label_error_text.setStyleSheet("color:red")

    def thread(self):
        t1 = threading.Thread(target=self.send_request)
        t1.start()

    def safe_key(self):
        self.setting_variables.setValue('key_app', self.lineEdit_key_app.text())
        self.pushButton_save_key.setEnabled(False)

    def closeEvent(self, event):
        self.destroy()
        self.parent.destroy()
        sys.exit(app.exec_())

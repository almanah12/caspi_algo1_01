"""
CREATE NEW VERSION
Main caspi_algo_mix application.
"""
import os
import sys
import uuid
from datetime import datetime

import ntplib
import requests

from PyQt5 import uic
from PyQt5.QtCore import QThreadPool

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from cryptocode import decrypt

from sqlalchemy import select, inspect, MetaData

from interface.add_base_data import Add_Base_Data
from interface.resources_qtdesigner import main_rs
from db_QSqlDatabase import model_temp, model_perm
from enums import filter_for_goods_with_data, filter_for_goods_without_data, filter_all_data, _AppName_, curr_uuid
from slots import initiate_slots
from helpers import resource_path, get_current_version, logger
from threads import runThread
from interface.utils import add_to_table_widget, show_and_bring_window_to_front, add_to_data_table_view
from interface.configuration import Configuration
from interface.update import Update
from interface.license import License


from db_tables import temporary_table, engine
app = QApplication(sys.argv)


class Interface(QMainWindow):
    """
    """
    def __init__(self, parent=None):
        # Беру конец uuid. потому что она постоянна
        main_rs.qInitResources()
        super(Interface, self).__init__(parent)  # Initializing object
        logger.info(curr_uuid)
        logger.info('curr_uuid')
        logger.info('curr_uuid123')

        self.license = License(parent=self)  # Loading configuration
        print(self.license.lineEdit_key_app.text())

        ntpCllient = ntplib.NTPClient()
        res = ntpCllient.request('pool.ntp.org')

        date_demo_work = datetime(2022, 3, 22)
        logger.info(date_demo_work.timestamp() - res.tx_time)

        if date_demo_work.timestamp() - res.tx_time < 0:
            QMessageBox.information(self, 'Демо-версия', 'Срок демо-версии истек')
            sys.exit()

        word_key = decrypt(
            self.license.lineEdit_key_app.text(), curr_uuid)
        if not word_key:
            logger.debug('Not key')
            licen = License(parent=self)  # Loading update
            self.show_simulation(licen)
        #
        # logger.info(word_key)

        # main_rs.qInitResources()
        # super(Interface, self).__init__(parent)  # Initializing object

        uic.loadUi(resource_path(r'UI/parsingMain.ui'), self)  # Loading the main UI

        self.configuration = Configuration(parent=self)  # Loading configuration

        # Initiating threading pool
        self.threadCount = self.configuration.number_thread_spinBox.value()

        self.threadPool = QThreadPool()
        self.threadPool.setMaxThreadCount(self.threadCount) # задаем число потоков

        initiate_slots(app=app, gui=self)  # Initiating slots.

        self.check_stop = False  # Для проверки нажался ли кнопка 'End simulition' , true - нажат

        if self.table_exists(engine, 'permanent_table'):
            add_to_data_table_view(self, model_perm, 'permanent_table', self.permanent_tableView)

        if self.table_exists(engine, 'temporary_table'):
            add_to_data_table_view(self, model_temp, 'temporary_table', self.temporary_tableView)

    def initiate_click_run_thread(self):
        """
        """
        try:
            if self.configuration.condition_filled_data_in_settings():
                self.check_stop = False  # Обновляет
                self.disable_interface(True, count=0)
                self.worker_boss = runThread.RunThread(gui=self, threadpool=self.threadPool)
                self.worker_boss.signals.activity_table.connect(self.add_to_data_table)
                self.worker_boss.signals.activity_monitor.connect(self.add_to_activity_monitor)
                self.worker_boss.signals.restore.connect(self.disable_interface)
                self.threadPool.start(self.worker_boss)
            else:
                QMessageBox.critical(self, 'Ошибка', 'Нужно заполнить обьязательные поля в "Настройки"')

        except Exception as ex:
            print('__main__py-initiate_click_run_thread: ', ex)

    # def closeEvent(self, event):
    #         """Main window closed, override PyQt5 widget function"""
    #
    #         reply = QMessageBox.question(self, 'Message',
    #                                      "Are you sure to quit?", QMessageBox.Yes |
    #                                      QMessageBox.No, QMessageBox.No)
    #         if reply == QMessageBox.Yes:
    #             event.accept()
    #         else:
    #             event.ignore()

    def show_simulation(self, qdialog):
        """
        Opens simulation settings in the configuration window.
        """
        show_and_bring_window_to_front(qdialog)


    def end_bot_thread(self):
        """
        Ends bot based on caller.pyin
        """
        self.disable_interface(True, 1, everything=True)  # Disable everything until everything is done.
        self.check_stop = True

    def disable_interface(self, disable: bool, count: int, everything: bool = False):
        """
        Function that will control trading configuration interfaces.
        :param everything: Disables everything during initialization.
        :param disable: If true, configuration settings get disabled.
        :param caller: Caller that determines which configuration settings get disabled.
        """
        self.progressBar.setMaximum(count)
        disable = not disable
        self.configureButton.setEnabled(disable)
        self.runButton.setEnabled(disable)

        if everything:
            self.endButton.setEnabled(disable)
        else:
            self.endButton.setEnabled(not disable)

    def add_to_data_table(self):
        """
        """
        add_to_data_table_view(self, model_temp, 'temporary_table', self.temporary_tableView)
        self.temporary_tableView.scrollToBottom()

        add_to_data_table_view(self, model_perm, 'permanent_table', self.permanent_tableView)
        self.permanent_tableView.scrollToBottom()

    def add_to_activity_monitor(self, message: str, color: int):
        """
        Function that adds activity information to the simulation activity monitor.
        :param color:
        :param message: Message to add to simulation activity log.
        """
        add_to_table_widget(self.activityMonitor, [message], color)
        # self.simulationActivityMonitor.scrollToBottom()

    def choice_table(self):
        if self.comboBox.currentText() == 'Временная табл.':
            add_to_data_table_view(self, model_temp, 'temporary_table', self.tableView)
        else:
            add_to_data_table_view(self, model_temp, 'permanent_table', self.tableView)

    def search_articul(self, s):
        filter_str = 'Артикул LIKE "%{}%"'.format(s)  # s это текст вводимый в поле поиска
        filter_str_term = 'Ссылка LIKE "%{}%"'.format(s)
        model_perm.setFilter(filter_str)
        model_temp.setFilter(filter_str_term)

    def update_table(self):
        model_temp.setFilter(filter_all_data)
        model_perm.setFilter(filter_all_data)

    def filter_data(self):
        """
        Фильтрует данные
        """
        if self.filter_comboBox.currentText() == 'Товары без данных':
            model_perm.setFilter(filter_for_goods_without_data)

        elif self.filter_comboBox.currentText() == 'Товары с данными':
            model_perm.setFilter(filter_for_goods_with_data)

        else:
            model_perm.setFilter(filter_all_data)

    def delete_row_data(self):
        links = []
        s = select(temporary_table)
        conn = engine.connect()
        res = conn.execute(s)
        for row in res:
            links.append(row.Ссылка)
        conn.close()

    def table_exists(self, engine, name):
        ins = inspect(engine)
        ret = ins.dialect.has_table(engine.connect(), name)
        return ret

    def check_updates(self):
        try:
            response = requests.get(
                'https://drive.google.com/uc?export=download&id=1EDctCOZbqzXvhIUfo8Qv-rTpVnjfi0gq')
            data = response.text

            if float(data) > float(get_current_version()):
                QMessageBox.about(self, 'Запрос', 'Обновление доступно')
                reply = QMessageBox.question(self, 'Обновление!',
                                             f'Нужно обновить {_AppName_} {get_current_version()} на {data}', QMessageBox.Yes |
                                             QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    update = Update(parent=self)  # Loading update
                    self.show_simulation(update)
                else:
                    pass
            else:
                QMessageBox.about(self, 'Запрос', 'Обновление не вышло')
        except Exception as ex:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка {ex}')


def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)


def main():
    """
    Main function.
    """
    app.setStyle('Fusion')
    interface = Interface()
    interface.showNormal()
    sys.excepthook = except_hook
    sys.exit(app.exec_())


def except_hook(cls, exception, trace_back):
    """
    Exception hook.
    """
    sys.__excepthook__(cls, exception, trace_back)


if __name__ == '__main__':
    main()

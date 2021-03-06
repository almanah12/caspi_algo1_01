"""
CREATE NEW VERSION
Main caspi_algo_mix application.
"""
import sys
import requests

from PyQt5 import uic
from PyQt5.QtCore import QThreadPool

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from cryptocode import decrypt

from sqlalchemy import select, inspect
from threading import Thread
from caspi_pars.interface.resources_qtdesigner import main_rs
from caspi_pars.db_QSqlDatabase import model_temp, model_perm
from caspi_pars.enums import filter_all_data, _AppName_, curr_uuid, all_perm_data, count_cities,filter_for_goods_without_data, filter_for_goods_with_data
from caspi_pars.slots import initiate_slots
from caspi_pars.helpers import resource_path, get_current_version, logger
from caspi_pars.threads import runThread
from caspi_pars.interface.utils import add_to_table_widget, show_and_bring_window_to_front, add_to_data_table_view
from caspi_pars.interface.configuration import Configuration

from caspi_pars.interface.update import Update
from caspi_pars.interface.license import License
from caspi_pars.db_tables import temporary_table, engine, session, permanent_table


app = QApplication(sys.argv)


class Interface(QMainWindow):
    """
    """
    def __init__(self, parent=None):
        # Беру конец uuid. потому что она постоянна
        main_rs.qInitResources()
        super(Interface, self).__init__(parent)  # Initializing object

        self.license = License(parent=self)  # Loading configuration

        # ntpCllient = ntplib.NTPClient()
        # res = ntpCllient.request('pool.ntp.org')
        #
        # date_demo_work = datetime(2022, 3, 22)
        # logger.info(date_demo_work.timestamp() - res.tx_time)
        #
        # if date_demo_work.timestamp() - res.tx_time < 0:
        #     QMessageBox.information(self, 'Демо-версия', 'Срок демо-версии истек')
        #     sys.exit()

        word_key = decrypt(
            self.license.lineEdit_key_app.text(), curr_uuid)
        if not word_key:
            logger.debug('Not key')
            licen = License(parent=self)  # Loading update
            self.show_simulation(licen)

        uic.loadUi(resource_path(r'UI/parsingMain.ui'), self)  # Loading the main UI

        self.configuration = Configuration(parent=self)  # Loading configuration
        # self.add_data_base = Add_Base_Data(parent=self)  # Loading

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

        self.comboBox_show_data_other_city.setToolTip("Показывает данные для определеннго числа городов")
        self.filter_comboBox.setToolTip("Фильтр данных")
        self.pushButton_path_to_excel_1c.setToolTip("Путь к файлу Excel(1С) для обн. данных")
        self.pushButton_update.setToolTip("Обновить данные")

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

    # def choice_table(self):
    #     if self.comboBox.currentText() == 'Временная табл.':
    #         add_to_data_table_view(self, model_temp, 'temporary_table', self.tableView)
    #     else:
    #         add_to_data_table_view(self, model_perm, 'permanent_table', self.tableView)

    def search_articul(self, s):
        filter_str = 'Артикул LIKE "%{}%"'.format(s)  # s это текст вводимый в поле поиска
        filter_str_term = 'Ссылка LIKE "%{}%"'.format(s)
        model_perm.setFilter(filter_str)
        model_temp.setFilter(filter_str_term)

    def update_table(self):

        model_temp.setFilter(filter_all_data)
        add_to_data_table_view(self, model_perm, 'permanent_table', self.permanent_tableView)

        if self.filter_comboBox.currentText() == 'Товары без данных':
            model_perm.setFilter(filter_for_goods_without_data)

        elif self.filter_comboBox.currentText() == 'Товары с данными':
            model_perm.setFilter(filter_for_goods_with_data)

        else:
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


    def thread_func(self, func):
        th = Thread(target=func)
        th.start()

    def fill_data(self):
        for row_d in all_perm_data:
            print(row_d)
            for city_c in range(count_cities):
                if row_d['Город_'+str(city_c+1)]:
                    session.query(permanent_table).filter(permanent_table.c.Артикул == row_d['Артикул']).update(
                        {'Сбстоимость' + str(city_c+1): int(int(row_d['Тек_ц' + str(city_c+1)])*0.75)}, synchronize_session=False)
                    session.commit()
                    session.query(permanent_table).filter(permanent_table.c.Артикул == row_d['Артикул']).update(
                        {'Мин_ц' + str(city_c+1): int(int(row_d['Тек_ц' + str(city_c+1)])*0.96)}, synchronize_session=False)
                    session.query(permanent_table).filter(permanent_table.c.Артикул == row_d['Артикул']).update(
                        {'Макс_ц' + str(city_c+1): int(int(row_d['Тек_ц' + str(city_c+1)])*2)}, synchronize_session=False)
                    session.commit()

        self.update_table()


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

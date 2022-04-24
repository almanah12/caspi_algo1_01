"""
CREATE NEW VERSION
Main caspi_algo_mix application.
"""
import sys
import threading
import time

import requests

from PyQt5 import uic
from PyQt5.QtCore import QThreadPool, QSettings

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from cryptocode import decrypt

from sqlalchemy import select, inspect
from threading import Thread
from caspi_pars.interface.resources_qtdesigner import main_rs
from caspi_pars.db_QSqlDatabase import model_temp, model_perm
from caspi_pars.enums import filter_all_active_data, _AppName_, curr_uuid, all_perm_data, count_cities, \
    filter_for_goods_without_data, filter_for_goods_with_data, filter_all_data, filter_all_data_for_temp_t
from caspi_pars.slots import initiate_slots, init_other_comm
from caspi_pars.helpers import resource_path, get_current_version, logger
from caspi_pars.threads import runThread
from caspi_pars.interface.utils import add_to_table_widget, show_and_bring_window_to_front, add_to_data_table_view
from caspi_pars.interface.configuration import Configuration

from caspi_pars.interface.update import Update
from caspi_pars.interface.license import License
from caspi_pars.db_tables import temporary_table, engine, session, permanent_table
from caspi_pars.other_func.auto_confirm_order import AutoConfirm


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
        init_other_comm(gui=self)
        self.check_stop = False  # Для проверки нажался ли кнопка 'End simulition' , true - нажат

        if self.table_exists(engine, 'permanent_table'):
            add_to_data_table_view(self, model_perm, 'permanent_table', self.permanent_tableView)

        if self.table_exists(engine, 'temporary_table'):
            add_to_data_table_view(self, model_temp, 'temporary_table', self.temporary_tableView)

        self.CONFIG_FILE_NAME = resource_path(r'data_shop/config.ini')
        self.setting_variables = QSettings(self.CONFIG_FILE_NAME, QSettings.IniFormat)
        self.comboBox_auto_confirm_order.setCurrentText(self.setting_variables.value('auto_confirm_order'))

        self.thread_func(self.auto_confirm_order_cond)
        self.stop_threads = False

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

    def closeEvent(self, event):
        """Main window closed, override PyQt5 widget function"""
        #
        # reply = QMessageBox.question(self, 'Message',
        #                              "Are you sure to quit?", QMessageBox.Yes |
        #                              QMessageBox.No, QMessageBox.No)
        # if reply == QMessageBox.Yes:
        #     event.accept()
        # else:
        #     event.ignore()
        self.stop_threads = True
        self.setting_variables.setValue('auto_confirm_order', self.comboBox_auto_confirm_order.currentText())
        self.checkbox(0)

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

        if self.filter_comboBox.currentText() == 'Товары без данных':
            model_perm.setFilter(filter_for_goods_without_data)

        elif self.filter_comboBox.currentText() == 'Товары с данными':
            model_perm.setFilter(filter_for_goods_with_data)

        elif self.filter_comboBox.currentText() == 'Активные':
            model_perm.setFilter(filter_all_active_data)
            filter_str = 'Артикул LIKE "%{}%" AND Active_g LIKE 1'.format(s)  # s это текст вводимый в поле поиска
            # filter_str_term = 'Ссылка LIKE "%{}%"'.format(s)
            model_perm.setFilter(filter_str)
        else:
            model_perm.setFilter(filter_all_data)


        filter_str_term = 'Ссылка LIKE "%{}%"'.format(s)
        model_temp.setFilter(filter_str_term)

    def update_table(self):

        model_temp.setFilter(filter_all_data_for_temp_t)
        add_to_data_table_view(self, model_perm, 'permanent_table', self.permanent_tableView)

        self.filter_data(self.search_table_articul_lineEdit.text())

    def filter_data(self, s):
        """
        Фильтрует данные
        """
        type_search = self.comboBox_search_name.currentText()
        if self.filter_comboBox.currentText() == 'Товары без данных':
            model_perm.setFilter(filter_for_goods_without_data.format(type_search, s))

        elif self.filter_comboBox.currentText() == 'Товары с данными':
            model_perm.setFilter(filter_for_goods_with_data.format(type_search, s))

        elif self.filter_comboBox.currentText() == 'Активные':
            model_perm.setFilter(filter_all_active_data.format(type_search, s))
        else:
            model_perm.setFilter(filter_all_data.format(type_search, s))
        return model_perm

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
        if self.comboBox_fill_data_table.currentText() == 'Заполнить данные':
            model_perm_filter = self.filter_data(self.search_table_articul_lineEdit.text())
            count_row_curr_table = model_perm_filter.rowCount()

            for i in range(count_row_curr_table):
                curr_vend_code = str(model_perm_filter.index(i, 3).data())
                row_d = all_perm_data.filter(permanent_table.c.Артикул == curr_vend_code).one()
                if row_d['C']:
                    for city_c in range(count_cities):
                        if row_d['Город_'+str(city_c+1)]:
                            session.query(permanent_table).filter(permanent_table.c.Артикул == row_d['Артикул']).update(
                                {'Сбстоимость' + str(city_c+1): int(int(row_d['Тек_ц' + str(city_c+1)])*self.doubleSpinBox_first_price_caf.value())})
                            session.query(permanent_table).filter(permanent_table.c.Артикул == row_d['Артикул']).update(
                                {'Мин_ц' + str(city_c+1): int(int(row_d['Тек_ц' + str(city_c+1)])*self.doubleSpinBox_min_price_caf.value())})
                            session.query(permanent_table).filter(permanent_table.c.Артикул == row_d['Артикул']).update(
                                {'Макс_ц' + str(city_c+1): int(int(row_d['Тек_ц' + str(city_c+1)])*self.doubleSpinBox_max_price_caf.value())})
                            session.commit()
        else:
            model_perm_filter = self.filter_data(self.search_table_articul_lineEdit.text())
            count_row_curr_table = model_perm_filter.rowCount()

            for i in range(count_row_curr_table):
                curr_vend_code = str(model_perm_filter.index(i, 3).data())
                row_d = all_perm_data.filter(permanent_table.c.Артикул == curr_vend_code).one()
                if row_d['C']:
                    for city_c in range(count_cities):
                        if row_d['Город_'+str(city_c+1)]:
                            if self.checkBox_curr_price.isChecked():
                                session.query(permanent_table).filter(permanent_table.c.Артикул == row_d['Артикул']).update(
                                    {'Тек_ц' + str(city_c+1): int(int(row_d['Тек_ц' + str(city_c+1)])*self.doubleSpinBox_change_price_caf.value())})
                            if self.checkBox_first_price.isChecked():
                                session.query(permanent_table).filter(permanent_table.c.Артикул == row_d['Артикул']).update(
                                    {'Сбстоимость' + str(city_c+1): int(int(row_d['Сбстоимость' + str(city_c+1)])*self.doubleSpinBox_change_price_caf.value())})
                            if self.checkBox_min_price.isChecked():
                                session.query(permanent_table).filter(permanent_table.c.Артикул == row_d['Артикул']).update(
                                    {'Мин_ц' + str(city_c+1): int(int(row_d['Мин_ц' + str(city_c+1)])*self.doubleSpinBox_change_price_caf.value())})
                            if self.checkBox_max_price.isChecked():
                                session.query(permanent_table).filter(permanent_table.c.Артикул == row_d['Артикул']).update(
                                    {'Макс_ц' + str(city_c+1): int(int(row_d['Макс_ц' + str(city_c+1)])*self.doubleSpinBox_change_price_caf.value())})
                            session.commit()

        self.update_table()

    def checkbox(self, cb_st):
        model_perm_filter = self.filter_data(self.search_table_articul_lineEdit.text())
        count_row_curr_table = model_perm_filter.rowCount()

        for i in range(count_row_curr_table):
            curr_vend_code = str(model_perm_filter.index(i, 3).data())
            row_d = all_perm_data.filter(permanent_table.c.Артикул == curr_vend_code).one()
            session.query(permanent_table).filter(permanent_table.c.Артикул == row_d['Артикул']).update(
                {'C': cb_st})

        session.commit()

    def check_box_table(self):
        if self.checkBox_tableview.isChecked():
            self.checkbox(1)
        else:
             self.checkbox(0)
        self.update_table()

    def auto_confirm_order_cond(self):
        while self.comboBox_auto_confirm_order.currentText() == 'Да':
            begin_time = str(int(time.time() * 1000) - 1200100100)
            end_time = str(int(time.time() * 1000))
            url = "https://kaspi.kz/shop/api/v2/orders?page[number]=0&page[size]=100&filter[orders][state]=NEW&" \
                  "filter[orders][creationDate][$ge]=" + begin_time + "&filter[orders][creationDate][$le]=" + end_time + "&filter[orders][status]=APPROVED_BY_BANK&" \
                                                                                                                         "filter[orders][deliveryType]=PICKUP&filter[orders][signatureRequired]=false&" \
                                                                                                                         "include[orders]=user"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
                'Content-Type': 'application/vnd.api+json',
                'X-Auth-Token': 'fe6KQN9hcTCmxbJW2trHntHmDC5kD/veVvwehQGoRSo='}

            r = requests.get(url=url, headers=headers)

            data = r.json()
            id_order = [i['id'] for i in data['data']]
            attributes = [i['attributes'] for i in data['data']]
            print('id_order', id_order)

            count_order = 0
            for i in attributes:
                delay_t = int(end_time) - i['creationDate']

                if delay_t > 4800000:  # больше 80 мин.
                    print(id_order[count_order])
                    print('Confirmed')
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
                                'HTTP': '/1.1',
                                'POST': '/api/v2/orders',
                                # 'Host': 'kaspi.kz/shop',
                                'Content-Type': 'application/vnd.api+json',
                                'X-Auth-Token': 'fe6KQN9hcTCmxbJW2trHntHmDC5kD/veVvwehQGoRSo='}
                    data = {"data": {"type": "orders", "id": id_order[count_order]+"=", "attributes": {"code": "", "status": "ACCEPTED_BY_MERCHANT"}}}
                    requests.post(url='https://kaspi.kz/shop/api/v2/orders', headers=headers, json=data)
                else:
                    print(id_order[count_order])
                    print(delay_t)
                    print('Wait')
                count_order += 1

            for _ in range(120):
                time.sleep(1)
            if self.stop_threads:
                break


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

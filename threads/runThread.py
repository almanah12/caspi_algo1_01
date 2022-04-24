"""
"""
import random
import threading
from datetime import datetime
from http.server import HTTPServer, CGIHTTPRequestHandler

from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot, QThreadPool
from sqlalchemy import select
import time

from caspi_pars.threads.runThreadMethods import run_autodownload_xml, auto_loading_xml
from caspi_pars.db_QSqlDatabase import model_perm
from caspi_pars.db_tables import temporary_table, engine, session
from caspi_pars.enums import filter_all_active_data, all_perm_data, all_temp_data
from caspi_pars.db_tables import permanent_table
from caspi_pars.helpers import resource_path, logger, server_http_ngrok, download_proxy_list, restart_time, Server_Http_Ngrok, ngrok_public_url
from caspi_pars.other_func.check_data_fill import ch_data_fill
from caspi_pars.threads.runThreadMethods.create_xml import create_xml
from caspi_pars.threads.runThreadMethods.gets_dt_caspi_client import GetDataKaspiSeller
from caspi_pars.threads.runThreadMethods.kaspi_merchant import MerchantInfo
from caspi_pars.threads.runThreadMethods.parser_urls import Parser
from caspi_pars.threads.runThreadMethods.processing_data import ProcessingData
from caspi_pars.threads.runThreadMethods.installment_plan import check_promotion
from caspi_pars.webdriver_options import get_driver_parser


class BotSignals(QObject):
    """
    Signals available for the BotThread.
    """
    # pylint: disable=too-few-public-methods
    started = pyqtSignal()  # Signal emitted when bot first starts.
    activity_table = pyqtSignal()  # Signal emitted to broadcast current activity.
    activity_monitor = pyqtSignal(str, int)
    updated = pyqtSignal()  # Signal emitted when bot is updated.
    restore = pyqtSignal(bool, int)
    finished = pyqtSignal()  # Signal emitted when bot is ended.
    procesing = pyqtSignal()


class RunThread(QRunnable):
    """
    """

    def __init__(self, gui, threadpool):
        super(RunThread, self).__init__()
        self.signals = BotSignals()
        self.gui = gui
        self.threadpool = threadpool
        self.threadPool = QThreadPool()

    @pyqtSlot()
    def run(self):
        try:
            while not self.gui.check_stop:
                start_time = time.time()
                curr_day = datetime.now().day
                curr_hour = datetime.now().hour
                if (curr_day == 1 or curr_day == 10 or curr_day == 15 or curr_day == 18 or curr_day == 25) and 6 < curr_hour < 22:
                    self.signals.activity_monitor.emit("Сбор данных с 'Kaspi Marketing'", 1)
                    logger.info("Сбор данных с 'Kaspi Marketing'")
                    MerchantInfo(self.gui)
                # # сбор товаров с маг. клиента
                if not self.gui.check_stop:
                    self.signals.activity_monitor.emit('Сбор данных с "Кабинета продавца"', 4)
                    # self.signals.activity_monitor.emit('Сбор данных с "Кабинета продавца" check demo-version', 4)

                    logger.info('Сбор данных с "Кабинета продавца"')
                    gets_data = GetDataKaspiSeller(self.gui, self.signals.activity_monitor)
                    gets_data.gets_data()
                    self.signals.activity_table.emit()
                    self.signals.restore.emit(True, 0)
                    self.signals.activity_monitor.emit(
                        'С "Каб.продавца" взята данных на {} товаров'.format(GetDataKaspiSeller.count_gds), 1)
                    logger.debug('С "Каб.продавца" взята данных на {} товаров.'.format(GetDataKaspiSeller.count_gds))
                    logger.info(GetDataKaspiSeller.count_other_city)

                # Парсинг товаров
                if not self.gui.check_stop:
                    self.signals.activity_monitor.emit("Сбор данных с сайта товара", 1)
                    logger.info('Сбор данных с сайта товара')

                    if self.gui.configuration.use_proxy_comboBox.currentText() == 'Да':
                        use_proxy = True
                    else:
                        use_proxy = False

                    all_cities = []
                    if self.gui.configuration.lineEdit_city_name_1.text():
                        all_cities.append(self.gui.configuration.lineEdit_city_name_1.text())
                    if self.gui.configuration.lineEdit_city_name_2.text():
                        all_cities.append(self.gui.configuration.lineEdit_city_name_2.text())
                    if self.gui.configuration.lineEdit_city_name_3.text():
                        all_cities.append(self.gui.configuration.lineEdit_city_name_3.text())
                    if self.gui.configuration.lineEdit_city_name_4.text():
                        all_cities.append(self.gui.configuration.lineEdit_city_name_4.text())

                    num_city = 1
                    for city in all_cities:
                        if self.gui.check_stop:
                            break
                        active_links_list = [i['Ссылка'] for i in all_temp_data.filter(temporary_table.c.Все_города.contains(city)).all() if not i['Scrap_st']]
                        logger.debug(active_links_list)
                        if active_links_list:
                            parser_site = Parser(self.gui, active_links_list, city, num_city, self.signals.activity_monitor, use_proxy)
                            parser_site.parse()
                            Parser.first_request = 0
                            num_city += 1
                            session.commit()
                            if self.gui.check_stop:
                                break
                        get_driver_parser(use_proxy).quit()

                    if self.gui.configuration.same_price_citiesradioButton.isChecked():
                        self.signals.activity_monitor.emit(
                            'С "Каб.продавца" взята данных на {} товаров. Сделано {} запросов'.format(
                                GetDataKaspiSeller.count_gds, Parser.count_requests), 1)
                        logger.debug('С "Каб.продавца" взята данных на {} товаров. Сделано {} запросов'
                                     .format(GetDataKaspiSeller.count_gds, Parser.count_requests))
                    else:
                        self.signals.activity_monitor.emit(
                            'С "Каб.продавца" взята данных на {} товаров. С учетом режима "Разные цены для городов" '
                            'сделано {} запросов'.format(GetDataKaspiSeller.count_gds, Parser.count_requests), 1)
                        logger.debug(
                            'С "Каб.продавца" взята данных на {} товаров. С учетом режима "Разные цены для городов" '
                            'сделано {} запросов'.format(GetDataKaspiSeller.count_gds, Parser.count_requests))

                # Обработка данных товаров
                if not self.gui.check_stop:
                    ch_dt_fill = ch_data_fill(self.gui)

                    proc_dt = ProcessingData(self.gui, self.signals.activity_monitor)
                    proc_dt.write_perm_table_data()
                    if ch_dt_fill[0]:
                        self.signals.activity_monitor.emit("Запуск обработки данных", 1)
                        logger.info('Запуск обработки данных')
                        proc_dt.processing_dt()
                    else:
                        self.signals.activity_monitor.emit(ch_dt_fill[1], 2)
                        logger.error('Данные товаров не заполнено, заполните таблицу')
                        break

                # # Собрать данные в xml файл
                if not self.gui.check_stop:
                    self.signals.activity_monitor.emit('Запуск создание "xml" файла ', 1)
                    logger.info('Запуск создание "xml" файла ')
                    create_xml(self.gui)

                if not self.gui.check_stop:
                    self.signals.activity_monitor.emit('Запуск записи xml файла в сервер', 1)
                    logger.info('Запуск записи xml файла в сервер')

                # запись xml файла в сервер google cloud storage
                if not self.gui.check_stop:
                    run_autodownload_xml.upload_to_bucket_xml(self.gui.configuration.name_xml_file_lineEdit.text(),
                                                              resource_path(r"data_shop/alash.xml"),
                                                              self.gui.configuration.name_folder_lineEdit.text())

                # запись xml файла в локальный http сервер через ngrok
                if not self.gui.check_stop:
                    if self.gui.configuration.auto_downl_xml_comboBox.currentText() == 'Да' \
                            and self.gui.configuration.radioButton_cond_use_ngrok.isChecked() == False\
                            :
                        self.signals.activity_monitor.emit('Поставлена автоматическая загрузка xml файла http-сервер', 1)
                        ngrok_thread = threading.Thread(target=server_http_ngrok)
                        ngrok_thread.start()
                        logger.info('Поставлена автоматическая загрузка xml файла http-сервер')
                        ngrok_url = ngrok_public_url()+'/alash.xml'
                        logger.debug(ngrok_url)
                        page_load = auto_loading_xml.set_http_adress(self.gui, self.signals.activity_monitor, ngrok_url)
                        # Если xml файл записался
                        if page_load == 'Good':
                            self.gui.configuration.radioButton_cond_use_ngrok.setChecked(True)
                        elif page_load == 'Timeout':
                            self.signals.activity_monitor.emit('Timeout or xml file error', 2)
                            logger.error('Timeout or xml file error')
                            break
                        else:
                            self.signals.activity_monitor.emit(page_load, 2)
                            logger.debug(page_load)
                            break

                # Проверка рассрочек
                if not self.gui.check_stop:
                    self.signals.activity_monitor.emit('Проверка рассрочек', 1)
                    if 6 <= curr_hour <= 22:
                        logger.info('Проверка рассрочек "Начало"')
                        th_start_installment = threading.Thread(target=check_promotion('data_cat_comm_start'))
                        th_start_installment.start()
                    if 6 <= curr_hour <= 22:
                        logger.info('Проверка рассрочек "Конец"')
                        th_end_installment = threading.Thread(target=check_promotion('data_cat_comm_end'))
                        th_end_installment.start()

                # Запуск программы через х время
                if not self.gui.check_stop:
                    # if GetDataKaspiSeller.count_gds == 0.5:
                    #     restart_time(25, 35, start_time, self.signals.activity_monitor, self.gui)

                    if GetDataKaspiSeller.count_gds == 0 and GetDataKaspiSeller.count_gds*0.8 <= Parser.count_requests:
                        restart_time(4, 8, start_time, self.signals.activity_monitor, self.gui)

                    else:
                        restart_time(self.gui.configuration.interval_from_spinBox.value(), self.gui.configuration.interval_before_spinBox.value(),
                                     start_time, self.signals.activity_monitor, self.gui)

                # Обнуления переменых
                GetDataKaspiSeller.count_gds = 0
                GetDataKaspiSeller.count_other_city = 0
                Parser.count_requests = 0

        except Exception as ex:
            logger.error(ex)
            self.signals.activity_monitor.emit('Ошибка в потоке RunThread: ' + str(ex), 2)
            self.signals.restore.emit(False, 1)

        finally:
            GetDataKaspiSeller.count_gds = 0
            GetDataKaspiSeller.count_other_city = 0
            Parser.count_requests = 0
            self.signals.restore.emit(False, 1)

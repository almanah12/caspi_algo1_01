"""
"""
import random
import threading

from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot, QThreadPool
from sqlalchemy import select

from threads.runThreadMethods import run_autodownload_xml, auto_loading_xml
from db_QSqlDatabase import model_perm
from db_tables import temporary_table, engine
from enums import filter_for_goods_with_data, filter_all_data
from helpers import resource_path, logger, server_http_ngrok, download_proxy_list
from threads.runThreadMethods.create_xml import create_xml
from threads.runThreadMethods.gets_dt_caspi_client import GetDataKaspiSeller
from threads.runThreadMethods.parser_urls import Parser
from threads.runThreadMethods.processing_data import ProcessingData
from threads.runThreadMethods.auto_loading_xml import set_http_adress

import time


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
        start_time = time.time()
        try:
            while not self.gui.check_stop:
                # сбор товаров с маг. клиента
                if self.gui.check_stop:
                    break
                self.signals.activity_monitor.emit('Сбор данных с "Кабинета продавца"', 4)
                self.signals.activity_monitor.emit('Сбор данных с "Кабинета продавца" check demo-version', 4)

                logger.info('Сбор данных с "Кабинета продавца"')

                gets_data = GetDataKaspiSeller(self.gui, self.signals.activity_monitor)
                gets_data.gets_data()
                self.signals.activity_table.emit()
                self.signals.restore.emit(True, 0)
                self.signals.activity_monitor.emit(
                    'С "Каб.продавца" взята данных на {} товаров'.format(GetDataKaspiSeller.count_gds), 1)
                logger.debug('С "Каб.продавца" взята данных на {} товаров.'.format(GetDataKaspiSeller.count_gds))
                logger.info(GetDataKaspiSeller.count_other_city)
                # # # Парсинг товаров
                # # # download_proxy_list()
                # if not self.gui.check_stop:
                #     links = []
                #     s = select(temporary_table)
                #     conn = engine.connect()
                #     res = conn.execute(s)
                #     for row in res:
                #         links.append(row.Ссылка)
                #     logger.debug(links)
                #     self.signals.activity_monitor.emit("Сбор данных с сайта товара", 1)
                #     logger.info('Сбор данных с сайта товара')
                #     parser_site = Parser(self.gui, links, self.signals.activity_monitor)
                #     parser_site.parse()
                #     if self.gui.configuration.same_price_citiesradioButton.isChecked():
                #         self.signals.activity_monitor.emit(
                #             'С "Каб.продавца" взята данных на {} товаров. Сделано {} запросов'.format(
                #                 GetDataKaspiSeller.count_gds, Parser.count_requests), 1)
                #         logger.debug('С "Каб.продавца" взята данных на {} товаров. Сделано {} запросов'
                #                      .format(GetDataKaspiSeller.count_gds, Parser.count_requests))
                #     else:
                #         self.signals.activity_monitor.emit(
                #             'С "Каб.продавца" взята данных на {} товаров. С учетом режима "Разные цены для городов" '
                #             'сделано {} запросов'.format(GetDataKaspiSeller.count_gds, Parser.count_requests), 1)
                #         logger.debug(
                #             'С "Каб.продавца" взята данных на {} товаров. С учетом режима "Разные цены для городов" '
                #             'сделано {} запросов'.format(GetDataKaspiSeller.count_gds, Parser.count_requests))
                #
                # # Обработка данных товаров
                # if not self.gui.check_stop:
                #     model_perm.setFilter(filter_for_goods_with_data)
                #     count_goods_with_data = model_perm.rowCount()
                #
                #     model_perm.setFilter(filter_all_data)
                #     count_goods_all_data = model_perm.rowCount()
                #
                #     if count_goods_all_data == count_goods_with_data:
                #         self.signals.activity_monitor.emit("Запуск обработки данных", 1)
                #         logger.info('Запуск обработки данных')
                #         proc_dt = ProcessingData(self.gui, self.signals.activity_monitor)
                #         proc_dt.processing_dt()
                #     else:
                #         self.signals.activity_monitor.emit("Данные товаров не заполнено, заполните таблицу", 2)
                #         logger.error('Данные товаров не заполнено, заполните таблицу')
                #         break
                #
                # # Собрать данные в xml файл
                # if not self.gui.check_stop:
                #     self.signals.activity_monitor.emit('Запуск создание "xml" файла ', 1)
                #     logger.info('Запуск создание "xml" файла ')
                #     create_xml(self.gui)
                #
                # self.signals.activity_monitor.emit('Запуск записи xml файла в сервер', 1)
                # logger.info('Запуск записи xml файла в сервер')

                # запись xml файла в сервер google cloud storage
                # if not self.gui.check_stop:
                #     run_autodownload_xml.upload_to_bucket_xml(self.gui.configuration.name_xml_file_lineEdit.text(),
                #                                               resource_path(r"data_shop/alash.xml"),
                #                                               self.gui.configuration.name_folder_lineEdit.text())
                #
                # # запись xml файла в локальный http сервер через ngrok
                if not self.gui.check_stop:
                    if self.gui.configuration.auto_downl_xml_comboBox.currentText() == 'Да' \
                            and self.gui.configuration.radioButton_cond_use_ngrok.isChecked() == False:
                        self.signals.activity_monitor.emit('Поставлена автоматическая загрузка xml файла http-сервер', 1)
                        ngrok_thread = threading.Thread(target=server_http_ngrok)
                        ngrok_thread.start()
                        logger.info('Поставлена автоматическая загрузка xml файла http-сервер')
                        auto_loading_xml.set_http_adress(self.gui, self.signals.activity_monitor)
                        self.gui.configuration.radioButton_cond_use_ngrok.setChecked(True)

                # Обнуления переменых
                GetDataKaspiSeller.count_gds = 0
                GetDataKaspiSeller.count_other_city = 0
                Parser.count_requests = 0

                # Запуск программы через х время
                if not self.gui.check_stop:
                    from_time_sec = self.gui.configuration.interval_from_spinBox.value() * 60
                    before_time_sec = self.gui.configuration.interval_before_spinBox.value() * 60
                    restart_time = random.randint(from_time_sec, before_time_sec)
                    m = (restart_time // 60) % 60
                    s = restart_time % 60
                    self.signals.activity_monitor.emit('Цикл перезапустится через {} мин. и {} сек.'.format(m, s), 4)
                    logger.info('Цикл перезапустится через {} мин. и {} сек.'.format(m, s))
                    for _ in range(restart_time):
                        if not self.gui.check_stop:
                            time.sleep(1)
                        else:
                            break
                end_time = time.time() - start_time
                logger.debug('Время выполнение: {}'.format(end_time))

        except Exception as ex:
            logger.error(ex)
            self.signals.activity_monitor.emit('Ошибка в потоке RunThread: ' + str(ex), 2)
            self.signals.restore.emit(False, 1)

        finally:
            self.signals.restore.emit(False, 1)

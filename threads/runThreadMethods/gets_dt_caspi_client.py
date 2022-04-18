import os
import pickle
import shutil
import time
import random
import pandas as pd

from collections import OrderedDict
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import MetaData
from selenium.common.exceptions import TimeoutException

from caspi_pars.helpers import resource_path, logger, enter_caspi_seller
from caspi_pars.webdriver_options import get_driver
from caspi_pars.db_tables import temporary_table, permanent_table, engine, session


class GetDataKaspiSeller:
    count_gds = 0
    count_other_city = 0
    active_goods = []

    def __init__(self, gui, signal_monitor):
        self.gui = gui
        self.signal_monitor = signal_monitor

        self.vend_code = [w for w in Path(resource_path(r'data_shop/cannot_be_parsed.txt')).read_text(encoding="utf-8").replace("\n", " ").split()]

    def gets_data(self):
        # Удаляем папку с excel файлами
        if os.path.exists(resource_path(r'data_files/data_shops')):
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), resource_path(r'data_files/data_shops'))
            shutil.rmtree(path)

        #  Создаем папку занова для excel файлов
        os.mkdir(resource_path(r'data_files/data_shops'))

        for _ in range(3):
            try:
                meta = MetaData()
                meta.create_all(engine)  # или books.create(engine), authors.create(engine)

                # Удаляем врем.табл перед записем новых данных
                session.query(temporary_table).delete()
                session.commit()



                # Заходит на стр. каспи клиент
                url = 'https://kaspi.kz/merchantcabinet/login?logout=true'

                driver = get_driver(False)
                driver.get(url)
                driver.set_page_load_timeout(60)
                driver.implicitly_wait(20)

                if self.gui.check_stop:
                    break
                # Установливает окно браузера в полный экран(потому что мешает подсказка-помощник сайта)
                driver.maximize_window()
                # Вбиваем логин и пароль
                enter_caspi_seller(driver, self.gui.configuration.email_login_lineEdit.text(), self.gui.configuration.password_lineEdit.text())

                # for cookie in pickle.load(open(resource_path('caspi_enter_cookies') 'wb'))):
                #     driver.add_cookie(cookie)
                # time.sleep(2)
                # driver.refresh()

                if self.gui.check_stop:
                    break
                # Если стр. занова заходит на  логинацию
                # Время задержки для загрузки стр. и всплывающего окна
                # Если нет текста 'Seller center' выводится ошибка и мы выходим из цикла(это значит что мы зашли в кабинет продавца)
                # try:
                #     """
                #     После входа в магаз.продовца появляется предупреждение(оно мешает), чтобы убрать
                #     его ждем определенное время пока оно появится и убираем его
                #     """
                #
                #     # products_btn1 = driver.find_element_by_xpath(
                #     #     '/html/body/div[7]/div/table/tbody/tr[2]/td[2]/div/div/div/button')
                #     # driver.execute_script('arguments[0].click();', products_btn1)
                #     # products_btn1.click()
                #     print('test')
                #
                # except Exception:
                #     driver.close()
                #     continue
                # else:
                #     break
                self.run_page(driver)

            except TimeoutException:
                logger.error('Превышено ожидание загрузки страницы(30 сек.)')
                self.signal_monitor.emit('Превышено ожидание загрузки страницы(30 сек.)', 3)
                driver.close()
                continue
            except Exception as ex:
                logger.error(ex)
                self.signal_monitor.emit("{}".format(ex), 3)
                driver.close()
                continue
            else:
                driver.close()
                break

    def run_page(self, driver):
        for _ in range(3):
            try:
                delay = random.randint(4, 8)
                products_btn = WebDriverWait(driver, delay).until(
                    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Товары")))
                driver.execute_script("arguments[0].click();", products_btn)
            except:
                driver.refresh()
                continue
            else:
                break

        # fol_column = driver.find_element(By.XPATH, '//select[@class="form__col _12-12"]')
        #
        # fol_column.click()
        # processing_count = driver.find_element(
        #     By.XPATH, '//option[@value="PROCESSING"]').text.split('(')[1].split(')')[0]

        # Цикл работает пока кнопка 'след' доступна
        while True:
        # for j in range(1):
            # Вычисляет есть ли товары которые ожидают применение изменение
            # if int(processing_count):
            #     GetDataKaspiSeller.count_gds = 0.5
            #     break

            if self.gui.check_stop:
                break
            # Ждем пока стр загрузится
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[@class='offer-managment__product-cell-link']")))
            # Название магазов
            count_shops = driver.find_elements_by_xpath("//a[@class='offer-managment__product-cell-link']")
            GetDataKaspiSeller.count_gds += len(count_shops)

            # Цикл для записи данных товаров
            for i in range(len(count_shops)):
            # for i in range(4):
                self.gets_dt_good(driver, i)

            # Берем значение кнопки след 'true' или 'false'
            click_next = driver.find_element_by_xpath('//img[contains(@aria-label, "Next page")]').\
                get_attribute('aria-disabled')
            click_next1 = driver.find_element_by_xpath('//img[contains(@aria-label, "Next page")]')

            # Если значение false то кликаем на кнопку след
            if click_next == 'false':  # Проверяет активна ли кнопка
                driver.execute_script('arguments[0].click();', click_next1)
            # Если нет то выходим из цикла(значит мы дошли до конца списка товаров)
            else:
                break

    def gets_dt_good(self, driver, i):
        try:
            vendor_code_goods = driver.find_elements_by_xpath('//div[@title="Артикул в системе продавца"]')[i].text
            logger.debug(vendor_code_goods)

        except:
            vendor_code_goods = "Нет артикула товара"

        # не парсить выбранные товары(по артикулам), добавляет только в постоянную табл.
        # Берем цену самую высокую, и ставим в первый город(Тек ц1)
        if vendor_code_goods in self.vend_code:
            GetDataKaspiSeller.count_gds -= 1
            try:
                name_goods = driver.find_elements_by_xpath('//div[@title="Название в системе продавца"]')[i].text
                logger.debug(name_goods)
            except:
                name_goods = "Нет название товара"

            try:
                price_goods = driver.find_elements_by_xpath('//div[@class="offer-managment__price-cell-price"]')[i].text
                if len(price_goods) > 10:
                    price_goods = price_goods.split('...')[1]
                word_list = price_goods.split()
                # Преобразование текста в число. напр '100 123 т' в 100123
                num_list = filter(lambda word: word.isnumeric(), word_list)
                price_goods = int(''.join(map(str, num_list)))
            except:
                price_goods = "Нет цены за товар"

            try:
                availability_in_stores = driver.find_elements_by_xpath(
                    '//div[@class="offer-managment__pickup-points-cell-point"]')[i].text
                logger.debug(availability_in_stores)

            except:
                availability_in_stores = "Нет доступных точек"

            try:
                list_cities = [None, None,None,None]
                availability_in_stors = driver.find_elements_by_xpath(
                    '//div[@class="offer-managment__pickup-points-cell-point"]')[i].text
                for pp in availability_in_stors.split(', '):
                    if pp in self.gui.configuration.lineEdit_seller_points_1.text().split(';'):
                        list_cities[0] = self.gui.configuration.lineEdit_city_name_1.text()
                    elif pp in self.gui.configuration.lineEdit_seller_points_2.text().split(';'):
                        list_cities[1] = self.gui.configuration.lineEdit_city_name_2.text()
                    elif pp in self.gui.configuration.lineEdit_seller_points_3.text().split(';'):
                        list_cities[2] = self.gui.configuration.lineEdit_city_name_3.text()
                    elif pp in self.gui.configuration.lineEdit_seller_points_4.text().split(';'):
                        list_cities[3] = self.gui.configuration.lineEdit_city_name_4.text()

                # Отфильтровывает убирает повт. города
                sort_list_cities = list(OrderedDict.fromkeys(list_cities))

                if None in sort_list_cities:
                    count_cities = len(sort_list_cities) - 1
                else:
                    count_cities = len(sort_list_cities)

                logger.debug('list_cities {} {} {} {}'.format(list_cities[0], list_cities[1], list_cities[2], list_cities[3]))

            except:
                availability_in_stores = "Нет доступных точек"
            all_cities = '{}, {}, {}, {}'.format(list_cities[0], list_cities[1], list_cities[2], list_cities[3])
            sql_insert_temporary_table = temporary_table.insert().values(
                Артикул=vendor_code_goods, Модель=name_goods, Брэнд=name_goods.split(' ')[0],
                Доступность=availability_in_stores, Колич_г=count_cities, Все_города=all_cities, Город_1=list_cities[0],
                Тек_ц1=price_goods, Город_2=list_cities[1], Город_3=list_cities[2], Город_4=list_cities[3], Scrap_st=1)

            conn = engine.connect()
            conn.execute(sql_insert_temporary_table)
            conn.close()

        # Товары которые нужно парсить
        else:
            GetDataKaspiSeller.active_goods.append(vendor_code_goods)
            try:
                name_goods = driver.find_elements_by_xpath('//div[@title="Название в системе продавца"]')[i].text
                logger.debug(name_goods)
            except:
                name_goods = "Нет название товара"

            try:
                link_goods = driver.find_elements_by_xpath('//a[@class="offer-managment__product-cell-link"]')[i].get_attribute('href')
                logger.debug('link_goods: {}'.format(link_goods))
            except:
                link_goods = "Нет ссылки товара"

            try:
                availability_in_stores = driver.find_elements_by_xpath(
                    '//div[@class="offer-managment__pickup-points-cell-point"]')[i].text
                logger.debug(availability_in_stores)

            except:
                availability_in_stores = "Нет доступных точек"

            try:
                list_cities = [None, None,None,None]
                availability_in_stors = driver.find_elements_by_xpath(
                    '//div[@class="offer-managment__pickup-points-cell-point"]')[i].text
                for pp in availability_in_stors.split(', '):
                    if pp in self.gui.configuration.lineEdit_seller_points_1.text().split(';'):
                        list_cities[0] = self.gui.configuration.lineEdit_city_name_1.text()
                    elif pp in self.gui.configuration.lineEdit_seller_points_2.text().split(';'):
                        list_cities[1] = self.gui.configuration.lineEdit_city_name_2.text()
                    elif pp in self.gui.configuration.lineEdit_seller_points_3.text().split(';'):
                        list_cities[2] = self.gui.configuration.lineEdit_city_name_3.text()
                    elif pp in self.gui.configuration.lineEdit_seller_points_4.text().split(';'):
                        list_cities[3] = self.gui.configuration.lineEdit_city_name_4.text()

                # Отфильтровывает убирает повт. города
                sort_list_cities = list(OrderedDict.fromkeys(list_cities))

                if None in sort_list_cities:
                    count_cities = len(sort_list_cities) - 1
                else:
                    count_cities = len(sort_list_cities)

                logger.debug('list_cities {} {} {} {}'.format(list_cities[0], list_cities[1], list_cities[2], list_cities[3]))

            except:
                availability_in_stores = "Нет доступных точек"
            all_cities = '{}, {}, {}, {}'.format(list_cities[0], list_cities[1], list_cities[2], list_cities[3])
            sql_insert_temporary_table = temporary_table.insert().values(
                Артикул=vendor_code_goods, Модель=name_goods, Брэнд=name_goods.split(' ')[0], Ссылка=link_goods,
                Доступность=availability_in_stores, Колич_г=count_cities, Все_города=all_cities, Город_1=list_cities[0],
                Город_2=list_cities[1], Город_3=list_cities[2], Город_4=list_cities[3])
            # Переменая которая нужна для записи в данных в постоянную табл.
            sql_insert_permanent_table = permanent_table.insert().values(
                Артикул=vendor_code_goods, Модель=name_goods, Город_1=list_cities[0],
                Город_2=list_cities[1], Город_3=list_cities[2],  Город_4=list_cities[3], Колич_г=count_cities)
            sql_permanent_update = permanent_table.update().where(permanent_table.c.Артикул==vendor_code_goods)\
                .values(Колич_г=count_cities, Город_1=list_cities[0], Город_2=list_cities[1], Город_3=list_cities[2],
                        Город_4=list_cities[3])

            condition_to_perm_table = session.query(permanent_table).filter(
                permanent_table.c.Артикул == vendor_code_goods).first()

            # Проверяет есть ли элемент в табл.
            # Если нет записываем данные товара в постоянную базу
            conn = engine.connect()
            if not bool(condition_to_perm_table):
                conn.execute(sql_insert_permanent_table)
            else:
                conn.execute(sql_permanent_update)

            conn.execute(sql_insert_temporary_table)
            conn.close()

            GetDataKaspiSeller.count_other_city += count_cities
import time
import os
import shutil
import pandas as pd

from collections import OrderedDict

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers import resource_path
from webdriver_options import get_driver
from sqlalchemy import MetaData
from db_tables import temporary_table, permanent_table, engine, session
from helpers import logger
from selenium.common.exceptions import TimeoutException


class GetDataKaspiSeller:
    count_gds = 0
    count_other_city = 0

    def __init__(self, gui, signal_monitor):
        self.gui = gui
        self.signal_monitor = signal_monitor

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

                driver = get_driver()
                driver.get(url)
                driver.set_page_load_timeout(30)
                if self.gui.check_stop:
                    break
                # Установливает окно браузера в полный экран(потому что мешает подсказка-помощник сайта)
                driver.maximize_window()
                driver.implicitly_wait(10)
                # Вбиваем логин и пароль
                mail = driver.find_element_by_id('email')
                mail.send_keys(self.gui.configuration.email_login_lineEdit.text())

                password = driver.find_element_by_id('password')
                password.send_keys(self.gui.configuration.password_lineEdit.text())

                enter_btn = driver.find_element_by_xpath('/html/body/div[4]/main/div[2]/div[4]/button')
                driver.implicitly_wait(10)
                enter_btn.click()

                if self.gui.check_stop:
                    break
                # time.sleep(3)

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
                # count_gds = run_page(driver)
                # return count_gds

            except TimeoutException:
                logger.error('Превышено ожидание загрузки страницы(30 сек.)')
                self.signal_monitor.emit('Превышено ожидание загрузки страницы(30 сек.)', 3)
                driver.close()
                continue
            except Exception as ex:
                logger.error(ex)
                self.signal_monitor.emit(ex, 3)
                driver.close()
                continue
            else:
                driver.close()
                break

    def run_page(self, driver):
        products_btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Товары")))
        products_btn.click()
        # Цикл проверяет будет ли работать по определенному списку товаров
        if self.gui.configuration.list_articulcomboBox.currentText() == 'Нет':
            # Цикл работает пока кнопка 'след' доступна
            while True:
            # for j in range(1):
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
                # for i in range(1):
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
        else:
            dt_chosen_csv = pd.read_csv(self.gui.configuration.list_articullineEdit.text())
            dt_chosen_list = dt_chosen_csv['Артикул'].tolist()
            """
            В каспи клиент странице при первом внесении текста в текстовое поле поиск производится без нажатия
            на кнопку 'поиск'. Поэтому возникала ошб. И чтобы избежать ошибки занасилось рандомный текст который
            не относится к основному поиску, так после можно было заносить текст в поле и нажимать кнопку поиска.
            """
            # Рандомный текст который не относится к основному поиску
            driver.find_element_by_xpath('/html/body/div[4]/div[3]/div/div[2]/div[1]/div/input').send_keys(
                'dt_chosen_list[1]')
            driver.implicitly_wait(10)
            for i in range(len(dt_chosen_list)):
                driver.find_element_by_xpath('/html/body/div[4]/div[3]/div/div[2]/div[1]/div/input').clear()
                driver.find_element_by_xpath('/html/body/div[4]/div[3]/div/div[2]/div[1]/div/input').send_keys(
                    dt_chosen_list[i])
                driver.find_element_by_xpath('/html/body/div[4]/div[3]/div/div[2]/div[1]/div/button').click()
                driver.implicitly_wait(10)
                self.gets_dt_good(driver, 0)

    def gets_dt_good(self, driver, i):
        try:
            vendor_code_goods = driver.find_elements_by_xpath('//div[@title="Артикул в системе продавца"]')[i].text
            logger.debug(vendor_code_goods)
        except:
            vendor_code_goods = "Нет артикула товара"

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
            ######### РЕШИТЬ ВОПРОС В БУДУЩЕМ(9/15/21)
            # ПРЕОБРОЗОВАТЬ STR В ИМЯ ЭКЗЕМПЛЯРА(ИСПОЛЬЗОВАТЬ STR ПОСЛЕ ОПЕАТОРА ТОЧКИ)(gui.configuration.PP1 -> gui.configuration.i)
            list_cities = []
            availability_in_stors = driver.find_elements_by_xpath(
                '//div[@class="offer-managment__pickup-points-cell-point"]')[i].text
            for i in availability_in_stors.split(', '):
                if i == self.gui.configuration.PP1.objectName():
                    list_cities.insert(0, self.gui.configuration.PP1.currentText())
                elif i == self.gui.configuration.PP2.objectName():
                    list_cities.append(self.gui.configuration.PP2.currentText())
                elif i == self.gui.configuration.PP3.objectName():
                    list_cities.append(self.gui.configuration.PP3.currentText())
                elif i == self.gui.configuration.PP4.objectName():
                    list_cities.append(self.gui.configuration.PP4.currentText())
            # Отфильтровывает убирает повт. города
            sort_list_cities = list(OrderedDict.fromkeys(list_cities))
            logger.debug(sort_list_cities)
            count_cities = len(sort_list_cities)

        except:
            availability_in_stores = "Нет доступных точек"

        # Переменая которая нужна для записи в данных в временную табл.
        if count_cities == 1:
            sql_insert_temporary_table = temporary_table.insert().values(
                Артикул=vendor_code_goods, Модель=name_goods, Брэнд=name_goods.split(' ')[0], Ссылка=link_goods, Текущая_цена=price_goods,
                Доступность=availability_in_stores, Колич_городов=count_cities, Город_1=sort_list_cities[0])
            # Переменая которая нужна для записи в данных в постоянную табл.
            sql_insert_permanent_table = permanent_table.insert().values(
                Артикул=vendor_code_goods, Модель=name_goods, Текущая_цена=price_goods, Город_1=sort_list_cities[0])

            sql_insert_permanent_table_current_price = permanent_table.update().where(permanent_table.c.Артикул==vendor_code_goods)\
                .values(Текущая_цена=price_goods, Город_1=sort_list_cities[0])

        if count_cities == 2:
            sql_insert_temporary_table = temporary_table.insert().values(
                Артикул=vendor_code_goods, Модель=name_goods, Брэнд=name_goods.split(' ')[0], Ссылка=link_goods, Текущая_цена=price_goods,
                Доступность=availability_in_stores, Колич_городов=count_cities, Город_1=sort_list_cities[0],
                Город_2=sort_list_cities[1])
            # Переменая которая нужна для записи в данных в постоянную табл.
            sql_insert_permanent_table = permanent_table.insert().values(
                Артикул=vendor_code_goods, Модель=name_goods, Текущая_цена=price_goods, Город_1=sort_list_cities[0],
                Город_2=sort_list_cities[1])
            sql_insert_permanent_table_current_price = permanent_table.update().where(permanent_table.c.Артикул==vendor_code_goods)\
                .values(Текущая_цена=price_goods, Город_1=sort_list_cities[0], Город_2=sort_list_cities[1])

        if count_cities == 3:
            sql_insert_temporary_table = temporary_table.insert().values(
                Артикул=vendor_code_goods, Модель=name_goods, Брэнд=name_goods.split(' ')[0], Ссылка=link_goods, Текущая_цена=price_goods,
                Доступность=availability_in_stores, Колич_городов=count_cities, Город_1=sort_list_cities[0],
                Город_2=sort_list_cities[1], Город_3=sort_list_cities[2])
            # Переменая которая нужна для записи в данных в постоянную табл.
            sql_insert_permanent_table = permanent_table.insert().values(
                Артикул=vendor_code_goods, Модель=name_goods, Текущая_цена=price_goods, Город_1=sort_list_cities[0],
                Город_2=sort_list_cities[1], Город_3=sort_list_cities[2])
            sql_insert_permanent_table_current_price = permanent_table.update().where(permanent_table.c.Артикул==vendor_code_goods)\
                .values(Текущая_цена=price_goods, Город_1=sort_list_cities[0], Город_2=sort_list_cities[1], Город_3=sort_list_cities[2])

        if count_cities == 4:
            sql_insert_temporary_table = temporary_table.insert().values(
                Артикул=vendor_code_goods, Модель=name_goods, Брэнд=name_goods.split(' ')[0], Ссылка=link_goods, Текущая_цена=price_goods,
                Доступность=availability_in_stores, Колич_городов=count_cities, Город_1=sort_list_cities[0],
                Город_2=sort_list_cities[1], Город_3=sort_list_cities[2], Город_4=sort_list_cities[3])
            # Переменая которая нужна для записи в данных в постоянную табл.
            sql_insert_permanent_table = permanent_table.insert().values(
                Артикул=vendor_code_goods, Модель=name_goods, Текущая_цена=price_goods, Город_1=sort_list_cities[0],
                Город_2=sort_list_cities[1], Город_3=sort_list_cities[2])
            sql_insert_permanent_table_current_price = permanent_table.update().where(permanent_table.c.Артикул==vendor_code_goods)\
                .values(Текущая_цена=price_goods, Город_1=sort_list_cities[0], Город_2=sort_list_cities[1], Город_3=sort_list_cities[2],
                        Город_4=sort_list_cities[3])

        condition_to_perm_table = session.query(permanent_table).filter(
            permanent_table.c.Артикул == vendor_code_goods).first()

        # Проверяет есть ли элемент в табл.
        # Если нет записываем данные товара в постоянную базу
        conn = engine.connect()
        if not bool(condition_to_perm_table):
            conn.execute(sql_insert_permanent_table)
        else:
            conn.execute(sql_insert_permanent_table_current_price)

        conn.execute(sql_insert_temporary_table)
        conn.close()

        GetDataKaspiSeller.count_other_city += count_cities
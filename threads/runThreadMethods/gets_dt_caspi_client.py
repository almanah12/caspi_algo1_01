import time
import os
import shutil
import pandas as pd

from collections import OrderedDict

from helpers import resource_path
from webdriver_options import get_driver
from sqlalchemy import MetaData
from db_tables import temporary_table, permanent_table, engine, session
from helpers import logger


def gets_data(gui, signals):
    try:
        meta = MetaData()
        meta.create_all(engine)  # или books.create(engine), authors.create(engine)

        # Удаляем врем.табл перед записем новых данных
        session.query(temporary_table).delete()
        session.commit()

        # Удаляем папку с excel файлами
        if os.path.exists(resource_path(r'data_files/data_shops')):
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), resource_path(r'data_files/data_shops'))
            shutil.rmtree(path)

        #  Создаем папку занова для excel файлов
        os.mkdir(resource_path(r'data_files/data_shops'))

        # while count_check < 3:
        for _ in range(3):
            driver = get_driver()

            url = 'https://kaspi.kz/merchantcabinet/login?logout=true'

            # Заходит на стр. каспи клиент
            driver.get(url)
            driver.set_page_load_timeout(30)
            if gui.check_stop:
                break
            # Установливает окно браузера в полный экран(мешает подсказка-помощник сайта)
            driver.maximize_window()
            driver.implicitly_wait(10)
            # Вбиваем логин и пароль
            mail = driver.find_element_by_id('email')
            mail.send_keys(gui.configuration.email_login_lineEdit.text())

            password = driver.find_element_by_id('password')
            password.send_keys(gui.configuration.password_lineEdit.text())

            enter_btn = driver.find_element_by_xpath('/html/body/div[4]/main/div[2]/div[4]/button')
            driver.implicitly_wait(10)
            enter_btn.click()

            if gui.check_stop:
                break

            # Если стр. занова заходит на  логинацию
            # Время задержки для загрузки стр. и всплывающего окна
            time.sleep(3)
            # Если в стр. не загрузилась
            if driver.current_url != 'https://kaspi.kz/merchantcabinet/#/orders/tabs':
                driver.close()
                # открывает новую сессию
                continue
            else:
                break
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
        run_page(gui, driver)

    except Exception as ex:
        logger.error(ex)
        driver.quit()

    else:
        # driver.close()
        driver.quit()


def run_page(gui, driver):
    products_btn = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/nav/ul/li[2]/a')
    # products_btn = driver.find_element_by_class_name("main-nav__el-link")

    products_btn.click()
    # Цикл проверяет будет ли работать по определенному списку товаров
    if gui.configuration.list_articulcomboBox.currentText() == 'Нет':
        # Цикл работает пока кнопка 'след' доступна
        # while True:
        for j in range(1):
            if gui.check_stop:
                break
            # Ждем пока стр загрузится
            driver.implicitly_wait(20)

            # Название магазов
            count_shops = driver.find_elements_by_xpath('//td[2]/div/div/div[2]/a')
            print('count_shops: ', len(count_shops))

            # Цикл для записи данных товаров
            # for i in range(len(count_shops)):
            for i in range(2):
                gets_dt_good(gui, driver, i)

            # Берем значение кнопки след 'true' или 'false'
            driver.implicitly_wait(2)
            # xpath кнопки-след. меняется временами(2 варианта)
            try:
                click_next = driver.find_element_by_xpath(
                    '/html/body/div[4]/div[4]/div/div[4]/table/tbody/tr/td[4]/img').get_attribute('aria-disabled')
                click_next1 = driver.find_element_by_xpath(
                    '/html/body/div[4]/div[4]/div/div[4]/table/tbody/tr/td[4]/img')
            except Exception:
                click_next = driver.find_element_by_xpath(
                    '/html/body/div[4]/div[3]/div/div[4]/table/tbody/tr/td[4]/img').get_attribute('aria-disabled')
                click_next1 = driver.find_element_by_xpath(
                    '/html/body/div[4]/div[3]/div/div[4]/table/tbody/tr/td[4]/img')

            driver.implicitly_wait(10)
            # Если значение false то кликаем на кнопку след
            print(1111)
            if click_next == 'false':  # Проверяет активна ли кнопка
                driver.execute_script('arguments[0].click();', click_next1)
                # click_next1.click()
                print(2222)
            # Если нет то выходим из цикла(значит мы дошли до конца списка товаров)
            else:
                break
    else:
        dt_chosen_csv = pd.read_csv(gui.configuration.list_articullineEdit.text())
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
            gets_dt_good(gui, driver, 0)


def gets_dt_good(gui, driver, i):
    try:
        vendor_code_goods = driver.find_elements_by_xpath('//td[2]/div/div/div[2]/div[2]')[i].text
        print(vendor_code_goods)
    except:
        vendor_code_goods = "Нет артикула товара"

    try:
        name_goods = driver.find_elements_by_xpath('//td[2]/div/div/div[2]/a')[i].text
        print(name_goods)
    except:
        name_goods = "Нет название товара"

    try:
        link_goods = driver.find_elements_by_xpath('//td[2]/div/div/div[2]/a')[i].get_attribute('href')
        print('link_goods', link_goods)
    except:
        link_goods = "Нет ссылки товара"

    try:
        price_goods = driver.find_elements_by_xpath('//td[3]/div/div')[i].text
        # Преобразование текста в число. напр '100 123 т' в 100123
        if len(price_goods) > 10:
            price_goods = price_goods.split('...')[1]
        word_list = price_goods.split()
        num_list = filter(lambda word: word.isnumeric(), word_list)
        price_goods = int(''.join(map(str, num_list)))

    except:
        price_goods = "Нет цены за товар"

    try:
        availability_in_stores = driver.find_elements_by_xpath('//td[4]/div/div')[i].text
        print(availability_in_stores)

    except:
        availability_in_stores = "Нет доступных точек"

    try:
        ######### РЕШИТЬ ВОПРОС В БУДУЩЕМ(9/15/21)
        # ПРЕОБРОЗОВАТЬ STR В ИМЯ ЭКЗЕМПЛЯРА(ИСПОЛЬЗОВАТЬ STR ПОСЛЕ ОПЕАТОРА ТОЧКИ)(gui.configuration.PP1 -> gui.configuration.i)
        list_cities = []
        availability_in_stors = driver.find_elements_by_xpath('//td[4]/div/div')[i].text
        for i in availability_in_stors.split(', '):
            print(i)
            if i == gui.configuration.PP1.objectName():
                list_cities.insert(0, gui.configuration.PP1.currentText())
            elif i == gui.configuration.PP2.objectName():
                list_cities.append(gui.configuration.PP2.currentText())
            elif i == gui.configuration.PP3.objectName():
                list_cities.append(gui.configuration.PP3.currentText())
            elif i == gui.configuration.PP4.objectName():
                list_cities.append(gui.configuration.PP4.currentText())
        # Отфильтровывает убирает повт. города
        sort_list_cities = list(OrderedDict.fromkeys(list_cities))
        print(sort_list_cities)
        count_cities = len(sort_list_cities)
        print(count_cities)

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

    condition_to_perm_table = session.query(permanent_table).filter(
        permanent_table.c.Артикул == vendor_code_goods).first()

    # Проверяет есть ли элемент в табл.
    # Если нет записываем данные товара в постоянную базу
    conn = engine.connect()
    if not bool(condition_to_perm_table):
        conn.execute(sql_insert_permanent_table)
        print('Goods adds')
    else:
        conn.execute(sql_insert_permanent_table_current_price)
        print('Goods almost exist')
    conn.execute(sql_insert_temporary_table)
    conn.close()
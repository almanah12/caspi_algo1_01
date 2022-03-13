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


def set_http_adress(gui, signals):
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
            time.sleep(2)
            # Если в стр. не загрузилась
            if driver.current_url != 'https://kaspi.kz/merchantcabinet/#/orders/tabs':
                driver.close()
                # открывает новую сессию
                continue
            else:
                break
        products_btn = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/nav/ul/li[2]/a')
        # products_btn = driver.find_element_by_class_name("main-nav__el-link")
        products_btn.click()
        time.sleep(3)

        products_btn2 = driver.find_element_by_link_text('Загрузить прайс-лист')
        products_btn2.click()
        time.sleep(3)
        auto_loading_xml_btn = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div/div[3]/div[4]/h4/label[1]')
        auto_loading_xml_btn.click()
        time.sleep(3)

        url_xml = driver.find_element_by_xpath(
            '/html/body/div[4]/div[3]/div/div[3]/div[5]/div/div[2]/form/div[1]/input')
        url_xml.clear()
        url_xml.send_keys("https://storage.googleapis.com/alash/")
        time.sleep(3)


        logger.debug('end auto loading')

    except Exception as ex:
        logger.error(ex)
        driver.quit()

    else:
        # driver.close()
        driver.quit()


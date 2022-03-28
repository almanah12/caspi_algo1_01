import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from caspi_pars.webdriver_options import get_driver

from caspi_pars.helpers import logger,ngrok_public_url


def set_http_adress(gui, signals):
    for _ in range(3):
        try:
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


            products_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Товары")))
            products_btn.click()

            products_btn2 = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Загрузить прайс-лист')))
            products_btn2.click()

            auto_loading_xml_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[4]/div[3]/div/div[3]/div[4]/h4/label[1]')))
            auto_loading_xml_btn.click()

            if gui.check_stop:
                break
            time.sleep(1)

            url_xml = driver.find_element_by_xpath(
                '/html/body/div[4]/div[3]/div/div[3]/div[5]/div/div[2]/form/div[1]/input')
            url_xml.clear()
            url_xml.send_keys(ngrok_public_url()+'/alash.xml')

            time.sleep(1)

            chesk_enter_btn_xml = driver.find_element_by_xpath(
                '/html/body/div[4]/div[3]/div/div[3]/div[5]/div/div[2]/form/button[1]')
            chesk_enter_btn_xml.click()

            save_enter_btn_xml = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[4]/div[3]/div/div[3]/div[5]/div/div[2]/form/button[2]')))
            save_enter_btn_xml.click()

            # save_enter_btn_xml = driver.find_element_by_xpath(
            #     '/html/body/div[4]/div[3]/div/div[3]/div[5]/div/div[2]/form/button[2]')
            # save_enter_btn_xml.click()
            time.sleep(3)

            logger.debug('end auto loading')

        except TimeoutException:
            logger.error('Превышение ожидание загрузки страницы(30 сек.) или проблема в xml файле')
            driver.close()
            continue
        except Exception as ex:
            logger.error(ex)
            driver.close()
            continue

        else:
            # driver.close()
            driver.close()
            break


import time
import random

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from caspi_pars.webdriver_options import get_driver

from caspi_pars.helpers import logger, ngrok_public_url, enter_caspi_seller


def set_http_adress(gui, signals, ngrok_url):
    page_load = 0
    for _ in range(10):
        try:
            driver = get_driver(False)

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
            enter_caspi_seller(driver, gui.configuration.email_login_lineEdit.text(),
                               gui.configuration.password_lineEdit.text())

            for _ in range(3):
                try:
                    delay = random.randint(4, 8)
                    products_btn = WebDriverWait(driver, delay).until(
                        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Товары")))
                    products_btn.click()
                except:
                    driver.refresh()
                    continue
                else:
                    break

            products_btn2 = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Загрузить прайс-лист')))
            driver.execute_script('arguments[0].click();', products_btn2)

            auto_loading_xml_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[4]/div[3]/div/div[3]/div[4]/h4/label[1]')))
            driver.execute_script('arguments[0].click();', auto_loading_xml_btn)

            if gui.check_stop:
                break
            time.sleep(1)

            url_xml = driver.find_element_by_xpath(
                '/html/body/div[4]/div[3]/div/div[3]/div[5]/div/div[2]/form/div[1]/input')
            url_xml.clear()
            url_xml.send_keys(ngrok_url)

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
            page_load = 'Timeout'
            driver.close()
            continue
        except Exception as ex:
            logger.error(ex)
            page_load = ex
            driver.close()
            continue

        else:
            page_load = 'Good'
            driver.close()
            break
    return page_load


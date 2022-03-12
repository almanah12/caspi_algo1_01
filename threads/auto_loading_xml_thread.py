
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot

from webdriver_options import get_driver


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
    Main bot thread to run simulations and live bots.
    """

    def __init__(self, gui):
        super(RunThread, self).__init__()
        self.gui = gui

    @pyqtSlot()
    def run(self):
        try:
            driver = get_driver()
            driver.set_page_load_timeout(40)
            # while count_check < 3:
            for _ in range(3):
                driver.set_page_load_timeout(40)
                url = 'https://kaspi.kz/merchantcabinet/login?logout=true'

                # Заходит на стр. каспи клиент
                driver.get(url)
                # Установливает окно браузера в полный экран(мешает подсказка-помощник сайта)
                driver.maximize_window()
                driver.implicitly_wait(10)
                # Вбиваем логин и пароль
                mail = driver.find_element_by_id('email')
                mail.send_keys(self.gui.email_login_lineEdit.text())

                password = driver.find_element_by_id('password')
                password.send_keys(self.gui.password_lineEdit.text())

                enter_btn = driver.find_element_by_class_name('button')
                enter_btn.click()

                driver.implicitly_wait(2)

                # Если стр. занова заходит на  логинацию
                try:
                    # Если в стр. есть текст 'Seller center'
                    if driver.find_element_by_xpath('/html/body/div[1]/header/div/div[1]/h4').get_attribute(
                            'class') == 'header__heading':
                        driver.close()
                        driver.start_session({})  # открывает новую сессию
                        # count_check += 1
                # Если нет текста 'Seller center' выводится ошибка и мы выходим из цикла(это значит что мы зашли в кабинет продавца)
                except:
                    break

            # Кликаем на Товары
            products_btn = driver.find_element_by_id('main-nav-offers')
            products_btn.click()
            # products_btn = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/nav/ul/li[2]/a')
            driver.implicitly_wait(5)
            products_btn = driver.find_element_by_xpath(
                '/html/body/div[4]/div[3]/div/nav/ul/li[2]/ul/li[2]')
            products_btn.click()
            driver.implicitly_wait(20)
            auto_loading_xml_btn = driver.find_element_by_xpath(
                '/html/body/div[4]/div[4]/div/div[3]/div[4]/h4/label[1]')
            auto_loading_xml_btn.click()

            url_xml = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[3]/div[5]/div/div[2]/form/div[1]/input')
            url_xml.clear()
            url_xml.send_keys("https://storage.googleapis.com/alash/"+self.gui.name_xml_file_lineEdit.text())

            mail_xml = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[3]/div[5]/div/div[2]/form/div[2]/div[1]/input')
            mail_xml.clear()
            mail_xml.send_keys(self.gui.email_login_lineEdit.text())

            password_xml = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[3]/div[5]/div/div[2]/form/div[2]/div[2]/input')
            password_xml.clear()
            password_xml.send_keys(self.gui.password_lineEdit.text())

            chesk_enter_btn_xml = driver.find_element_by_xpath(
                '/html/body/div[4]/div[4]/div/div[3]/div[5]/div/div[2]/form/button[1]')
            chesk_enter_btn_xml.click()

            driver.implicitly_wait(40)

            save_enter_btn_xml = driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[3]/div[5]/div/div[2]/form/button[2]')
            save_enter_btn_xml.click()
            print("аписано линк в каспи")

        except Exception as ex:
            print(ex)

        finally:
            driver.close()
            driver.quit()

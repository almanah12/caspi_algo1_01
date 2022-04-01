from pathos.pools import ThreadPool
import pandas as pd

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from caspi_pars.webdriver_options import get_driver
from caspi_pars.db_tables import temporary_table, session
from caspi_pars.helpers import resource_path, logger


class Parser:
    count_requests = 0

    def __init__(self, gui, urls, signals, use_proxy):
        self.gui = gui
        self.urls = urls
        self.signals = signals
        self.use_proxy = use_proxy

    def parse(self):
        pool = ThreadPool(self.gui.configuration.number_thread_spinBox.value())
        pool.map(self.parser, self.urls)
        pool.terminate()
        pool.restart()

    def parser(self, url):
        articul = url.split('/')[5].split('-')[-1] + '_' + \
                  self.gui.configuration.id_partner_lineEdit.text()
        curr_row = session.query(temporary_table).filter(temporary_table.c.Ссылка == url).one()
        curr_numb_city = curr_row.Колич_г
        curr_city = curr_row.Город_1
        self.signals.emit('Парсинг товара {}'.format(url.split('/')[5]), 1)
        for _ in range(3):
            if self.gui.check_stop:
                break
            try:
                logger.debug(self.use_proxy)
                driver = get_driver(self.use_proxy)
                # еСЛИ стр. не загрузится выдаст ошибку и закроет стр.
                driver.set_page_load_timeout(30)

                if self.gui.check_stop:
                    break
                driver.get(url=url)
                driver.implicitly_wait(10)
                self.start_page_push_city(driver, curr_city)
                driver.implicitly_wait(10)

                # Если колич. г. равно 1
                if curr_numb_city == 1:
                    # self.move_to_mouse(driver)
                    self.gets_data_shops_i(driver, articul, count_cities=0)
                    Parser.count_requests += 1

                # Если колич. г. больше 1
                elif curr_numb_city > 1:
                    if self.gui.check_stop:
                        break
                    # self.move_to_mouse(driver)
                    self.gets_data_shops_i(driver, articul, count_cities=0)
                    Parser.count_requests += 1
                    # Цикл для сбора данных с нескольких городов на одного товара
                    for i in range(1, curr_numb_city):
                        if self.gui.check_stop:
                            break
                        # новый список для данных кажд. г.
                        driver.find_element_by_xpath('//a[@id="citySelector"]').click()

                        # chec25nnggggggggg
                        # driver.find_element_by_link_text(curr_row.Город_(1+i)).click()

                        # Кликаем на след. город
                        # РЕШИТЬ ВОПРОС В БУДУЩЕМ(9/15/21)
                        # ПРЕОБРОЗОВАТЬ STR В ИМЯ ЭКЗЕМПЛЯРА(ИСПОЛЬЗОВАТЬ STR ПОСЛЕ ОПЕАТОРА ТОЧКИ)
                        # (row.Город_2 -> row.Город_{i})
                        if i == 1:
                            driver.find_element_by_link_text(curr_row.Город_2).click()
                        elif i == 2:
                            driver.find_element_by_link_text(curr_row.Город_3).click()
                        elif i == 3:
                            driver.find_element_by_link_text(curr_row.Город_4).click()
                        ##########
                        # self.move_to_mouse(driver)
                        # метод использует итерационный элемент i для создание новых ексел файлов для кажд. г.
                        self.gets_data_shops_i(driver, articul, i)
                        Parser.count_requests += 1
                        self.signals.emit('Парсинг товара {} для Город_{}'.format(url.split('/')[5], i+1), 1)

                else:
                    logger.error('Число городов ОТСУСТВУЕТ')

            # еСЛИ стр. не загрузится выдаст ошибку и закроет стр.
            except TimeoutException:
                self.signals.emit("Превышение ожидание загрузки страницы(30 сек.)", 3)
                logger.error('Превышение ожидание загрузки страницы(30 сек.)')
                # Parser.count_requests -= 1
                driver.close()
                continue

            except Exception as ex:
                self.signals.emit('{}'.format(ex), 3)
                logger.error(ex)
                driver.close()
                continue

            else:
                driver.close()
                break
        logger.debug(Parser.count_requests)

    # Используется только раз. нужен чтобы убрать выбор города при первом загрузке
    def start_page_push_city(self, driver, current_city):
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, current_city))))

    # Движение стрелки по вкладкам для разблокировки подвкладок магазинов товара
    # def move_to_mouse(self, driver):
    #     move1 = driver.find_element_by_link_text("ОБУВЬ")
    #     action = ActionChains(driver)
    #     action.move_to_element(move1).perform()
    #
    #     # Наведение на одну из нижних вкладок для доступности подстраниц магазов
    #     move2 = driver.find_element_by_link_text("Смартфоны и гаджеты")
    #     action = ActionChains(driver)
    #     action.move_to_element(move2).perform()

    # Собираеть данные магаза и нажимает на следующие подвкладки
    def gets_data_shops_i(self, driver, url, count_cities):
        shops_result = []
        # Проверяет есть ли элемент на стр.
        while True:
            # Название магазов
            count_shops = driver.find_elements_by_xpath('//td[1]/a')

            # Цикл для записи данных магазов
            for i in range(len(count_shops)):
                # уловливает ошибку в случае отсуствие элемента
                try:
                    name_shops = driver.find_elements_by_xpath('//td[1]/a')[i].text
                except:
                    name_shops = "Нет название магазина"

                try:
                    delivery_day = driver.find_element_by_xpath(
                        '//tr[{}]//span[@class="sellers-table__delivery-date"]'.format(i+1)).text

                except:
                    delivery_day = "Только самовывоз"

                try:
                    price_item = driver.find_elements_by_xpath(
                        '//div[@class="sellers-table__price-cell-text"]')[i].text
                    # Преобразование текста в число. напр '100 123 т' в 100123
                    word_list = price_item.split()
                    num_list = []

                    for word in word_list:
                        if word.isnumeric():
                            num_list.append(word)

                    price_item = int(''.join(map(str, num_list)))
                except:
                    price_item = "Нет цены за товар"

                shops_result.append({'Name shops': name_shops,
                                    'Delivery_day': delivery_day,  # mistake у редких нет достовки соответсвенно
                                     'Price': price_item
                                    })
            # Данные магазов
            df_data = pd.DataFrame(shops_result)


            try:
                driver.find_element_by_xpath('//li[contains(.,"Следующая")]')
            except NoSuchElementException:
                break
            click_next = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//li[contains(.,"Следующая")]')))

            # click_next = driver.find_element_by_xpath('//li[contains(.,"Следующая")]')
            # Условие проверки доступности кнопки След.
            if click_next.get_attribute("class") == 'pagination__el _disabled':
                break

            driver.execute_script('arguments[0].click();', click_next)
            driver.implicitly_wait(3)

        # Запись данн.маг. в екселл с атрибутом и назв.города
        df_data.to_excel(resource_path(fr"data_files/data_shops/{url}"
                         fr"{'-Город_' + str(count_cities + 1)}.xlsx"), index=False)  #

        logger.debug("Данные записались в {}".format(url))



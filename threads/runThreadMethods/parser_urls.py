import time

from pathos.pools import ThreadPool, ProcessPool
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from caspi_pars.webdriver_options import get_driver, get_driver_parser
from caspi_pars.db_tables import temporary_table, permanent_table, engine
from caspi_pars.helpers import resource_path, logger
from sqlalchemy.orm import sessionmaker


class Parser:
    count_requests = 0
    first_request = 0

    def __init__(self, gui, urls, city, num_city, signals, use_proxy):
        self.gui = gui
        self.urls = urls
        self.city = city
        self.num_city = num_city
        self.signals = signals
        self.use_proxy = use_proxy

    def parse(self):
        pool = ThreadPool(self.gui.configuration.number_thread_spinBox.value())
        pool.map(self.parser, self.urls)
        # pool = ProcessPool(4)
        # pool.map(self.parser, self.urls)
        pool.terminate()
        pool.restart()

    def parser(self, url):
        if not self.gui.check_stop:
            articul = url.split('/')[5].split('-')[-1] + '_' + \
                      self.gui.configuration.id_partner_lineEdit.text()

            self.signals.emit('Парсинг товара {}'.format(url.split('/')[5]), 1)
        for _ in range(3):
            if self.gui.check_stop:
                break
            try:
                logger.debug(self.use_proxy)
                driver = get_driver_parser(self.use_proxy)
                # еСЛИ стр. не загрузится выдаст ошибку и закроет стр.
                driver.set_page_load_timeout(30)

                if self.gui.check_stop:
                    break
                driver.get(url=url)
                driver.implicitly_wait(10)
                if Parser.first_request==0:
                    time.sleep(2)
                    WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.LINK_TEXT, self.city)))
                    self.start_page_push_city(driver, self.city)

                driver.implicitly_wait(10)

                # Если колич. г. равно 1
                # if curr_numb_city == 1:
                    # self.move_to_mouse(driver)
                self.gets_data_shops_i(driver, articul, count_cities=0)
                Parser.count_requests += 1

            # еСЛИ стр. не загрузится выдаст ошибку и закроет стр.
            except TimeoutException:
                self.signals.emit("Превышение ожидание загрузки страницы(30 сек.) {}".format(url), 3)
                logger.error('Превышение ожидание загрузки страницы(30 сек.)')
                # Parser.count_requests -= 1
                # driver.close()
                continue

            except Exception as ex:
                self.signals.emit('{}'.format(ex), 3)
                logger.error(ex)
                # driver.close()
                continue

            else:
                Parser.first_request += 1
                # driver.close()
                break
        logger.debug(Parser.count_requests)

    # Используется только раз. нужен чтобы убрать выбор города при первом загрузке
    def start_page_push_city(self, driver, current_city):
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, current_city)))
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, current_city))))

    # Собираеть данные магаза и нажимает на следующие подвкладки
    def gets_data_shops_i(self, driver, articul, count_cities):
        self.itemprop(driver, articul)
        shops_result = []
        # Проверяет есть ли элемент на стр.
        while True:

            # Название магазов
            count_shops = driver.find_elements_by_xpath('//td[1]/a')

            # Цикл для записи данных магазов
            for i in range(len(count_shops)):
                if self.gui.check_stop:
                    break
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
        df_data.to_excel(resource_path(fr"data_files/data_shops/{self.num_city}_{self.city}"
                         fr"#{articul}.xlsx"), index=False)  #

        logger.debug("Данные записались в {}".format(articul))

    def itemprop(self, driver, articul):
        Session = sessionmaker(bind=engine)
        session = Session()
        curr_row = session.query(permanent_table).filter(
            permanent_table.c.Артикул == articul).one()
        if not curr_row['ItemProp1']:
            count_itempromp = len(driver.find_elements(By.XPATH, '//div[3]/div/div/div/a/span'))
            logger.debug(count_itempromp)
            d_pr = pd.read_excel(resource_path(
                r'data_files/data_goods/Категории+и+Тарифы.xlsx'),
                sheet_name=0)
            categ1 = d_pr['Categ1'].tolist()
            categ2 = d_pr['Categ2'].tolist()
            categ3 = d_pr['Categ3'].tolist()
            comm = d_pr['Comm'].tolist()
            for i in range(1, count_itempromp):
                categ = driver.find_element(By.XPATH, f'//div[3]/div/div/div[{i + 1}]/a/span').text
                if i == 4:
                    categ = driver.find_element(By.XPATH, f'//div[3]/div/div/div[{i + 1}]/a/span').text
                    session.query(permanent_table).filter(permanent_table.c.Артикул == articul).update(
                        {'ItemProp' + str(i-1): categ})
                else:
                    session.query(permanent_table).filter(permanent_table.c.Артикул == articul).update(
                        {'ItemProp'+str(i): categ})
                for count_categ in range(len(categ1)):
                    if categ == categ1[count_categ]:
                        session.query(permanent_table).filter(permanent_table.c.Артикул == articul).update(
                            {'Comm': comm[count_categ]})
                    if categ == categ2[count_categ]:
                        session.query(permanent_table).filter(permanent_table.c.Артикул == articul).update(
                            {'Comm': comm[count_categ]})
                    if categ == categ3[count_categ]:
                        session.query(permanent_table).filter(permanent_table.c.Артикул == articul).update(
                            {'Comm': comm[count_categ]})
                    # session.commit()
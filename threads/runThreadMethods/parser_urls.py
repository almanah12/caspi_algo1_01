from pathos.pools import ThreadPool
import pandas as pd

from selenium.webdriver.common.action_chains import ActionChains
from webdriver_options import get_driver
from selenium.common.exceptions import TimeoutException
from db_tables import temporary_table, session
from helpers import resource_path


class Parser:
    def __init__(self, gui, urls, signals):
        self.gui = gui
        self.urls = urls
        self.signals = signals

    def parse(self):
        pool = ThreadPool(self.gui.configuration.number_thread_spinBox.value())
        print('Multiply error 2')
        pool.map(self.parser, self.urls)
        pool.terminate()
        pool.restart()

        # return results

    def parser(self, url):
        if not self.gui.check_stop:
            while True:
                try:
                    print('Multiply error 3')

                    # driver = get_driver()
                    # Время для загрузки стр.
                    # driver.set_page_load_timeout(40)
                    articul = url.split('/')[5].split('-')[-1] + '_' + self.gui.configuration.id_partner_lineEdit.text()

                    curr_row = session.query(temporary_table).filter(temporary_table.c.Ссылка == url).one()

                    curr_numb_city = curr_row.Колич_городов
                    curr_city = curr_row.Город_1

                    shops_result = []
                    # Для перезагр. стр. когда входит в стр. логинации(Не знаю работает ли 11.07)
                    count_check = 0
                    while count_check < 3:
                        driver = get_driver()
                        print('Multiply error 4')
                        driver.set_page_load_timeout(70)

                        # еСЛИ стр. не загрузится выдаст ошибку и закроет стр.
                        if self.gui.check_stop:
                            break
                        driver.get(url=url)
                        driver.set_page_load_timeout(35)
                        driver.implicitly_wait(10)
                        print('Multiply error 5')

                        # Список для хранения данных о магазинах товара
                        if driver.current_url.split('/')[3].split('?')[0] == 'entrance':
                            print('Try connect before choose city ', count_check)
                            # driver.close()
                            # driver.start_session({})  # открывает новую сессию
                            # count_check += 1
                            count_check += 1
                            continue
                        elif driver.current_url.split(';')[0] == 'data':
                            print('GLuk reconect', count_check)
                            # driver.close()
                            # driver.start_session({})  # открывает новую сессию
                            # count_check += 1
                            count_check += 1
                            continue

                        # else:
                        driver.implicitly_wait(10)
                        print("catch city choose error1")
                        self.start_page_push_city(driver, curr_city)
                        driver.implicitly_wait(10)
                        if driver.current_url.split('/')[3].split('?')[0] == 'entrance':
                            print('Try connect after choose city ', count_check)
                            # driver.close()
                            # driver.start_session({})  # открывает новую сессию
                            count_check += 1
                            continue
                        # Если это усл. все норм
                        else:
                            print("catch city choose error end")
                            break

                    # driver.get(url=url)
                    # driver.set_page_load_timeout(30)
                    # driver.implicitly_wait(10)
                    # self.start_page_push_city(driver, curr_city)

                    if not self.gui.check_stop:
                        # Если колич. г. равно 1
                        if curr_numb_city == 1:
                            print('Multiply error 6')

                            # self.move_to_mouse(driver)
                            print('Multiply error 7')

                            self.gets_data_shops_i(driver, articul, count_cities=0)
                            print('Multiply error 8')


                        # Если колич. г. больше 1
                        elif curr_numb_city > 1:
                            shops_result = []
                            # self.move_to_mouse(driver)
                            self.gets_data_shops_i(driver, articul, count_cities=0)

                            # Цикл для сбора данных с нескольких городов на одного товара

                            for i in range(1, curr_numb_city):
                                if not self.gui.check_stop:
                                    # новый список для данных кажд. г.
                                    driver.find_element_by_xpath('//*[@id="citySelector"]').click()

                                    # Кликаем на след. город
                                    ######### РЕШИТЬ ВОПРОС В БУДУЩЕМ(9/15/21)
                                    # ПРЕОБРОЗОВАТЬ STR В ИМЯ ЭКЗЕМПЛЯРА(ИСПОЛЬЗОВАТЬ STR ПОСЛЕ ОПЕАТОРА ТОЧКИ)(row.Город_2 -> row.Город_{i})
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
                                    self.signals.emit('Запись данных '+str(i), 1)
                                    # self.signals.emit('Файл ' + i + ' успешно обработан', 1)

                        else:
                            print('Число городов ОТСУСТВУЕТ')
                # except Exception:
                #     print('Попадает на стр. логинации')
                #     continue
                except TimeoutException:
                    print('Превышение тайм-аута 35 сек')
                    continue
                else:
                    driver.close()
                    driver.quit()
                    break

    # Используется только раз. нужен чтобы убрать выбор города при первом загрузке
    def start_page_push_city(self, driver, current_city):
        driver.implicitly_wait(5)
        print("catch city choose error2")

        city_button = driver.find_element_by_link_text(current_city)
        print("catch city choose error3")

        driver.execute_script("arguments[0].click();", city_button)

        print("catch city choose error4")

    # Движение стрелки по вкладкам для разблокировки подвкладок магазинов товара
    def move_to_mouse(self, driver):
        move1 = driver.find_element_by_link_text("ОБУВЬ")
        action = ActionChains(driver)
        action.move_to_element(move1).perform()

        # Наведение на одну из нижних вкладок для доступности подстраниц магазов
        move2 = driver.find_element_by_link_text("Смартфоны и гаджеты")
        action = ActionChains(driver)
        action.move_to_element(move2).perform()

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
                    delivery_day = driver.find_elements_by_xpath('//div[1]/span/span[1]')[i].text
                except:
                    delivery_day = "Только самовывоз"

                try:
                    price_item = driver.find_elements_by_xpath('//td[4]/div')[i].text
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

            # Проверяет есть ли данный элемент в стр.
            try:
                # Кнопка Следующая, условие для разных xpath в разных стр. товаров
                if driver.find_element_by_xpath('//*[@id="offers-list"]/div/div/div[2]/li[4]').text == 'Следующая':
                    click_next = driver.find_element_by_xpath('//*[@id="offers-list"]/div/div/div[2]/li[4]')
                elif driver.find_element_by_xpath(
                        '//*[@id="offers-list"]/div/div/div[2]/li[5]').text == 'Следующая':
                    click_next = driver.find_element_by_xpath('//*[@id="offers-list"]/div/div/div[2]/li[5]')
                elif driver.find_element_by_xpath('//*[@id="offers-list"]/div/div/div[2]/li[6]').text == 'Следующая':
                    click_next = driver.find_element_by_xpath('//*[@id="offers-list"]/div/div/div[2]/li[6]')
                elif driver.find_element_by_xpath('//*[@id="offers-list"]/div/div/div[2]/li[7]').text == 'Следующая':
                    click_next = driver.find_element_by_xpath('//*[@id="offers-list"]/div/div/div[2]/li[7]')

                # Условие проверки доступности кнопки След.
                if click_next.get_attribute("class") == 'pagination__el _disabled':  # Проверяет активна ли кнопка
                    break

                driver.execute_script('arguments[0].click();', click_next)
                driver.implicitly_wait(3)
            except:
                break

            # Время для загрузки подвкладок стр. магазов

        print("Данные взяты")
        # Запись данн.маг. в екселл с атрибутом и назв.города
        df_data.to_excel(resource_path(fr"data_files/data_shops/{url}"
                         fr"{'-Город_' + str(count_cities + 1)}.xlsx"), index=False)  #

        print("Данные записались в ", url)



import os
import shutil

import pandas as pd
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import random

from caspi_pars.webdriver_options import get_driver
from caspi_pars.enums import dict_month

from caspi_pars.helpers import logger, resource_path, get_key_dict

import threading
import time

from caspi_pars.helpers import resource_path, logger


class MerchantInfo:

    def __init__(self, gui):
        self.gui = gui

        self.thread()

    def thread(self):
        # self.gui.check_stop = False
        t1 = threading.Thread(target=self.merchant_info)
        t1.start()

    def merchant_info(self):
        logger.info('Загрузка всех акции(рассрочек)')
        for _ in range(3):
            try:
                if self.gui.check_stop:
                    break
                driver = get_driver(False)
                url = 'https://marketing.kaspi.kz/sign-in'

                # Заходит на стр. каспи мерч
                driver.get(url)
                driver.set_page_load_timeout(30)
                # Установливает окно браузера в полный экран(мешает подсказка-помощник сайта)
                driver.maximize_window()
                driver.implicitly_wait(10)
                # Вбиваем логин и пароль
                mail = driver.find_element(By.ID, 'email')
                mail.send_keys('almas8891@gmail.com')

                password = driver.find_element(By.ID, 'password')
                password.send_keys('ANRI2022@rs')
                if self.gui.check_stop:
                    break

                enter_btn = driver.find_element(By.XPATH,
                                                '//button[@class="sign-in__btn btn btn-lg btn-primary btn-block"]')
                driver.implicitly_wait(10)
                enter_btn.click()
                time.sleep(1)

                for _ in range(3):
                    try:
                        delay = random.randint(4, 8)
                        all_promotions = WebDriverWait(driver, delay).until(
                            EC.presence_of_element_located((By.XPATH, '//a[@href="/promotions/all"]')))
                        driver.execute_script('arguments[0].click();', all_promotions)
                    except:
                        driver.refresh()
                        continue
                    else:
                        break

                count_all_promotion = driver.find_elements(
                    By.XPATH, '//div[@class="promotion ddl_product segmentstream_product_link"]')

                # delete folder
                if os.path.exists(resource_path(r'data_files/data_cat_comm_start')) or os.path.exists(
                        resource_path(r'data_files/data_cat_comm_end')):
                    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                        resource_path(r'data_files/data_cat_comm_start'))
                    shutil.rmtree(path)
                    path_end = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                        resource_path(r'data_files/data_cat_comm_end'))
                    shutil.rmtree(path_end)

                #  Создаем папку занова для  файлов рассрочки
                os.mkdir(resource_path(r'data_files/data_cat_comm_start'))
                os.mkdir(resource_path(r'data_files/data_cat_comm_end'))

                for i in range(len(count_all_promotion)):
                    if self.gui.check_stop:
                        break
                    inst_plan_tx = driver.find_element(By.XPATH,
                                        f'//div[{i + 1}]/div[@class="promotion-img__container"]').text
                    # if inst_plan_tx == "0·0·6" or "0·0·12" or "0·0·18" or "0·0·24":
                    if inst_plan_tx == "0·0·6" or inst_plan_tx == "0·0·12" or inst_plan_tx == "0·0·18" or inst_plan_tx \
                            == "0·0·24":

                        lead = driver.find_element(By.XPATH, f'//div[{i + 1}]/div[2]/p[1]').text
                        # lead = lead.split()[0]
                        year_curr = datetime.datetime.now().year
                        month_curr = datetime.datetime.now().month

                        interval_data = driver.find_element(By.XPATH, f'//div[{i + 1}]/div[2]/p[2]').text
                        start_data = interval_data.split('-')[0]
                        end_data = interval_data.split('-')[1].split('(')[0]
                        day_s_d = start_data.split()[0]
                        if int(day_s_d) < 10:
                            day_s_d = '0' + day_s_d
                        month_s_d = start_data.split()[1]
                        month_s_d = get_key_dict(dict_month, month_s_d)

                        day_e_d = end_data.split()[0]
                        if int(day_e_d) < 10:
                            day_e_d = '0' + day_e_d
                        month_e_d = end_data.split()[1]
                        month_e_d = get_key_dict(dict_month, month_e_d)

                        # WebDriverWait(driver, 10).until(
                        #     EC.presence_of_element_located(
                        #         (By.XPATH, f'//div[{str(i + 1)}]/div[3]/button[@class="btn btn-outline-primary"]')))

                        outline_primary = driver.find_element(By.XPATH,
                                                              f'//div[{str(i + 1)}]/div[3]/button[@class="btn btn-outline-primary"]')
                        driver.implicitly_wait(10)
                        driver.execute_script('arguments[0].click();', outline_primary)
                        time.sleep(2)

                        category_commission = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Категории и комиссии")))
                        driver.execute_script('arguments[0].click();', category_commission)
                        time.sleep(2)
                        count_category = len(driver.find_elements(By.XPATH, '//ul[@class="list"]'))
                        # count_category = len(driver.find_elements(By.XPATH, '//li[@class="sub-category"]'))
                        print('count_category', count_category)
                        cat_comm_all_data = []
                        for c_c in range(count_category):
                            count_sub_category = len(driver.find_elements(By.XPATH, f'//ul[{c_c + 1}]/li/ul/li'))
                            print('count_sub_category: ', count_sub_category)
                            if count_sub_category != 0:
                                for s_c in range(count_sub_category):
                                    name_category = driver.find_element(By.XPATH,
                                                                        f'//ul[{c_c + 1}]/li/ul/li[{s_c + 1}]/span[1]').text
                                    value_commission = driver.find_element(By.XPATH,
                                                                           f'//ul[{c_c + 1}]/li/ul/li[{s_c + 1}]/span[2]').text.split(
                                        '%')[0]
                                    print('name_category: ', name_category, '### value_commission: ', value_commission)
                                    cat_comm_all_data.append({'Name category': name_category,
                                                              'Value commission': value_commission.split('%')[0]})
                            else:
                                name_category = driver.find_element(By.XPATH, f'//ul[{c_c + 1}]/li/div/span[1]').text
                                value_commission = \
                                driver.find_element(By.XPATH, f'//ul[{c_c + 1}]/li/div/span[2]').text.split('%')[0]
                                print('SUB_name_category: ', name_category, '### SUB_value_commission: ',
                                      value_commission)
                                cat_comm_all_data.append({'Name category': name_category,
                                                          'Value commission': value_commission.split('%')[0]})
                        df_data = pd.DataFrame(cat_comm_all_data)

                        if month_curr == 12 and month_e_d == 'января':
                            df_data.to_excel(resource_path(
                                fr"data_files/data_cat_comm_start/{year_curr}_{month_s_d}_{day_s_d}_{lead}.xlsx"),
                                             index=False)
                            df_data.to_excel(resource_path(
                                fr"data_files/data_cat_comm_end/{year_curr + 1}_{month_e_d}_{day_e_d}_{lead}.xlsx"),
                                             index=False)
                        elif month_curr == 1 and month_s_d == 'декабря':
                            df_data.to_excel(resource_path(
                                fr"data_files/data_cat_comm_start/{year_curr - 1}_{month_s_d}_{day_s_d}_{lead}.xlsx"),
                                             index=False)
                            df_data.to_excel(resource_path(
                                fr"data_files/data_cat_comm_end/{year_curr}_{month_e_d}_{day_e_d}_{lead}.xlsx"),
                                             index=False)

                        else:
                            df_data.to_excel(resource_path(
                                fr"data_files/data_cat_comm_start/{year_curr}_{month_s_d}_{day_s_d}_{lead}.xlsx"),
                                index=False)
                            df_data.to_excel(resource_path(
                                fr"data_files/data_cat_comm_end/{year_curr}_{month_e_d}_{day_e_d}_{lead}.xlsx"),
                                index=False)

                        button_x = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, '//img[@class="d-block"]')))
                        driver.execute_script('arguments[0].click();', button_x)
                        time.sleep(2)

            except TimeoutException:
                logger.warning('Превышение ожидание загрузки страницы(30 сек.)')
                driver.close()
                continue
            except Exception as ex:
                logger.warning(ex)
                driver.close()
                continue

            else:
                # driver.close()
                driver.close()
                break


# merchant_info()

"""
Miscellaneous helper functions and constants.
"""

import os
import pickle
import random
import sys
import threading
import time

import requests
from loguru import logger
from http.server import HTTPServer, CGIHTTPRequestHandler
from pyngrok import ngrok
from selenium.webdriver.common.by import By


BASE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(BASE_DIR)

log_file_path = os.path.join(BASE_DIR, 'Logs/check.log')
log_time_path = os.path.join(BASE_DIR, 'Logs/time.log')

logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
logger.add(log_file_path, rotation="00:00", retention="30 days", encoding='utf-8', level="INFO")
logger.add(log_time_path, rotation="00:00", retention="30 days", encoding='utf-8', level="CRITICAL")


# def find_data_file(filename):
#     if getattr(sys, "frozen", False):
#         # The application is frozen
#         datadir = os.path.dirname(sys.executable)
#     else:
#         # The application is not frozen
#         # Change this bit to match where you store your data files:
#         datadir = os.path.dirname(__file__)
#     return os.path.join(datadir, filename)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def get_current_version() -> str:
    """
    Reads version from version.txt and returns it.
    """
    version_file = resource_path(r'data_files/data_update_app/version.txt')

    if not os.path.isfile(version_file):
        version = 'not found'
    else:
        with open(version_file) as f:
            version = f.read().strip()

    return version


# Зашифруем файл и записываем его
# def encrypt(filename, key):
#     f = Fernet(key)
#     with open(filename, 'rb') as file:
#         # прочитать все данные файла
#         file_data = file.read()
#     encrypted_data = f.encrypt(file_data)
#
#     # записать зашифрованный файл
#     with open(filename, 'wb') as file:
#         file.write(encrypted_data)
#
#
# # Расшифруем файл и записываем его
# def decrypt(encMessage, key):
#     fernet = Fernet(key)
#     decMessage = fernet.decrypt(encMessage).decode()
#     return decMessage


def ngrok_public_url():
    public_url = ngrok.connect('file:///'+resource_path('data_shop')).public_url
    logger.debug("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, 8000))
    return public_url


class Server_Http_Ngrok:
    def __init__(self):
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, CGIHTTPRequestHandler)

    def start_s(self):
        self.httpd.serve_forever()

    def stop_s(self):
        self.httpd.socket.close()


def server_http_ngrok():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, CGIHTTPRequestHandler)
    try:
        # Block until CTRL-C or some other terminating event
        httpd.serve_forever()
    # return httpd
    except KeyboardInterrupt:
        logger.debug('KILL http')
        httpd.socket.close()


def download_proxy_list():
    image_url = "https://proxy.webshare.io/proxy/list/download/dxwiuynzkcbwocodmgfhpjaonpyyfysflavigcwe/-/http/username/direct/"

    # URL of the image to be downloaded is defined as image_url
    r = requests.get(image_url)  # create HTTP response object

    # send a HTTP request to the server and save
    # the HTTP response in a response object called r
    with open("data_shop/proxy_list.txt", 'wb') as f:
        # to a new file in binary mode.
        f.write(r.content)


def enter_caspi_seller(driver, email_login, password_login):
    mail = driver.find_element(By.ID, 'email')
    mail.send_keys(email_login)

    password = driver.find_element(By.ID, 'password')
    password.send_keys(password_login)

    enter_btn = driver.find_element(By.XPATH, '//button[@class="button"]')
    driver.implicitly_wait(10)
    enter_btn.click()
    # pickle.dump(driver.get_cookies(), open(f"caspi_enter_cookies", "wb"))


def restart_time(first_time, second_time, start_time, activity_monitor, gui):
    from_time_sec = first_time * 60
    before_time_sec = second_time * 60
    restart_time = random.randint(from_time_sec, before_time_sec)
    m = (restart_time // 60) % 60
    s = restart_time % 60
    activity_monitor.emit('Цикл перезапустится через {} мин. и {} сек.'.format(m, s), 4)
    logger.info('Цикл перезапустится через {} мин. и {} сек.'.format(m, s))

    end_time = time.time() - start_time
    activity_monitor.emit('Время выполнение цикла: {} сек'.format(end_time), 4)
    logger.critical('Время выполнениецикла: {} сек'.format(end_time))
    logger.debug(restart_time)
    for _ in range(restart_time):
        if not gui.check_stop:
            time.sleep(1)
        else:
            break


def get_key_dict(dict, value):
    for k, v in dict.items():
        if v == value:
            return k

# def auto_confirm_order_cond(gui):
#     while gui.comboBox_auto_confirm_order.currentText() == 'Да':
#
#         begin_time = str(int(time.time() * 1000) - 1200100100)
#         end_time = str(int(time.time() * 1000))
#         url = "https://kaspi.kz/shop/api/v2/orders?page[number]=0&page[size]=100&filter[orders][state]=NEW&" \
#               "filter[orders][creationDate][$ge]=" + begin_time + "&filter[orders][creationDate][$le]=" + end_time + "&filter[orders][status]=APPROVED_BY_BANK&" \
#                                                                                                                      "filter[orders][deliveryType]=PICKUP&filter[orders][signatureRequired]=false&" \
#                                                                                                                      "include[orders]=user"
#
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
#             'Content-Type': 'application/vnd.api+json',
#             'X-Auth-Token': 'fe6KQN9hcTCmxbJW2trHntHmDC5kD/veVvwehQGoRSo='}
#
#         r = requests.get(url=url, headers=headers)
#
#         data = r.json()
#         id_order = [i['id'] for i in data['data']]
#         attributes = [i['attributes'] for i in data['data']]
#         print('id_order', id_order)
#
#         count_order = 0
#         for i in attributes:
#             delay_t = int(end_time) - i['creationDate']
#
#             if delay_t > 4800000:  # больше 80 мин.
#                 print(id_order[count_order])
#                 print('Confirmed')
#                 # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
#                 #             'HTTP': '/1.1',
#                 #             'POST': '/api/v2/orders',
#                 #             # 'Host': 'kaspi.kz/shop',
#                 #             'Content-Type': 'application/vnd.api+json',
#                 #             'X-Auth-Token': 'fe6KQN9hcTCmxbJW2trHntHmDC5kD/veVvwehQGoRSo='}
#                 # data = {"data": {"type": "orders", "id": id_order[count_order]+"=", "attributes": {"code": "", "status": "ACCEPTED_BY_MERCHANT"}}}
#                 # r = requests.post(url='https://kaspi.kz/shop/api/v2/orders', headers=headers, json=data)
#                 # data = r.json()
#             else:
#                 print(id_order[count_order])
#                 print('Wait')
#             count_order += 1












from random import randint

from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
import selenium

from caspi_pars.helpers import resource_path, logger


def get_driver():
    args = ["hide_console", ]

    options = selenium.webdriver.ChromeOptions()
    # user-agent
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
    # for ChromeDriver version 79.0.3945.16 or over
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")
    # ser = Service(resource_path(r"driver_browser/chromedriver.exe"))

    driver = selenium.webdriver.Chrome(
        executable_path=resource_path(r"driver_browser/chromedriver.exe"),
        service_args=args, options=options)
    return driver


def get_driver_proxy():
    proxies = open('data_shop/proxy_list.txt').read().split('\n')
    proxy = proxies[randint(0, 9)]
    address = proxy.split(':')[0]
    port = proxy.split(':')[1]
    logger.debug(proxy)
    login = proxy.split(':')[2]
    password = proxy.split(':')[3]
    # print(password)
    args = ["hide_console", ]

    options = webdriver.ChromeOptions()

    # user-agent
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
    # for ChromeDriver version 79.0.3945.16 or over
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless")
    proxy_options = {
        "proxy": {
            "https": f"http://{login}:{password}@{address}:{port}"
        }
    }
    driver = webdriver.Chrome(executable_path=resource_path(r"driver_browser/chromedriver.exe"), service_args=args,
                              seleniumwire_options=proxy_options, options=options)
    return driver
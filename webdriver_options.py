import random
import zipfile
from random import randint

from selenium.webdriver.chrome.service import Service
import selenium
import threading
from seleniumwire import webdriver

from caspi_pars.helpers import resource_path, logger


def get_driver(use_proxy):
    args = ["hide_console", ]
    options = selenium.webdriver.ChromeOptions()
    # if use_proxy:
    #     pluginfile = resource_path('proxy_auth_plugin.zip')
    #     with zipfile.ZipFile(pluginfile, 'w') as zp:
    #         zp.writestr("manifest.json", manifest_json())
    #         zp.writestr("background.js", background_json())
    #     options.add_extension(pluginfile)
    # user-agent
    with open(resource_path('data_files/data_update_app/u_a.txt')) as file:
        user_agent = random.choice(list(file))
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'

    logger.debug(user_agent)
    options.add_argument(f"user-agent={user_agent}")

    # for ChromeDriver version 79.0.3945.16 or over
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument('--window-size=1920,1080')
    # options.add_argument("--headless")
    # ser = Service(resource_path(r"driver_browser/chromedriver.exe"))

    driver = selenium.webdriver.Chrome(
        executable_path=resource_path(r"driver_browser/chromedriver.exe"),
        service_args=args, options=options)
    return driver


threadLocal = threading.local()


def get_driver_parser(use_proxy):
    driver = getattr(threadLocal, resource_path("driver_browser/chromedriver.exe"), None)
    if driver is None:
        args = ["hide_console", ]
        options = webdriver.ChromeOptions()
        # user-agent
        options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        # for ChromeDriver version 79.0.3945.16 or over
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")
        if use_proxy:
            proxies = open(resource_path('data_shop/test_proxy')).read().split('\n')
            proxy = proxies[randint(0, 4)]
            address = proxy.split(':')[0]
            port = proxy.split(':')[1]
            logger.debug(proxy)
            login = proxy.split(':')[2]
            password = proxy.split(':')[3]

            proxy_options = {
                "proxy": {
                    "https": f"http://{login}:{password}@{address}:{port}"
                }
            }
            driver = webdriver.Chrome(executable_path=resource_path(r"driver_browser/chromedriver.exe"), service_args=args,
                                      seleniumwire_options=proxy_options, options=options)
            setattr(threadLocal, resource_path("driver_browser/chromedriver.exe"), driver)
        else:

            driver = selenium.webdriver.Chrome(executable_path=resource_path(r"driver_browser/chromedriver.exe"),
                                      service_args=args, options=options)
            setattr(threadLocal, resource_path("driver_browser/chromedriver.exe"), driver)
    return driver

#
# def manifest_json():
#     manifest_js = """
#     {
#         "version": "1.0.0",
#         "manifest_version": 2,
#         "name": "Chrome Proxy",
#         "permissions": [
#             "proxy",
#             "tabs",
#             "unlimitedStorage",
#             "storage",
#             "<all_urls>",
#             "webRequest",
#             "webRequestBlocking"
#         ],
#         "background": {
#             "scripts": ["background.js"]
#         },
#         "minimum_chrome_version":"22.0.0"
#     }
#     """
#     return manifest_js
#
#
# def background_json():
#     proxies = open(resource_path(r'data_shop\test_proxy')).read().split('\n')
#     proxy = proxies[randint(0, 4)]
#     address = proxy.split(':')[0]
#     port = proxy.split(':')[1]
#     logger.debug(proxy)
#     login = proxy.split(':')[2]
#     password = proxy.split(':')[3]
#     background_js = """
#     var config = {
#             mode: "fixed_servers",
#             rules: {
#             singleProxy: {
#                 scheme: "http",
#                 host: "%s",
#                 port: parseInt(%s)
#             },
#             bypassList: ["localhost"]
#             }
#         };
#     chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
#     function callbackFn(details) {
#         return {
#             authCredentials: {
#                 username: "%s",
#                 password: "%s"
#             }
#         };
#     }
#     chrome.webRequest.onAuthRequired.addListener(
#                 callbackFn,
#                 {urls: ["<all_urls>"]},
#                 ['blocking']
#     );
#     """ % (address, port, login, password)
#     return background_js
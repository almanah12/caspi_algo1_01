from selenium import webdriver

from helpers import resource_path


def get_driver():
    args = ["hide_console", ]

    options = webdriver.ChromeOptions()

    # user-agent
    options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
    # for ChromeDriver version 79.0.3945.16 or over
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=resource_path(r"driver_browser/chromedriver.exe"), service_args=args,
                              options=options)
    return driver
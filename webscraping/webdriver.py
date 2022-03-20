from selenium import webdriver

class WebDriver(object):
    __instance = None
    driver = None
    def get_driver(self):
        return self.driver
    def __new__(cls):
        if WebDriver.__instance is None:
            WebDriver.__instance = object.__new__(cls)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            WebDriver.__instance.driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', options=chrome_options)
        return WebDriver.__instance
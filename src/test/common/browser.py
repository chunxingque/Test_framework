import time
import os
from selenium import webdriver
from utils.config import DRIVER_PATH, REPORT_PATH

# 可根据需要自行扩展
CHROMEDRIVER_PATH = os.path.join(DRIVER_PATH, 'chromedriver.exe')
IEDRIVER_PATH = os.path.join(DRIVER_PATH, 'IEDriverServer.exe')
PHANTOMJSDRIVER_PATH = os.path.join(DRIVER_PATH, 'phantomjs.exe')

TYPES = {'firefox': webdriver.Firefox, 'chrome': webdriver.Chrome, 'ie': webdriver.Ie, 'phantomjs': webdriver.PhantomJS}
EXECUTABLE_PATH = {'firefox': 'wires', 'chrome': CHROMEDRIVER_PATH, 'ie': IEDRIVER_PATH, 'phantomjs': PHANTOMJSDRIVER_PATH}


class UnSupportBrowserTypeError(Exception):
    pass


class Browser(object):
    def __init__(self, browser_type='chrome'):
        self._type = browser_type.lower()
        if self._type in TYPES:
            self.browser = TYPES[self._type]
        else:
            raise UnSupportBrowserTypeError('仅支持%s!' % ', '.join(TYPES.keys()))
        self.driver = None

    def get(self, url, maximize_window=True, implicitly_wait=30):
        self.driver = self.browser(executable_path=EXECUTABLE_PATH[self._type])
        self.driver.get(url)
        if maximize_window:
            self.driver.maximize_window()
        self.driver.implicitly_wait(implicitly_wait)
        return self

    def driver_init(self, maximize_window: bool = True, implicitly_wait: int = 30) -> webdriver:
        self.driver = self.browser(executable_path=EXECUTABLE_PATH[self._type])
        if maximize_window:
            self.driver.maximize_window()
        self.driver.implicitly_wait(implicitly_wait)
        return self.driver

    def save_screen_shot(self, name='screen_shot'):
        day = time.strftime('%Y%m%d', time.localtime(time.time()))
        screenshot_path = os.path.join(REPORT_PATH, 'screenshot_%s' % day)
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)

        tm = time.strftime('%H%M%S', time.localtime(time.time()))
        screenshot = self.driver.save_screenshot(os.path.join(screenshot_path, '%s_%s.png' % (name, tm)))
        return screenshot

    def close(self):
        self.driver.close()

    def quit(self):
        self.driver.quit()


if __name__ == '__main__':
    url = "https://www.baidu.com"
    browser = Browser('chrome')
    driver = browser.driver_init(True, 20)
    driver.get(url)
    browser.save_screen_shot('test_baidu')
    time.sleep(3)
    browser.quit()

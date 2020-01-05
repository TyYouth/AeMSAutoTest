import os
import inspect
import time
from utils.common.log import logger
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoSuchFrameException, JavascriptException, \
    ScreenshotException
from utils.Config import DRIVER_PATH, REPORT_PATH

CHROME_DRIVER_PATH = os.path.join(DRIVER_PATH, 'chromedriver.exe')

TYPES = {'chrome': webdriver.Chrome, 'firefox': webdriver.Firefox, 'ie': webdriver.Ie}
EXECUTABLE_PATH = {'chrome': CHROME_DRIVER_PATH, 'firefox': ''}


class UnSupportBrowserTypeError(Exception):
    pass


class Browser(object):
    def __init__(self, browser_type):
        super(Browser, self).__init__()
        self.driver = None
        self._type = browser_type
        if self._type in TYPES:
            self.browser = TYPES[self._type]
        else:
            raise UnSupportBrowserTypeError("UnSupport browser type, support %s only" % ''.join(TYPES.keys()))
        self.accept_next_alert = None

    def browser_init(self, maximize_windows=True, implicitly_wait=10):
        logger.info('driver init start, opened browser')
        self.driver = self.browser(executable_path=EXECUTABLE_PATH[self._type])
        if maximize_windows:
            self.driver.maximize_window()
        self.driver.implicitly_wait(implicitly_wait)
        self.accept_next_alert = True
        return self

    # get driver
    def get_driver(self):
        return self.driver

    # Page factory
    def find_element(self, *loc):
        try:
            return self.driver.find_element(*loc)
        except NoSuchElementException as e:
            logger.error("can NOT find element by {0} with {1}".format(loc[0], loc[1]))
            logger.exception(e.msg)

    def find_elements(self, *loc):
        try:
            return self.driver.find_elements(*loc)
        except NoSuchElementException as e:
            logger.error("can NOT find element {0} with {1}".format(loc[0], loc[1]))
            logger.exception(e.msg)

    def find_name(self, _name):
        try:
            return self.driver.find_element(By.NAME, _name)
        except NoSuchElementException as e:
            logger.error("can NOT find element by {}".format(_name))
            logger.exception(e.msg)

    def finds_name(self, _name):
        try:
            return self.driver.find_elements(By.NAME, _name)
        except NoSuchElementException as e:
            logger.error("can NOT find elements by {}".format(_name))
            logger.exception(e.msg)

    def find_id(self, _id):
        try:
            return self.driver.find_element(By.ID, _id)
        except NoSuchElementException as e:
            logger.error("can NOT find element by {}".format(_id))
            logger.exception(e.msg)

    def finds_id(self, _id):
        try:
            return self.driver.find_elements(By.ID, _id)
        except NoSuchElementException as e:
            logger.error("can NOT find elements by {}".format(_id))
            logger.exception(e.msg)

    def find_class(self, _class_name):
        try:
            return self.driver.find_element(By.CLASS_NAME, _class_name)
        except NoSuchElementException as e:
            logger.error("can NOT find element by {}".format(_class_name))
            logger.exception(e.msg)

    def finds_class(self, _class_name):
        try:
            return self.driver.find_elements(By.CLASS_NAME, _class_name)
        except NoSuchElementException as e:
            logger.error("can NOT find elements by {}".format(_class_name))
            logger.exception(e.msg)

    def find_xpath(self, label_name=None, attr_name=None, value=None):
        try:
            if label_name and attr_name:
                return self.driver.find_element(By.XPATH,
                                                "//{0}[contains(@{1}, '{2}')]".format(label_name, attr_name, value))
            # The value can be xpath directly
            elif value is not None:
                return self.driver.find_element(by=By.XPATH, value=value)
        except NoSuchElementException as e:
            logger.error("can NOT find element by such a xpath")
            logger.exception(e.msg)

    def finds_xpath(self, label_name=None, att_name=None, value=None):
        try:
            if label_name and att_name:
                return self.driver.find_elements(By.XPATH,
                                                 "//{0}[contains(@{1}, '{2}')]".format(label_name, att_name, value))
            else:
                return self.driver.find_elements(by=By.XPATH, value=value)
        except NoSuchElementException as e:
            logger.error("can NOT find elements by such a xpath")
            logger.exception(e.msg)

    def find_xpath_by_text(self, label_name, text_val):
        try:
            web_ele = self.driver.find_element(By.XPATH, "//{0}[contains(text(), '{1}')]".format(label_name, text_val))
            return web_ele
        except NoSuchElementException as e:
            logger.error("can NOT find element by such a xpath")
            logger.exception(e.msg)

    # The value is css
    def find_css(self, css_value=None):
        try:
            if css_value:
                return self.driver.find_element(by=By.CSS_SELECTOR, value=css_value)
        except NoSuchElementException as e:
            logger.error("can NOT find element by such a css path")
            logger.exception(e.msg)

    def finds_css(self, css_value=None):
        try:
            if css_value:
                return self.driver.find_elements(by=By.CSS_SELECTOR, value=css_value)
        except NoSuchElementException as e:
            logger.error("can NOT find elements by such a css path")
            logger.exception(e.msg)

    def save_screen_shot(self):
        day = time.strftime("%Y%m%d", time.localtime(time.time()))
        screen_shot_path = os.path.join(REPORT_PATH, 'screen_shot_{0}'.format(day))
        if not os.path.exists(screen_shot_path):
            os.makedirs(screen_shot_path)
        name = inspect.stack()[1][3]
        screen_shot_file = os.path.join(screen_shot_path, '{0}.png'.format(name))
        try:
            self.driver.save_screenshot(screen_shot_file)
            logger.info("screen shot {0} has been saved in {1}".format(name, screen_shot_path))
        except ScreenshotException as e:
            logger.exception(e.msg)

# Encapsulate selenium method
    # right click
    def right_click(self, web_element):
        ActionChains(self.driver).context_click(web_element).perform()

    def double_click(self, web_element):
        ActionChains(self.driver).double_click(web_element).perform()

    # hover: move mouse to special element
    def hover(self, web_element):
        ActionChains(self.driver).move_to_element(web_element).perform()

    @staticmethod
    def select_by_index(web_element, index=0):
        Select(web_element).select_by_index(index)

    @staticmethod
    def select_by_value(web_element, value):
        Select(web_element).select_by_value(value)

    @staticmethod
    def select_by_text(web_element, text):
        Select(web_element).select_by_visible_text(text)

    def refresh(self):
        self.driver.refresh()

    @staticmethod
    def clear(web_element):
        web_element.clear()

    @staticmethod
    def click(web_element):
        web_element.click()
        time.sleep(0.25)

    @staticmethod
    def send_keys(web_element, value, clear_first=True):
        """
        :param web_element: web element found by driver
        :param value: keys to send
        :param clear_first: flag for clear input box
        :return: None
        """
        if clear_first:
            web_element.clear()
        web_element.send_keys(value)

    @staticmethod
    def get_text(web_element):
        return web_element.text

    @staticmethod
    def submit(web_element):
        web_element.submit()

    @staticmethod
    def get_attr(web_element, attr_name):
        attr_value = web_element.get_attribute(attr_name)
        logger.debug("the attribute {} is {}".format(attr_name, attr_value))
        return attr_value

    def upload_file(self, web_element, path):
        """
        :param web_element:  web element of upload button
        :param path: path of the upload file
        :return: None
        """
        self.send_keys(web_element, value=path)

    # run a JavaScript script
    def run_js_script(self, js):
        try:
            self.driver.execute_script(js)
        except JavascriptException as e:
            logger.exception(e.msg)

    def switch_frame(self, frame_attr=None, web_element=None):
        """
        :param frame_attr: attr(id or name) of frame
        :param web_element: need to locate frame first, if no id or name
        :return:
        """
        try:
            if frame_attr:
                self.driver.switch_to.frame(frame_attr)
            else:
                self.driver.switch_to.frame(web_element)
            time.sleep(0.5)
        except NoSuchFrameException as e:
            logger.error("No such frame to switch by id or name")
            logger.exception(e.msg)

    def close(self):
        self.driver.close()
        logger.info("web has been closed")

    def quit(self):
        self.driver.quit()
        logger.info("browser has been quited")

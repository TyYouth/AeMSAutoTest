import os
import inspect
import time
import datetime
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from utils.config import DRIVER_PATH, REPORT_PATH
from utils.log import logger
CHROME_DRIVER_PATH = os.path.join(DRIVER_PATH, 'chromedriver.exe')


class Browser(object):
	def __init__(self, browser_name='chrome', maximize_windows=True):
		super(Browser, self).__init__()
		logger.info('opened browser')
		if browser_name == 'chrome':
			self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
		elif browser_name == 'firefox':
			pass
		else:
			self.driver = None
		if maximize_windows:
			self.driver.maximize_window()
		self.driver.implicitly_wait(5)
		self.accept_next_alert = True


	# get driver
	def get_driver(self):
		return self.driver

	def save_screenshot(self):
		day = time.strftime("%Y%m%d", time.localtime(time.time()))
		screenshot_path = os.path.join(REPORT_PATH, 'screenshot_%s' % (day))
		if not os.path.exists(screenshot_path):
			os.makedirs(screenshot_path)
		name = inspect.stack()[1][3]
		screenshot_file = os.path.join(screenshot_path, '%s.png' % (name))
		self.driver.save_screenshot(screenshot_file)
		logger.info("screenshot %s has been saved in %s" % (name, screenshot_path))

	def close_alert_and_get_its_text(self):
		try:
			# time.sleep(0.5)
			alert = self.driver.switch_to.alert()
			alert_text = alert.text
			if self.accept_next_alert:
				alert.accept()
			else:
				alert.dismiss()
			return alert_text
		finally:
			self.accept_next_alert = True

	def dismiss_alert(self):
		try:
			self.driver.switch_to.alert().dismiss()
		except:
			pass

	# run a JavaScript script
	def run_js_script(self, js):
		try:
			self.driver.execute_script(js)
		except:
			pass

	# right click
	def right_click(self, loc):
		ActionChains(self.driver).context_click(loc).perform()

	def double_click(self, loc):
		ActionChains(self.driver).double_click(loc).perform()

	# hover: move mouse to special element
	def hover(self, loc):
		ActionChains(self.driver).move_to_element(loc).perform()

	def select_by_value(self, loc, value=None):
		Select(loc).select_by_value(value)

	def refresh(self):
		self.driver.refresh()

	def click(self, *loc):
		element_loc = self.find_element(*loc)
		element_loc.click()

	def send_keys(self, loc, value=None, clear_first=True):
		element_loc = self.find_element(loc)
		if clear_first:
			element_loc.clear()
		element_loc.send_keys(value)

	def upload_file(self, loc, path):
		"""
		:param loc:  upload button's web location
		:param path: path of to upload file
		:return:
		"""
		self.send_keys(loc=loc, value=path)

	def expectedTime(self, daysDelta=0, minDeleta=0):
		"""
		:param daysDelta: int, delta day
		:param minDeleta: int, delta minute
		:return: expected time
		"""
		time = datetime.datetime.now() + datetime.timedelta(days=daysDelta, minutes=minDeleta)
		return time.strftime('%Y-%m-%d %H:%M:%S')

	def compareTime(self, earlierTime, laterTime):
		if earlierTime >= laterTime:
			return True
		else:
			return False

	def close(self):
		self.driver.close()
		logger.info("web has been closed")

	def quit(self):
		self.driver.quit()
		logger.info("browser has been quited")




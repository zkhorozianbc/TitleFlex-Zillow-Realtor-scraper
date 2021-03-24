from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import os


class FirefoxDriver:
	
	def __init__(self):

		self.firefox_driver_path = os.path.join("usr/local/bin/geckodriver")
		self.ff_profile = self.initialize_profile_settings()


	def initialize_profile_settings(self):

		ff_profile = webdriver.FirefoxProfile()
		ff_profile.set_preference("browser.download.folderList", 2)
		ff_profile.set_preference("browser.download.manager.showWhenStarting", False)
		ff_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, application/pdf, text/comma-separated-values, text/xml, application/xml, text/html; charset=utf-8")
		ff_profile.set_preference("pdfjs.disabled", True)
		ff_profile.set_preference("print.always_print_silent", True)
		ff_profile.set_preference("dom.disable_open_during_load", False)
		ff_profile.set_preference("browser.privatebrowsing.autostart", True)
		ff_profile.set_preference("browser.privatebrowsing.autostart", True)
		ff_profile.set_preference("general.useragent.override", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36")

		return ff_profile


	def get_driver(self):

		driver = webdriver.Firefox(executable_path=self.firefox_driver_path, firefox_profile=self.ff_profile)
		driver.set_page_load_timeout(200)

		return driver






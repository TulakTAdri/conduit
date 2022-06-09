import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from testdatas import test_user, registration_msg, registration_error
import base_functions
from selenium.webdriver.chrome.options import Options


class TestConduitLogin(object):

	def setup(self):
		browser_options = Options()
		browser_options.headless = True
		self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
		self.browser.implicitly_wait(10)
		URL = "http://localhost:1667/#/"
		self.browser.get(URL)
		self.browser.maximize_window()

	def teardown(self):
		self.browser.quit()

	# def test_register(self):  # Vizsgáljuk meg a regisztrációt negatív ágon, már létező adatokkal.
	# 	register_nav = self.browser.find_element_by_xpath('//a[@href="#/register"]')
	# 	register_nav.click()
	#
	# 	username_input = self.browser.find_element_by_xpath('//input[@placeholder="Username"]')
	# 	email_input = self.browser.find_element_by_xpath('//input[@placeholder="Email"]')
	# 	pwd_input = self.browser.find_element_by_xpath('//input[@placeholder="Password"]')
	#
	# 	username_input.send_keys(test_user['username'])
	# 	email_input.send_keys(test_user['user_email'])
	# 	pwd_input.send_keys(test_user['user_pwd'])
	#
	# 	sign_up_btn = self.browser.find_element_by_xpath('//button[contains(text(), "Sign up")]')
	# 	sign_up_btn.click()
	# 	time.sleep(3)
	#
	# 	WebDriverWait(self.browser, 30).until(
	# 		EC.visibility_of_element_located((By.XPATH, '//div[@class="swal-icon swal-icon--error"]')))
	#
	# 	registration_error_title = WebDriverWait(self.browser, 30).until(
	# 		EC.visibility_of_element_located((By.XPATH, '//div[@class="swal-title"]')))
	# 	assert registration_error_title.text == registration_error['error']
	#
	# 	registration_error_msg = WebDriverWait(self.browser, 30).until(
	# 		EC.presence_of_element_located((By.XPATH, '//div[@class="swal-text"]')))
	# 	assert registration_error_msg.text == registration_msg['error_msg']
	#
	# 	error_msg_button = self.browser.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]')
	# 	error_msg_button.click()

	def test_sign_in(self):  # Ellenőrizzük a bejelentkezést pozitív ágon
		base_functions.login(self.browser, test_user['user_email'], test_user['user_pwd'])

		# profile = self.browser.find_elements_by_xpath('//a[@class="nav-link"]')[2]
		assert self.browser.current_url == 'http://localhost:1667/#/'

		# profile = WebDriverWait(self.browser, 30).until(
		# 	EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))
		# assert profile[2].text == test_user['username']

	def test_cookie_bar(self):  # Vizsgáljuk meg az adatkezelési nyilatkozat működését
		cookie_panel = self.browser.find_element_by_xpath('//div[@id="cookie-policy-panel"]')
		assert cookie_panel.is_displayed()

		cookie_accept_btn = self.browser.find_element_by_xpath(
			'//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
		cookie_accept_btn.click()
		time.sleep(0.5)

		assert len(self.browser.find_elements_by_xpath('//div[@id="cookie-policy-panel"]')) == 0
# lista-ként kell rákeresni az eltűnő panelre és úgy kell nullának venni a hosszát
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

	def test_register(self):
		# Vizsgáljuk meg a regisztrációt negatív ágon, már létező adatokkal.
		# Ehhez először elvégezzük a regisztrációt, majd kilépünk
		try:
			base_functions.registration(self.browser, test_user['username'], test_user['user_email'], test_user['user_pwd'])
			WebDriverWait(self.browser, 20).until(
				EC.visibility_of_element_located((By.XPATH, '//button[@class="swal-button swal-button--confirm"]'))).click()
			time.sleep(0.5)
			WebDriverWait(self.browser, 20).until(
				EC.visibility_of_element_located((By.XPATH, '//a[contains(text(), "Log out")]'))).click()
			# Újraregisztrálunk a már felhasznált adatokkal
			base_functions.registration(self.browser, test_user['username'], test_user['user_email'], test_user['user_pwd'])
			WebDriverWait(self.browser, 30).until(
				EC.visibility_of_element_located((By.XPATH, '//div[@class="swal-icon swal-icon--error"]')))
		except:
			assert False
		else:
			assert True
		# Ellenőrizzük, hogy a megfelelő hibaüzenet megjelenik
		registration_error_title = WebDriverWait(self.browser, 30).until(
			EC.visibility_of_element_located((By.XPATH, '//div[@class="swal-title"]')))
		assert registration_error_title.text == registration_error['error']

		registration_error_msg = WebDriverWait(self.browser, 30).until(
			EC.presence_of_element_located((By.XPATH, '//div[@class="swal-text"]')))
		assert registration_error_msg.text == registration_msg['error_msg']

		error_msg_button = self.browser.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]')
		error_msg_button.click()

	def test_sign_in(self):  # Ellenőrizzük a bejelentkezést pozitív ágon
		try:
			base_functions.login(self.browser, test_user['user_email'], test_user['user_pwd'])
		except:
			assert False
		else:
			assert True
		# Ellenőrizzük, hogy bejelentkezést követően a főoldalra kerültünk.
		assert self.browser.current_url == 'http://localhost:1667/#/'
		# Ellenőrizzük, hogy a regisztrált felhasználónév megjelenik a menüpontok között
		profile = WebDriverWait(self.browser, 30).until(
			EC.presence_of_all_elements_located((By.XPATH, '//a[@class="nav-link"]')))
		assert profile[2].text == test_user['username']

	def test_cookie_bar(self):  # Vizsgáljuk meg az adatkezelési nyilatkozat működését
		try:
			cookie_panel = self.browser.find_element_by_xpath('//div[@id="cookie-policy-panel"]')
			assert cookie_panel.is_displayed()

			cookie_accept_btn = self.browser.find_element_by_xpath(
				'//button[@class="cookie__bar__buttons__button cookie__bar__buttons__button--accept"]')
			cookie_accept_btn.click()
			time.sleep(0.5)
		except:
			assert False
		else:
			assert True
		# lista-ként rákeresünk az eltűnő panelre és nullának vesszük a hosszát, azaz nem jelenik meg az oldalon
		assert len(self.browser.find_elements_by_xpath('//div[@id="cookie-policy-panel"]')) == 0
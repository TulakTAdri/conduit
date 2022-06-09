from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.color import Color
from base_functions import *
from testdatas import test_user, new_article, modified_article
from selenium.webdriver.chrome.options import Options


class TestConduit(object):

	def setup(self):
		browser_options = Options()
		browser_options.headless = True
		self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
		self.browser.implicitly_wait(10)
		URL = "http://localhost:1667/#/"
		self.browser.get(URL)
		self.browser.maximize_window()
		login(self.browser, test_user['user_email'], test_user['user_pwd'])

	def teardown(self):
		self.browser.quit()

	def test_logout(self):  ## Vizsgáljuk meg a kijelentkezés funkciót
		logout_nav = self.browser.find_element_by_xpath('//a[contains(text(), "Log out")]')
		logout_nav.click()

		WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#/login"]')))
		# Kijelentkezés után ellenőrizzük, hogy a Sign in és Sign up menüpontok megjelennek
		assert len(self.browser.find_elements_by_xpath('//a[@class="nav-link"]')) == 2
		assert self.browser.find_element_by_xpath('//a[@href="#/login" and @class="nav-link"]').is_enabled()
		assert self.browser.find_element_by_xpath('//a[@href="#/register" and @class="nav-link"]').is_displayed()

	def test_datas_to_list(self):  ## Szűrjünk rá és listázzuk ki a 'loret' tag-et tartalmazó article-ket
		loret_tag = self.browser.find_element_by_xpath('//div[@class="sidebar"]/div/a[@href="#/tag/loret"]')
		loret_tag.click()
		time.sleep(0.5)
		WebDriverWait(self.browser, 20).until(
			EC.visibility_of_element_located((By.XPATH, '//div[@class="feed-toggle"]/ul/li/a[@href="#/tag/loret"]')))
		article_titles = self.browser.find_elements_by_xpath(
			'//div[@class="article-preview"]//a[@class="preview-link" and contains(@href, "articles")]/h1')

		articles = []
		for title in article_titles:
			articles.append(title)

		assert len(articles) > 0

		with open('test/article_out_titles.txt', 'w', encoding='UTF-8') as data_file:
			for i in articles:
				data_file.write(i.text)
				data_file.write("\n")

	# def test_pagination(self):  ## Lapozás.
	# 	# Vizsgáljuk meg, hogy a lapozó gombok kattinthatók, és az aktív gomb színe zöld.
	# 	pagination_btn = self.browser.find_elements_by_xpath(
	# 		'//ul[@class="pagination"]/li/a[contains(@class, "page-link")]')
	# 	page_counter = 1
	# 	for btn in pagination_btn:
	# 		assert btn.is_enabled()
	#
	# 		active_btn = self.browser.find_element_by_xpath(
	# 			'//ul[@class="pagination"]/li[contains(@class, "page-item active")]/a')
	# 		active_btn_rgbcolor = active_btn.value_of_css_property('background-color')
	# 		active_btn_hexcolor = Color.from_string(active_btn_rgbcolor).hex
	#
	# 		assert active_btn_hexcolor == '#5cb85c'
	#
	# 		page_counter += 1
	#
	# def test_new_article(self):
	# 	new_article_nav = self.browser.find_element_by_xpath('//a[@href="#/editor"]')
	# 	new_article_nav.click()
	#
	# 	editor_article(self.browser, new_article['title'], new_article['about'], new_article['descr'],
	# 				   new_article['tags'])
	#
	# 	WebDriverWait(self.browser, 20).until(
	# 		EC.url_matches(f'http://localhost:1667/#/articles/{new_article["about"]}'))
	# 	assert self.browser.current_url == f'http://localhost:1667/#/articles/{new_article["about"]}'
	#
	# def test_delete_article(self):
	# 	my_articles_titles(self.browser)[0].click()
	#
	# 	WebDriverWait(self.browser, 20).until(
	# 		EC.visibility_of_element_located((By.XPATH, '//button[@class="btn btn-outline-danger btn-sm"]'))).click()
	# 	assert self.browser.current_url == 'http://localhost:1667/#/articles/tesztcikk'
	# 	time.sleep(2)
	# 	assert self.browser.current_url == 'http://localhost:1667/#/'
	#
	# ## hogyan lehet az eltűnő felugró ablakot "elkapni"???
	#
	# def test_edit_article(self):
	# 	my_articles_titles(self.browser)[0].click()
	#
	# 	WebDriverWait(self.browser, 20).until(
	# 		EC.visibility_of_element_located((By.XPATH, '//a[@href="#/editor/tesztcikk"]'))).click()
	# 	time.sleep(1)
	# 	assert self.browser.current_url == 'http://localhost:1667/#/editor/tesztcikk'
	#
	# 	editor_article(self.browser, modified_article['title'], modified_article['about'], modified_article['descr'],
	# 				   modified_article['tags'])
	# 	time.sleep(0.5)
	# 	my_articles_titles(self.browser)
	# 	assert self.browser.find_element_by_xpath(f'//h1[text()="{modified_article["title"]}"]').is_displayed()


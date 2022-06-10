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
import csv
import pandas as pd


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

	def test_pagination(self):  # Lapozás.
		# Vizsgáljuk meg, hogy a lapozó gombok kattinthatók, és az aktív gomb színe zöld.
		pagination_btn = self.browser.find_elements_by_xpath(
			'//ul[@class="pagination"]/li/a[contains(@class, "page-link")]')
		page_counter = 1
		for btn in pagination_btn:
			assert btn.is_enabled()

			active_btn = self.browser.find_element_by_xpath(
				'//ul[@class="pagination"]/li[contains(@class, "page-item active")]/a')
			active_btn_rgbcolor = active_btn.value_of_css_property('background-color')
			active_btn_hexcolor = Color.from_string(active_btn_rgbcolor).hex

			assert active_btn_hexcolor == '#5cb85c'

			page_counter += 1

	def test_new_article(self):
		new_article_nav = self.browser.find_element_by_xpath('//a[@href="#/editor"]')
		new_article_nav.click()

		editor_article(self.browser, new_article['title'], new_article['about'], new_article['descr'],
					   new_article['tags'])

		# Ellenőrzöm, hogy a létrehozott article felületére irányít az oldal
		WebDriverWait(self.browser, 20).until(
			EC.url_matches(f'http://localhost:1667/#/articles/{new_article["about"]}'))
		assert self.browser.current_url == f'http://localhost:1667/#/articles/{new_article["about"]}'

	def test_edit_article(self):  # article módosításához első lépésben megkeresem az article-t, amit módosítani fogok
		my_articles(self.browser)
		article_to_edit = WebDriverWait(self.browser, 20).until(
			EC.presence_of_element_located(
				(By.XPATH, f'//a[@class="preview-link" and @href="#/articles/{new_article["about"]}"]')))
		article_to_edit.click()
		time.sleep(1)
		edit_article_btn = WebDriverWait(self.browser, 20).until(
			EC.visibility_of_element_located((By.XPATH, f'//a[@href="#/editor/{new_article["about"]}"]')))
		edit_article_btn.click()
		time.sleep(0.5)
		# Módosítom a létrehozott article adatait
		editor_article(self.browser, modified_article['title'], modified_article['about'], modified_article['descr'],
					   modified_article['tags'])
		# Megvizsgálom, hogy megjelenik az oldalon a módosított
		modified_article_title = WebDriverWait(self.browser, 20).until(
			EC.visibility_of_element_located((By.XPATH, f'//h1[contains(text(), {modified_article["title"]})]')))
		assert modified_article_title.is_displayed()

		# Megvizsgálom, hogy a módosítást követően a módosított article title-je szerepel a My Articles listában
		my_articles(self.browser)
		assert self.browser.find_element_by_xpath(f'//h1[text()="{modified_article["title"]}"]').is_displayed()

	def test_delete_article(self):  # article törléséhez első lépésben létrehozom amit majd törölni fogok
		self.browser.find_element_by_xpath('//a[@href="#/editor"]').click()
		editor_article(self.browser, new_article['title'], new_article['about'], new_article['descr'],
					   new_article['tags'])
		time.sleep(0.5)
		# Törlöm az article-t
		del_article_btn = WebDriverWait(self.browser, 20).until(
			EC.visibility_of_element_located((By.XPATH, '//button[@class="btn btn-outline-danger btn-sm"]')))
		del_article_btn.click()
		# Ellenőrzöm, hogy törlés után automatikusan a főoldalra irányít az oldal
		time.sleep(2)
		assert self.browser.current_url == 'http://localhost:1667/#/'
		# Ellenőrzöm, hogy a My Articles listájában nem szerepel a kitörölt article, így 1 db article-nek kell lennie
		my_articles(self.browser)
		my_articles_elements = WebDriverWait(self.browser, 20).until(
			EC.visibility_of_all_elements_located((By.XPATH, '//a[@class="preview-link"]')))
		assert len(my_articles_elements) == 1

	def test_datas_to_file(self):
		# Elmentem a Global Feedben található article-k title-jeit, about-jait és szerzőjét egy .csv fájlba
		article_author = self.browser.find_elements_by_xpath('//a[@class="author"]')
		article_title = self.browser.find_elements_by_xpath('//a[@class="preview-link"]/h1')
		article_about = self.browser.find_elements_by_xpath('//a[@class="preview-link"]/p')

		with open('test/general_feed_articles.csv', 'w', newline='') as csvfile:
			gen_feed_art = csv.writer(csvfile, delimiter=';')
			gen_feed_art.writerow(['Nr.', 'Title', 'About', 'Author'])
			for index, title in enumerate(article_title, start=1):
				gen_feed_art.writerow(
					[index, title.text, article_about[index - 1].text, article_author[index - 1].text])

		pt_csv = pd.read_csv('test/general_feed_articles.csv')
		assert len(article_title) == len(pt_csv.index)

	def test_datas_from_file(self):
		try:
			with open('test/test_datas_articles.csv', 'r', encoding='UTF-8') as data_file:
				data_table = csv.reader(data_file, delimiter=';')
				next(data_table)
				i = 0
				for row in data_table:
					i = i + 1
					new_article_nav = self.browser.find_element_by_xpath('//a[@href="#/editor"]')
					new_article_nav.click()
					editor_article(self.browser, row[0], row[1], row[2], row[3])
		except:
			assert False
		else:
			assert True

		pt_csv = pd.read_csv('test/test_datas_articles.csv')
		assert i == len(pt_csv.index)

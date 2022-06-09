from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time


def registration(browser, username, useremail, userpwd):
	register_nav = WebDriverWait(browser, 20).until(
		EC.presence_of_element_located((By.XPATH, '//a[@href="#/register"]')))
	register_nav.click()

	username_input = browser.find_element_by_xpath('//input[@placeholder="Username"]')
	email_input = browser.find_element_by_xpath('//input[@placeholder="Email"]')
	pwd_input = browser.find_element_by_xpath('//input[@placeholder="Password"]')

	username_input.send_keys(username)
	email_input.send_keys(useremail)
	pwd_input.send_keys(userpwd)

	sign_up_btn = browser.find_element_by_xpath('//button[contains(text(), "Sign up")]')
	sign_up_btn.click()
	time.sleep(2)


def login(browser, useremail, userpwd):
	login_nav = browser.find_element_by_xpath('//a[@href="#/login"]')
	login_nav.click()

	email_input = browser.find_elements_by_xpath('//input')[0]
	pwd_input = browser.find_elements_by_xpath('//input')[1]
	email_input.send_keys(useremail)
	pwd_input.send_keys(userpwd)

	sign_in_btn = browser.find_element_by_xpath('//button[contains(text(), "Sign in")]')
	sign_in_btn.click()
	time.sleep(2)


# WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Log out")]')))


# Kilistázzuk a My Article-ből az article title-ket
def my_articles_titles(browser):
	nav_profile = WebDriverWait(browser, 20).until(
		EC.visibility_of_element_located((By.XPATH, '//a[@href="#/@KimmelDezso/"]')))
	nav_profile.click()
	WebDriverWait(browser, 20).until(
		EC.visibility_of_element_located(
			(By.XPATH, '//a[@href="#/@KimmelDezso/" and contains(text(), "My Articles")]')))
	article_titles = browser.find_elements_by_xpath('//a[@href="#/articles/tesztcikk"]/h1')
	return article_titles


# Cikk lérehozása/szerkesztése
def editor_article(browser, art_title, art_about, art_descr, art_tags):
	input_title = browser.find_element_by_xpath('//input[@placeholder="Article Title"]')
	input_about = browser.find_element_by_xpath('//input[@type="text" and @placeholder="What\'s this article about?"]')
	input_descr = browser.find_element_by_xpath('//textarea[@placeholder="Write your article (in markdown)"]')
	input_tags = browser.find_element_by_xpath('//input[@placeholder="Enter tags"]')

	input_title.clear()
	input_about.clear()
	input_descr.clear()
	input_tags.clear()

	input_title.send_keys(art_title)
	input_about.send_keys(art_about)
	input_descr.send_keys(art_descr)
	input_tags.send_keys(art_tags)

	publish_btn = browser.find_element_by_xpath('//button[@type="submit" and contains(text(), "Publish Article")]')
	publish_btn.click()

#!/usr/local/bin/python3
import pip
import time
import os
import sys
import csv
try:
    from bs4 import BeautifulSoup
except ImportError:
    pip.main(['install', 'BeautifulSoup4'])
try:
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.common.keys import Keys
except ImportError:
    pip.main(['install', 'selenium'])
try:
    import pySmartDL
except ImportError:
    pip.main(['install', 'pySmartDL'])


class KissAnime:

	def __init__(self):
		self.driver = webdriver.Firefox()
		self.driver.set_page_load_timeout(100)
		self.anime_page = ""
		self.episode_list = []

	def login(self, username, password):

		# go to the site login page
		self.driver.get("https://kissanime.to/Login")

		#wait for cloudflare to figure itself out
		time.sleep(10)

		username_field = self.driver.find_element_by_id("username")
		password_field = self.driver.find_element_by_id("password")

		#type login info into fields
		username_field.send_keys(username)
		password_field.send_keys(password)

		# send the filled out login form adnd wait
		password_field.send_keys(Keys.RETURN)
		time.sleep(5)

		if self.driver.current_url == "https://kissanime.to/":
			return True
		else:
			return False

	def get_episodes_url(self,anime_url):
		self.driver.get(anime_url)
		self.anime_page = self.driver.page_source
		soup = BeautifulSoup(self.anime_page, 'html.parser')

		hyperlink_list = soup.findAll('a')

		_url_list = []
		for hyperlink in hyperlink_list:
			href = hyperlink.get('href')
			if href is None:
				continue
			_href_split = href.split('?')

			if len(_href_split) == 2 and _href_split[1][0:2]== 'id':
				_url_list.append(href)
				print(href)
		return _url_list

	def get_downlink_link(self, episode_url):
		print(episode_url)



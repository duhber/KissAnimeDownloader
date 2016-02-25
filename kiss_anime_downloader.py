#!/usr/local/bin/python3
import pip
import time
import configparser
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


class KissDownloader:

	def __init__(self, params):
		self.driver = webdriver.Firefox()
		self.driver.set_page_load_timeout(100)
		self.rootPage = ""
		self.episode_list = []

	def login(self, user, password):
		global config

		# go to the site login page
		self.driver.get("https://kissanime.to/Login")

		#wait for cloudflare to figure itself out
		time.sleep(10)

		username = self.driver.find_element_by_id("username")
		password = self.driver.find_element_by_id("password")

		#type login info into fields
		username.send_keys(user)
		username.send_keys(password)

		# send the filled out login form adnd wait
		password.send_keys(Keys.RETURN)
		time.sleep(5)

		if self.driver.current_url == "https://kissanime.to/":
			return True
		else:
			return False

	def get_
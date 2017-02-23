#!/usr/local/bin/python3
import pip
import time
import os
import sys
import csv
import settings
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


class KissAnime:

	def __init__(self,anime_url):
		self.anime_page = ""
		self.ANIME_URL = anime_url
		self.ANIME_TITLE = self.get_title()

	def login(self):
		self.driver = webdriver.Firefox()
		self.driver.set_page_load_timeout(100)
		# go to the site login page
		self.driver.get(settings.LOGIN_PAGE)
		#wait for cloudflare to figure itself out
		time.sleep(10)
		username_field = self.driver.find_element_by_id("username")
		password_field = self.driver.find_element_by_id("password")

		#type login info into fields
		username_field.send_keys(settings.USERNAME)
		password_field.send_keys(settings.PASSWORD)

		# send the filled out login form adnd wait
		password_field.send_keys(Keys.RETURN)
		time.sleep(5)
		print(self.driver.current_url)
		print(settings.HOME_PAGE)
		if self.driver.current_url == settings.HOME_PAGE+"/":
			return True
		else:
			return False

	def get_video_urls(self): # return all the url of videos page

		self.driver.get(self.ANIME_URL)
		self.anime_page = self.driver.page_source
		soup = BeautifulSoup(self.anime_page, 'html.parser')

		hyperlink_list = soup.findAll('a')

		_url_dict = dict()
		for hyperlink in hyperlink_list:
			href = hyperlink.get('href')
			if href is None:
				continue
			_href_split = href.split('?')
			if len(_href_split) == 2 and _href_split[1][0:2]== 'id':
				video_name = _href_split[0].split('/')[-1]
				video_url = settings.HOME_PAGE + href
				print(video_name)
				if not video_name in _url_dict.keys():
					_url_dict[video_name] = video_url

		return _url_dict

	def get_download_link(self, video_url):

		load=False

		while not load:
			try:
				self.driver.get(video_url)
				load=True
			except TimeoutException:
				print("LOADING "+ video_url +" TIMED OUT.. TRYING AGAIN")

		time.sleep(10)
		video_page = self.driver.page_source
		soup_page = BeautifulSoup(video_page, 'html.parser')
		video_link=[]

		for quality in settings.VIDEO_QUALITY:

			video_link = soup_page.find_all("a",string=quality)
			if not len(video_link) == 0:
				break
		if len(video_link) == 0:

			return None

		download_link = video_link[0].get('href')

		return download_link


	def close(self):
		self.driver.close()

	def get_title(self):
		return self.ANIME_URL.split('/')[-1]

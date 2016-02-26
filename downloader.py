#!/usr/local/bin/python3
from kissanime import KissAnime
import settings
import sys
import os

if __name__=='__main__':
	
	arg_length = len(sys.argv)

	if not arg_length == 2:

		print('USAGE: ANIME URL IS MANDATORY: https://kissanime.to/Anime/Tamako-Love-Story')
		exit()
		
	ANIME_URL = sys.argv[1]
	print(ANIME_URL)

	kissanime = KissAnime(ANIME_URL)

	# need to login to download file
	is_login = kissanime.login()

	if is_login is not True:
		print('USERNAME or PASSWORD is INVALID')
		kissanime.close()
		exit()

	destination = settings.DESTINATION + kissanime.ANIME_TITLE + '/'

	try:
		os.stat(destination)
		print(destination+' EXIST')
	except:
		print(destination+' NOT EXIST')
		os.mkdir(destination)

	_url_file = destination + settings.VIDEO_URLS

	video_urls = dict()


	# save video page url in a file or read video page url if file alread exist
	if not os.path.isfile(_url_file):
		print("WRITE")
		video_urls=kissanime.get_video_urls()
		with open(_url_file,'w') as f:
			for _name in video_urls.keys():
				#print(_name+' '+video_urls[_name])
				f.write(_name+' '+video_urls[_name]+'\n')
	else:
		print("READ")
		with open(_url_file,'r') as f:
			for line in f:

				_name = line.split(' ')[0]
				_url  = line.split(' ')[-1]
				#print(_name+' '+video_urls[_name])
				video_urls[_name] = _url

	download_list = sorted(video_urls.keys()) # user choice

	_link_file = destination + settings.DOWNLOAD_LINKS

	download_links = dict()
	
	# link which are already saved
	if os.path.isfile(_link_file):
		file = open(_link_file,'r')
		for line in file:
			_name = line.split(' ')[0]
			_link = line.split(' ')[-1]

			download_links[_name] = _link

		file.close()
	
	# get and save link in a file
	for _name in download_list:

		if _name in download_links.keys():
			continue

		_url = video_urls[_name]

		_link = kissanime.get_download_link(_url)

		if _link is None:
			continue
		print(_name+' '+_link)
		
		download_links[_name] = _link
		file = open(_link_file,'a')
		file.write(_name+' '+_link+'\n')
		file.close()

	#for url in episodes_url:
	#	print(url)

	kissanime.close()

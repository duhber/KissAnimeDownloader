#!/usr/local/bin/python3
from kissanime import KissAnime
import settings
import sys
import os
try:
    import pySmartDL
except:
    pip.main(['install','pySmartDL'])

import time

def download(download_list,download_links, destination, anime_title):

	for(dirpath,dirnames,filenames) in os.walk(destination):

		break

	_finished = []

	for file in filenames:
		if file.endswith(".mp4"):
			_finished.append(file)

	for video in download_list:

		filename = anime_title+'-'+video + ".mp4"
		if filename in _finished:# check if already download
			print(filename + ' '*5+'[DONE]' )
			continue

		_link = download_links[video]

		if _link == settings.LINK_NOT_FOUND:
			print(filename + ' '*5+'['+_link+']')
			continue

		try:
			#print(_link+' ' + filename + ' ' + destination)
			download_video(_link, filename, destination)
		except:
			print("DOWNLOAD ERROR")
			return


def download_video(link, filename, destination):
        path = destination + filename
        obj = pySmartDL.SmartDL(link, destination, progress_bar=False, fix_urls=True)
        obj.start(blocking=False)
        location = obj.get_dest()
        j=10
        i=1
        while True:
            if obj.isFinished():
                break
            k=j-i
            print(filename+' '*5+'[DOWNLOADING '+'.'*i+' '*k+' ' +str(float("{0:.2f}".format((float(obj.get_progress())*100))))+'%  '+pySmartDL.utils.sizeof_human(obj.get_speed(human=False)) +'/s]', end='\r',flush=True)
            sys.stdout.write("\033[K")
            time.sleep(1)
            if i==10:
                i=1
            else:
                i=i+1
        if obj.isFinished():
            print(filename+' '*5+'[DONE]')
            os.rename(location, path)
        else:
            print("DOWNLOAD OF " + filename + " FAILED")
        return path

if __name__=='__main__':

	arg_length = len(sys.argv)

	if arg_length < 2:

		print('USAGE: ANIME URL IS MANDATORY: https://kissanime.to/Anime/Tamako-Love-Story')
		print('USAGE: ANIME_URL <OPTIONAL> EPISODE_FROM EPISODE_TO')
		exit()

	ANIME_URL = sys.argv[1]
	EPISODE_FROM=0
	EPISODE_TO=0
	if  arg_length == 4:
		EPISODE_FROM=int(sys.argv[2])
		EPISODE_TO = int(sys.argv[3])
	#print(ANIME_URL)

	kissanime = KissAnime(ANIME_URL)

	destination = settings.DESTINATION + kissanime.ANIME_TITLE + '/'
	print('*'*10 +' '+ kissanime.ANIME_TITLE +' '+'*'*10)
	try:
		os.stat(destination)
		#print(destination+' EXIST')
	except:
		#print(destination+' NOT EXIST')
		os.mkdir(destination)

	_url_file = destination + settings.VIDEO_URLS

	video_urls = dict()

	is_login = False
	# save video page url in a file or read video page url if file alread exist
	if not os.path.isfile(_url_file):
		#print("WRITE")
		is_login = kissanime.login()
		if not is_login:
			print('USERNAME or PASSWORD is INVALID')
			kissanime.close()
			exit()

		video_urls=kissanime.get_video_urls()
		with open(_url_file,'w') as f:
			for _name in video_urls.keys():
				#print(_name+' '+video_urls[_name])
				f.write(_name+' '+video_urls[_name]+'\n')
	else:
		#print("READ")
		with open(_url_file,'r') as f:
			for line in f:

				_name = line.split(' ')[0]
				_url  = line.split(' ')[-1]
				#print(_name+' '+video_urls[_name])
				video_urls[_name] = _url

	download_list = sorted(video_urls.keys()) # user choice
	if  arg_length == 4:
		download_list=[]
		for i in range(EPISODE_FROM,EPISODE_TO):
			download_list.append("Episode-"+str(i))




	_link_file = destination + settings.DOWNLOAD_LINKS
	print(download_list)
	download_links = dict()

	# link which are already saved
	if os.path.isfile(_link_file):
		file = open(_link_file,'r')
		for line in file:
			_name = line.split(' ')[0]
			_link = line.split(' ')[-1]

			download_links[_name] = _link.split('\n')[0]
		file.close()

	# get and save link in a file
	for _name in download_list:

		_link = None
		if not _name in download_links.keys():
			_url = video_urls[_name]

			if not is_login: # need to login to get download link
				if kissanime.login():
					is_login = True
				else:
					is_login = False
					print('USERNAME or PASSWORD is INVALID')
					kissanime.close()
					exit()

			_link = kissanime.get_download_link(_url)

			if _link is None:

				download_links[_name] = settings.LINK_NOT_FOUND
				continue
				#_link = settings.LINK_NOT_FOUND
			download_links[_name] = _link
			file = open(_link_file,'a')
			file.write(_name+' '+_link+'\n')
			file.close()

		print(_name+' '+ download_links[_name])
	if is_login:
		kissanime.close()

	print("DOWNLOADING VIDEO")
	download(download_list,download_links, destination,kissanime.ANIME_TITLE)

	#for url in episodes_url:
	#	print(url)

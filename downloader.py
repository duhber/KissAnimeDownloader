#!/usr/local/bin/python3
from kissanime import KissAnime
import sys

if __name__=="__main__":
	
	arg_length = len(sys.argv)

	if not arg_length == 2:

		print("USAGE: ANIME URL IS MANDATORY: https://kissanime.to/Anime/Tamako-Love-Story")
		exit()
		
	URL = sys.argv[1]
	print(URL)

	kissanime = KissAnime()

	is_login = kissanime.login("duhbera","dewey0921")

	if is_login is not True:
		print("USERNAME or PASSWORD is INVALID")
		exit()

	kissanime.get_episodes_url(URL)




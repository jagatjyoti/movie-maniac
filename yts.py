#!/usr/bin/python

import requests
import platform
import json
import subprocess
import os
import sys
import argparse


def get_distro():
    var = platform.dist()
    os  = var[0]
    if os != 'Ubuntu':
    	print "Distribution is other than Ubuntu! Exiting ..."
    	sys.exit(1)
    

def torrent_client_check():
	try:
		print "Checking if client present \n"
		subprocess.call(["transmission-cli"])
	except OSError as e:
		if e.errno == os.errno.ENOENT:
			print "Torrent client not installed ... Installing now ! \n"
			cmd = "sudo apt-get -y install transmission-cli"
			subprocess.call(cmd, shell=True)
		else:
			print "Something else went wrong while trying to run `transmission-cli`"
			raise


def check_diskspace():
	space = subprocess.check_output(["df --output=avail / | sed -n '2p'"], shell=True)
	if (space < 1500000):
		print "Disk space of root filesystem less than 1.5 GB. Please free up space before downloading... Exiting !"
		sys.exit(1)


def movie_search(args):
	global movie_id
	movie_id = ""
	try: 
		url = 'https://yts.ag/api/v2/list_movies.json?query_term=' + args.movie_name
		headers = {'Content-type': 'application/json'}
		print "Trying to hit API of YTS and get response ... \n"
		r = requests.get(url, headers=headers) 
		try:
			data = json.loads(r.content)
		except ValueError as e:
			print "Exception raised: ", e
			sys.exit(1)
		if data["data"]["movie_count"] == 0:
			print "No such movie or incorrect spell of movie name ! Exiting ..." + "\n"
			sys.exit(1)
		for i in data["data"]["movies"]:
			if i["title"] == args.movie_name:
				title = i["title"]
				movie_id = i["id"]
		url = 'https://yts.ag/api/v2/movie_details.json?movie_id=' + str(movie_id)
		headers = {'Content-type': 'application/json'}
		r = requests.get(url, headers=headers) 
		print "Status Code: ", r.status_code, r.reason + "\n"
		try: 
			data = json.loads(r.content)
		except ValueError as e:
			print "Exception raised: ", e 
			sys.exit(1)
		try:
			if data["data"]["movie_count"] == 0:
				print "No such movie or incorrect spell of movie name ! Exiting ..." + "\n"
				sys.exit(1)
		except:
			pass

		print "********************** Movie Details *************************"
		print "Movie Name:", data["data"]["movie"]["title"]
		print "Release Year:", data["data"]["movie"]["year"]
		print "URL:", data["data"]["movie"]["url"]
		print "Rating:", data["data"]["movie"]["rating"]
		gen = data["data"]["movie"]["genres"]
		print "Genre:", [str(item) for item in gen]
		print "Description:", data["data"]["movie"]["description_intro"]
		print "\n"
		#print json.dumps(data, indent=4)

	except requests.exceptions.RequestException as e: 
		print "Exception: \n", e
        sys.exit(1)

def movie_suggestions(args):
	try: 
		url = 'https://yts.ag/api/v2/list_movies.json?query_term=' + args.movie_name
		headers = {'Content-type': 'application/json'}
		r = requests.get(url, headers=headers) 
		print "Status Code: ", r.status_code, r.reason + "\n"
		try:
			data = json.loads(r.content)
		except ValueError as e:
			print "Exception raised: ", e
			sys.exit(1)
		if data["data"]["movie_count"] == 0:
			print "No such movie or incorrect spell of movie name ! Exiting ..." + "\n"
			sys.exit(1)	
		movie_id = data["data"]["movies"][0]["id"]	
		print "Got corresponding movie ID: ", movie_id
		url = 'https://yts.ag/api/v2/movie_suggestions.json?movie_id=' + str(movie_id)
		print "Trying to hit API of YTS and get response ... \n"
		headers = {'Content-type': 'application/json'}
		r = requests.get(url, headers=headers) 
		print "Status Code: ", r.status_code, r.reason + "\n"
		try:
			data = json.loads(r.content)
		except ValueError as e:
			print "Exception raised: ", e
			sys.exit(1)
		print "************************ Movie Suggestions ************************* \n"
		for i in data["data"]["movies"]:
			print "\n ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n"
			print "Movie Name:", i["title"]
			print "Release Year:", i["year"]
			print "Rating:", i["rating"]
			print "URL:", i["url"]
			print "Description:", i["summary"]
		print "========================================"

	except requests.exceptions.RequestException as e: 
		print "Exception: \n", e
        sys.exit(1)

def movie_download(args):
	check_diskspace()
	torrent_client_check()
	try: 
		url = 'https://yts.ag/api/v2/list_movies.json?query_term=' + args.movie_name
		headers = {'Content-type': 'application/json'}
		print "Trying to hit API of YTS and get response ... \n"
		r = requests.get(url, headers=headers) 
		try:
			data = json.loads(r.content)
		except ValueError as e:
			print "Exception raised: ", e
			sys.exit(1)
		if data["data"]["movie_count"] == 0:
			print "No such movie or incorrect spell of movie name ! Exiting ..." + "\n"
			sys.exit(1)
		for i in data["data"]["movies"]:
			if i["title"] == args.movie_name:
				title = i["title"]
				movie_id = i["id"]
		url = 'https://yts.ag/api/v2/movie_details.json?movie_id=' + str(movie_id)
		headers = {'Content-type': 'application/json'}
		r = requests.get(url, headers=headers) 
		print "Status Code: ", r.status_code, r.reason + "\n"
		try:
			data = json.loads(r.content)
		except ValueError as e:
			print "Exception raised: ", e
			sys.exit(1)
		try:
			if data["data"]["movie_count"] == 0:
				print "No such movie or incorrect spell of movie name ! Exiting ..." + "\n"
				sys.exit(1)
		except:
			pass

	except requests.exceptions.RequestException as e: 
		print "Exception: \n", e
		sys.exit(1)	

	hash_id = data["data"]["movie"]["torrents"][1]["hash"]
	print "Hash ID for corresponding movie: ", hash_id
	download_dir = "~/Downloads"
	if not os.path.exists(download_dir):
		print "Creating directory Downloads in home folder to save file ..."
		os.makedirs(download_dir)
	print "Downloading movie ... \n"
	cmd = "/usr/bin/transmission-cli https://yts.ag/torrent/download/" + hash_id
	subprocess.call(cmd, shell=True)
	#subprocess.call(["/usr/bin/transmission-cli", "https://yts.ag/torrent/download/", hash_id],shell=True)   
	 
parser = argparse.ArgumentParser(description='Python movie maniac program')
subparsers = parser.add_subparsers()
 

parser_movie_search = subparsers.add_parser('movie_search', help='Search and fetch details of a movie')
parser_movie_search.add_argument('movie_name', type=str)
parser_movie_search.set_defaults(func=movie_search)
 
parser_movie_suggestions = subparsers.add_parser('movie_suggestions', help='Show related movies to the movie')
parser_movie_suggestions.add_argument('movie_name', type=str)
parser_movie_suggestions.set_defaults(func=movie_suggestions)

parser_movie_download = subparsers.add_parser('movie_download', help='Download a movie')
parser_movie_download.add_argument('movie_name', type=str)
parser_movie_download.set_defaults(func=movie_download)
 
if len(sys.argv) <= 1:
    sys.argv.append('--help')
 
args = parser.parse_args()
 
#args.func(args)


if __name__ == "__main__":
	get_distro()
	args.func(args)


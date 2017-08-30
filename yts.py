#!/usr/bin/python

import requests
import platform
import json
import time
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
    

def check_diskspace():
	space = subprocess.check_output(["df --output=avail / | sed -n '2p'"], shell=True)
	if (space < 1500000):
		print "Disk space of root filesystem less than 1.5 GB. Please free up space before downloading... Exiting !"
		sys.exit(1)


def movie_search(args):
	try: 
		url = 'https://yts.ag/api/v2/list_movies.json?query_term=' + args.movie_name
		headers = {'Content-type': 'application/json'}
		print "Trying to hit web address ", url + "\n"
		r = requests.get(url, headers=headers) 
		print "Status Code: ", r.status_code, r.reason + "\n"
		data = json.loads(r.content)
		print "********************** Movie Details *************************"
		print "Movie Name:", data["data"]["movies"][0]["title"]
		print "Release Year:", data["data"]["movies"][0]["year"]
		print "URL:", data["data"]["movies"][0]["url"]
		print "Rating:", data["data"]["movies"][0]["rating"]
		gen = data["data"]["movies"][0]["genres"]
		print "Genre:", [str(item) for item in gen]
		print "Description:", data["data"]["movies"][0]["summary"]
		print "\n"
		#print json.dumps(data, indent=4)
	except requests.exceptions.RequestException as e: 
		print e
        sys.exit(1)

def movie_reviews(args):
	try: 
		url = 'https://yts.ag/api/v2/list_movies.json?movie_id=' + args.movie_id
		headers = {'Content-type': 'application/json'}
		print url
		r = requests.get(url, headers=headers) 
		print r.status_code
		data = json.loads(r.content)
		print json.dumps(data, indent=4)
	except requests.exceptions.RequestException as e: 
		print e
        sys.exit(1)

def movie_download(args):
	check_diskspace()
	try: 
		url = 'https://yts.ag/api/v2/list_movies.json?query_term=' + args.movie_name
		headers = {'Content-type': 'application/json'}
		print url
		r = requests.get(url, headers=headers) 
		print r.status_code
		data = json.loads(r.content)
		print "in func"
	except requests.exceptions.RequestException as e: 
		print e
		sys.exit(1)	
	print "outside try block"
	hash_id = data["data"]["movies"][0]["torrents"][0]["hash"]
	print hash_id
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
 
parser_movie_reviews = subparsers.add_parser('movie_reviews', help='Show reviews of a movie')
parser_movie_reviews.add_argument('movie_id', type=int)
parser_movie_reviews.set_defaults(func=movie_reviews)

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


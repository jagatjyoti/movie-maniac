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
    return False


def movie_search(args):
	try: 
		url = 'https://yts.ag/api/v2/list_movies.json?query_term=' + args.movie_name
		headers = {'Content-type': 'application/json'}
		print url
		r = requests.get(url, headers=headers) 
		print r.status_code
		data = json.loads(r.content)
		print data
	except requests.exceptions.RequestException as e: 
		print e
        sys.exit(1)

def movie_reviews(args):
	try: 
		url = 'https://yts.ag/api/v2/list_movies.json?movie_id=' + args.movie_id
		print url
		r = requests.get(url) 
		print r.status_code
		print r.content
	except requests.exceptions.RequestException as e: 
		print e
        sys.exit(1)

 
parser = argparse.ArgumentParser(description='Python movie maniac program')
subparsers = parser.add_subparsers()
 

parser_movie_search = subparsers.add_parser('movie_search', help='Search and fetch details of a movie')
parser_movie_search.add_argument('movie_name', type=str)
parser_movie_search.set_defaults(func=movie_search)
 
parser_movie_reviews = subparsers.add_parser('movie_reviews', help='Show reviews of a movie')
parser_movie_reviews.add_argument('movie_id', type=str)
parser_movie_reviews.set_defaults(func=movie_reviews)
 
if len(sys.argv) <= 1:
    sys.argv.append('--help')
 
args = parser.parse_args()
 
args.func(args)


if __name__ == "__main__":
	get_distro()


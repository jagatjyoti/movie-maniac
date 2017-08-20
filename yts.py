#!/usr/bin/python

import requests
import platform
import json
import time
import subprocess
import os
import sys
import argparse


# #def get_args():
# '''This function parses and return arguments passed in'''
# # Assign description to the help doc
parser = argparse.ArgumentParser(
    description='Python program for processing movie torrents')
# Add arguments
parser.add_argument(
    '-s', '--search', type=str, help='Movie search', required=False)
parser.add_argument(
    '-r', '--reviews', type=str, help='Movie reviews', required=False)
# Array for all arguments passed to script
args = parser.parse_args()
print args
# Assign args to variables
# global movie_search, movie_details
# movie_search = args.movie
# movie_details = args.details

# FUNCTION_MAP = {'search_movie' : movie_search,
#                 'reviews_of_movie' : movie_reviews}

# parser.add_argument('command', choices=FUNCTION_MAP.keys())

# args = parser.parse_args()

# func = FUNCTION_MAP[args.command]
# func()


def get_distro():
    var = platform.dist()
    os  = var[0]
    if os != 'Ubuntu':
    	print "Distribution is other than Ubuntu! Exiting ..."
    	sys.exit(1)
    return False


def movie_search():
	try: 
		url = 'https://yts.ag/api/v2/list_movies.json?query_term=movie_name'
		print url
		r = requests.get(url) 
		print r.status_code
		print r.content
	except requests.exceptions.RequestException as e: 
		print e
        sys.exit(1)

def movie_reviews():
	try: 
		url = 'https://yts.ag/api/v2/list_movies.json?movie_id='
		print url
		r = requests.get(url) 
	except requests.exceptions.RequestException as e: 
		print e
        sys.exit(1)


if __name__ == "__main__":
	get_distro()
	movie_search()


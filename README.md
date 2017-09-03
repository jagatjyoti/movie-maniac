# Movie-Maniac

Movie-Maniac is a program written in Python to search, suggest and download movies from [YTS](https://yts.ag/) (my personal favourite). 

## Description

The program takes a movie name from user as Input and makes an API call to YTS and does some post processing of data before it prints the intended output. 

Currently, it supports searching, getting suggestions and downloading a movie. 

## Running it 

```
$ python yts.py movie_search "Iron Man"

Trying to hit web address  https://yts.ag/api/v2/list_movies.json?query_term=Iron Man

Status Code:  200 OK

********************** Movie Details *************************
Movie Name: Iron Man
Release Year: 2008
URL: https://yts.ag/movie/iron-man-2008
Rating: 7.9
Genre: ['Action', 'Adventure', 'Sci-Fi']
Description: Tony Stark. Genius, billionaire, playboy, philanthropist. Son of legendary inventor and weapons contractor Howard Stark. When Tony Stark is assigned to give a weapons presentation to an Iraqi unit led by Lt. Col. James Rhodes, he's given a ride on enemy lines. That ride ends badly when Stark's Humvee that he's riding in is attacked by enemy combatants. He survives - barely - with a chest full of shrapnel and a car battery attached to his heart. In order to survive he comes up with a way to miniaturize the battery and figures out that the battery can power something else. Thus Iron Man is born. He uses the primitive device to escape from the cave in Iraq. Once back home, he then begins work on perfecting the Iron Man suit. But the man who was put in charge of Stark Industries has plans of his own to take over Tony's technology for other matters.



$ python yts.py movie_download "Iron Man"
Checking if client present 

transmission-cli 2.84 (14307)
A fast and easy BitTorrent client

Usage: transmission-cli [options] <file|url|magnet>

Options:
 -h  --help                          Display this help page and exit
 -b  --blocklist                     Enable peer blocklists
 -B  --no-blocklist                  Disable peer blocklists
 -d  --downlimit            <speed>  Set max download speed in kB/s
 -D  --no-downlimit                  Don't limit the download speed
 -er --encryption-required           Encrypt all peer connections
 -ep --encryption-preferred          Prefer encrypted peer connections
 -et --encryption-tolerated          Prefer unencrypted peer connections
 -f  --finish               <script> Run a script when the torrent finishes
 -g  --config-dir           <path>   Where to find configuration files
 -m  --portmap                       Enable portmapping via NAT-PMP or UPnP
 -M  --no-portmap                    Disable portmapping
 -p  --port                 <port>   Port for incoming peers (Default: 51413)
 -t  --tos                  <tos>    Peer socket TOS (0 to 255,
                                     default=default)
 -u  --uplimit              <speed>  Set max upload speed in kB/s
 -U  --no-uplimit                    Don't limit the upload speed
 -v  --verify                        Verify the specified torrent
 -V  --version                       Show version number and exit
 -w  --download-dir         <path>   Where to save downloaded data
Trying to hit web address  https://yts.ag/api/v2/list_movies.json?query_term=Iron Man

Iron Man
1648
Status Code:  200 OK

Hash ID for corresponding movie:  71754637FD29B4BE433723A4A559086E2BC083DC
Downloading movie ... 

transmission-cli 2.84 (14307)
[2017-09-03 12:55:55.100 IST] Transmission 2.84 (14307) started
[2017-09-03 12:55:55.101 IST] RPC Server: Adding address to whitelist: 127.0.0.1

```

Please feel free to report issues. Contribution and pull requests are very much welcome. :) 


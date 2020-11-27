# Lab 3
Client-Server based **web_scraper** console application over TCP connection described in [Scenario](#scenario).

## Scenario
Creating a client-server based console application with two roles: client and server. The server must start and wait for the request from a client. Server should scrape the web page received from the client and respond with the number of ***< img >***  and leaf  ***< p >*** tags. The leaf paragraphs in HTML document represents only the last paragraphs in the nested structures. 

## Installation
Install the requiremens for  Lab3:
``` console
$ pip install -r requirements.txt
```
## Usage
```console
usage: web_scraper.py [-h] [-host HOST] [-port PORT] {server,client}

simple web scraping over TCP

positional arguments:
  {server,client}  which role to play

optional arguments:
  -h, --help       show this help message and exit
  --host HOST       interface the server listens at; host the client sends to
                   (default: 127.0.0.1)
  --port PORT       TCP port (default: 1060)
  -p PAGE          web page URL to scrape -> this is only for the client
```

Two terminal windows should be opened. (one for the server side, and another for the client side)
### Server
Default port number is 1060, but it can be changed by specifying -port PORT, Default host is 127.0.0.1, but it can be changed by specifying -host HOST. Server receives the URL from the client, scrapes the web page requested, and respond with an answer. To start the server:
``` console
$ python3 web_scraper.py server
```

Note that this program uses threading. The program divides itself into two or more simultaneously (or pseudo-simultaneously) running tasks. Thus, the server could receive multiple requests.
### Client
Client should specify the link for the web page by -p PAGE. Below, an example has been given:
 ``` console
 $ python3 web_scraper.py client -p www.github.com
 ```
As a response from the server, client gets the number of < img > and leaf < p > tags.

 Server can be killed by pressing <code>Ctrl+C
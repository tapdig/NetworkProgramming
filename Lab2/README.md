# Lab 2
Creating the TCP based client-server console application "text_service" where a client sends two files to the server through sockets with two modes based on the [Scenario](#scenario).

## Scenario

### Modes:
**change_text:** The client sends the text and the JSON file to the server. In response, the server must read the json file and swap the words in the text according to the JSON file.
**encode_decode:** The client sends the text file and the key (another text) to the server. In response, the server must XOR (Vernam cipher; One-Time Pad) the text message with the key and return it to the client. 

## Installation
Install the requiremens for  Lab2:
``` console
$ pip install -r requirements.txt
```
## Usage
To see usage and which positional or optional arguments we have in detail:
##### For server: 
```console
python3 text_service.py server -h
```
##### For client:
```console
python3 text_service.py client -h
```
Two terminal windows should be opened. (one for the server side, and another for the client side)
### Server
On the server side, *host* positional argument can be "127.0.0.1" to indicate that you want packets from other programs running only on the same machine, or an empty string "" as a wildcard to indicate that you are willing to receive packets arriving at the server via any of its network interfaces, or you can provide the IP address of one of the machine's external IP interfaces, such as its Ethernet connection or wireless card, and the server will listen only for packets destined to those IPs. Default port number is 1060, but it can be changed by specifying -p PORT.
``` console
$ python3 text_service.py server ""
```
### Client
 On the client side, *hostname* should be the IP address or the hostname of the interface/machine client wants to connect. Default port number is 1060, but it can be changed by specifying -p PORT.
 ``` console
 $ python3 text_service.py client hostname --mode change_text textfile.txt swap.json
 ```
 OR
 ``` console
 $ python3 text_service.py client hostname --mode encode_decode textfile.txt key.txt
 ```
 Server can be killed by pressing Ctrl+C

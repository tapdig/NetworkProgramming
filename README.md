# NetworkProgramming
This repository contains lab assignments from Network Programming course.
1. [Lab1](#lab1)

<a name="Lab1"></a>
# Lab1
Create the basic UDP Client-Server console application with simple test messaging from the client to the server with the backoff strategies based on the [Scenario](#scenario). No need to send media files, just send test messages. 


<a  name="Scenario"></a>
## Scenario
Spotify regional server warehouse provides music streaming services for the millions of clients 24/7. Spotify servers responding time depends on clients' load number. That's why, clients must wait for responding with regard to the time schedule: 

**First interval:** Between 12:00 and 17:00 -  maximum wait time must be 2 seconds.
**Second Interval:** Between 17:00 and 23:59 - maximum wait time must be 4 seconds.
**Third Interval:** Between 23:59 and 12:00 - maximum waiting time must be 1 second. 

The exponential backoff of these intervals must be increased by the next factors:
For the *first* and *third* intervals: *doubles* on each iteration.
For the *second* interval: *triples* on each iteration.

## Installation
Clone this repository into any location of your choice on your device:
``` console
$ git clone https://github.com/tapdig/NetworkProgramming
```	
Install the requiremens for  Lab1:
``` console
$ pip install -r Lab1/requirements.txt
```
## Usage
To see usage and which positional or optional arguments we have:
```console
$  python3 Lab1/udp.py -h
```
Two terminal windows should be opened. (one for server side, and another for client side)

On the server side, *host* positional argument can be "127.0.0.1" to indicate that you want packets from other programs running only on the same machine, or an empty string "" as a wildcard to indicate that you are willing to receive packets arriving at the server via any of its network interfaces, or you can provide the IP address of one of the machine's external IP interfaces, such as its Ethernet connection or wireless card, and the server will listen only for packets destined to those IPs. Default port number is 1060, but it can be changed by specifying -p PORT.
``` console
$ python3 Lab1/udp.py server ""
```
 On the client side, *hostname* should be the IP address or the hostname of the machine client wants to connect.
 ``` console
 $ python3 Lab1/udp.py client hostname
 ```
 Server can be killed by pressing Ctrl+C


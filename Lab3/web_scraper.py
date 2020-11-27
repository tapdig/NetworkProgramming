#!/usr/bin/env python3
# simple web scraping over TCP

import sys
import socket
import argparse
import requests
import threading
from bs4 import BeautifulSoup


class Server:
    def __init__(self, address):
        self.address = address


    def server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(self.address)
        sock.listen(1)
        print(f"[SERVER] started and listens at {sock.getsockname()}")
        print()

        while True:
            sc, sockname = sock.accept()
            print("=" * 50)
            print(f"Accepted a connection from {sockname}")
            print(f"Socket name: {sc.getsockname()}")
            print(f"Socket peer: {sc.getpeername()}")
            print()
            thread = threading.Thread(target=self.process, args=(sc, sockname))
            thread.start()


    def scrape_img_tags(self, soup):
        return len(soup.find_all("img"))


    def scrape_leaf_p_tags(self, soup):
        paragraphs = soup.find_all("p")

        number_of_leaves = 0
        for paragraph in paragraphs:
            if not paragraph.find_all("p"):
                number_of_leaves += 1
        
        return number_of_leaves


    def process(self, connection, address):
        try:
            URL = connection.recv(4096).decode("ascii")
            if URL.startswith("http://") or URL.startswith("https://"):
                pass
            else:
                URL = "https://" + f"{URL}"

            print(f"Client requested to scrape {URL}")
            print(f"{URL} web page is being scraped...")

            webpage = requests.get(URL)
            soup = BeautifulSoup(webpage.text, "html.parser")

            message = f"{self.scrape_img_tags(soup)} {self.scrape_leaf_p_tags(soup)}".encode("ascii")
            connection.sendall(message)
            print(f"Message sent to the client at {address}: {message.decode('ascii')}")
            print("=" * 50)
        
        except OSError as e:
            print(f"Oops... {e.__class__} occurred. Failure in network transmission.")

        finally:
            connection.close()


class Client:
    def __init__(self, address):
        self.address = address


    def client(self, URL):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.address)
        sock.send(URL.encode("ascii"))

        response = sock.recv(4096)
        img_number, leaf_p_number = response.decode("ascii").split()
        print(f"In {URL}, there are {img_number} <img> and {leaf_p_number} leaf <p> tags.")


if __name__ == "__main__":
    choices = {"server": Server, "client": Client}
    parser = argparse.ArgumentParser(description="simple web scraping over TCP")
    parser.add_argument('role', choices=choices, help="which role to play")
    parser.add_argument('--host', metavar='HOST', default="127.0.0.1", help='interface the server listens at; host the client sends to (default: 127.0.0.1)')
    parser.add_argument('--port', metavar='PORT', type=int, default=1060, help='TCP port (default: 1060)')

    if sys.argv[1] == "client":
        parser.add_argument('-p', metavar="PAGE", type=str, help="web page URL to scrape")

    args = parser.parse_args()
    class_ = choices[args.role]

    if args.role == "server":
        class_((args.host, args.port)).server()

    elif args.role == "client":
        class_((args.host, args.port)).client(args.p)
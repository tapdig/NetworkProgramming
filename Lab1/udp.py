import socket, argparse, sys
import datetime
from random import random

MAX_BYTES = 65535

class Server:
	def __init__(self, interface, port):
		self.interface = interface
		self.port = port

	def connect(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind((self.interface, self.port))
		print(f"Listening at {sock.getsockname()}")

		while True:
			data, addr = sock.recvfrom(MAX_BYTES)
			if random() < 0.5: # used to randomly decide whether the request will be answered
				print(f"Pretending to drop packet from {addr}")
				continue

			text = data.decode("ascii")
			print(f"The client at {addr} says {text}")
			message = f"Your data is {len(data)} bytes long"
			sock.sendto(message.encode('ascii'), addr)

class Client:
	def __init__(self, hostname, port):
		self.hostname = hostname
		self.port = port

	def schedule(self):
		now = datetime.datetime.now().time()

		if datetime.time(12, 0, 0) <= now < datetime.time(17, 0, 0):
			return 1
		elif datetime.time(17, 0, 0) <= now <= datetime.time(23, 59, 59):
			return 2
		else:
			return 3

	def connect(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.connect((self.hostname, self.port))
		print(f"Client socket name is {sock.getsockname()}")

		delay = 0.1
		text = f"Time is {datetime.datetime.now()}"
		data = text.encode('ascii')

		while True:
			sock.send(data)
			print(f"Waiting up to {delay} seconds for a reply")
			sock.settimeout(delay)

			try:
				data = sock.recv(MAX_BYTES)
			except socket.timeout:
				interval = self.schedule()
				if interval == 1 or interval == 3:
					delay *= 2
				elif interval == 2:
					delay *= 3

				if (interval == 1 and delay > 2.0) or (interval == 2 and delay > 4.0) or (interval == 3 and delay > 1.0):
					raise RuntimeError("Server might be down")
			else: 
				break

		print(f"The server says {data.decode('ascii')}")

if __name__ == "__main__":
	choices = {"server": Server, "client": Client}
	parser = argparse.ArgumentParser(description="send and receive UDP packets with exponentional backoff strategies")
	parser.add_argument('role', choices=choices, help="which role to take")
	parser.add_argument('-p', metavar='PORT',  type=int, default=1060, help='UDP port (default 1060)')
	parser.add_argument('host', help='interface server listens at; hostname client sends to')
	args = parser.parse_args()

	choice = choices[args.role](args.host, args.p)
	choice.connect()

#!/usr/local/bin/python3

import socket
import sys


def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('169.232.218.20', 10000)
	print("connecting")
	sock.connect(server_address)

	while True:
		data = sock.recv(16)
		print(data.decode('utf-8'))

if __name__ == "__main__":
	main()

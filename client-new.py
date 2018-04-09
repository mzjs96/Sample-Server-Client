#!/usr/local/bin/python3

import socket
import sys
import time

from random import *

def main():
	#let us start in SF and SJ
	coord_a = [37.7749, 122.4194]
	coord_b = [37.3382, 121.8863]
	acc_a = [0, 0]
	acc_b = [0, 0]
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('128.97.104.46', 10000)
	print("connecting")
	sock.connect(server_address)

	current_time = time.time() + 1
	while True:
		if(time.time() > current_time):
			d_acc = [(randint(1,50)-25)/20,(randint(1,50)-25)/20,(randint(1,50)-25)/20,(randint(1,50)-25)/20]
			mov_a = [randint(1,100)/1000-0.02, randint(1,100)/1000-0.08]
			mov_b = [randint(1,100)/1000-0.02, randint(1,100)/1000-0.08]
			data_1 = "Gene" + "," + str(int((coord_a[0]+mov_a[0])*1000)) + "," + str(int((coord_a[1]+mov_a[1])*1000)) + "," + str(int((acc_a[0]+d_acc[0])*1000)) + "," + str(int((acc_a[1]+d_acc[1])*1000)) + ",|,,,,,,,,,,"
			data_2 = "Block" + "," + str(int((coord_b[0]+mov_b[0])*1000)) + "," + str(int((coord_b[1]+mov_b[1])*1000)) + "," + str(int((acc_b[0]+d_acc[2])*1000)) + "," + str(int((acc_b[1]+d_acc[2])*1000)) + ",|,,,,,,,,,,"
			sock.send(data_1.encode())
			sock.send(data_2.encode())
			current_time += 1

if __name__ == "__main__":
	main()

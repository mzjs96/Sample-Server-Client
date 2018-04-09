#!/usr/local/bin/python3

from twilio.rest import Client
from parse import *
from queue import *
from math import pow
from math import atan
from math import sqrt
from math import pi
import time
import socket
import sys

account_sid = 'AC6dec468120029b3e8eb327027d91452e'
auth_token = 'b0dcf779dfd6c385fe0f5d8ae4106a25'
myPhone = '+16502089884'
TwilioNumber = '+18317039125'

client = Client(account_sid, auth_token)

def main():
	socke = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('127.0.0.1', 10000)
	print("connecting")
	# sock.connect(server_address)
	socke.bind(server_address)
	socke.listen(5)
	sock, client_addr = socke.accept()
	print("connected")
	'''
		velocity calculation through position
	'''
	acc_x = 0
	acc_y = 0
	vel_x_q = Queue()
	vel_y_q = Queue()
	pos_x_q = Queue()
	pos_y_q = Queue()
	prev_dir = 0
	cur_dir = 0
	dt = 1
	data = ''
	'''
		velocity calculation through acceleration
	'''
	pos_x = 0
	pos_y = 0
	acc_x = 0
	acc_y = 0
	vel_x = 0
	vel_y = 0
	vel = 0
	acc = 0
	'''
		direction
	'''
	prev_dir = 0
	cur_dir = 0

	while True:
		emergency = False
		raw = sock.recv(8)
		temp = raw.decode('utf-8') #assuming input data is like '________[username]_[lat]_[lon]_[acc_x]_[acc_y]_|________' (ex. __23_34__)
		# assuming temp will be like '___|___' '23___' '___345__' '45___'
		# temp CANNOT BE '___|____532' otherwise next data will become corrupted
		print(temp)
		data += temp
		if(data.find('|') == -1):
			continue
		parsed = data.rsplit("_")
		parsed = list(filter(None, parsed))
		# parsed is a list: [user, position_x, position_y, acc_x, acc_y, '|']

		if (pos_x_q.qsize() < 2):
		    # build the initial position queue
			pos_x_q.put(int(parsed[1])/1000)
			pos_y_q.put(int(parsed[2])/1000)
			vel_x_q.put(0)
			vel_y_q.put(0)
		else:
			'''
				velocity calculation through position
			'''
			# NOTE: since using GPS coordinates, lower velocities will have larger error
		    # get position
			pos_x_q.put(int(parsed[1])/1000)
			pos_y_q.put(int(parsed[2])/1000)
			# velocity processing
			cur_vel_x = int(parsed[1])/1000 - pos_x_q.get()
			vel_x_q.put(cur_vel_x)
			cur_vel_y = int(parsed[2])/1000 - pos_y_q.get()
			vel_y_q.put(cur_vel_y)
			vel = sqrt(pow(cur_vel_x,2) + pow(cur_vel_y,2))/dt #NOTE: x and y values need to be divided by dt
			# acceleration processing
			acc_x = cur_vel_x - vel_x_q.get()
			acc_y = cur_vel_y - vel_y_q.get()
			acc = sqrt(pow(acc_x,2) + pow(acc_y,2))/dt
			'''
				velocity calculation through acceleration
			'''
			# NOTE: due to Reinmann sum calculation, first couple velocity points will be less accurate
			# NOTE: if loop is optional in this implementation
			# get position
			pos_x = int(parsed[1])/1000
			pos_y = int(parsed[2])/1000
			# get acceleration
			acc_x = int(parsed[3])/1000
			acc_y = int(parsed[4])/1000
			acc = sqrt(pow(vel_x,2) + pow(vel_y,2))
			# velocity processing
			vel_x += acc_x*dt
			vel_y += acc_y*dt
			vel = sqrt(pow(vel_x,2) + pow(vel_y,2))

			print(vel)
			'''
				direction calculations
			'''
			# NOTE: If using acceleration calculation method: replace cur_vel_x with vel_x and cur_vel_y with vel_y
			prev_dir = cur_dir
			cur_dir = atan(cur_vel_y/cur_vel_x)*180/pi
			'''
				emergency!
			'''
			if (emergency == True):
				# NOTE: remove following line to stop recieving messages
				'''
				client.messages.create(
					to=myPhone,
					from_=TwilioNumber,
					body='Your child is dead. :)' + u'\U0001f680')
				print("send text message!")
				'''
				sleep(3)
				emergency = False


if __name__ == "__main__":
    main()

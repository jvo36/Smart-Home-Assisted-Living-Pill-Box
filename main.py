#!/usr/bin/python
import sys
import fileinput
import time
from threading import Thread
from datetime import datetime, timedelta # python module for date operation
import pygame # module to play sound
import requests # post request
import json

# function to connect to the firebase and access to the phone app.
def authkey():
	FIREBASE_KEY = 'AAAAxy3wfUk:APA91bFWXRgdA2s4a_qd49Y6b-B_A9X91B6dxsKAtqaDlc-1K2gjuzcygAvN_VjbipOEKpyWcBWZ4_9iJVV4gHGNGiqZFHkm1D8yzzIrU1_eCCN2QGvOZsbughJdXYjPVLtAC6t9kbxQ'
	ACCESS_TOKEN = 'ckwjyIJUThy7XphEX2FIjw:APA91bHDusNyHzhqXd06cDzjlMzW_PzZI6ZsBNvFASXlfk7HXRaeKURIEz-BRhu_Sk0O03-WF-V7i01N88A7SOsHhg1k5rKjHQBu8Q0RrKR1mxd8eUvLKsvW4bjeLDdb5M07waWkGM4F'
	url = 'https://fcm.googleapis.com/fcm/send'
	headers = {'Content-type': 'application/json', 'Authorization': 'Bearer {}'.format(FIREBASE_KEY)}

	# json file to phone app
	payload = {
		'to': ACCESS_TOKEN,
		'notification': {
		'title': "Pill Box Alert!",
		'body': "Overdue pills needs to be taken!"
		}
	}

	r = requests.post(url, data=json.dumps(payload), headers=headers)

def checkkey():
	while True:
		enterKey = raw_input("Enter the key: \n")
		found = False

		for line in fileinput.input("database.txt", inplace=True):
			line_arr = line.split(',')
			bottle_id = line_arr[0].strip()
			curr_time = line_arr[1].strip()
			deadline = line_arr[2].strip()

			if enterKey == bottle_id:
				found = True
				now = datetime.now()
				current_time = now.strftime("%Y/%m/%d %H:%M:%S")
				time_range = now + timedelta(seconds=30)
				time_range2 = time_range.strftime("%Y/%m/%d %H:%M:%S")
				print('{},{},{}'.format(bottle_id, current_time, time_range2))
			else:
				print('{},{},{}'.format(bottle_id, curr_time, deadline))

		if found:
			print('Found bottle id: {}'.format(enterKey))
		else:
			print('Unable to find bottle id: {}'.format(enterKey))

def checktime():
	for line in fileinput.input("database.txt"):
		line_arr = line.split(',')
		bottle_id = line_arr[0].strip()
		curr_time = line_arr[1].strip()
		deadline = line_arr[2].strip()

		now = datetime.now()
		current_time = now.strftime("%Y/%m/%d %H:%M:%S")

		if deadline <= current_time:
			print('Past deadline. Please take medicine on bottle id: {}'.format(bottle_id))
			authkey()

def test():
	while True:
		checktime()
	 	pygame.mixer.init()
	 	pygame.mixer.music.load("storedoor.mp3")
	 	pygame.mixer.music.play()

	 	while pygame.mixer.music.get_busy() == True:
	 		continue

		time.sleep(10)


def main():
	# multi-threading so 2 function can run almost at the same time
	t1 = Thread(target=checkkey)
	t2 = Thread(target=test)
	t1.start()
	t2.start()

if __name__ == "__main__":		# another way of making "main" as main function
	main()

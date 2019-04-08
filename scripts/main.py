#!/usr/bin/python3

#Import Libraries
import queue, threading, time, os, sys
from check_online import check_online, grab_dev
from check_new_devices import check_new_devices

#Libraries Necessary for running script in Django Environment
sys.path.append('/home/pi/Documents/Scripts')
import setup

from django.contrib.auth.models import User
from home.models import setting as settings
from home.models import device as dev_model

print("started")

#Daemon Function which saves each device that is put in the queue.
def queue_save(q):
	while True:
		d = q.get()
		d.save()
		time.sleep(0.001)

#Creates a thread for each device, and a thread for checking for a new device.
def create_threads():
	threads = []
	devices = grab_dev()
	new_devices = threading.Thread(target=check_new_devices)
	new_devices.start()
	new_devices.join()
	
	for d in devices:
		threads.append(threading.Thread(target=check_online, args=(d,q)))
	for t in threads:
		t.start()
		time.sleep(0.001)
	for t in threads:
		t.join()
		time.sleep(0.001)

#Create the queue, and start the queue_save daemon thread
q = queue.Queue()
save_devices = threading.Thread(target=queue_save, args=(q,), daemon=True)
save_devices.start()

#Run forever, sleep for the time set in the database.
while True:
	create_threads()
	s = settings.objects.first()
	time.sleep(s.ping_time)

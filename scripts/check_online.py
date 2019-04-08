#Import Libraries
import os, sys, subprocess
from datetime import datetime
from notification import email_down, email_up
import multiprocessing as mp

#Libraries Necessary for running script in Django Environment
sys.path.append('/home/pi/Documents/Netscan')
import setup

from django.contrib.auth.models import User
from home.models import setting as settings
from home.models import device as dev_model

#Function which uses arping to see if a device is online, if its online return true, else false.
def ping(d):
	mac = '-t ' + d.mac
	FNULL = open(os.devnull, 'w')
	retcode = subprocess.call(['sudo', 'arping', '-c 3', mac, d.ip],
							  stdout=FNULL,
							  stderr=subprocess.STDOUT)
	if retcode == 0:
		return True
	else:
		return False

#Function which returns a list of all device objects
def grab_dev():
	return(dev_model.objects.all())
	
#https://stackoverflow.com/questions/8906926/formatting-python-timedelta-objects USER: Shawn Chin
#Function takes a time delta and a format and returns a string.
def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

#If the device is online, update the uptime. If it is changing from offline to online, set the flag, and send an email if the notification flag is 1. Place the device in the queue for saving.
def update_uptime(d, q):
	mac = d.mac
	first_ping_time = d.first_ping
	flag = d.down_flag
	
	if flag == '1':
		d.first_ping = datetime.now()
		d.down_flag = '0'
		
		if(d.notification):
			emails = list(User.objects.values_list('email', flat=True))
			email = mp.Process(target=email_up, args=(d,emails))
			email.start()
			email.join()
	
	time = strfdelta((datetime.now() - first_ping_time), "{days} Days {hours}:{minutes}:{seconds}")
	d.uptime = time
	q.put(d)

#If the device is offline, update the downtime. If it is changing from online to offline, set the flag, and send an email if the notification flag is 1. Place the device in the queue for saving.
def update_downtime(d, q):
	mac = d.mac
	last_ping_time = d.first_ping
	flag = d.down_flag
	
	if flag == '0':
		d.first_ping = datetime.now()
		d.down_flag = '1'
		
		if(d.notification):
			emails = list(User.objects.values_list('email', flat=True))
			email = mp.Process(target=email_down, args=(d,emails))
			email.start()
			email.join()
		
	time = strfdelta((datetime.now() - last_ping_time), "{days} Days {hours}:{minutes}:{seconds}")
	d.uptime = time
	q.put(d)

#Ping each device, if its online update uptime, otherwise update downtime.
def check_online(d, q):
	if ping(d):
		update_uptime(d, q)
	else:
		update_downtime(d, q)

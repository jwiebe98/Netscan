#Import models, post_save signal.
from django.db import models
from django.db.models.signals import post_save

#Import json, get_channel_layer, async_to_sync
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

#Define channel layer
channel_layer = get_channel_layer()

#Define device model with attributes.
class device(models.Model):
	device = models.CharField(max_length=50)
	ip = models.CharField(max_length=20, unique=True)
	mac = models.CharField(max_length=20, unique=True)
	uptime = models.CharField(max_length=20)
	down_flag = models.CharField(max_length=1)
	first_ping = models.DateTimeField()
	notification = models.BooleanField()
	
	#How each device is displayed in the admin page
	def __str__(self):
		return 'Device: {} IP: {}'.format(self.device, self.ip)

#Define setting model.
class setting(models.Model):
	ping_time = models.IntegerField()

#Function which sends a device to the front end each time a device is modified or saved in the database.
def send(sender, instance, raw, **kwargs):
	#If the save method is raw, do not send data to frontend
	if not raw:
		#Create a dictionary with values that need to be sent, convert to json
		data = {"id": instance.id, "uptime": instance.uptime, "flag": instance.down_flag, "name": instance.device, "ip": instance.ip, "mac": instance.mac}
		data = json.dumps(data)
		#convert from syncronous code to asyncronous code and send the json data to the channel layer 'home' using the send_data function.
		async_to_sync(channel_layer.group_send)(
					"home",
					{
					"type": "send_data",
					"text": data
					}
				)
		print("data sent " + str(instance.id))
	
post_save.connect(send, sender=device)

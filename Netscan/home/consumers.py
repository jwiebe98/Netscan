import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer

#Import Models
from .models import device, setting

#HomeConsumer handles how the backend sends and recieves data to and from the frontend.
class HomeConsumer(AsyncConsumer):
	async def websocket_connect(self, event):
		print("connected", event)
		
		#Set the group
		await self.channel_layer.group_add(
			"home",
			self.channel_name
		)
		
		#Accept the connection
		await self.send({
			"type": "websocket.accept"
		})
	
	#Method dictates how the HomeConsumer recieves data
	async def websocket_receive(self, event):
		data = event.get('text', None)
		if data is not None:
			loaded_data = json.loads(data)
			identity = loaded_data.get("id")
			notification = loaded_data.get("notification")
			#val = {"identity": identity, "notification": notification}
			d = device.objects.get(id=identity)
			
			#If a name is passed from frontend, replace the name in the database
			if(loaded_data.get("name")):
				d.device = loaded_data.get("name");
			
			#Convert javascript bool to python bool.
			if(notification == "True"):
				d.notification = True
			else:
				d.notification = False
				
			#Save as raw IE. don't send a signal
			d.save_base(raw=True)
			
			#Relay information to all people viewing the home page.
			await self.channel_layer.group_send(
				"home",
				{
				"type": "send_data",
				"text": data,
				}
			)
	
	#Function which handles sending json data to users in a channel.
	async def send_data(self, event):
		await self.send({
			"type": "websocket.send",
			"text": event['text']
		})
		
	#Function which handles disconnects.
	async def websocket_disconnect(self, event):
		print("disconnected", event)
	
#Consumer which handles how the backend handles data for the setting page
class SettingsConsumer(AsyncConsumer):
	async def websocket_connect(self, event):
		print("connected", event)
		
		#Set channel layer to 'settings'
		await self.channel_layer.group_add(
			"settings",
			self.channel_name
		)
		
		#Accept connection
		await self.send({
			"type": "websocket.accept"
		})
	
	#When data is recieved, load the data, save it to database, and send data to all users on the settings channel
	async def websocket_receive(self, event):
		data = event.get('text', None)
		if data is not None:
			loaded_data = json.loads(data)
			
			id = loaded_data.get('id')
			time = loaded_data.get('time')
			
			s = setting.objects.first()
			if(id):
				if(id == "ping_time"):
					s.ping_time = time
				
			s.save()
			
			#Send data to settings channel layer
			await self.channel_layer.group_send(
				"settings",
				{
				"type": "send_data",
				"text": data,
				}
			)
	
	#Sends data to backend when called.
	async def send_data(self, event):
		await self.send({
			"type": "websocket.send",
			"text": event['text']
		})
		
	#Disconnect method
	async def websocket_disconnect(self, event):
		print("disconnected", event)

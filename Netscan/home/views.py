#Import libraries used for http requests.
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

#Import models
from .models import device
from .models import setting as settings

#Class which serves http get requests for the home page.
class index(TemplateView):
	template_name = 'home/index.html'
	
	def get(self, request):
		#Passes all device objects and all id's to html page as arguments.
		device_obj = device.objects.order_by('ip')
		all_ids= list(device.objects.values_list('id', flat=True))
		args = {'device': device_obj, 'all_ids': all_ids}
		return render(request, self.template_name, args)
		
#Class which serves http get requests for the settings page.
class setting(TemplateView):
	template_name = 'home/settings.html'

	def get(self, request):
		#passes settings object to frontend
		setting = settings.objects.order_by('id')
		args = {'setting': setting}
		return render(request, self.template_name, args)

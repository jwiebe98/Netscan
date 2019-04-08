#Import admin and models.
from django.contrib import admin
from .models import device, setting

#Register user createed models in the admin site.
admin.site.register(device)
admin.site.register(setting)

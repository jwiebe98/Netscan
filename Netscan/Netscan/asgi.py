import os
import django
from channels.routing import get_default_application

#Setup for Asyncronous server gateway interface rather than the default Web server gateway interface
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Netscan.settings")
django.setup()
application = get_default_application()

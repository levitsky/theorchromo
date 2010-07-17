import os
import sys
from django.core.handlers.wsgi import WSGIHandler

# put the Django project on sys.path
sys.path.insert(0, 
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), 
        "../")))
os.environ["DJANGO_SETTINGS_MODULE"] = "theorchromo_online/settings.py"
application = WSGIHandler()

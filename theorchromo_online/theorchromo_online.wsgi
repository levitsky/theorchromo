import os
import sys
from django.core.wsgi import get_wsgi_application
# put the Django project on sys.path
sys.path.insert(0, 
    os.path.join(os.path.abspath(os.path.dirname(__file__)), '../'))
os.environ["DJANGO_SETTINGS_MODULE"] = 'theorchromo_online.settings'
application = get_wsgi_application()

import os
import sys

# Project directory
project_home = '/home/smartops/Smartops'

if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'SmartOps.settings'

# Load Django application
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()